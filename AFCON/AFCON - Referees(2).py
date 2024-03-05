#!/usr/bin/env python
# coding: utf-8

# # Data Visualization - African Cup of Nations
# ## Load AFCON match data from github
# Define and adjust the url as needed - in this case I had to change the url to raw.githubusercontent.com to access any raw data
# 

# In[1]:


import requests

# Modify the URL to point to the raw content
url = 'https://raw.githubusercontent.com/Rog96/open-data/master/data/matches/1267/107.json'

# Use requests to fetch the content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # The content of the file can now be accessed via response.text
    # For a JSON file, you can use response.json()
    data = response.json()
    
    # Now you can work with the data object as needed
    print(data)
else:
    print("Failed to retrieve the file")


# In[2]:


import pandas as pd

# Flatten the main structure
df = pd.json_normalize(data)


# In[3]:


df


# In[4]:


df.columns


# ### Visualization 1: Referee Match Counts
# 
# A bar chart showing the number of matches officiated by each referee, which could indicate referee experience or trust by the organizing body.

# In[5]:


import matplotlib.pyplot as plt
import seaborn as sns

# Referee Match Count
plt.figure(figsize=(12, 8))
sns.countplot(data=df, y='referee.name', order=df['referee.name'].value_counts().index)
plt.title('Number of Matches Officiated by Each Referee')
plt.xlabel('Number of Matches')
plt.ylabel('Referee Name')
plt.grid(axis='x')

plt.show()


# ### Visualization 2: Referees by Country
# 
# A bar chart showing the distribution of referees by country, highlighting the diversity (or lack thereof) in referee nationality

# In[6]:


# Assuming 'referee.country.name' is the column with referee nationalities

# Count the number of referees per country and sort them for better visualization
referee_country_counts = df['referee.country.name'].value_counts().reset_index()
referee_country_counts.columns = ['Country', 'Number of Referees']

plt.figure(figsize=(12, 8))
sns.barplot(data=referee_country_counts, x='Number of Referees', y='Country')
plt.title('Distribution of Referees by Country')
plt.xlabel('Number of Referees')
plt.ylabel('Country')

plt.show()


# ### Visualization 3: Referees by Country - Interactive Map
# 
# Using the geopy library to visualize the home country of the referees 

# In[7]:


referee_country = df['referee.country.name']
print(referee_country)


# In[8]:


referee_country_counts


# pip install of the geopy library:
# 
# __Geopy__ is a Python library that provides tools to help developers locate the coordinates of addresses, cities, countries, and landmarks across the world using third-party geocoders and other data sources. It acts as a wrapper for several popular geocoding services, making it easier to perform geocoding (converting addresses into latitude and longitude) and reverse geocoding (converting latitude and longitude into addresses) operations in Python

# In[9]:


#!pip install geopy folium geopandas


# Retrieving longitude & latitude coordinates for each country and storing them in a DataFrame.

# In[10]:


from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geoapiExercises")

referee_coordinates = {}
for country in referee_country_counts['Country']:
    location = geolocator.geocode(country)
    if location:
        referee_coordinates[country] = (location.latitude, location.longitude)

# Convert coordinates to a DataFrame
ref_coords_df = pd.DataFrame.from_dict(referee_coordinates, orient='index', columns=['Latitude', 'Longitude'])
ref_coords_df['Number of Referees'] = referee_country_counts.set_index('Country')['Number of Referees']


# In[11]:


referee_coordinates


# In[12]:


ref_coords_df


# Developing an interactive map to showcase the geographic origins of referees, highlighting the global diversity among them.

# In[13]:


import folium

# Create a base map
m = folium.Map(location=[20, 0], zoom_start=2)

# Add points for each country with referees
for country, row in ref_coords_df.iterrows():
    folium.CircleMarker(
        location=(row['Latitude'], row['Longitude']),
        radius=row['Number of Referees'] / ref_coords_df['Number of Referees'].max() * 20,  # scaling size of circles
        popup=f"{country}: {row['Number of Referees']} referees",
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(m)

# Display the map
m

