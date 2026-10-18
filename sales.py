"""Datos sintéticos y lógica del dashboard; importable sin Streamlit."""
from datetime import date, timedelta
from random import Random

import pandas as pd

CATEGORIES = ("Tecnología", "Hogar", "Oficina", "Moda")
REGIONS = ("Norte", "Centro", "Sur", "Oriente")


def generate_data(seed=42, orders=2400):
    """Un registro por pedido, importes en céntimos para evitar errores de suma."""
    rng = Random(seed)
    rows = []
    for i in range(orders):
        day = date(2025, 1, 1) + timedelta(days=rng.randrange(365))
        category = rng.choice(CATEGORIES)
        region = rng.choice(REGIONS)
        units = rng.randint(1, 5)
        sale = units * rng.randint(2500, 65000)
        cost = sale * rng.randint(55, 90) // 100
        rows.append((f"DEM-{i + 1:05d}", day, category, region, units, sale, cost, sale - cost))
    return pd.DataFrame(rows, columns=["pedido", "fecha", "categoría", "región", "unidades", "venta_cent", "costo_cent", "ganancia_cent"]).sort_values(["fecha", "pedido"]).reset_index(drop=True)


def filter_data(data, start, end, categories, regions):
    return data.loc[(data.fecha >= start) & (data.fecha <= end) & data["categoría"].isin(categories) & data["región"].isin(regions)].copy()


def metrics(data):
    sales = int(data.venta_cent.sum()) / 100
    orders = data.pedido.nunique()
    return {"ventas": sales, "ganancias": int(data.ganancia_cent.sum()) / 100,
            "pedidos": orders, "ticket": sales / orders if orders else 0.0}


def display_data(data):
    result = data[["pedido", "fecha", "categoría", "región", "unidades"]].copy()
    for source, target in [("venta_cent", "ventas_pen"), ("costo_cent", "costos_pen"), ("ganancia_cent", "ganancias_pen")]:
        result[target] = data[source] / 100
    return result


def csv_bytes(data):
    return display_data(data).to_csv(index=False, lineterminator="\n").encode("utf-8-sig")
