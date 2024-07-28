import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from opencage.geocoder import OpenCageGeocode

lista_proyectos = ["", "(SUE)" , "3D Laser Scanning" , "6370 Manor lane up to the intersection of SW 66 Avenue and SW 80 Street" ,
                   "ALTA Survey" , "As Built Survey" , "As-Built" , "As-Built Survey" ,
                   "As-Built SurveySR 997/Krome Ave from" , "Bathymetric Survey" , "Boundary" ,
                   "Boundary Analysis" , "Boundary and Topographic Survey" , "Boundary Survey" ,
                   "Collect elevations" , "Construction" , "Construction Layout" , "Elevation Certificate" ,
                   "Engineering Services" , "Final Plat" , "Final Survey" , "Foundation Survey" ,
                   "Legal Description" , "Map of Boundary Survey" , "Mark the property corners" ,
                   "Miscellaneous" , "Miscellaneous Surveying" , "Photogrammetric Survey" ,
                   "Plat" , "Re-Certification" , "Right-of-Way" , "Setback Survey" , "Sewer As-Built/Water" ,
                   "Site Plan Survey" , "Sketch to Accompany Legal" , "stakeout" , "SUE" , "Survey" ,
                   "Tentative Plat" , "Topographic" , "Topographic Survey" , "Unknown Point Feature" ,
                   "Update" , "Update Alta Survey" , "Update Boundary Survey" , "Update Survey" , "Up-Date Survey"
                    ]

# Función para geocodificar una dirección utilizando OpenCage
def geocode_address(address, key):
    geocoder = OpenCageGeocode(key)
    results = geocoder.geocode(address)
    if results and len(results):
        return results[0]['geometry']['lat'], results[0]['geometry']['lng']
    else:
        return None, None

# Ingresar tu clave API de OpenCage aquí
OPENCAGE_API_KEY = 'cc29841c73244c6699e642e6e7beac37'

def mapas(datos):
    data = datos

    if address_lat and address_lon:
        m = folium.Map(location=[address_lat, address_lon], zoom_start=12, tiles='OpenStreetMap')
        folium.Marker(location=[address_lat, address_lon], popup='Dirección buscada', tooltip='Dirección').add_to(m)
    # Crear mapa
    else:
        m = folium.Map(location=[data['LATITUDE'].mean(),
                                 data['LONGITUDE'].mean()],
                       zoom_start=10, tiles='OpenStreetMap',
                       control_scale=True, )  # OpenStreetMap , Cartodb Positron, Cartodb dark_matter, Stamen Watercolor

    # Añadir puntos al mapa
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in data.iterrows():
        folium.Marker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            popup=row['LABEL'],
            tooltip=row['LAYER']
        ).add_to(marker_cluster)

    # Mostrar mapa en Streamlit
    folium_static(m)


# Cargar datos

st.title("Longitude Data Projects")
st.text("Years 2019 - 2022")


with st.form('Year of project'):

        st.write("Choose a year")
        star_year = st.selectbox("Year", options=["2019", '2020', '2021', '2022'], index=0, key='Year')
        submit_btn = st.form_submit_button("Load year", type='primary')
        col1, col2 = st.columns(2)


        if star_year == '2019':
            data = pd.read_csv("depurados/2019 LONGITUDE PROJECTS-D.csv",
                               dtype={'LONGITUDE' : float,
                                      'LATITUDE' : float,
                                      'LABEL': str,
                                      'LAYER' : str,
                                     'SYMBOL': str,
                                      'KML_STYLE': str})
            data_layer = data
        if star_year == '2020':
            data = pd.read_csv("depurados/2020 LONGITUDE PROJECTS-D.csv",
                               dtype={'LONGITUDE' : float,
                                      'LATITUDE' : float,
                                      'LABEL': str,
                                      'LAYER' : str,
                                     'SYMBOL': str,
                                      'KML_STYLE': str})
            data_layer = data
        if star_year == '2021':
            data = pd.read_csv("depurados/2021 LONGITUDE PROJECTS-D.csv",
                               dtype={'LONGITUDE' : float,
                                      'LATITUDE' : float,
                                      'LABEL': str,
                                      'LAYER' : str,
                                     'SYMBOL': str,
                                      'KML_STYLE': str})
            data_layer = data
        if star_year == '2022':
            data = pd.read_csv("depurados/2022 LONGITUDE PROJECTS-D.csv",
                               dtype={'LONGITUDE' : float,
                                      'LATITUDE' : float,
                                      'LABEL': str,
                                      'LAYER' : str,
                                     'SYMBOL': str,
                                      'KML_STYLE': str})
            data_layer = data

st.divider()
col1, col2 = st.columns(2)

with col1:
        # Input de búsqueda
        label_search = st.text_input("Search project number:", max_chars=5, placeholder="19000")
        if label_search:
           data = data[data['LABEL'].str.contains(label_search, case=False, na=False)]

        # Input de búsqueda por dirección
        address_search = st.text_input("Buscar por dirección:")
        address_lat, address_lon = None, None
        if address_search:
            address_lat, address_lon = geocode_address(address_search, OPENCAGE_API_KEY)


        label_search2 = st.selectbox('Choose a type projects', lista_proyectos, index=0)
        if label_search2:
            data = data_layer[data_layer['LAYER'].str.contains(label_search2, case=False, na=False)]

with col2:
    st.write(data)

st.write(mapas(data))









