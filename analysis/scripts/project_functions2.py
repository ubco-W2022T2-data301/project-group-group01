import pandas as pd
import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import dates as dates
import warnings as w
import re


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


def PE_ordering_filtering(PopEstimate):
    """
    Takes the Population Estimate dataset and drops a number of erraneous columns and rows, then returns the wrangled dataset.
    
    Parameters:
    * PopEstimate (pandas.DataFrame): specified dataframes containing columns and rows with conserved names.
    
    Returns:
    df: a pandas dataframe, containing only the desired metropolitan areas and columns related to population for further analysis.
    """
    w.simplefilter(action='ignore', category=FutureWarning)
    PE_Wrangled = PopEstimate.drop(columns=['DGUID','UOM_ID','SCALAR_FACTOR','SCALAR_ID','VECTOR','COORDINATE','STATUS','SYMBOL','TERMINATED','DECIMALS'], axis=1).reset_index().drop(columns=["index"])
    PE_ordered_filtered = PE_Wrangled.drop(PE_Wrangled[PE_Wrangled.GEO.isin(['Canada',
                                                                'All areas outside census metropolitan areas and census agglomerations, Canada',
                                                                'All census agglomerations, Canada',
                                                                'All census metropolitan areas and census agglomerations, Canada',
                                                                'All census metropolitan areas, Canada',
                                                                'Area outside census metropolitan areas and census agglomerations, Alberta',
                                                                'Area outside census metropolitan areas and census agglomerations, British Columbia',
                                                                'Area outside census metropolitan areas and census agglomerations, Manitoba',
                                                                'Area outside census metropolitan areas and census agglomerations, New Brunswick',
                                                                'Area outside census metropolitan areas and census agglomerations, Newfoundland and Labrador',
                                                                'Area outside census metropolitan areas and census agglomerations, Northwest Territories',
                                                                'Area outside census metropolitan areas and census agglomerations, Nova Scotia',
                                                                'Area outside census metropolitan areas and census agglomerations, Nunavut',
                                                                'Area outside census metropolitan areas and census agglomerations, Ontario',
                                                                'Area outside census metropolitan areas and census agglomerations, Prince Edward Island',
                                                                'Area outside census metropolitan areas and census agglomerations, Quebec',
                                                                'Area outside census metropolitan areas and census agglomerations, Saskatchewan',
                                                                'Area outside census metropolitan areas and census agglomerations, Yukon',
                                                                'Ottawa - Gatineau (CMA), Ontario part, Ontario',
                                                                'Ottawa - Gatineau (CMA), Quebec part, Quebec'])].index).reset_index().drop(columns=["index"])

    PE_ordered_filtered["GEO"] = (PE_ordered_filtered["GEO"].str.replace(r'\(CMA\)', '', regex=True).str.strip().str.replace(r' ,', ',', regex=True).str.strip().str.replace(r' - ', '-', regex=True).str.strip())
    
    PE_ordered_filtered_v2 = PE_ordered_filtered.drop(PE_ordered_filtered[PE_ordered_filtered.GEO.isin(['Barrie, Ontario',
                                                                                           'Abbotsford-Mission, British Columbia',
                                                                                           'Kingston, Ontario', 'Ottawa-Gatineau, Ontario/Quebec',
                                                                                           'Saguenay, Quebec', 'Brantford, Ontario',
                                                                                           'Moncton, New Brunswick'])].index).reset_index().drop(columns=["index"])
    PE_ordered_filtered_v2.to_csv("../data/processed/PE_ordered_filtered_v2.csv")
    return PE_ordered_filtered_v2.sample(4)


