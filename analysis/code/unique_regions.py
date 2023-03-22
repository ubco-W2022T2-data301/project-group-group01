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