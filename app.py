# app.py

import streamlit as st
import pandas as pd
import pydeck as pdk

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    # Asegúrate de que las columnas de lat/long sean float
    df["LATITUD"]  = df["LATITUD"].astype(float)
    df["LONGITUD"] = df["LONGITUD"].astype(float)
    return df

df = load_data("clues.csv")

st.sidebar.title("Filtrar por Estado")
entidades = sorted(df["ENTIDAD"].unique())
seleccion = st.sidebar.selectbox("Elige una ENTIDAD", entidades)

# Filtramos
df_filtrado = df[df["ENTIDAD"] == seleccion]

st.write(f"Mostrando {len(df_filtrado)} puntos en **{seleccion}**")

# Centro aproximado para el view_state
prom_lat = df_filtrado["LATITUD"].mean()
prom_lon = df_filtrado["LONGITUD"].mean()

# Capa de puntos
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_filtrado,
    get_position=["LONGITUD", "LATITUD"],
    get_radius=1000,                # radio en metros
    pickable=True,
    tooltip={
        "html": "<b>Calle:</b> {CALLE} <br/>"
                "<b>Núm:</b> {NUMERO} <br/>"
                "<b>Tel:</b> {TELEFONO} <br/>"
                "<b>Horario:</b> {HORARIO}",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }
)

view = pdk.ViewState(
    latitude=prom_lat,
    longitude=prom_lon,
    zoom=6,
    pitch=0
)

r = pdk.Deck(layers=[layer], initial_view_state=view, map_style="mapbox://styles/mapbox/streets-v11")

st.pydeck_chart(r)
