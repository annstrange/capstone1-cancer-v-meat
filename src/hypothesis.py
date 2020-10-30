
import numpy as np
import pandas as pd
import scipy as sp
import scipy.stats as stats
import matplotlib.pyplot as plt

plt.style.use('ggplot')

# The functions here operate on either of two expected datasets, the least animal consumers or the most

def get_subset (df_combo, nrows, ascending):
    # expects a dataframe with the consolidated data for all countries we have full data for
    # to return the lowest 10 e.g set nrows = 10, ascending = True.
    # 
    return df_combo.sort_values('animal_product_kg_cap_yr', ascending=ascending).head(nrows) 


def weighted_mean (df):

    # Weighted average mean, by P20_49, on low meat population
    df['wav_num'] = df['Incidence Per Age Capita'] * df['P20_49']
    df['wav_num'].sum()
    wav_num = df['wav_num'].sum()
    wav_denom = df['P20_49'].sum()

    wav_mean = wav_num / wav_denom
    return wav_mean

def get_population_size (df):
    tot_pop= df['P20_49'].sum()
    return tot_pop

def get_cases (df):
    tot_cases = df['N20_49'].sum()    
    return tot_cases

def get_shared_sample_freq(df_m, df_v):
    pop_m = get_population_size(df_m)
    cases_m = get_cases(df_m)
    pop_v = get_population_size(df_v)
    cases_v = get_cases(df_v)

    return (cases_m + cases_v) / (pop_m + pop_v)

def get_shared_sample_variance(df_m, df_v, shared_sample_freq):

    tot_pop_m = get_population_size(df_m)
    tot_pop_v = get_population_size(df_v)
    total_pop = tot_pop_m + tot_pop_v
    var = total_pop * (shared_sample_freq * (1 - shared_sample_freq)) / (tot_pop_m * tot_pop_v)  # suuuper small 2.1528615317495398e-11

    return var


def gen_stats(df_combo):

    total_n = len(df_combo)
    df_v = get_subset(df_combo, nrows=10, ascending=True)
    df_m = get_subset(df_combo, nrows=(total_n - 10), ascending=False)

    mean_s = get_shared_sample_freq(df_m, df_v)
    var_s = get_shared_sample_variance(df_m, df_v, mean_s)
    print('Shared mean: {}'.format(mean_s))
    print('Shared var: {}'.format(var_s))

    # use the normal distribution 
    meat_sample_freq = get_cases(df_m) / get_population_size(df_m)
    vegan_sample_freq = get_cases(df_v) / get_population_size(df_v)
    difference_in_sample_proportions = meat_sample_freq - vegan_sample_freq

    difference_in_proportions = stats.norm(mean_s, np.sqrt(var_s))

    p_value = 1 - difference_in_proportions.cdf(difference_in_sample_proportions)
    print("p-value for two sample frequency comparison: {:2.32f}".format(p_value))

    return p_value