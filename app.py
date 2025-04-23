import streamlit as st
import pandas as pd
import pydeck as pdk

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)  # o pd.read_excel
    df["LATITUD"]  = df["LATITUD"].astype(float)
    df["LONGITUD"] = df["LONGITUD"].astype(float)
    return df

df = load_data("clues.csv")

st.sidebar.title("Filtrar por Estado")
entidades = sorted(df["ENTIDAD"].unique())
seleccion = st.sidebar.selectbox("Elige una ENTIDAD", entidades)

df_filtrado = df[df["ENTIDAD"] == seleccion]

st.write(f"Mostrando {len(df_filtrado)} puntos en **{seleccion}**")

# Centro del mapa
prom_lat = df_filtrado["LATITUD"].mean()
prom_lon = df_filtrado["LONGITUD"].mean()

# 1) Capa con color rojo semitransparente y tooltips en cada punto
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_filtrado,
    get_position=["LONGITUD", "LATITUD"],
    pickable=True,
    get_fill_color=[200, 30, 0, 160],  # tu rojo semitransparente

    # Usa unidades en pixeles y un radio fijo base (en px)
    radiusUnits="pixels",
    get_radius=8,            # 8px de base
    radiusMinPixels=4,       # nunca menos de 4px
    radiusMaxPixels=20       # nunca más de 20px
)

# 2) Configuración general de Deck con tooltip
tooltip = {
    "html": (
        "<b>Calle:</b> {VIALIDAD} <br/>"
        "<b>Núm:</b> {NUMERO EXTERIOR} <br/>"
        "<b>Tel:</b> {TELEFONO 1 DEL ESTABLECIMIENTO} <br/>"
        "<b>Horario:</b> {CODIGO POSTAL}"
    ),
    "style": {
        "backgroundColor": "steelblue",
        "color": "white",
        "fontSize": "12px",
        "padding": "10px",
        "borderRadius": "5px"
    }
}

view_state = pdk.ViewState(
    latitude=prom_lat,
    longitude=prom_lon,
    zoom=6,
    pitch=0
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/streets-v11",
    tooltip=tooltip
)

st.pydeck_chart(deck)
