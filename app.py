import streamlit as st
import folium
from folium.plugins import HeatMap
from folium.plugins import GroupedLayerControl
from branca.element import Template, MacroElement
import requests
from datetime import datetime, timedelta
# my custom css
import appstyle

# Earthquake data GeoJSON URL:
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson"

# Getting the earthquake data
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as expt:
    st.error("Error: Could not retrieve data from API")
    st.error("details: ", +str(expt))
    st.stop()

st.set_page_config(
    page_title="QuakeEye",
    page_icon="https://cdn-icons-png.flaticon.com/512/2377/2377860.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    'Get help': "https://github.com/IndigoWizard/QuakeEye",
    'Report a bug': "https://github.com/IndigoWizard/QuakeEye/issues",
    'About': "# This is a header. This is an *extremely* cool app!"
    }
)

########### SIDEBAR  MENU ########### 
# Set up the sidebar
st.sidebar.title("Navigation")

# Project summary section
st.sidebar.subheader("Project Summary")
st.sidebar.success("Real-Time Earthquake Data Visualization App.")

# About section
st.sidebar.subheader("About me:")
st.sidebar.caption("**Ahmed I. Mokhtari (IndigoWizard):** <br> Tech & Open Source enthusiast | Geo Environment & Spatial Planning | Maps & Cartography | Remote Sensing & Geospatial Analysis | Indie Game Dev | House of M.",
    unsafe_allow_html=True)

# Contact section
st.sidebar.subheader("Find me at:")

## Define columns in the sidebar
c1, c2, c3 = st.sidebar.columns([1, 1, 1])

# Display info in the columns
with c1:
    st.info("[![LinkedIn](https://static.licdn.com/sc/h/8s162nmbcnfkg7a0k8nq9wwqo)](https://linkedin.com/in/ahmed-islem-mokhtari)")
with c2:
    st.info("[![GitHub](https://github.githubassets.com/favicons/favicon-dark.png)](https://github.com/IndigoWizard)")
with c3:
    st.info("[![Medium](https://miro.medium.com/1*m-R_BkNf1Qjr1YbyOIJY2w.png)](https://medium.com/@Indigo.Wizard/mt-chenoua-forest-fires-analysis-with-remote-sensing-614681f468e9)")

st.sidebar.caption("ʕ •ᴥ•ʔ : Dont forget to star ⭐ this project on [GitHub.com/IndigoWizard/QuakeEye](https://github.com/IndigoWizard/QuakeEye/stargazers)")

# App custom CSS
st.markdown(appstyle.st_css,unsafe_allow_html=True,)

########### MAIN PAGE CONTENT ###########
# App title
# Add a title to your Streamlit app
st.subheader("QuakeEye - Real-Time Earthquake Data Visualization")

# Add a description of your Streamlit app
st.write("This app visualizes the latest earthquake data from [USGS](https://www.usgs.gov/) in real-time. The app retrieves earthquake data from the USGS API and displays the data on a map using the [Folium](https://python-visualization.github.io/folium/) library and is deployed using [Streamlit](https://streamlit.io/).")
st.write("Users can filter and explore earthquake data by magnitude, frequency magnitude distribution and time range.")

# st.subheader("Earthquake Map")

########### MAIN APP ###########
# Extracting main information (location (latitde & longitude), magnitude)
places = [feature["properties"]["place"] for feature in data ["features"]]
magnitudes = [feature["properties"]["mag"] for feature in data ["features"]]
times = [feature["properties"]["time"] for feature in data ["features"]] 
longs = [feature["geometry"]["coordinates"][0] for feature in data ["features"]]
lats = [feature["geometry"]["coordinates"][1] for feature in data ["features"]]

# Main project folium map
m = folium.Map(location=[36.5, 37.5], tiles=None, zoom_start=3)

#Primary basemaps
basemap0 = folium.TileLayer("cartodbdark_matter", name="Dark Theme Basemap").add_to(m)
basemap1 = folium.TileLayer("openstreetmap", name="Open Street Map").add_to(m)

### Frequency Magnitude Distribution Heatmap
# Making a coordinates list
coords = [[lat, lon, mag] for lat, lon, mag in zip(lats, longs, magnitudes)]

# Defning a color ramp for the heat map
colors = {0.2: '#0f0b75', 0.45: '#9e189c', 0.75: '#ed7c50', 1: '#f4ee27'}

