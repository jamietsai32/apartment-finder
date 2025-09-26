import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import folium

df = pd.read_csv('apartments.csv')

st.title('Campus Housing Finder')
st.subheader('Find apartments based on your preferences')
st.write('Choose your preferences and narrow down your apartment search.')
rent_range = st.slider('Select Rent Range', 500, 2500, (1000, 1500), step=100)
filtered_df = df[(df['Rent'] >= rent_range[0]) & (df['Rent'] <= rent_range[1])]
num_bedrooms = st.multiselect('Select Number of Bedrooms', options=sorted(df['Bedrooms'].unique()), default=sorted(df['Bedrooms'].unique()))
filtered_bd = filtered_df[filtered_df['Bedrooms'].isin(num_bedrooms)]
num_bathrooms = st.multiselect('Select Number of Bathrooms', options=sorted(df['Bathrooms'].unique()), default=sorted(df['Bathrooms'].unique()))
filtered_bath = filtered_bd[filtered_bd['Bathrooms'].isin(num_bathrooms)]
room_type = st.selectbox('Select Room Type', options=['Private Bedroom', 'Shared Bedroom'], index=0)
filtered_type = filtered_bath[filtered_bath['Room Type'] == room_type]
walk_dist = st.slider('Select Maximum Walking Time to Campus (minutes)', 5, 10, 15, step=1)
final_df = filtered_type[filtered_type['Distance to Campus'] <= walk_dist]

final_df["Distance to Campus"] = final_df["Distance to Campus"].astype(str) + " min walk"
final_df["Rent"] = "$" + final_df["Rent"].astype(str)

if "button_pressed" not in st.session_state:
    st.session_state.button_pressed = False

if (st.button('Search Apartments')):
    st.session_state.button_pressed = True
if st.session_state.button_pressed:
    if final_df.empty:
        st.write('No apartments found matching your criteria.')
    else:
        st.write(f'Found {len(final_df)} apartments matching your criteria:')
        show_columns = ['Name', 'Address', 'Bedrooms', 'Bathrooms', 'Room Type', 'Rent', 'Distance to Campus', 'Amenities']
        st.dataframe(final_df[show_columns].reset_index(drop=True))
        map = folium.Map(location=[43.0731, -89.4012], zoom_start=15)
        for idx, row in final_df.iterrows():
            folium.Marker(
                location=[row['LATITUDE'], row['LONGITUDE']],
                popup=f"{row['Name']}",
                icon=folium.Icon(color="red", icon="home", prefix="fa")
            ).add_to(map)
        st_folium(map, width=700, height=500)
    