def PE_Wrangled(PE_ordered_filtered_v2):
    """
    Takes the Wrangled Population Estimate dataset and drops a number of erraneous rows, modifies names by removing "-", "(CMA)", and extra spacing, then returns the wrangled dataset with row names that are conserved between all datasets being investigated.
    
    Parameters:
    * PE_ordered_filtered_v2 (pandas.DataFrame): specified dataframes containing columns and rows with conserved names.
    
    Returns:
    df: a pandas dataframe, containing only the desired metropolitan areas and columns related to population for further analysis, wiht proper names.
    """
    PE_Wrangled = PE_ordered_filtered_v2.drop(PE_ordered_filtered_v2[PE_ordered_filtered_v2.GEO.isin(['Canada',
                                                                'All areas outside census metropolitan areas and census agglomerations, Canada',
                                                                'All census agglomerations, Canada',
                                                                'All census metropolitan areas and census agglomerations, Canada',
                                                                'All census metropolitan areas, Canada',
                                                                'Area outside census metropolitan areas and census agglomerations, Alberta',
                                                                'Area outside census metropolitan areas and census agglomerations, British Columbia',
                                                                'Area outside census metropolitan areas and census agglomerations, Manitoba',
                                                                'Area outside census metropolitan areas and census agglomerations, New Brunswick',
                                                                'Area outside census metropolitan areas and census agglomerations, Newfoundland and Labrador',
                                                                'Area outside census metropolitan areas and census agglomerations, Northwest Territories',
                                                                'Area outside census metropolitan areas and census agglomerations, Nova Scotia',
                                                                'Area outside census metropolitan areas and census agglomerations, Nunavut',
                                                                'Area outside census metropolitan areas and census agglomerations, Ontario',
                                                                'Area outside census metropolitan areas and census agglomerations, Prince Edward Island',
                                                                'Area outside census metropolitan areas and census agglomerations, Quebec',
                                                                'Area outside census metropolitan areas and census agglomerations, Saskatchewan',
                                                                'Area outside census metropolitan areas and census agglomerations, Yukon',
                                                                'Ottawa - Gatineau (CMA), Ontario part, Ontario',
                                                                'Ottawa - Gatineau (CMA), Quebec part, Quebec'])].index).reset_index()
    
    PE_Wrangled["GEO"] = (PE_Wrangled["GEO"].str.replace(r'\(CMA\)', '', regex=True).str.strip().str.replace(r' ,', ',', regex=True).str.strip().str.replace(r' - ', '-', regex=True).str.strip())
    
    PE_Wrangled = PE_Wrangled.drop(PE_Wrangled[PE_Wrangled.GEO.isin(['Barrie, Ontario',
                                                                 'Abbotsford-Mission, British Columbia',
                                                                 'Kingston, Ontario',
                                                                 'Ottawa-Gatineau, Ontario/Quebec',
                                                                 'Saguenay, Quebec',
                                                                 'Brantford, Ontario',
                                                                 'Moncton, New Brunswick'])].index).drop(columns=["index","Unnamed: 0"]) 
    PE_Wrangled.to_csv("../data/processed/PE_Wrangled.csv")
    PE_Wrangled_Final = PE_Wrangled.drop(PE_Wrangled[PE_Wrangled.GEO.isin(['Parksville (CA), British Columbia',
                                                                           'Steinbach (CA), Manitoba',
                                                                           'Moose Jaw (CA), Saskatchewan',
                                                                           'Shawinigan (CA), Quebec',
                                                                           'Owen Sound (CA), Ontario',
                                                                           'Norfolk (CA), Ontario',
                                                                           'Petawawa (CA), Ontario',
                                                                           'Stratford (CA), Ontario',
                                                                           'Baie-Comeau (CA), Quebec',
                                                                           'Sault Ste. Marie (CA), Ontario',
                                                                           'Dawson Creek (CA), British Columbia',
                                                                           'Campbellton (CA), New Brunswick/Quebec',
                                                                           'Medicine Hat (CA), Alberta',
                                                                           'Weyburn (CA), Saskatchewan',
                                                                           'North Bay (CA), Ontario',
                                                                           'Camrose (CA), Alberta',
                                                                           'Terrace (CA), British Columbia',
                                                                           'Campbell River (CA), British Columbia',
                                                                           'Rimouski (CA), Quebec',
                                                                           'Cranbrook (CA), British Columbia',
                                                                           'New Glasgow (CA), Nova Scotia',
                                                                           'Nanaimo (CA), British Columbia',
                                                                           'Saint-Hyacinthe (CA), Quebec',
                                                                           'Winkler (CA), Manitoba',
                                                                           'Wood Buffalo (CA), Alberta',
                                                                           'Strathmore (CA), Alberta',
                                                                           'Grand Falls-Windsor (CA), Newfoundland and Labrador',
                                                                           'Wetaskiwin (CA), Alberta',
                                                                           'Kawartha Lakes (CA), Ontario',
                                                                           'Hawkesbury (CA), Quebec part, Quebec',
                                                                           'Campbellton (CA), Quebec part, Quebec',
                                                                           'Corner Brook (CA), Newfoundland and Labrador',
                                                                           'Brandon (CA), Manitoba',
                                                                           'Bay Roberts (CA), Newfoundland and Labrador',
                                                                           'Kentville (CA), Nova Scotia',
                                                                           'Rouyn-Noranda (CA), Quebec',
                                                                           'Matane (CA), Quebec',
                                                                           'Centre Wellington (CA), Ontario',
                                                                           'Brooks (CA), Alberta',
                                                                           'Truro (CA), Nova Scotia',
                                                                           'Hawkesbury (CA), Ontario part, Ontario',
                                                                           'Lloydminster (CA), Alberta/Saskatchewan',
                                                                           'Campbellton (CA), New Brunswick part, New Brunswick',
                                                                           'Charlottetown (CA), Prince Edward Island',
                                                                           'Penticton (CA), British Columbia',
                                                                           'Hawkesbury (CA), Ontario/Quebec',
                                                                           'Lacombe (CA), Alberta',
                                                                           'Granby (CA), Quebec',
                                                                           'Woodstock (CA), Ontario',
                                                                           'Edmundston (CA), New Brunswick',
                                                                           'Rivière-du-Loup (CA), Quebec',
                                                                           'Red Deer (CA), Alberta',
                                                                           'Quesnel (CA), British Columbia',
                                                                           'Whitehorse (CA), Yukon',
                                                                           'Victoriaville (CA), Quebec',
                                                                           'Sarnia (CA), Ontario',
                                                                           'Joliette (CA), Quebec','Dolbeau-Mistassini (CA), Quebec',
                                                                           'Port Alberni (CA), British Columbia',
                                                                           'North Battleford (CA), Saskatchewan',
                                                                           'Orillia (CA), Ontario',
                                                                           'Bathurst (CA), New Brunswick',
                                                                           'Okotoks (CA), Alberta',
                                                                           'Prince Rupert (CA), British Columbia',
                                                                           'Sorel-Tracy (CA), Quebec',
                                                                           'Chatham-Kent (CA), Ontario',
                                                                           'Cobourg (CA), Ontario',
                                                                           'Lloydminster (CA), Alberta part, Alberta',
                                                                           'Portage la Prairie (CA), Manitoba',
                                                                           'Courtenay (CA), British Columbia',
                                                                           'Lloydminster (CA), Saskatchewan part, Saskatchewan',
                                                                           'Lethbridge, Alberta',
                                                                           "Val-d'Or (CA), Quebec",
                                                                           'Cowansville (CA), Quebec',
                                                                           'Miramichi (CA), New Brunswick',
                                                                           'Midland (CA), Ontario',
                                                                           'Sept-Îles (CA), Quebec',
                                                                           'Alma (CA), Quebec',
                                                                           'Peterborough, Ontario',
                                                                           'Cape Breton (CA), Nova Scotia',
                                                                           'Prince George (CA), British Columbia',
                                                                           'Squamish (CA), British Columbia',
                                                                           'Carleton Place (CA), Ontario',
                                                                           'High River (CA), Alberta',
                                                                           'Swift Current (CA), Saskatchewan',
                                                                           'Vernon (CA), British Columbia',
                                                                           'Williams Lake (CA), British Columbia',
                                                                           'Kamloops (CA), British Columbia',
                                                                           'Collingwood (CA), Ontario',
                                                                           'Saint John, New Brunswick',
                                                                           'Belleville, Ontario',
                                                                           'Estevan (CA), Saskatchewan',
                                                                           'Leamington (CA), Ontario',
                                                                           'Salmon Arm (CA), British Columbia',
                                                                           'Gander (CA), Newfoundland and Labrador',
                                                                           'Pembroke (CA), Ontario',
                                                                           'Timmins (CA), Ontario',
                                                                           'Port Hope (CA), Ontario',
                                                                           'Salaberry-de-Valleyfield (CA), Quebec',
                                                                           'Yorkton (CA), Saskatchewan',
                                                                           'Cornwall (CA), Ontario',
                                                                           'Canmore (CA), Alberta',
                                                                           'Thompson (CA), Manitoba',
                                                                           'Ingersoll (CA), Ontario',
                                                                           'Cold Lake (CA), Alberta',
                                                                           'Prince Albert (CA), Saskatchewan',
                                                                           'Powell River (CA), British Columbia',
                                                                           'Sainte-Marie (CA), Quebec',
                                                                           'Grande Prairie (CA), Alberta',
                                                                           'Arnprior (CA), Ontario',
                                                                           'Duncan (CA), British Columbia',
                                                                           'Wasaga Beach (CA), Ontario',
                                                                           'Brockville (CA), Ontario',
                                                                           'Nelson (CA),British Columbia',
                                                                           'Fredericton (CA), New Brunswick',
                                                                           'Saint-Georges (CA), Quebec',
                                                                           'Thunder Bay, Ontario',
                                                                           'Elliot Lake (CA), Ontario',
                                                                           'Kenora (CA), Ontario',
                                                                           'Yellowknife (CA), Northwest Territories',
                                                                           'Summerside (CA), Prince Edward Island',
                                                                           'Chilliwack (CA), British Columbia',
                                                                           'Fort St. John (CA), British Columbia',
                                                                           'Tillsonburg (CA), Ontario', 'Lachute (CA), Quebec',
                                                                           'Sylvan Lake (CA), Alberta',
                                                                           'Thetford Mines (CA), Quebec',
                                                                           'Drummondville (CA), Quebec'])].index).reset_index().drop(columns=["index"])
    
    PE_Wrangled_Final['REF_DATE'] = pd.to_datetime(PE_Wrangled_Final['REF_DATE'], format='%Y')
    PE_Wrangled_Final.to_csv("../data/processed/PE_Wrangled_Final.csv")
    return PE_Wrangled_Final.sample(4)