# Adding the folium heatmap layer using the HeatMap plugin
heatmap = HeatMap(data=coords, gradient=colors, name="Earthquake Distribution Heatmap").add_to(m)

# Date range input (10 days delta)
col1, col2 = st.columns(2)
start_date = col1.date_input("Start date", datetime.now() - timedelta(days=10))
end_date = col2.date_input("End date", datetime.now())

# storing start & end dates as datetime objects
start_datetime = datetime.combine(start_date, datetime.min.time())
end_datetime = datetime.combine(end_date, datetime.max.time())

# Earthquake Marker layers
# Making a main earthquake layers group to enable/disable all the layers at once from the defaul layer panel
main_layer = folium.FeatureGroup("Earthquakes Location").add_to(m)

# Earthquakes are split into categories based on their magnitudes
# micro_layer = folium.FeatureGroup(name="Micro: Less than 2.9").add_to(main_layer)
minor_layer = folium.FeatureGroup(name="Minor: Less than 3.9").add_to(main_layer)
light_layer = folium.FeatureGroup(name="Light: 4.0 - 4.9").add_to(main_layer)
moderate_layer = folium.FeatureGroup(name="Moderate: 5.0 - 5.9").add_to(main_layer)
strong_layer = folium.FeatureGroup(name="Strong: 6.0 - 6.9").add_to(main_layer)
major_layer = folium.FeatureGroup(name="Major: 7.0 - 7.9").add_to(main_layer)
great_layer = folium.FeatureGroup(name="Great: 8.0 and higher").add_to(main_layer)

# Injecting custom css through branca macro elements and template
app_css = appstyle.map_css
# configuring the style
style = MacroElement()
style._template = Template(app_css)

# Adding style to the map
m.get_root().add_child(style)

# Adding Markers to layers based on earthquake magnitude
for place, mag, time, lat, lon  in zip(places, magnitudes, times, lats, longs):

    # Configure data display in popups when clicking on markers <span></span>
    date_time = datetime.fromtimestamp(time/1000)
    if start_datetime <= date_time <= end_datetime:
        time_date = date_time.strftime("%Y-%m-%d")
        time_hour = date_time.strftime("%H:%M:%S")

        popup_info = f"<div class='popinfo'><h5><b>Earthquake Information</b></h5><b>Magnitude:</b> <span>{mag}</span><br><b>Date:</b> <span>{time_date}</span><br><b>Time:</b> <span>{time_hour}</span><br><b>Location:</b> <span>{place}</span><br><b>Coordinates:</b> <span>{lat} , {lon}</span></div>"

        if mag <= 3.9:
            folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color="beige")).add_to(minor_layer)
        elif mag <= 4.9:
            folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color="orange")).add_to(light_layer)
        elif mag <= 5.9:
            folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color="lightred")).add_to(moderate_layer)
        elif mag <= 6.9:
            folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color="red")).add_to(strong_layer)
        elif mag <= 7.9:
            folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color="darkred")).add_to(major_layer)
        else:
            folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color="black")).add_to(great_layer)

# Adding the layer control
folium.LayerControl(collapsed=False).add_to(m)

# Ctreating multiple magnitude layers based on Richter classification
# Using GroupedLayerControl to stack the new layers under a one category and make them individually interactive
GroupedLayerControl(
    groups={
    "Earthquake Classes by Magnitude": [minor_layer, light_layer, moderate_layer, strong_layer, major_layer, great_layer]
    },
    exclusive_groups=False,
    collapsed=False
).add_to(m)

# Display the map using streamlit-folium
html_string = m._repr_html_()

# Display the HTML string using Streamlit
st.components.v1.html(html_string, width=1000, height=600)

st.write("## Contribute to the Project")
st.write("You can help improve this project and contribute in many ways, such as:")
st.write("- 🐛 Reporting bugs and issues")
st.write("- ✨ Suggesting new features")
st.write("- 🛠️ Improving the existing codebase")
st.write("- 💬 Spreading the word and encouraging others to use the app")
st.markdown("<div class='footer-info'>To learn more and get involved, visit the project <span><a href='https://github.com/IndigoWizard/QuakeEye/blob/streamlit-app/.github/CONTRIBUTING.md' target='_blank' rel='noopener noreferrer'>GitHub repository</a> <img src='https://github.githubassets.com/favicons/favicon-dark.png' alt='icon-github' id='contribute'></span></div>", unsafe_allow_html=True)
