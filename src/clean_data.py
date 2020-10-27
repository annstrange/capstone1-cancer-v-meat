import pandas as pd 
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt 
import folium
import string


def clean_country_region (country_col):
    '''
    country_col is a string value
    returns
    clean_lst with extra spaces, asterisk, and date range e.g. (2008-2012) removed
    preserves country and region and demographic breakdown
    e.g. country_region should be e.g. "Ecuador, Quito"
    '''
    str1 = country_col.strip().replace('*','')
    str2 = str1.split('(')[0].strip()

    #print(str2)
    return str2

def get_country_star(country_col):
    '''
    country_col is a Series/column which we'll treat as an iterable
    returns
    has star (bool)
    
    '''
    
    #print(country_col)
    idx = country_col.find('*')
    if idx == -1:
        return False
    else:
        return True

def get_country(country_col):
    '''
    Expects string with lots of extras
    returns only the country name
    '''
    str1 = country_col.strip() 
    str2 = str1.split(',')[0].replace('*','')
    str3 = str2.split('(')[0].strip()
    str4 = str3.split(':')[0]
    str5 = str4.split(';')[0]
    #print(str2)
    return str5


def set_national(country_col):
    # Returns true if the country long version let's you know it's national by not having : or ;
    if (country_col.find(':') == -1 and country_col.find(';') == -1 and country_col.find(',') == -1):
        return 1
    else:
        return 0

def set_is_subset(national_exists, is_national):
    # expects two integer values, 1 or 0 for T/F
    # Returns 0 if the national_exists is 1 and is_national is 0, else 1
    if (national_exists == 0 and is_national == 0):
        return 1
    else:   
        return 0

def munge_registry(df_registry):        

    df_registry['country_region'] = list(map(clean_country_region, df_registry['country_long']))
    df_registry['star'] = list(map(get_country_star, df_registry['country_long']))
    df_registry['country_name'] = list(map(get_country, df_registry['country_long'])) 
    df_registry['is_national'] = list(map(set_national, df_registry['country_long']))
    # Some countries have cancer data at the national level and a sub-region by registry.  Others have regions that need to be summed.
    # Detect national registry by format of country name not containing ;:, then exclude all non national subsets for that country
    df_reg_group2 =  df_registry.groupby('country_name')['is_national'].sum().reset_index()
    df_registry2 = pd.merge(df_registry, df_reg_group2, on=['country_name'], suffixes=['', '_exists'])
    df_registry2['is_subset'] = list(map (set_is_subset, df_registry2['is_national_exists'], df_registry2['is_national']) )

    # use mask to eliminate redundant registries.  count goes from 464 to 273. 
    df_reduced = df_registry2[(df_registry2['is_national'] == 1 ) | (df_registry2['is_subset'] == 1)] 
    df_reduced.set_index('REGISTRY')
    return df_reduced