def all_ages_both_sexes(PE_Wrangled_Final):
    """
    Takes the PE_Wrangled_final dataset and drops rows corresponding to individual age groups and sexes, then returns the wrangled dataset.
    
    Parameters:
    * PE_Wrangled_Final (pandas.DataFrame): the input dataframe containing columns and rows with conserved names.
    
    Returns:
    pandas.DataFrame: a dataframe containing only the desired metropolitan areas and columns related to population for further analysis.
    """
    PE_Wrangled_Final_all_ages = PE_Wrangled_Final[(PE_Wrangled_Final['Age group'] == 'All ages')&(PE_Wrangled_Final['Sex'] == 'Both sexes')].reset_index().drop(columns=["index","Unnamed: 0"])
    
    PE_Wrangled_Final_all_ages.to_csv("../data/processed/PE_Wrangled_Final_all_ages.csv")
    return PE_Wrangled_Final_all_ages.sample(4)


    
def NHPI_ordering_filtering(NewHousingPIndex):
    """
    Takes the NewHousingPIndex dataset and drops a number of erraneous columns and rows, then returns the wrangled dataset.
    
    Parameters:
    *dfs (pandas.DataFrame): specified dataframes containing columns and rows with conserved names.
    
    Returns:
    df: a pandas dataframe, containing only the desired metropolitan areas and columns related to population for further analysis.
    """
    NewHousingPIndex_Wrangled = NewHousingPIndex.drop(columns=['DGUID','UOM_ID','SCALAR_FACTOR','SCALAR_ID','VECTOR','COORDINATE','STATUS','SYMBOL','TERMINATED','DECIMALS'], axis=1).reset_index().drop(columns=["index"]) 
    NewHousingPIndex_Wrangled['REF_DATE'] = pd.to_datetime(NewHousingPIndex_Wrangled['REF_DATE'])
    NHPI_W_v2 = NewHousingPIndex_Wrangled[~(NewHousingPIndex_Wrangled['REF_DATE'] < '2001-01-01')].reset_index().drop(columns=["index"])
    NHPI_W_v3 = NHPI_W_v2.drop(NHPI_W_v2[NHPI_W_v2['New housing price indexes'].isin(['House only','Land only'])].index).reset_index().drop(columns=["index"])
    NHPI_W_Final = NHPI_W_v3.drop(NHPI_W_v3[NHPI_W_v3.GEO.isin(['Alberta',
                                                                'Atlantic Region',
                                                                'British Columbia',
                                                                'Canada',
                                                                'Charlottetown, Prince Edward Island',
                                                                'Manitoba',
                                                                'New Brunswick',
                                                                'Newfoundland and Labrador',
                                                                'Nova Scotia',
                                                                'Ontario',
                                                                'Ottawa-Gatineau, Ontario part, Ontario/Quebec',
                                                                'Ottawa-Gatineau, Quebec part, Ontario/Quebec',
                                                                'Prairie Region','Prince Edward Island',
                                                                'Quebec',
                                                                'Saint John, Fredericton, and Moncton, New Brunswick',
                                                                'Saskatchewan'])].index).reset_index().drop(columns=["index"])
    
    NHPI_W_Final.to_csv("../data/processed/NHPI_W_Final.csv")
    return NHPI_W_Final.head(4)


