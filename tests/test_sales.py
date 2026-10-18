from datetime import date
from io import BytesIO

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from sales import CATEGORIES, REGIONS, csv_bytes, filter_data, generate_data, metrics


def test_reproducible_and_consistent():
    data = generate_data()
    pd.testing.assert_frame_equal(data, generate_data())
    assert len(data) == data.pedido.nunique() == 2400
    assert data.fecha.min() == date(2025, 1, 1)
    assert data.fecha.max() == date(2025, 12, 31)
    assert (data.venta_cent - data.costo_cent == data.ganancia_cent).all()
    assert (data.ganancia_cent >= 0).all()


@pytest.fixture
def sample():
    return pd.DataFrame({
        "pedido": ["A", "B", "C"],
        "fecha": [date(2025, 1, 1), date(2025, 1, 2), date(2025, 1, 3)],
        "categoría": ["Hogar", "Moda", "Hogar"], "región": ["Sur", "Norte", "Sur"],
        "unidades": [1, 2, 1], "venta_cent": [10000, 20000, 30000],
        "costo_cent": [7000, 15000, 20000], "ganancia_cent": [3000, 5000, 10000]})


def test_known_metrics(sample):
    assert metrics(sample) == {"ventas": 600, "ganancias": 180, "pedidos": 3, "ticket": 200}


def test_combined_inclusive_filters(sample):
    selected = filter_data(sample, date(2025, 1, 1), date(2025, 1, 3), ["Hogar"], ["Sur"])
    assert selected.pedido.tolist() == ["A", "C"]
    assert metrics(selected)["ticket"] == 200
    single_day = filter_data(sample, date(2025, 1, 2), date(2025, 1, 2), ["Moda"], ["Norte"])
    assert single_day.pedido.tolist() == ["B"]
    assert filter_data(sample, date(2025, 1, 1), date(2025, 1, 3), ["Hogar"], ["Norte"]).empty


@pytest.mark.parametrize("categories,regions", [([], REGIONS), (CATEGORIES, []), ([], [])])
def test_empty_selection(sample, categories, regions):
    empty = filter_data(sample, date(2025, 1, 1), date(2025, 1, 3), categories, regions)
    assert metrics(empty) == {"ventas": 0, "ganancias": 0, "pedidos": 0, "ticket": 0}
    assert pd.read_csv(BytesIO(csv_bytes(empty))).empty


def test_csv_matches_filtered_rows(sample):
    selected = filter_data(sample, date(2025, 1, 2), date(2025, 1, 2), ["Moda"], ["Norte"])
    csv = pd.read_csv(BytesIO(csv_bytes(selected)))
    assert csv.pedido.tolist() == ["B"]
    assert csv.ventas_pen.sum() == 200
    assert "categoría" in csv.columns


def test_app_and_filter_interactions():
    app = AppTest.from_file("app.py").run(timeout=30)
    assert not app.exception
    assert app.metric[2].value == "2400"
    assert len(app.get("plotly_chart")) == 3
    app.sidebar.multiselect[0].set_value(["Hogar"])
    app.sidebar.multiselect[1].set_value(["Sur"])
    app.sidebar.date_input[0].set_value((date(2025, 3, 1), date(2025, 3, 31)))
    app.run()
    assert not app.exception
    expected = filter_data(generate_data(), date(2025, 3, 1), date(2025, 3, 31), ["Hogar"], ["Sur"])
    assert app.metric[2].value == str(len(expected))
    assert len(app.dataframe[0].value) == len(expected)
    assert app.dataframe[0].value.ventas_pen.sum() == pytest.approx(metrics(expected)["ventas"])
    app.sidebar.multiselect[0].set_value([]).run()
    assert not app.exception
    assert app.metric[2].value == "0"
    assert app.dataframe[0].value.empty
    assert len(app.get("plotly_chart")) == 0


def test_incomplete_date_range():
    app = AppTest.from_file("app.py").run()
    app.sidebar.date_input[0].set_value((date(2025, 1, 1),)).run()
    assert not app.exception
    assert "Selecciona" in app.warning[0].value
