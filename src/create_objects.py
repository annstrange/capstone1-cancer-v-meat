import argparse
from clean_data import *
from plots import *


def read_cancer_data(filename):
    # Returns data frame with cancer data
    df_cases = pd.read_csv(filename)  # ('../data/CI5-XI/cases.csv')
    df_cases.set_index('REGISTRY')
    return df_cases

def read_population_data(filename):
    # Returns data frame with cancer data
    df_pop = pd.read_csv(filename)  # (../data/CI5-XI/pop.csv')
    return df_pop

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
    df_combo2 = df_combo.loc[:,('country_name', 'Alpha3', 'N20_49', 'P20_49', 'Incidence Per Age Capita', 'year', 'animal_product_kg_cap_yr')]

    return df_combo2


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
    #dump_df('../data/clean_registry.csv', df_registry2)
    df_reg = reload_df_utf8('../data/clean_registry.csv')
    print('Reloaded reg UTF-8 Number of rows in registry: {}'.format(len(df_reg)))

    df_cancer_data = turn_cancer_to_per_capita(df_cases, df_pop, df_reg)
    df_cancer_by_iso = get_cancer_isos(df_cancer_data, df_all_countries)

    # Munging the Animal product data => one single data set to work with, animal consumption 
    df_animal_cons = munge_meats(df_meat, df_milk, df_egg, 2008)
    df_animal_by_iso = get_animal_isos(df_animal_cons, df_all_countries)

    dump_df('../data/clean_animal.csv', df_animal_by_iso)
    dump_df('../data/clean_cases.csv', df_cancer_by_iso)

    # World Map, Animal product consumption
    m = world_map(df_animal_cons, 'alpha3', 'animal')
    m.save('../images/animal_consumption.html')

    # World Map, Cancer rates
    m_c = world_map(df_cancer_by_iso, 'alpha3', 'cases')
    m_c.save('../images/cancer_percapita.html')

    # reduce to countries in common
    df_combo = combine_data(df_cancer_by_iso, df_animal_by_iso)
    dump_df('../data/combo.csv', df_combo)    




    '''
    Todo: implement plotting
    print("\nPlotting")
    fname = 'm1_plot.png'
    ax = plot_computation_time(n_lst, comp_times_m1, title='method 1, double for',
                               label='m1: double for', color='blue', fname=fname,
                               keepopen=args['fit'])
    if args['fit'] == 'True':
        plot_fit(x, y_m1, p_m1, fname, ax)

    fname = 'm2_plot.png'
    ax = plot_computation_time(n_lst, comp_times_m2, title='method 2, use dictionary',
                               label='m2: use dict', color='green', fname=fname,
                               keepopen=args['fit'])
    if args['fit'] == 'True':
        plot_fit(x, y_m2, p_m2, fname, ax)

    '''
    print('\nComplete')