def NI_ordering_filtering(NewInventory):
    """
    Takes the NewInventory dataset and drops a number of erraneous columns and rows, then returns the wrangled dataset.
    
    Parameters:
    *dfs (pandas.DataFrame): specified dataframes containing columns and rows with conserved names.
    
    Returns:
    df: a pandas dataframe, containing only the desired metropolitan areas and columns related to population for further analysis.
    """
    w.simplefilter("ignore", category=UserWarning)
    NI_Wrangled = NewInventory.drop(columns=['DGUID','UOM_ID','SCALAR_FACTOR','SCALAR_ID','VECTOR','COORDINATE','STATUS','SYMBOL','TERMINATED','DECIMALS'], axis=1).reset_index().drop(columns=["index"])
    NI_Wrangled['REF_DATE'] = pd.to_datetime(NI_Wrangled['REF_DATE'])
    NI_Wrangled = NI_Wrangled[~(NI_Wrangled['REF_DATE'] < '2001-01-01')].reset_index().drop(columns=["index"])
    NI_Wrangled_totals_completions = NI_Wrangled.drop(NI_Wrangled[NI_Wrangled['Housing estimates'] != 'Housing completions'].index)
    NI_Wrangled_totals_completions = NI_Wrangled_totals_completions.drop(NI_Wrangled_totals_completions[NI_Wrangled['Type of unit'] != 'Total units'].index)
    NI_Wrangled_totals_completions.reset_index().drop(columns=["index"])
    NI_Wrangled_Final = NI_Wrangled_totals_completions.drop(NI_Wrangled_totals_completions[NI_Wrangled_totals_completions.GEO.isin(['Abbotsford-Mission, British Columbia','Barrie, Ontario','Brantford, Ontario','Census metropolitan areas','Kingston, Ontario','Moncton, New Brunswick','Ottawa-Gatineau, Ontario part, Ontario/Quebec','Ottawa-Gatineau, Ontario/Quebec','Ottawa-Gatineau, Quebec part, Ontario/Quebec','Peterborough, Ontario','Saguenay, Quebec','Saint John, New Brunswick','Thunder Bay, Ontario'])].index).reset_index().drop(columns=["index"])
    
    NI_Wrangled_Final.to_csv("../data/processed/NI_Wrangled_Final.csv")
    return NI_Wrangled_Final.head(4)


