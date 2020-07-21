#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!conda install plotly --yes
#!conda install pandas


# In[2]:


#y


# In[3]:


import plotly.express as px
import pandas as pd

latimes = pd.read_csv(
    "https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/latimes-place-totals.csv"
)


# In[4]:


latimes.head()


# In[5]:


latimes.query("x == 'NaN'")


# In[6]:


# What about positive x (longitude) coordinates?
latimes.query("x > 0")
# any null dates?
latimes.query("date.isnull()", engine='python')
latimes = latimes.query("confirmed_cases != 'NaN' & x < 0 & x != 'NaN' & date.notnull()", engine='python')
latimes.head()


# In[7]:


latimes = latimes.sort_values(by=["date"], ascending=True)
# put it in a variable `lastdate`
lastdate = latimes.iloc[-1]['date']
lastdate


# In[8]:


#by making that variable we can now use it in our query code
latimes_single_day = latimes.query('date==@lastdate')
latimes_single_day


# In[9]:


latimes.confirmed_cases.describe()


# In[10]:


#grouping before is suoer effective(county level)
latimes.groupby("county").confirmed_cases.describe()


# In[11]:


#can use sortby function with column names
latimes_CC = latimes.query("county=='Contra Costa'")
latimes_CC.groupby("place").confirmed_cases.describe().sort_values(by=["max"], ascending=False).head(50)


# In[12]:


WestLA = latimes.query("place == ['Westwood']")
px.bar(WestLA,
      x='date',
      y='confirmed_cases')


# In[47]:


WestLA = latimes.query("place == ['san ramon','danville','pleasenton']")
px.bar(WestLA,
      x='date',
      y='confirmed_cases',
      color ="place",
      facet_row ="place")#makes 3 graphs


# In[14]:


px.scatter(latimes_single_day,
           x='x',
           y='y',
           hover_name='place',
          color = 'confirmed_cases')#can click and drag to zome in (use buttons in top right)


# In[15]:


px.scatter(latimes_single_day,
           x='x',
           y='y',
           color='confirmed_cases', 
           size='confirmed_cases',
           size_max=40, 
           hover_name='place',
           title = 'Confirmed Cases for ' + lastdate,
          color_continuous_scale = 'RdYlGn_r') # added _r to reverse color scheme)


# In[16]:


latimes_single_day_mean = latimes_single_day.confirmed_cases.mean()
latimes_single_day_mean


# In[17]:


px.scatter(latimes_single_day,
           x='x',
           y='y',
           color='confirmed_cases', 
           size='confirmed_cases',
           size_max=40, 
           hover_name='place',
           color_continuous_scale = 'RdYlGn_r', # added _r to reverse color scheme
           range_color = (0,latimes_single_day_mean * 2) # double the mean
          )


# In[18]:


latimes_CC_mean = latimes_CC.confirmed_cases.mean()
latimes_CC_mean


# In[19]:


px.scatter(latimes_CC,
           x='x',
           y='y',
           color='confirmed_cases', 
           size='confirmed_cases',
           size_max=40, 
           hover_name='place',
           animation_frame='date', # this creates a frame by frame animation by day
           color_continuous_scale = 'RdYlGn_r',
           range_color = (0,latimes_CC_mean*2))


# In[20]:


fig = px.scatter_geo(latimes_single_day,
           lon='x',
           lat='y',
           color='confirmed_cases', 
           size='confirmed_cases',
           size_max=40, 
           hover_name='place',
           scope='usa',
           color_continuous_scale = 'RdYlGn_r',
           range_color = (0,latimes_single_day_mean * 2) # double the mean 
            )

fig.update_geos(fitbounds="locations") 


# In[21]:


fig = px.scatter_geo(latimes_CC,
           lon='x',
           lat='y',
           color='confirmed_cases', 
           size='confirmed_cases',
           size_max=40, 
           hover_name='place',
           scope='usa',                     
           animation_frame='date',
           color_continuous_scale = 'RdYlGn_r',
           range_color = (0,latimes_CC_mean*2))

fig.update_geos(fitbounds="locations") 


# In[22]:


help(px.scatter_geo)


# In[23]:


#!conda install -c conda-forge folium


# In[ ]:





# In[24]:


import folium


# In[34]:


# Create a Map instance
map = folium.Map(location=[38,-122], 
               zoom_start=8, 
               control_scale=True
                )

map


# In[39]:


# add a circle
my_circle = folium.Circle(
    radius=10000, # this is in meters
    location=[37.9,-122.2],
    color='crimson',
    fill=True,
)
my_circle.add_to(map)
map


# In[40]:


# add a circle
my_circle = folium.Circle(
    radius=10000, # this is in meters
    location=[37.9,-122.2],
    color='crimson',
    fill=True,
)
my_circle.add_to(map)
map


# In[43]:


# reset the map (only way to get rid of circles)
map = folium.Map(location=[37.9,-122.2], 
                zoom_start=8, 
                control_scale=True,
                tiles='CartoDB dark_matter',
                attr= '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>')
map


# In[44]:


# create a subset dataset for a single day in Los Angeles
latimes_today = latimes.query("date == @lastdate & county == 'Contra Costa'")
latimes_today


# In[46]:


import matplotlib
latimes_today.plot(x ='x', y='y', kind = 'scatter')


# In[49]:


# loop through the rows in Los Angeles, and create a circle based on confirmed cases
for index, row in latimes_today.iterrows():
    # set up the variables
    lat = row['y']
    lon = row['x']
    label = str(row['confirmed_cases']) + ' confirmed cases in ' + row['place']
    size = row['confirmed_cases']
    
    # create a circle for every row
    circle = folium.Circle(
        radius=size,
        location=[lat,lon],
        tooltip = label,
        color='crimson',
        fill = True
    )
    circle.add_to(map)
map


# In[50]:


import altair as alt #fulium support this not plotly


# In[51]:


# reset the map (only way to get rid of circles)
map = folium.Map(location=[37.9,-122.2], 
                zoom_start=8, 
                control_scale=True,
                tiles='CartoDB dark_matter',
                attr= '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>')


# In[52]:


# create a function to create circles, and also add a chart in the popup window (a lot here, will break it up later)
def createCircle(lat,lon,size,place,label):
    # create a bar chart for each circle
    bar = alt.Chart(latimes.query('place == @place')).mark_bar().encode(
        x=alt.X('date', axis=alt.Axis(labels=False)), # turn the labels off because there are too many
        y='confirmed_cases',
        color='confirmed_cases',
        tooltip = ['date','place','confirmed_cases']
    ).properties(width=400,height=200)

    # add the bar chart as a folium feature
    vega = folium.features.VegaLite(
        bar,
        width=600,
        height=200,
    )

    # create the circle
    circle = folium.Circle(
        radius=size,
        location=[lat,lon],
        tooltip = label,
        color='crimson',
        fill = True
    )

    # create a popup
    popup = folium.Popup()

    # add the chart to the popup
    vega.add_to(popup)
    
    # add the popup to the circle
    popup.add_to(circle)
    
    # add the circle to the map
    circle.add_to(map)
    


# In[54]:


# loop through the rows in Los Angeles, and create a circle based on confirmed cases
for index, row in latimes_today.iterrows():
    label = str(row['confirmed_cases']) + ' confirmed cases in ' + row['place']
    createCircle(row['y'],row['x'],row['confirmed_cases'],row['place'],label)

map


# In[55]:


# save it!
map.save('index.html')


# In[ ]:




