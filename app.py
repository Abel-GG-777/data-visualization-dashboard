"""Dashboard de ventas de demostración."""
import pandas as pd
import plotly.express as px
import streamlit as st

from sales import CATEGORIES, REGIONS, csv_bytes, display_data, filter_data, generate_data, metrics

st.set_page_config(page_title="Pulso comercial · Demo", page_icon="📊", layout="wide")
st.title("Pulso comercial")
st.caption("DASHBOARD DE VENTAS · DATOS DE DEMOSTRACIÓN")
st.info("Datos ficticios reproducibles (semilla 42). No representan operaciones reales. Moneda: soles peruanos (PEN).")

@st.cache_data
def load_data():
    return generate_data()

data = load_data()
with st.sidebar:
    st.header("Filtros")
    dates = st.date_input("Período", value=(data.fecha.min(), data.fecha.max()), min_value=data.fecha.min(), max_value=data.fecha.max(), format="DD/MM/YYYY")
    categories = st.multiselect("Categoría", CATEGORIES, default=list(CATEGORIES))
    regions = st.multiselect("Región", REGIONS, default=list(REGIONS))
    st.caption("Las fechas incluyen ambos extremos. Una selección vacía no devuelve pedidos.")

if len(dates) != 2:
    st.warning("Selecciona la fecha inicial y final del período.")
    st.stop()
filtered = filter_data(data, dates[0], dates[1], categories, regions)
values = metrics(filtered)

def money(value):
    return (f"S/ {value:,.2f}".replace(",", "_").replace(".", ",").replace("_", "."))

for column, (label, value) in zip(st.columns(4), [("Ventas", money(values["ventas"])), ("Ganancias", money(values["ganancias"])), ("Pedidos", str(values["pedidos"])), ("Ticket promedio", money(values["ticket"]))]):
    column.metric(label, value)
st.caption("Ganancias = ventas − costos simulados. Ticket promedio = ventas / pedidos únicos. Sin impuestos ni devoluciones.")
st.subheader("Panorama del período")
if filtered.empty:
    st.warning("No hay pedidos para estos filtros. Amplía el período o selecciona categorías y regiones.")
else:
    daily = filtered.groupby("fecha", as_index=True).venta_cent.sum()
    calendar = pd.date_range(dates[0], dates[1], freq="D")
    daily.index = pd.to_datetime(daily.index)
    trend = daily.reindex(calendar, fill_value=0).rename_axis("Fecha").reset_index(name="centavos")
    trend["Ventas (PEN)"] = trend.centavos / 100
    fig = px.line(trend, x="Fecha", y="Ventas (PEN)", title="Evolución diaria de ventas", color_discrete_sequence=["#2563eb"])
    st.plotly_chart(fig, width="stretch")
    left, right = st.columns(2)
    category = filtered.groupby("categoría", as_index=False).venta_cent.sum().sort_values("venta_cent", ascending=False)
    category["Ventas (PEN)"] = category.venta_cent / 100
    left.plotly_chart(px.bar(category, x="categoría", y="Ventas (PEN)", title="Ventas por categoría", labels={"categoría": "Categoría"}, color_discrete_sequence=["#2563eb"]), width="stretch")
    regional = filtered.groupby("región", as_index=False)[["venta_cent", "ganancia_cent"]].sum()
    regional = regional.rename(columns={"región": "Región", "venta_cent": "Ventas", "ganancia_cent": "Ganancias"})
    regional[["Ventas", "Ganancias"]] /= 100
    regional = regional.melt(id_vars="Región", var_name="Indicador", value_name="Importe (PEN)")
    right.plotly_chart(px.bar(regional, x="Región", y="Importe (PEN)", color="Indicador", barmode="group", title="Resultados por región", color_discrete_sequence=["#2563eb", "#10b981"]), width="stretch")

st.subheader("Detalle de pedidos")
st.caption(f"{len(filtered):,} pedidos filtrados de {len(data):,} · Período: {dates[0]:%d/%m/%Y} al {dates[1]:%d/%m/%Y}")
st.dataframe(display_data(filtered), hide_index=True, width="stretch")
st.download_button("Descargar datos filtrados (CSV)", data=csv_bytes(filtered), file_name="ventas_demo_filtradas.csv", mime="text/csv")
st.caption("CSV en UTF-8 con BOM, separador coma e importes decimales en PEN. Cada fila corresponde a un pedido.")
