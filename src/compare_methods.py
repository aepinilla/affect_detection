"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import pingouin as pg
from pingouin import ttest
import seaborn as sns
from scipy import stats
pd.options.mode.chained_assignment = None  # default='warn'

from src.helper import conduct_iqr, strings2means
from src.settings import d, dimensions, feature_selection_approaches, participants_codes


def remove_outliers():
    all_participant_metrics = []
    for p in participants_codes:
        for fsa in feature_selection_approaches:
            file_path = (d + '/reports/metrics/%s/' % (fsa)) + p + '.csv'
            participant_metrics = pd.read_csv(file_path)
            participant_metrics = participant_metrics.reset_index(drop=['index'])
            participant_metrics = participant_metrics.rename(columns = {'Unnamed: 0': 'random_state', 'Unnamed: 1': 'metric'})
            participant_metrics['participant'] = p
            participant_metrics['approach'] = fsa

            for dim in dimensions:
                dim_metrics = participant_metrics[dim]
                means_dimension = dim_metrics.apply(lambda row: strings2means(row[1:-1]))
                participant_metrics[dim] = means_dimension

            all_participant_metrics.append(participant_metrics)

    all_metrics_df = pd.concat(all_participant_metrics)
    # Precision, recall and F1-score
    all_means = all_metrics_df.groupby(['participant', 'approach', 'metric']).mean()
    all_means = all_means.drop(['random_state'], axis=1)
    all_means_of_means = all_means.groupby(['approach', 'metric']).mean()
    all_std_of_means = all_means.groupby(['approach', 'metric']).std()
    print(round(all_means_of_means * 100, 4))
    print(round(all_std_of_means * 100, 3))
    # Subset accuracy
    accuracy = all_metrics_df.loc[all_metrics_df['metric'] == 'accuracy']
    # Participant means
    means_pp = accuracy.groupby(['participant', 'approach']).mean()
    means_pp = means_pp.reset_index().drop(['random_state'], axis=1)
    # Reshape data
    reshaped_data = means_pp.melt(id_vars=['participant', 'approach'], var_name='dimension', value_name='mean_accuracy')
    # Remove outliers
    outlier_participants = list(conduct_iqr(reshaped_data))
    no_outliers = reshaped_data[~reshaped_data['participant'].isin(outlier_participants)]
    no_outliers['mean_accuracy'] = no_outliers['mean_accuracy'] * 100
    no_outliers['approach'] = no_outliers['approach'].str.upper()

    return no_outliers, outlier_participants


def compare_methods():
    no_outliers, outlier_participants = remove_outliers()
    # Assupmtions check
    # Shapiro-Wilk test of normal distribution
    results_shapiro = stats.shapiro(no_outliers['mean_accuracy'])
    print('Shapiro-Wilk statistic: ' + str(round(results_shapiro[0], 3)))
    print('Shapiro-Wilk p-value: ' + str(round(results_shapiro[1], 3)))
    # Sphericity
    # Mauchly's test of sphericity
    result_mauchly = pg.sphericity(no_outliers, dv='mean_accuracy', subject='participant', within=['approach', 'dimension'])
    print('Mauchly test chi2: ' + str(round(result_mauchly[2], 3)))
    print('Mauchly test p-value: ' + str(round(result_mauchly[4], 3)))
    # ANOVA
    # Perform two-way repeated m ANOVA
    two_way_aov = pg.rm_anova(dv='mean_accuracy', within=['approach', 'dimension'], subject='participant', data=no_outliers)
    print('Results of two-way repeated measures ANOVA:')
    print(two_way_aov)
    # Main effect for dimension
    main_effect_dimension = pg.anova(dv='mean_accuracy', between='dimension', data=no_outliers, detailed=True)
    print('Main effect of affect dimension:')
    print(main_effect_dimension)
    # Main effect for feature selection method
    print('Main effect of feature selection method:')
    main_effect_approach = pg.anova(dv='mean_accuracy', between='approach', data=no_outliers, detailed=True)
    print(main_effect_approach)
    # Paired samples t-test
    nested_dict = lambda: defaultdict(nested_dict)
    posthoc_results = nested_dict()
    for dim in dimensions:
        dim_data = no_outliers.loc[no_outliers.dimension == dim]
        dim_rfecv = dim_data.loc[dim_data.approach == 'RFECV'][['mean_accuracy']].values.flatten()
        dim_lme = dim_data.loc[dim_data.approach == 'LME'][['mean_accuracy']].values.flatten()
        res_dim_ttest = ttest(dim_rfecv, dim_lme, paired=True).round(3)
        posthoc_results[dim]['ttest_results'] = res_dim_ttest.copy()
        posthoc_results[dim]['mean_lme'] = dim_lme.mean().round(3)
        posthoc_results[dim]['mean_rfecv'] = dim_rfecv.mean().round(3)
        posthoc_results[dim]['std_lme'] = dim_lme.std().round(3)
        posthoc_results[dim]['std_rfecv'] = dim_rfecv.std().round(3)

    print('Results of pair-waise t-test (posthoc analysis):')
    for dim in dimensions:
        print('Results for dimension: ' + dim)
        print('T-test:')
        print(posthoc_results[dim]['ttest_results'])
        print('Mean LME: ')
        print(posthoc_results[dim]['mean_lme'])
        print('Mean RFECV: ')
        print(posthoc_results[dim]['mean_rfecv'])
        print('STD LME: ')
        print(posthoc_results[dim]['std_lme'])
        print('STD RFECV: ')
        print(posthoc_results[dim]['std_rfecv'])

    # Plot
    sns.set_palette("Paired")
    sns.set_style("whitegrid")
    g = sns.barplot(data=no_outliers, x="dimension", y="mean_accuracy", hue='approach')
    g.set(xlabel='Affective dimension', ylabel='Mean accuracy of classification models')
    g.set_xticklabels(['Negativity', 'Positivity', 'Net Predisposition'])
    g.legend(title='Feature selection method')
    sns.move_legend(g, "lower left")
    g.yaxis.set_major_formatter('{x:1.0f}%')
    plt.savefig(d + '/reports/figures/anova_results.png', dpi=300)
    plt.show()


if __name__ == "__main__":
    compare_methods()