import streamlit as st
import numpy as np
import pandas as pd
from pathlib import Path
import pydeck as pdk


# load the data
data = pd.read_excel(Path('data/Dataset_code4green.xlsx'))

data['lat'] = data.Latitude
data['lon'] = data.Longitude

# Adding code so we can have map default to the center of the data
midpoint = (round(np.average(data['lat']), 6), round(np.average(data['lon']), 6))

# Set the title
st.title('Contamination Explorer')

# Define the sidebar
# Define contamination
st.sidebar.title("Choose contaminant:")
options = st.sidebar.multiselect("", ['Zinc', 'Lead'])

#Define coordinates
st.sidebar.title("Choose your coordinates:")
lat_txt = st.sidebar.number_input("Latitude:", value=midpoint[0], format='%f', step=0.001)
lon_txt = st.sidebar.number_input("Longitude:", value=midpoint[1], format='%f', step=0.001)


# Define the map
layer = pdk.Layer('ScatterplotLayer',     # Change the `type` positional argument here
    data,
    get_position=['lon', 'lat'],
    auto_highlight=True,
    get_radius=10,          # Radius is given in meters
    get_fill_color=[255, 0, 0, 140],  # Set an RGBA value for fill
    pickable=True)

view_state = pdk.ViewState(
    latitude=float(lat_txt),
    longitude=float(lon_txt),
    zoom=15,
    min_zoom=5,
    max_zoom=15,
    pitch=40.5,
    bearing=-27.36)

# Combined all of it and render a viewport
r = pdk.Deck(layers=[layer], initial_view_state=view_state, width=100)
st.pydeck_chart(r)
