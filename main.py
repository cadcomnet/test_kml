import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static, st_folium
from opencage.geocoder import OpenCageGeocode

url_1 = "https://github.com/cadcomnet/data/blob/main/longitude/depurados/2019%20LONGITUDE%20PROJECTS-D.csv"
url_2 = "https://github.com/cadcomnet/data/blob/main/longitude/depurados/2020%20LONGITUDE%20PROJECTS-D.csv"
url_3 = "https://github.com/cadcomnet/data/blob/main/longitude/depurados/2021%20LONGITUDE%20PROJECTS-D.csv"
url_4 = "https://github.com/cadcomnet/data/blob/main/longitude/depurados/2022%20LONGITUDE%20PROJECTS-D.csv"

# codigo css y configuracion general de la pagina
# Configurar la página en modo wide screen
st.set_page_config(layout="wide")



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

    folium_static(m)

def obten_numeros_unicos(numeros):

    lista_de_numeros_unicos = []

    numeros_unicos = set(numeros)

    for numero in numeros_unicos:
        lista_de_numeros_unicos.append(numero)

    return lista_de_numeros_unicos



# Cargar datos
st.sidebar.header("Longitude Data Projects")
st.sidebar.text("Years 2019 - 2022")

#st.sidebar.title('Year of project')
#st.write("Choose a year")
#star_year = st.selectbox("Year", options=["2019", '2020', '2021', '2022'], index=0, key='Year')
#submit_btn = st.form_submit_button("Load year", type='primary')

data = pd.read_csv("depurados/2013-2022.csv",
                   dtype={'LONGITUDE' : float,
                          'LATITUDE' : float,
                          'LABEL': str,
                          'LAYER' : str,
                         'SYMBOL': str,
                          'KML_STYLE': str})

#lista_proyectos = data['LAYER'].to_list()
lista_proyectos = obten_numeros_unicos(data['LAYER'].to_list())
lista_proyectos.insert(0, '')
data_layer = data

# Input de búsqueda

label_search = st.sidebar.text_input("Search project number:", max_chars=5, placeholder="19000")
if label_search:
   data = data[data['LABEL'].str.contains(label_search, case=False, na=False)]

# Input de búsqueda por dirección
address_search = st.sidebar.text_input("Buscar por dirección:")
address_lat, address_lon = None, None
if address_search:
    address_lat, address_lon = geocode_address(address_search, OPENCAGE_API_KEY)



label_search2 = st.sidebar.selectbox('Choose a type projects', lista_proyectos, index=0)
if label_search2:
    data = data_layer[data_layer['LAYER'].str.contains(label_search2, case=False, na=False)]


dicc_ = { 'PROJECT' : data['LABEL'].to_list() ,  'TYPE':  data['LAYER'].to_list() }
st.sidebar.table(dicc_)


st.write(mapas(data))
