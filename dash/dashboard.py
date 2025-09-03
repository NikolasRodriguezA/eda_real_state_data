# dashboard_realstate.py

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Base.txt"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, sep=",", engine="python")
    df.columns = df.columns.str.strip()
    df = df.dropna(how="all") 
    
    for col in ["VALOR TOTAL", "VL. CUOTA INICIAL"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("[$,.]", "", regex=True)
            .str.strip()
            .replace("", None)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

df = load_data()


st.sidebar.header("Filtros")
estado = st.sidebar.multiselect("Estado de la unidad", df["ESTADO"].dropna().unique())
medio = st.sidebar.multiselect("Medio de publicidad", df["MEDIO DE PUBLICIDAD"].dropna().unique())
tipo = st.sidebar.multiselect("Tipo de unidad", df["TIPO"].dropna().unique())

df_filtered = df.copy()
if estado:
    df_filtered = df_filtered[df_filtered["ESTADO"].isin(estado)]
if medio:
    df_filtered = df_filtered[df_filtered["MEDIO DE PUBLICIDAD"].isin(medio)]
if tipo:
    df_filtered = df_filtered[df_filtered["TIPO"].isin(tipo)]

st.title("🏢 Dashboard Inmobiliario - PoC")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total Unidades", len(df_filtered))
with c2:
    st.metric("Unidades Vendidas", (df_filtered["ESTADO"] == "VENDIDO").sum())
with c3:
    st.metric("Ingresos Estimados", f"${df_filtered['VALOR TOTAL'].sum():,.0f}")

st.subheader("Ventas por Año")
ventas_anio = df_filtered.groupby("AÑO").size().reset_index(name="Ventas")
fig1 = px.bar(ventas_anio, x="AÑO", y="Ventas", title="Unidades Vendidas por Año")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Evolución Mensual de Ventas")
if "MES DE VENTA" in df_filtered.columns:
    ventas_mes = df_filtered.groupby("MES DE VENTA").size().reset_index(name="Ventas")
    fig2 = px.line(ventas_mes, x="MES DE VENTA", y="Ventas", markers=True, title="Tendencia Mensual")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Ventas por Medio de Publicidad")
if "MEDIO DE PUBLICIDAD" in df_filtered.columns:
    ventas_medio = df_filtered.groupby("MEDIO DE PUBLICIDAD")["VALOR TOTAL"].sum().reset_index()
    fig3 = px.bar(ventas_medio, x="MEDIO DE PUBLICIDAD", y="VALOR TOTAL", title="Ingresos por Canal de Publicidad")
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Distribución de Subsidios")
if "APLICA SUBSIDIO" in df_filtered.columns:
    fig4 = px.pie(df_filtered, names="APLICA SUBSIDIO", title="Uso de Subsidios")
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("Ingresos por Tipo de Unidad")
fig5 = px.box(df_filtered, x="TIPO", y="VALOR TOTAL", title="Valor de Venta por Tipo de Vivienda")
st.plotly_chart(fig5, use_container_width=True)

st.subheader("Ranking de Asesores por Ventas")
asesores = df_filtered[df_filtered["ESTADO"] == "VENDIDO"].groupby("ASESOR")["VALOR TOTAL"].sum().reset_index()
fig6 = px.bar(asesores.sort_values("VALOR TOTAL", ascending=False), 
              x="ASESOR", y="VALOR TOTAL", title="Top Asesores")
st.plotly_chart(fig6, use_container_width=True)

st.subheader("Mapa de Calor: Ventas por Piso y Tipo")
if "PISO" in df_filtered.columns:
    heatmap = pd.crosstab(df_filtered["PISO"], df_filtered["TIPO"])
    st.dataframe(heatmap)

st.subheader("Detalle de Unidades")
st.dataframe(df_filtered[["APTO #", "PISO", "TIPO", "ESTADO", "VALOR TOTAL", "CLIENTE 1", "ASESOR"]])
