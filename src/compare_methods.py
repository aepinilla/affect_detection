"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import pingouin as pg
from pingouin import ttest
import seaborn as sns
from scipy import stats
pd.options.mode.chained_assignment = None  # default='warn'

from src.helper import remove_outliers
from src.participants_age import participants_age
from src.settings import d, corrupted_participants, dimensions, feature_selection_approaches, participants_codes


def compare_methods():
    all_metrics_df, no_outliers, outlier_participants = remove_outliers()
    # Calculate participant's age
    participants_age(outlier_participants)
    results_dict = {}

    # Precision, recall and F1-score
    all_metrics_df_non_outliers = all_metrics_df[~all_metrics_df['participant'].isin(outlier_participants)]
    all_means = all_metrics_df_non_outliers.groupby(['participant', 'approach', 'metric']).mean()
    all_means = all_means.drop(['random_state'], axis=1)
    all_means_of_means = all_means.groupby(['approach', 'metric']).mean()
    all_std_of_means = all_means.groupby(['approach', 'metric']).std()
    results_dict['all_means_of_means'] = round((all_means_of_means * 100), 2)
    results_dict['all_std_of_means'] = round((all_std_of_means * 100), 2)

    # Assupmtions check
    # Shapiro-Wilk test of normal distribution
    results_shapiro = stats.shapiro(no_outliers['mean_accuracy'])
    results_dict['shapiro-statistic'] = round(results_shapiro[0], 3)
    results_dict['shapiro-p'] = round(results_shapiro[1], 3)
    # print('Shapiro-Wilk statistic: ' + str(round(results_shapiro[0], 3)))
    # print('Shapiro-Wilk p-value: ' + str(round(results_shapiro[1], 3)))
    # Sphericity
    # Mauchly's test of sphericity
    result_mauchly = pg.sphericity(no_outliers, dv='mean_accuracy', subject='participant', within=['approach', 'dimension'])
    results_dict['mauchly-chi2'] = round(result_mauchly[2], 3)
    results_dict['mauchly-p'] = round(result_mauchly[4], 3)
    # print('Mauchly test chi2: ' + str(round(result_mauchly[2], 3)))
    # print('Mauchly test p-value: ' + str(round(result_mauchly[4], 3)))
    # ANOVA
    # Perform two-way repeated m ANOVA
    two_way_aov = pg.rm_anova(dv='mean_accuracy', within=['approach', 'dimension'], subject='participant', data=no_outliers)
    results_dict['two_way_aov'] = two_way_aov
    # print('Results of two-way repeated measures ANOVA:')
    # print(two_way_aov)
    # Main effect for dimension
    main_effect_dimension = pg.anova(dv='mean_accuracy', between='dimension', data=no_outliers, detailed=True)
    results_dict['main_effect_dimension'] = main_effect_dimension
    # print('Main effect of affect dimension:')
    # print(main_effect_dimension)
    # Main effect for feature selection method
    main_effect_approach = pg.anova(dv='mean_accuracy', between='approach', data=no_outliers, detailed=True)
    results_dict['main_effect_approach'] = main_effect_approach
    # print('Main effect of feature selection method:')
    # print(main_effect_approach)
    # Paired samples t-test
    posthoc_results = {
        'negativity' : dict(),
        'positivity': dict(),
        'net_predisposition': dict()
    }
    for dim in dimensions:
        dim_data = no_outliers.loc[no_outliers.dimension == dim]
        dim_rfecv = dim_data.loc[dim_data.approach == 'RFECV'][['mean_accuracy']].values.flatten()
        dim_lme = dim_data.loc[dim_data.approach == 'LME'][['mean_accuracy']].values.flatten()
        res_dim_ttest = ttest(dim_rfecv, dim_lme, paired=True).round(3)
        posthoc_results[dim]['ttest_results'] = res_dim_ttest.copy()
        posthoc_results[dim]['mean_lme'] = dim_lme.mean().round(2)
        posthoc_results[dim]['mean_rfecv'] = dim_rfecv.mean().round(2)
        posthoc_results[dim]['std_lme'] = dim_lme.std().round(2)
        posthoc_results[dim]['std_rfecv'] = dim_rfecv.std().round(2)

    results_dict['posthoc'] = posthoc_results
    results_file_name = d + '/reports/results.pickle'
    with open(results_file_name, 'wb') as handle:
        pickle.dump(results_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


    sns.set_palette("Paired")
    sns.set_style("whitegrid")
    g = sns.barplot(data=no_outliers, x="dimension", y="mean_accuracy", hue='approach')
    g.set(xlabel='Affective dimension', ylabel='Mean accuracy of classification models')
    g.set_xticklabels(['Negativity', 'Positivity', 'Net Predisposition'])
    g.set_yticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])
    g.legend(title='Feature selection method')
    sns.move_legend(g, "lower left")
    plt.savefig(d + '/reports/figures/anova_results.jpg', dpi=300)
    plt.show()


if __name__ == "__main__":
    compare_methods()