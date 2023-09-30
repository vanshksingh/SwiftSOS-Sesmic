import folium
from folium.plugins import HeatMap
from folium.plugins import GroupedLayerControl
from branca.element import Template, MacroElement
import requests
from datetime import datetime
import appstyle
import webbrowser

# Earthquake data GeoJSON URL:
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson"

# Getting the earthquake data
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as expt:
    print("Error: Could not retrieve data from API")
    print("details: ", expt)
    exit(1)

# Extracting main information (location (latitde & longitude), magnitude)
places = [feature["properties"]["place"] for feature in data ["features"]]
magnitudes = [feature["properties"]["mag"] for feature in data ["features"]]
times = [feature["properties"]["time"] for feature in data ["features"]] 
longs = [feature["geometry"]["coordinates"][0] for feature in data ["features"]]
lats = [feature["geometry"]["coordinates"][1] for feature in data ["features"]]

# Making a coordinates list
coords = [[lat, lon, mag] for lat, lon, mag in zip(lats, longs, magnitudes)]

# Main project folium map
m = folium.Map(location=[36.5, 37.5], tiles=None, zoom_start=3)

#Primary basemaps
basemap0 = folium.TileLayer("cartodbdark_matter", name="Dark Theme Basemap").add_to(m)
basemap1 = folium.TileLayer("openstreetmap", name="Open Street Map").add_to(m)

# Defning a color ramp for the heat map
colors = {0.2: '#0f0b75', 0.45: '#9e189c', 0.75: '#ed7c50', 1: '#f4ee27'}

# Adding the folium heatmap layer using the HeatMap plugin
heatmap = HeatMap(data=coords, gradient=colors, name="Earthquake Distribution Heatmap").add_to(m)

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
    
    # converting API earthquake time info from unix time to human-readable time format
    time_date = datetime.fromtimestamp(time/1000.0).strftime("%Y-%m-%d") 
    time_hour = datetime.fromtimestamp(time/1000.0).strftime("%H:%M:%S") 
    # Configure data display in popups when clicking on markers <span></span>
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

# saving the map as html and opening it in default browser
m.save("index.html")
webbrowser.open("index.html")
