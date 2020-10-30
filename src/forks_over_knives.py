import argparse
from clean_data import *
from plots import *
from hypothesis import *

def read_cancer_data(filename):
    # Returns data frame with cancer data
    df_cases = pd.read_csv(filename)  # ('../data/CI5-XI/cases.csv')
    df_cases2 = remove_subset_codes(df_cases)
    df_cases3 = annualize_case_data(df_cases2)
    df_cases3.set_index('REGISTRY')
    return df_cases3

def read_population_data(filename):
    # Returns data frame with cancer data
    df_pop = pd.read_csv(filename)  # (../data/CI5-XI/pop.csv')
    df_pop2 = add_total_pop(df_pop)
    df_pop3 = annualize_pop_data(df_pop2)
    return df_pop3

def read_cancer_registry(filename):
        # Returns data frame with cancer data
    df_registry = pd.read_csv(filename, sep = "\t", header=0, encoding='iso-8859-1') # '../data/CI5-XI/cancer_summary.txt'
    # cleansing
    df_registry.columns = (['REGISTRY', 'country_long'])
    df_reg = munge_registry(df_registry)
    return df_reg

def dump_df(filename, df):
    df.to_csv(filename)    

def reload_df_utf8(filename):
    df = pd.read_csv(filename, encoding='utf-8')
    return df    

def combine_data(df_cancer_data, df_animal_cons):
    df_combo = df_cancer_data.merge(df_animal_cons, on="Alpha3", suffixes=('', '_animal'))
    df_combo2 = df_combo.loc[:,('country_name', 'Alpha3', 'N20_49', 'P20_49', 'TOTAL', 'Total_Pop', 'Incidence Per Age Capita', 'year', 'animal_product_kg_cap_yr')]

    return df_combo2

def plotting(df_combo):
    #Correlation plots
    df_combo['corr_diff'] = df_combo['animal_product_kg_cap_yr'] - df_combo['Incidence Per Age Capita']
    correlation_plot(df_combo)
    df_bar = df_combo.sort_values('corr_diff', ascending=False).iloc[:10, :]
    df_bar2 = df_combo.sort_values('corr_diff', ascending=True).iloc[:10, :]
    correlation_bar(df_bar, 'Most')
    correlation_bar(df_bar2, "Least")



if __name__ == '__main__':
    '''
    todo: We'll use this to accept filenames as parameteris
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="text file containing words")
    ap.add_argument("-m", "--mode", required=True, help="""mode determining
                    output. single: computation times based on one random
                    selection from word list, average: computation times based
                    on average of 10 random selections from word list""")
    ap.add_argument("-t", "--fit", required=True, help="""True or False: plot
                    polynomial fit on plots""")
    args = vars(ap.parse_args())

    if args['mode'] == 'single': ...
    '''
    # Cancer and population data from WHO
    df_cases = read_cancer_data('../data/CI5-XI/cases.csv')
    df_pop = read_population_data('../data/CI5-XI/pop.csv')

    # Lookup tables
    df_registry = read_cancer_registry('../data/CI5-XI/registry.txt')
    df_all_countries = pd.read_csv('../data/country_iso.csv')

    # Meat and animal product consumption data from FAO via ___
    df_meat = pd.read_csv('../data/FAO/per-capita-meat-consumption-by-type-kilograms-per-year.csv')
    df_milk = pd.read_csv('../data/FAO/per-capita-milk-consumption.csv')
    df_egg = pd.read_csv('../data/FAO/per-capita-egg-consumption-kilograms-per-year.csv')

    print('Number of rows in cases: {}'.format(len(df_cases)))
    print('Number of rows in pop: {}'.format(len(df_pop)))
    print('Number of rows in registry: {}'.format(len(df_registry)))

    print('Number of rows in raw meat, milk, egg data (mult year): {}, {}, {}'.format(len(df_meat), len(df_milk), len(df_egg)))
    print('Number of rows in country iso : {}'.format(len(df_all_countries)))

    # Munging the registry data, already done.
    # df_registry2 = munge_registry(df_registry)

    # Removed because it's not working correctly.  Using fixed data file now.
    dump_df('../data/clean_registry.csv', df_registry)
    df_reg = reload_df_utf8('../data/clean_registry.csv')
    print('Reloaded reg UTF-8 Number of rows in registry: {}'.format(len(df_reg)))

    df_cancer_data = turn_cancer_to_per_capita(df_cases, df_pop, df_reg)
    df_cancer_by_iso = get_cancer_isos(df_cancer_data, df_all_countries)

    # Munging the Animal product data => one single data set to work with, animal consumption 
    df_animal_cons = munge_meats(df_meat, df_milk, df_egg, 2008)
    df_animal_by_iso = get_animal_isos(df_animal_cons, df_all_countries)

    dump_df('../data/clean_animal.csv', df_animal_by_iso)
    dump_df('../data/clean_cases.csv', df_cancer_by_iso)

    # reduce to countries in common
    df_combo = combine_data(df_cancer_by_iso, df_animal_by_iso)

    # set back to USA
    df_combo['country_name'] = list(map(fix_usa_back, df_combo['country_name']))
    dump_df('../data/combo.csv', df_combo)    

    country_list = countries_in_common(df_combo)
    print('Countries in common: {} '.format(len(country_list)))

    #reduce both datasets to countries in common for mapping

    print("\nPlotting")
    # World Map, Animal product consumption
    #m = world_map(df_animal_cons, 'alpha3', 'animal')
    m = world_map(df_combo, 'alpha3', 'animal')
    m.save('../images/animal_consumption.html')

    # World Map, Cancer rates
    m_c = world_map(df_cancer_by_iso, 'alpha3', 'cases')
    m_c.save('../images/cancer_percapita.html')

    # Correlation Plots
    plotting(df_combo)

    # Hypothesis Test
    p_value = gen_stats(df_combo)


    print('\nComplete')

