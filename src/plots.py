import pandas as pd 
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt 
import folium
import branca
import json
import requests


def world_map(df_map, country_code_type, type):
    '''
    Plots a Folium World map 
    ARGS:
        df_map must have at least a Alpha3 country code or name and numeric value
        country_code_type = str: alpha3, or name
        type = str: animal, cases, combo

    RETURN:
        folium Map    
    '''

    if country_code_type == 'alpha3':
        keyon = 'feature.properties.iso_a3'
    else:
        keyon =  'feature.properties.name'   

    if type == 'animal':
        legendname = 'Animal Product Consumption Kg/Capita/Yr 2008 (age 20-50)'
        keycolumns=['Alpha3', 'animal_product_kg_cap_yr']
        colorscheme = 'Blues'
    elif type == 'cases':
        legendname = "Cancer Indicents Capita/Yr 2008-2012 (age 20-50)"        
        keycolumns=['Alpha3', 'Incidence Per Age Capita']
        colorscheme = 'Reds'
    else:
        legendname = "Correlation between Animal Consumption and Cancer Incidence 2008-2012 (age 20-50)"        
        keycolumns=['Alpha3', 'Incidence Per Age Capita']
        colorscheme = 'Purples'

    geojsonsite = 'https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson'
    worldgeo = json.loads(requests.get(geojsonsite).text)
    m = folium.Map(location=[30, 0], zoom_start=1.6)

    folium.Choropleth(
        geo_data=worldgeo,
        name='choropleth',
        data=df_map,
        columns=keycolumns,  # from my df
        key_on=keyon,
        fill_color=colorscheme,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=legendname,
        nan_fill_color='dimgrey'
    ).add_to(m)

    folium.LayerControl().add_to(m)
    return m



