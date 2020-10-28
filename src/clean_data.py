import pandas as pd 
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt 
import folium



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

def std_country_region (country_region_col):
    '''
    country_col is a string value, standardize format
    ARGS:
        country_col String to transform
    RETURN:
        ISO recognized country name 
    '''
    dict = { 
        'Australian Capital Territory' : 'Australia, Australian Capital Territory',
        'Greater Poland':'Poland',
        'Iran':'Iran, Islamic Replublic of',
        'Republic of Korea':'Korea (South)',                  
        'South Australia':'Australia, South Australia',
        'The Netherlands':'Netherlands',
        'UK':'United Kingdom',
        'USA':'United States of America',
        'Western Australia':'Australia, Western Australia'
    }
    if (dict.get(country_region_col) == None):
        return country_region_col
    else:
        return dict.get(country_region_col)

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
    # one off fix for Australia to make it roll up as a single country
    df_registry['country_region'] = list(map(std_country_region, df_registry['country_region']))

    df_registry['star'] = list(map(get_country_star, df_registry['country_long']))
    # change this to get country from cleansed country_region 
    df_registry['country_name'] = list(map(get_country, df_registry['country_region'])) 

    df_registry['is_national'] = list(map(set_national, df_registry['country_region']))
    # Some countries have cancer data at the national level and a sub-region by registry.  Others have regions that need to be summed.
    # Detect national registry by format of country name not containing ;:, then exclude all non national subsets for that country
    df_reg_group2 =  df_registry.groupby('country_name')['is_national'].sum().reset_index()
    #print('columns are {}'.format(df_registry.columns))

    # Zombie column wants to be here from last run, what the heck. 
    cols = ['is_national_exists', 'is_subset']
    for col in cols:
        if col in df_registry.columns:
            df_registry = df_registry.drop(columns=col, axis=1)
    df_registry.reset_index()        

    df_registry2 = df_registry.merge(df_reg_group2, left_on=['country_name'], right_on=['country_name'], suffixes=['', '_exists'])
    #print('columns are {}'.format(df_registry2.columns))
    # Trouble here, we seem to have to cols w/ same name, WTF, doesn't happen in Lab
    df_registry2['is_subset'] = list(map (set_is_subset, df_registry2['is_national_exists'], df_registry2['is_national']) )

    # use mask to eliminate redundant registries.  count goes from 464 to 273. 
    df_reduced = df_registry2[(df_registry2['is_national'] == 1 ) | (df_registry2['is_subset'] == 1)] 
    #df_reduced = df_registry2[(df_registry2['is_national'] == 1 ) | (df_registry2['is_national_exists'] == 0)] 
    df_reduced.set_index('REGISTRY')
    return df_reduced


def munge_meats(df_meat, df_milk, df_egg, year=2008):
    '''
    Accepts three data frames with annual meat, milk, and egg consumption data, cleans and reduceds them
    returns dataframe with joined, filtered, and summed data on kg per capital animal product consumption
    '''

    columns = (['country_name', 'country_code', 'year', 'bovine', 'poultry', 'pig', 'goat', 'other' ])
    df_meat.columns = columns
    df_meat2 = df_meat.fillna(0)
    df_meat2['meat'] = df_meat2['bovine'] + df_meat2['poultry']+ df_meat2['pig']+ df_meat2['goat']+ df_meat2['other']

    columns = (['country_name', 'country_code', 'year', 'milk'])
    df_milk.columns = columns
    df_milk2 = df_milk.fillna(0)

    columns = (['country_name', 'country_code', 'year', 'egg'])
    df_egg.columns = columns
    df_egg2 = df_egg.fillna(0)

    # filter year 
    df_meat3 = df_meat2[df_meat2['year'] == year]  #209 records expected
    df_milk3 = df_milk2[df_milk2['year'] == year]  #209
    df_egg3 = df_egg2[df_egg2['year'] == year]


    df_animal1 = df_meat3.merge(df_milk3, left_on='country_name', right_on = 'country_name', suffixes=('', '_milk'))
    df_animal2 = df_animal1.merge(df_egg3, left_on='country_name', right_on = 'country_name', suffixes=('', '_egg'))

    # sum
    df_animal2['animal_product_kg_cap_yr'] = df_animal2['meat'] + df_animal2['milk'] + df_animal2['egg'] 

    # select only columns we care about
    df_animal3 = df_animal2.loc[:,('country_name', 'country_code', 'year', 'animal_product_kg_cap_yr')]
    return df_animal3

def turn_cancer_to_per_capita(df_cases, df_pop):
    # returns reduced dataframe for registries we want, summed and merged with population data
    # Note: I can decide to accept df's as args (functional) or use pseudo-oop here w df's part of the state
    
    df_cases.drop(['N_unk','N85', 'N80_84', 'N75_79','N70_74','N65_69','N60_64','N55_59','N50_54','N0_4','N5_9','N10_14','N15_19'], axis=1, inplace=True)
    df_cases['N20_49'] = df_cases['N20_24'] + df_cases['N25_29'] + df_cases['N30_34'] + df_cases['N35_39'] + df_cases['N40_44'] + df_cases['N45_49']
    df_case_sum = df_cases.groupby(['REGISTRY']).sum()['N20_49'].reset_index()

    df_pop.drop(['P_unk','P85', 'P80_84', 'P75_79','P70_74','P65_69','P60_64','P55_59','P50_54','P0_4','P5_9','P10_14','P15_19'], axis=1, inplace=True)
    df_pop['P20_49'] = df_pop['P20_24'] + df_pop['P25_29'] + df_pop['P30_34'] + df_pop['P35_39'] + df_pop['P40_44'] + df_pop['P45_49']
    df_pop_sum = df_pop.groupby(['REGISTRY']).sum()['P20_49'].reset_index()

    df_case_v_pop = df_case_sum.merge(df_pop_sum, left_on='REGISTRY', right_on='REGISTRY', suffixes=('', '_pop'))

    df_case_v_pop_reg = df_case_v_pop.merge(df_reg, left_on='REGISTRY', right_on='REGISTRY', suffixes=('', '_lu'))[['REGISTRY', 'N20_49', 'P20_49', 'country_name']]
    df_case_v_pop_country = df_case_v_pop_reg.groupby('country_name').agg({'N20_49':sum, 'P20_49':sum}).reset_index()
    df_case_v_pop_country.sort_values('country_name')

    df_case_v_pop_country['Incidence Per Age Capita'] = df_case_v_pop_country['N20_49'] / df_case_v_pop_country['P20_49'] * 100

    return df_case_v_pop_country

def cancer_pc_by_country (df_cancer, df_all_countries):
     # returns cancer per capita joined with the country table, reduced to our set of countries


    df_cancer_pc_by_country = df_cancer.merge(df_all_countries, how='left', left_on="country_name", right_on='Name', suffixes = ('', 'iso'))

    return df_cancer_pc_by_country

def get_cancer_isos(df_cancer, df_iso):

    #df_results = 

    #return df_results
    pass

def get_animal_isos(df_animal, df_iso):

    df_results = df_animal.merge(df_iso, left_on='country_code', right_on = 'Alpha3')  
    return df_results

