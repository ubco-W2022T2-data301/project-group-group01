def CityProcess():
        import pandas as pd
        import seaborn as sns
        import numpy as np
        import os
        import matplotlib.pyplot as plt
        from matplotlib import dates as dates
        import numpy as np
        
        locales = ["Edmonton", "Montréal", "Vancouver", "Edmonton", "Calgary"]


        NewHousingPIndex = pd.read_csv("../data/raw/NewHousingPIndex.csv")
        NewInventory = pd.read_csv("../data/raw/NewInventory.csv", low_memory = False)
        PopEstimate = pd.read_csv("../data/raw/PopEstimate.csv")
        DailyInterestRate = pd.read_csv("../data/raw/DailyInterestRate.csv")

        #Outputs a df with yearly: pop, popchange, relative price, new inventory, housing shortfall, and int rate for top 5 canadian cities. 


        #Make all ref dates date time
        NewHousingPIndex["REF_DATE"] = pd.to_datetime(NewHousingPIndex["REF_DATE"])
        NewInventory["REF_DATE"] = pd.to_datetime(NewInventory["REF_DATE"])
        DailyInterestRate["REF_DATE"] = pd.to_datetime(DailyInterestRate["REF_DATE"])

        #Filter out dates before 2001
        NewHousingPIndex = NewHousingPIndex[~(NewHousingPIndex["REF_DATE"] < '2001-01-01')].reset_index().drop(columns=["index"])
        NewInventory = NewInventory[~(NewInventory["REF_DATE"] < '2001-01-01')].reset_index().drop(columns=["index"])
        DailyInterestRate = DailyInterestRate[~(DailyInterestRate["REF_DATE"] < "2001-01-01")].reset_index().drop(columns=["index"])

        #Dropping Uneeded cities and dates for NewHousingPIndex
        cities = NewHousingPIndex["GEO"].unique().tolist()
        output = [j for i in locales for j in cities if i in j]
        cities = set(cities)
        output = set(output)
        removecit = cities - output
        removecit = list(removecit)

        NewHousingPIndex = NewHousingPIndex\
        .drop(columns = ["UOM_ID","UOM","DGUID","SCALAR_FACTOR","SCALAR_ID","VECTOR","COORDINATE", "STATUS", "SYMBOL", "TERMINATED", "DECIMALS" ] , axis=1)\
        .drop(NewHousingPIndex[NewHousingPIndex.GEO.isin(removecit)].index)\
        .reset_index()\
        .drop(columns=["index"])\

        #Dropping Uneeded indexes
        NewHousingPIndex = NewHousingPIndex\
        .drop(list(NewHousingPIndex[NewHousingPIndex["New housing price indexes"].isin(["Land only", "House only"])].index))\
        .reset_index()\
        .drop(columns=["index"])

        NewHousingPIndex["IND_VALUE"] = NewHousingPIndex["VALUE"]





        #Dropping Uneeded cities and dates for NewInventory
        cities = NewInventory["GEO"].unique().tolist()
        output = [j for i in locales for j in cities if i in j]
        cities = set(cities)
        output = set(output)
        removecit = cities - output
        removecit = list(removecit)

        NewInventory = NewInventory\
        .drop(columns = ["UOM_ID","UOM","DGUID","SCALAR_FACTOR","SCALAR_ID","VECTOR","COORDINATE", "STATUS", "SYMBOL", "TERMINATED", "DECIMALS" ] , axis=1)\
        .drop(NewInventory[NewInventory.GEO.isin(removecit)].index)\
        .reset_index()\
        .drop(columns=["index"])\

        #Dropping types of units
        NewInventory = NewInventory\
        .drop(list(NewInventory[NewInventory["Type of unit"].isin(["Single-detached units", "Semi-detached units", "Row units", "Apartment and other unit types"])].index))\
        .reset_index()\
        .drop(columns=["index"])\

        #Dropping housing starts
        NewInventory = NewInventory\
        .drop(list(NewInventory[NewInventory["Housing estimates"].isin(["Housing starts","Housing under construction"])].index))\
        .reset_index()\
        .drop(columns=["index"])\

        #Sum of the year
        NewInventory ["NewHomes"] = NewInventory ["VALUE"]

        NewInventory = NewInventory\
        .sort_values(["GEO", "REF_DATE"],ascending=True)\
        .reset_index()\
        .drop(columns=["index"])\


        #Dropping Uneeded cities and dates for PopEstimate

        cities = PopEstimate["GEO"].unique().tolist()

        output = [j for i in locales for j in cities if i in j]
        cities = set(cities)
        output = set(output)
        removecit = cities - output
        removecit = list(removecit)


        PopEstimate = PopEstimate\
        .drop(columns = ["UOM_ID","UOM","DGUID","SCALAR_FACTOR","SCALAR_ID","VECTOR","COORDINATE", "STATUS", "SYMBOL", "TERMINATED", "DECIMALS" ] , axis=1)\
        .drop(PopEstimate[PopEstimate.GEO.isin(removecit)].index)\
        .reset_index()\
        .drop(columns=["index"])\

        PopEstimate = PopEstimate[(PopEstimate["Age group"] == "All ages") & (PopEstimate["Sex"] == "Both sexes")]\
        .reset_index()\
        .drop(columns=["index"])\

        PopEstimate = PopEstimate\
        .sort_values(["GEO", "REF_DATE"],ascending=True)\
        .reset_index()\
        .drop(columns=["index"])\
        .drop(columns = ["Age group", "Sex" ] , axis=1)

        PopEstimate["Population"] = PopEstimate["VALUE"]\

        PopEstimate["GEO"] = PopEstimate.GEO.apply(lambda x: x.replace(" (CMA)", "")).drop(columns = ["VALUE"] , axis=1)



        #Dataset for each city
        #array(['Calgary, Alberta', 'Edmonton, Alberta', 'Montréal, Quebec','Vancouver, Ontario', 'Vancouver, British Columbia'], dtype=object)


        #'Calgary, Alberta'
        CalgaryN = NewInventory[(NewInventory["GEO"] == "Calgary, Alberta")]\
        .reset_index()\
        .drop(columns=["index"])
        CalgaryN = CalgaryN.groupby(pd.PeriodIndex(CalgaryN["REF_DATE"], freq="Y"))["NewHomes"].sum().reset_index()

        CalgaryPr = NewHousingPIndex[(NewHousingPIndex["GEO"] == "Calgary, Alberta")]\
        .reset_index()\
        .drop(columns=["index"])
        CalgaryPr = CalgaryPr.groupby(pd.PeriodIndex(CalgaryPr["REF_DATE"], freq="Y"))["IND_VALUE"].mean().reset_index()

        CalgaryPop = PopEstimate[(PopEstimate["GEO"] == "Calgary, Alberta")]\
        .reset_index()\
        .drop(columns=["index"])\


        CalgaryN["REF_DATE"] = CalgaryN["REF_DATE"].dt.to_timestamp('s').dt.strftime("%Y")
        CalgaryN = CalgaryN.astype({"REF_DATE":int})
        CalgaryPr["REF_DATE"] = CalgaryPr["REF_DATE"].dt.to_timestamp('s').dt.strftime("%Y")
        CalgaryPr = CalgaryPr.astype({"REF_DATE":int})
        CalgaryPop = CalgaryPop.astype({"REF_DATE":int})


        Calgary = CalgaryPr.merge(CalgaryN, on = "REF_DATE")
        Calgaryf = CalgaryPop.merge(Calgary, on = "REF_DATE")
        Calgaryf


        #'Edmonton, Alberta'
        EdmontonN = NewInventory[(NewInventory["GEO"] == "Edmonton, Alberta")]\
        .reset_index()\
        .drop(columns=["index"])
        EdmontonN = EdmontonN.groupby(pd.PeriodIndex(EdmontonN["REF_DATE"], freq="Y"))["NewHomes"].sum().reset_index()

        EdmontonPr = NewHousingPIndex[(NewHousingPIndex["GEO"] == "Edmonton, Alberta")]\
        .reset_index()\
        .drop(columns=["index"])
        EdmontonPr = EdmontonPr.groupby(pd.PeriodIndex(EdmontonPr["REF_DATE"], freq="Y"))["IND_VALUE"].mean().reset_index()

        EdmontonPop = PopEstimate[(PopEstimate["GEO"] == "Edmonton, Alberta")]\
        .reset_index()\
        .drop(columns=["index"])\


        EdmontonN["REF_DATE"] = EdmontonN["REF_DATE"].dt.to_timestamp('s').dt.strftime("%Y")
        EdmontonN = EdmontonN.astype({"REF_DATE":int})
        EdmontonPr["REF_DATE"] = EdmontonPr["REF_DATE"].dt.to_timestamp('s').dt.strftime("%Y")
        EdmontonPr = EdmontonPr.astype({"REF_DATE":int})
        EdmontonPop = EdmontonPop.astype({"REF_DATE":int})


        Edmonton = EdmontonPr.merge(EdmontonN, on = "REF_DATE")
        Edmontonf = EdmontonPop.merge(Edmonton, on = "REF_DATE")
        Edmontonf


        #'Montréal, Quebec'
        MontréalN = NewInventory[(NewInventory["GEO"] == "Montréal, Quebec")]\
        .reset_index()\
        .drop(columns=["index"])
        MontréalN = MontréalN.groupby(pd.PeriodIndex(MontréalN["REF_DATE"], freq="Y"))["NewHomes"].sum().reset_index()

        MontréalPr = NewHousingPIndex[(NewHousingPIndex["GEO"] == "Montréal, Quebec")]\
        .reset_index()\
        .drop(columns=["index"])
        MontréalPr = MontréalPr.groupby(pd.PeriodIndex(MontréalPr["REF_DATE"], freq="Y"))["IND_VALUE"].mean().reset_index()

        MontréalPop = PopEstimate[(PopEstimate["GEO"] == "Montréal, Quebec")]\
        .reset_index()\
        .drop(columns=["index"])\


        MontréalN["REF_DATE"] = MontréalN["REF_DATE"].dt.to_timestamp('s').dt.strftime("%Y")
        MontréalN = MontréalN.astype({"REF_DATE":int})
        MontréalPr["REF_DATE"] = MontréalPr["REF_DATE"].dt.to_timestamp('s').dt.strftime("%Y")
        MontréalPr = MontréalPr.astype({"REF_DATE":int})
        MontréalPop = MontréalPop.astype({"REF_DATE":int})


        Montréal = MontréalPr.merge(MontréalN, on = "REF_DATE")
        Montréalf = MontréalPop.merge(Montréal, on = "REF_DATE")
        Montréalf



        #Toronto,
        TorontoN = NewInventory[(NewInventory["GEO"] == "Toronto, Ontario")]\
        .reset_index()\
        .drop(columns=["index"])
        TorontoN = TorontoN.groupby(pd.PeriodIndex(TorontoN["REF_DATE"], freq="Y"))["NewHomes"].sum().reset_index()

        TorontoPr = NewHousingPIndex[(NewHousingPIndex["GEO"] == "Toronto, Ontario")]\
        .reset_index()\
        .drop(columns=["index"])
        TorontoPr = TorontoPr.groupby(pd.PeriodIndex(TorontoPr["REF_DATE"], freq="Y"))["IND_VALUE"].mean().reset_index()

        TorontoPop = PopEstimate[(PopEstimate["GEO"] == "Toronto, Ontario")]\
        .reset_index()\
        .drop(columns=["index"])\


        TorontoN["REF_DATE"] = TorontoN["REF_DATE"].dt.to_timestamp('s').dt.strftime("%Y")
        TorontoN = TorontoN.astype({"REF_DATE":int})
        TorontoPr["REF_DATE"] = TorontoPr["REF_DATE"].dt.to_timestamp('s').dt.strftime("%Y")
        TorontoPr = TorontoPr.astype({"REF_DATE":int})
        TorontoPop = TorontoPop.astype({"REF_DATE":int})


        Toronto = TorontoPr.merge(TorontoN, on = "REF_DATE")
        Torontof = TorontoPop.merge(Toronto, on = "REF_DATE")
        Torontof



        #Vancouver, British Columbia'
        VancouverN = NewInventory[(NewInventory["GEO"] == "Vancouver, British Columbia")]\
        .reset_index()\
        .drop(columns=["index"])
        VancouverN = VancouverN.groupby(pd.PeriodIndex(VancouverN["REF_DATE"], freq="Y"))["NewHomes"].sum().reset_index()

        VancouverPr = NewHousingPIndex[(NewHousingPIndex["GEO"] == "Vancouver, British Columbia")]\
        .reset_index()\
        .drop(columns=["index"])
        VancouverPr = VancouverPr.groupby(pd.PeriodIndex(VancouverPr["REF_DATE"], freq="Y"))["IND_VALUE"].mean().reset_index()

        VancouverPop = PopEstimate[(PopEstimate["GEO"] == "Vancouver, British Columbia")]\
        .reset_index()\
        .drop(columns=["index"])\


        VancouverN["REF_DATE"] = VancouverN["REF_DATE"].dt.to_timestamp('s').dt.strftime("%Y")
        VancouverN = VancouverN.astype({"REF_DATE":int})
        VancouverPr["REF_DATE"] = VancouverPr["REF_DATE"].dt.to_timestamp('s').dt.strftime("%Y")
        VancouverPr = VancouverPr.astype({"REF_DATE":int})
        VancouverPop = VancouverPop.astype({"REF_DATE":int})


        Vancouver = VancouverPr.merge(VancouverN, on = "REF_DATE")
        Vancouverf = VancouverPop.merge(Vancouver, on = "REF_DATE")
        Vancouverf

        return Calgaryf
        return Edmontonf
        return Montréalf
        return Torontof
        return Vancouverf
