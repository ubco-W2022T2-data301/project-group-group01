import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

PE_Wrangled = pd.read_csv("../data/processed/PE_Wrangled_Final.csv")

def age_grouper():
    """
    This function groups the ages in a given dataset into predefined age ranges, and returns a pandas dataframe containing the total count of individuals in each age group.

    The function takes no arguments and uses a pre-defined dictionary 'age_groups' to group ages into categories.

    Then it calculates the total count of individuals in each age group by summing the 'VALUE' column of the input dataset 'PE_Wrangled' for the corresponding age ranges in the dictionary. It then stores the age group and the total count in a new pandas dataframe 'grouped_df', and returns this dataframe as output.
    """
    warnings.filterwarnings("ignore", category=FutureWarning)
    age_groups = {'20-24': ['20 to 24 years'],
                  '25-29': ['25 to 29 years'],
                  '30-34': ['30 to 34 years'],
                  '35-39': ['35 to 39 years'],
                  '40-44': ['40 to 44 years'],
                  '45-49': ['45 to 49 years'],
                  '50-54': ['50 to 54 years'],
                  '55-59': ['55 to 59 years'],
                  '60-64': ['60 to 64 years'],
                  '65-69': ['65 to 69 years'],
                  '70-74': ['70 to 74 years'],
                  '75-79': ['75 to 79 years']}

    grouped_df = pd.DataFrame(columns=['Age group', 'total_count'])
    for key in age_groups.keys():
        age_range_list = age_groups[key]
        total_count = PE_Wrangled.loc[PE_Wrangled['Age group'].isin(age_range_list), 'VALUE'].sum()
        grouped_df = grouped_df.append({'Age group': key, 'total_count': total_count}, ignore_index=True)

    return grouped_df


def plot_age_distribution(filtered_df):
    """
    Takes pandas dataframes and creates catplots respective of the cities in the dataframe,
    then returns the formatted plots, and saves the plots as .png files.

    Parameters:
    * filtered_df (pandas.DataFrame): specified dataframes containing the GEO, VALUE columns to be plotted.

    Returns:
    .png files: containing an image of the desired catplot.
    plt: seaborn catplots created from the respective dataframes.
    """
    for city in filtered_df['GEO'].unique():
        city_filtered = filtered_df[filtered_df['GEO'] == city].copy()
        g = sns.catplot(x="Age group", y="VALUE", kind="box", data=city_filtered, height=4, aspect=7.5, palette='pastel')
        g.set_xlabels("Age Range")
        g.set_ylabels("Population")
        g.fig.suptitle(f"Age distribution of population in {city}")
        plt.subplots_adjust(top=0.9)
        plt.savefig(f"../images/{city}.png", bbox_inches="tight")
        plt.show()
