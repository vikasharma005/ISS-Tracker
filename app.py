
import streamlit as st
import folium
from streamlit_folium import folium_static
import urllib.request
import json
import geocoder

def main():

    with st.sidebar:
      st.image("https://github.com/vikasharma005/ISS-Tracker/blob/main/iss.png")
      st.title("ISS Location Tracker")

    # Fetch and display astronaut data
    astronaut_data = fetch_astronaut_data()
    st.write(f"There are currently {astronaut_data['number']} astronauts on the ISS:")
    for person in astronaut_data['people']:
        st.write(f"- {person['name']}")

    # Display user's current lat/long
    user_location = get_user_location()
    st.write(f"Your current lat/long is: {user_location}")

    # Display ISS location on a map
    iss_lat, iss_lon = fetch_iss_location()
    m = create_map(iss_lat, iss_lon)
    folium_static(m)

def fetch_astronaut_data():
    url = "http://api.open-notify.org/astros.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    return result

def get_user_location():
    g = geocoder.ip('me')
    return g.latlng

def fetch_iss_location():
    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    location = result["iss_position"]
    lat = float(location['latitude'])
    lon = float(location['longitude'])
    return lat, lon

def create_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=2)
    
    # Add the ISS icon as a marker
    icon = folium.CustomIcon(icon_image="https://github.com/vikasharma005/ISS-Tracker/blob/main/iss.png", icon_size=(50, 50))
    folium.Marker([lat, lon], icon=icon, popup="ISS").add_to(m)

    return m

if __name__ == "__main__":
    main()