def calculate_total_rate_change_PE(PE_Wrangled_Final_all_ages):
    """
    Using the pandas dataframe `PE_Wrangled_Final_all_ages` with columns "GEO" and "VALUE", 
    calculates the total rate change for each unique "GEO" value.
    
    Returns:
    a pandas dataframe with columns "GEO" and "PE_rate_total", sorted in ascending order by "PE_rate_total".
    """
    import warnings as w
    w.filterwarnings("ignore", message="The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.")


    total_rate_change = pd.DataFrame(columns=["GEO", "PE_rate_total"])

    for city in PE_Wrangled_Final_all_ages["GEO"].unique():

        city_df = PE_Wrangled_Final_all_ages[PE_Wrangled_Final_all_ages["GEO"] == city]

        initial_pop = city_df.iloc[0]["VALUE"]
        final_pop = city_df.iloc[-1]["VALUE"]

        rate = (final_pop - initial_pop) / initial_pop * 100

        total_rate_change = total_rate_change.append({"GEO": city, "PE_rate_total": rate}, ignore_index=True)

    total_rate_change_PE = total_rate_change.sort_values('PE_rate_total').reset_index().drop(columns=['index'])
    total_rate_change_PE.to_csv("../data/processed/total_rate_change_PE.csv")
    
    return total_rate_change_PE.sample(4) 


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
    total_rate_change_NI.to_csv("../data/processed/total_rate_change_NI.csv")
    
    return total_rate_change_NI.sample(4)

