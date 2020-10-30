import pandas as pd 
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt 
import folium
import branca
import json
import requests

plt.style.use('ggplot')
plt.rcParams.update({'font.size': 20})

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
        colorscheme = 'BuPu'
    else:  
        # Intent here is a layered look but need to munge the data to create that illusion... todo: 
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

def correlation_plot(df_combo):
    plt.rcParams.update({'font.size': 20})
    df_ranked = df_combo.sort_values('Incidence Per Age Capita', ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(12,5))

    x = np.arange(len(df_ranked['Incidence Per Age Capita']))
    y1 = df_ranked['Incidence Per Age Capita']
    y2 = df_ranked['animal_product_kg_cap_yr']

    ax.set_title('Correlation of Measures')
    ax.plot(x, y1, color='b')
    ax.set_ylabel('Cancer Incidence p/Capita', color='b')
    ax.set_xlabel('Country')

    ax2=ax.twinx()
    ax2.scatter(x, y2, color='dimgrey')
    ax2.set_ylabel('Animal Product Consumption\n kg p/Capita', color='dimgrey')

    plt.savefig('../images/correlation.png')


def correlation_bar(df, title):
    # Expects a dataframe of either the most or least correlated countries
    plt.rcParams.update({'font.size': 14})
    fig, ax  = plt.subplots(figsize=(10,5))

    x = np.arange(len(df['country_name']))
    y1 = df['Incidence Per Age Capita']
    y2 = df['animal_product_kg_cap_yr']


    ax.bar(x, y1, alpha = .4, color='b')
    ax.set_xticks(x)
    ax.set_xticklabels(df['country_name'], rotation=60)
    ax.set_ylabel('Cancer Incidence\n p/Capita', color='b')

    ax2=ax.twinx()
    ax2.bar(x, y2, alpha = .6, color = 'dimgrey')
    ax2.set_ylim ([0,450])
    ax2.set_ylabel('Animal Consumption\n kg p/Capita', color='dimgrey');
    ax.set_title('{} Correlated'.format(title))

    fig.tight_layout()
    plt.savefig('../images/{}_corr.png'.format(title), bbox_inches='tight')

