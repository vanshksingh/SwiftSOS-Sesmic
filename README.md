# QuakeEye

QuakeEye is a Real-Time Earthquake Data Visualization project built using Folium and Streamlit and USGS API.

**Consider starring the project ʕ •ᴥ•ʔ ... ʕ　·ᴥ·ʔ**

## Table of Contents

- [App](#app)
- [Description](#description)
- [Info](#info)
- [Usage](#usage)
- [Preview](#preview)
- [Features](#features)
- [Contributing](#contributing)
- [Credit](#credit)

## App

This is the Streamlit app. The app exists in two forms;

**Streamlit app:** The Strealit app, it lives in the `streamlit-app branch`, it is deployed on Streamlit Community Cloud and accessible at: <https://quakeeye.streamlit.app/>

**Folium app:** A python script to render the Folium map as an HTML file that lives in the project's GitHub Page, built from `folium-app branch`: <https://indigowizard.github.io/QuakeEye/>

## Description

QuakeEye is a data visualization project that displays real-time earthquake data from the USGS API using an interactive map. The project is designed to provide users with an easy-to-use interface for exploring earthquake data on a global scale.

## Info

This project was developed in the wake of the recent unfortunate events of the earthquakes that hit Türkiye and Syria during the month of February 2023, therefore the map is zoomed on the region of Türkiye and Syria common border.

You can zoom-out for a global view of earthquakes around the globe.

## Preview

![ezgif com-gif-maker_qe](https://user-images.githubusercontent.com/43890965/223300592-0cd3e930-d10f-4699-b124-8cfa212ca80f.gif)

## Usage

This app requires Python 3.6 and newer and the following packages:

- `folium`
- `streamlit`

Or:

Install the required packages by running the following command in your terminal:

`conda install --file requirements.txt`

To start the QuakeEye app, run the following command in your terminal:

`streamlit run app.py`

Or:

`python map.py`

## Features

- Interactive map displaying earthquake data
- Real-time updates from the USGS API
- Heatmap of earthquake frequency magnitude distribution
- Marker layers for different categories of earthquakes based on their magnitudes (Richter scale)
- PopUp info on individual earthquake markers; *Magnitude, Date and Time, Location address and Coordinates*
- Dark / Light Theme Basemaps

## Contributing

If you would like to contribute to QuakeEye, read the [contributing guidelines](.github/CONTRIBUTING.md)

## Credit

-- Project by [Ahmed I. Mokhtari](https://www.linkedin.com/in/ahmed-islem-mokhtari/).