def calculate_total_rate_change_NHPI(NHPI_W_Final):
    """
    Using the pandas dataframe `NHPI_W_Final` with columns "GEO" and "VALUE", 
    calculates the total rate change for each unique "GEO" value.
    
    Returns:
    a pandas dataframe with columns "GEO" and "NHPI_rate_total", sorted in ascending order by "NHPI_rate_total".
    """
    w.filterwarnings("ignore", message="The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.")
    total_rate_change_NHPI_noNaN = pd.DataFrame(columns=["GEO", "NHPI_rate_total"])

    for city in NHPI_W_Final["GEO"].unique():

        city_df = NHPI_W_Final[NHPI_W_Final["GEO"] == city]

        initial_value = city_df.loc[city_df["VALUE"].first_valid_index()]["VALUE"]
        final_value = city_df.loc[city_df["VALUE"].last_valid_index()]["VALUE"]

        rate = (final_value - initial_value) / initial_value * 100

        total_rate_change_NHPI_noNaN = total_rate_change_NHPI_noNaN.append({"GEO": city, "NHPI_rate_total": rate}, ignore_index=True)

    total_rate_change_NHPI = total_rate_change_NHPI_noNaN.sort_values('NHPI_rate_total').reset_index().drop(columns=['index'])
    total_rate_change_NHPI.to_csv("../data/processed/total_rate_change_NHPI.csv")
    return total_rate_change_NHPI.sample(4)


def merging_rate_totals(total_rate_change_PE, total_rate_change_NHPI, total_rate_change_NI):
    """
    Merges the pandas dataframes `total_rate_change_PE`, 'total_rate_change_NHPI', 'total_rate_change_NI' on column "GEO", returns a merged dataset with the total 20 yr rate change for population, housing price index, and housing inventory for each unique "GEO" value.
    
    Returns:
    a pandas dataframe with columns "GEO" and "NHPI_rate_total", sorted in ascending order by "NHPI_rate_total".
    """
    merged_rate_totals = pd.merge(total_rate_change_PE, total_rate_change_NHPI, on='GEO').merge(total_rate_change_NI, on='GEO')
    merged_rate_totals.to_csv("../data/processed/merged_rate_totals.csv")
    return merged_rate_totals.sample(4)


def score_em(merged_rate_totals):
    """
    Creates a "aggregated_score" column populated with values corresponding to each metropolitan area. Scoring is calculated by taking 50% of the 'PE_rate_total' column, 30% of 'NHPI_rate_total', 20% of 'NI_rate_total', and adding each value together.
    
    Returns:
    a pandas dataframe with columns "GEO", "NHPI_rate_total", "PE_rate_total", "NI_rate_total" and "aggregated_score".
    """
    merged_rate_totals['aggregated_score'] = (merged_rate_totals['PE_rate_total']*0.5) + (merged_rate_totals['NHPI_rate_total']*0.3) + (merged_rate_totals['NI_rate_total']*0.2)
    scored_metros = merged_rate_totals.sort_values('aggregated_score').reset_index().drop(columns=['index'])
    scored_metros.to_csv("../data/processed/scored_metros.csv")
    return scored_metros.sample(4)