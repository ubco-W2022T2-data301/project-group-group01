import pandas as pd
import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import dates as dates
import numpy as np
import warnings as w



def unique_regions(*dfs, col_name='GEO'): 
    """
    Takes pandas dataframes and a conserved region column name and returns a list of sets,
    with each set in the list containing the unique regions per given dataframe.

    Parameters:
    *dfs (pandas.DataFrame): specified dataframes containing a column with conserved name.
    col_name (str): The name of the column containing the region names. (Default is 'GEO').

    Returns:
    list: A list of sets, where each set contains the unique regions for a given dataframe.
    The first set contains regions unique to the first dataframe, the second set contains regions unique
    to the second dataframe, etc.
    """
    regions = []
    for df in dfs:
        regions.append(set(df[col_name].unique()))
    unique_sets = []
    for i, region_set in enumerate(regions):
        unique_set = set()
        for j, other_set in enumerate(regions):
            if i == j:
                continue
            unique_set.update(region_set.difference(other_set))
        unique_sets.append(unique_set)
    return unique_sets




def calculate_total_rate_change_NI(NI_Wrangled_Final):
    """
    Using the pandas dataframe `NI_Wrangled_Final` with columns "GEO" and "VALUE", 
    calculates the total rate change for each unique "GEO" value.
    
    Returns:
    a pandas dataframe with columns "GEO" and "NI_rate_total", sorted in ascending order by "NI_rate_total".
    """
    w.filterwarnings("ignore", message="The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.")

    total_rate_change_NI = pd.DataFrame(columns=["GEO", "NI_rate_total"])

    for city in NI_Wrangled_Final["GEO"].unique():
        city_df = NI_Wrangled_Final[NI_Wrangled_Final["GEO"] == city]
        diff_rates = [city_df.iloc[i+1]["VALUE"] - city_df.iloc[i]["VALUE"] for i in range(len(city_df)-1)]
        avg_diff = sum(diff_rates) / len(diff_rates)
        city_rate_change = pd.DataFrame({"GEO": [city], "NI_rate_total": [avg_diff * len(city_df)]})

        total_rate_change_NI = pd.concat([total_rate_change_NI, city_rate_change], ignore_index=True)

    total_rate_change_NI = total_rate_change_NI.sort_values('NI_rate_total').reset_index()
    total_rate_change_NI = total_rate_change_NI.drop(columns=['index'])
    
    return total_rate_change_NI