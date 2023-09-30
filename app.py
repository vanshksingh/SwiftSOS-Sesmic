import streamlit as st
import folium
from folium.plugins import HeatMap
from folium.plugins import GroupedLayerControl
from branca.element import Template, MacroElement
import requests
from datetime import datetime, timedelta

import appstyle


url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson"


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
 
)




places = [feature["properties"]["place"] for feature in data ["features"]]
magnitudes = [feature["properties"]["mag"] for feature in data ["features"]]
times = [feature["properties"]["time"] for feature in data ["features"]] 
longs = [feature["geometry"]["coordinates"][0] for feature in data ["features"]]
lats = [feature["geometry"]["coordinates"][1] for feature in data ["features"]]


m = folium.Map(location=[36.5, 37.5], tiles=None, zoom_start=3)


basemap1 = folium.TileLayer("openstreetmap", name="Open Street Map").add_to(m)
basemap0 = folium.TileLayer("cartodbdark_matter", name="Dark Theme Basemap").add_to(m)



coords = [[lat, lon, mag] for lat, lon, mag in zip(lats, longs, magnitudes)]


colors = {0.2: '#0f0b75', 0.45: '#9e189c', 0.75: '#ed7c50', 1: '#f4ee27'}


heatmap = HeatMap(data=coords, gradient=colors, name="Earthquake Distribution Heatmap").add_to(m)


col1, col2 = st.columns(2)
start_date = col1.date_input("Start date", datetime.now() - timedelta(days=10))
end_date = col2.date_input("End date", datetime.now())


start_datetime = datetime.combine(start_date, datetime.min.time())
end_datetime = datetime.combine(end_date, datetime.max.time())


main_layer = folium.FeatureGroup("Earthquakes Location").add_to(m)


minor_layer = folium.FeatureGroup(name="Minor: Less than 3.9").add_to(main_layer)
light_layer = folium.FeatureGroup(name="Light: 4.0 - 4.9").add_to(main_layer)
moderate_layer = folium.FeatureGroup(name="Moderate: 5.0 - 5.9").add_to(main_layer)
strong_layer = folium.FeatureGroup(name="Strong: 6.0 - 6.9").add_to(main_layer)
major_layer = folium.FeatureGroup(name="Major: 7.0 - 7.9").add_to(main_layer)
great_layer = folium.FeatureGroup(name="Great: 8.0 and higher").add_to(main_layer)


app_css = appstyle.map_css

style = MacroElement()
style._template = Template(app_css)


m.get_root().add_child(style)


for place, mag, time, lat, lon  in zip(places, magnitudes, times, lats, longs):


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


folium.LayerControl(collapsed=False).add_to(m)

GroupedLayerControl(
    groups={
    "Earthquake Classes by Magnitude": [minor_layer, light_layer, moderate_layer, strong_layer, major_layer, great_layer]
    },
    exclusive_groups=False,
    collapsed=False
).add_to(m)


html_string = m._repr_html_()


st.components.v1.html(html_string, width=1000, height=600)
