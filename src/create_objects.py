import argparse
from clean_data import *


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

def join_cancer_data():
    # returns reduced dataframe for registries we want, summed and merged with population data
    # Note: I can decide to accept df's as args (functional) or use pseudo-oop here w df's part of the state
    

    #return df_joined
    pass 

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

    df_cases = read_cancer_data('../data/CI5-XI/cases.csv')
    df_pop = read_population_data('../data/CI5-XI/pop.csv')
    df_registry = read_cancer_registry('../data/CI5-XI/registry.txt')

    print('Number of rows in cases: {}'.format(len(df_cases)))
    print('Number of rows in pop: {}'.format(len(df_pop)))
    print('Number of rows in registry: {}'.format(len(df_registry)))

    dump_df('../data/cases_tmp.csv', df_cases)
    dump_df('../data/pop_tmp.csv', df_pop)
    dump_df('../data/clean_registry.csv', df_registry)
    df_reg = reload_df_utf8('../data/clean_registry.csv')


    print('Reloaded reg UTF-8 Number of rows in registry: {}'.format(len(df_reg)))

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

