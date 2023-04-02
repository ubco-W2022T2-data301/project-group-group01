def CityProcess(city, factor):


        import pandas as pd
        import seaborn as sns
        import numpy as np
        import os
        import matplotlib.pyplot as plt
        from matplotlib import dates as dates
        import numpy as np

        cityname = {city}

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
        output = [j for i in cityname for j in cities if i in j]
        cities = set(cities)
        outputN = set(output)
        removecit = cities - outputN
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
        output = [j for i in cityname for j in cities if i in j]
        cities = set(cities)
        outputN = set(output)
        removecit = cities - outputN
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

        output = [j for i in cityname for j in cities if i in j]
        cities = set(cities)
        outputP = set(output)
        removecit = cities - outputP
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


        #Adding Interest Rates
        DailyInterestRateP = pd.DataFrame()
        DailyInterestRateP["REF_DATE"] = DailyInterestRate["REF_DATE"]
        DailyInterestRate = DailyInterestRate[(DailyInterestRate["Financial market statistics"] == "Overnight money market financing")]
        DailyInterestRateP["RATE"]  = DailyInterestRate["VALUE"]
        DailyInterestRateP = DailyInterestRateP.dropna(axis = 0, how = "any")
        intrate = DailyInterestRateP.groupby(pd.PeriodIndex(DailyInterestRateP["REF_DATE"], freq="Y"))["RATE"].mean().reset_index()



        #Processing for City
        cityN = NewInventory[(NewInventory["GEO"] == (str(outputN)[2:-2]))]\
        .reset_index()\
        .drop(columns=["index"])
        cityN = cityN.groupby(pd.PeriodIndex(cityN["REF_DATE"], freq="Y"))["NewHomes"].sum().reset_index()

        cityPr = NewHousingPIndex[(NewHousingPIndex["GEO"] == (str(outputN)[2:-2]))]\
        .reset_index()\
        .drop(columns=["index"])
        cityPr = cityPr.groupby(pd.PeriodIndex(cityPr["REF_DATE"], freq="Y"))["IND_VALUE"].mean().reset_index()

        cityPop = PopEstimate[(PopEstimate["GEO"] == (str(outputN)[2:-2]))]\
        .reset_index()\
        .drop(columns=["index"])\


        #Convert all years into int
        cityN["REF_DATE"] = cityN["REF_DATE"].dt.to_timestamp('s').dt.strftime("%Y")
        cityN = cityN.astype({"REF_DATE":int})
        cityPr["REF_DATE"] = cityPr["REF_DATE"].dt.to_timestamp('s').dt.strftime("%Y")
        cityPr = cityPr.astype({"REF_DATE":int})
        cityPop = cityPop.astype({"REF_DATE":int})
        intrate = intrate.astype({"REF_DATE":str}).astype({"REF_DATE":int})

        #MErges into 1 df
        cityPr = cityPr.merge(intrate, on = "REF_DATE")
        cityt = cityPr.merge(cityN, on = "REF_DATE")
        cityf = cityPop.merge(cityt, on = "REF_DATE")

        #Drops duplicate rows
        cityf = cityf.drop(columns = ["VALUE" ] , axis=1)




        #Calulate pop increase
        cityf["PopChange"] = cityf["Population"].diff()

        #calculates Price change
        cityf["PriceChange"] = cityf["IND_VALUE"].diff()


        #Cancels price change for 2% inflation
        cityf["PriceChangeR"] = cityf["PriceChange"] - (cityf["IND_VALUE"] * 0.02)


        #calulate Shortfall 
        cityf["Shortfall"] =  (cityf["NewHomes"] * factor) - cityf["PopChange"]
        cityf["ShortfallP"] = cityf["Shortfall"] / cityf["Population"] * 100







        #Returns data
        return cityf

def trimmer(dataset):
        
        import pandas as pd
        import seaborn as sns
        import numpy as np
        import os
        import matplotlib.pyplot as plt
        from matplotlib import dates as dates
        import numpy as np
        
        
        dataseto = pd.DataFrame()
        dataseto["Date"] =  dataset["REF_DATE"]
        dataseto["ShortfallP"] =  dataset["ShortfallP"]
        dataseto["PriceChangeR"] =  dataset["PriceChangeR"]
        dataseto["Int"] =  dataset["RATE"]
        dataseto = dataseto.dropna(axis = 0, how = "any")
        return dataseto



def graph(dataset, city,  occ, how):
        
        import pandas as pd
        import seaborn as sns
        import numpy as np
        import os
        import matplotlib.pyplot as plt
        from matplotlib import dates as dates
        import numpy as np
        import warnings
        warnings.filterwarnings("ignore")
        
        if how == "shortfall":
                
                #print("shortfall")
                dataset2 = pd.DataFrame()
                dataset2["Date"] = dataset["Date"]
                #dataset2["Interest Rate (%)"] = dataset["Int"]
                dataset2["Shortfall"] = dataset["ShortfallP"]
                dataset2["Price Changes (%)"] = dataset["PriceChangeR"]
                dataset2 = pd.melt(dataset2, ['Date'])
                
                plt.figure()
                
                graph = sns.lineplot(x='Date', y='value', hue='variable', data = dataset2)

                graph.set(xlabel = "Date",
                                ylabel = "Percentage",
                                title = F"Housing Price and housing shortfall in {city} \nassuming {occ} persons per home and 2% inflation"
                        )

                graph.set_xticks([ 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022])
                graph.set_xticklabels([ "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", '17', "18", "19", "20", "21", "22"])
                plt.grid()
                plt.legend(title = "Legend", loc = "lower left")
                
                        
                fig = graph.get_figure()

        
        elif how == "int":
                
                #print("int")
                dataset2 = pd.DataFrame()
                dataset2["Date"] = dataset["Date"]
                dataset2["Interest Rate (%)"] = dataset["Int"]
                #dataset2["Shortfall"] = dataset["ShortfallP"]
                dataset2["Price Changes (%)"] = dataset["PriceChangeR"]
                dataset2 = pd.melt(dataset2, ['Date'])

                plt.figure()
                
                graph = sns.lineplot(x='Date', y='value', hue='variable', data = dataset2)

                graph.set(xlabel = "Date",
                                ylabel = "Percentage",
                                title = F"Housing Price and housing shortfall in {city} \n assuming {occ} persons per home and 2% inflation"
                        )

                graph.set_xticks([ 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022])
                graph.set_xticklabels([ "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", '17', "18", "19", "20", "21", "22"])
                plt.grid()
                plt.legend(title = "Legend", loc = "lower left")
                
                        
                fig = graph.get_figure()
                

        else:
                dataset2 = pd.DataFrame()
                dataset2["Date"] = dataset["Date"]
                dataset2["Interest Rate (%)"] = dataset["Int"]
                dataset2["Shortfall"] = dataset["ShortfallP"]
                dataset2["Price Changes (%)"] = dataset["PriceChangeR"]
                dataset2 = pd.melt(dataset2, ['Date'])

                plt.figure()

                graph = sns.lineplot(x='Date', y='value', hue='variable', data = dataset2)

                graph.set(xlabel = "Date",
                                ylabel = "Percentage",
                                title = F"Housing Price, shortfall, and interest rate in {city} \nassuming {occ} persons per home and 2% inflation"
                        )

                graph.set_xticks([ 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022])
                graph.set_xticklabels([ "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", '17', "18", "19", "20", "21", "22"])
                plt.grid()
                plt.legend(title = "Legend", loc = "lower left")
                        
                fig = graph.get_figure()
                
        return fig



def pcgraph():
        import pandas as pd
        import seaborn as sns
        import numpy as np
        import os
        import matplotlib.pyplot as plt
        from matplotlib import dates as dates
        import numpy as np

        citylist = {"Vancouver","Toronto", "Montréal","Edmonton","Quebec","London","Calgary", "Winnipeg", "Saskatoon"}

        for city in citylist:
                
                df = CityProcess(city, 2) 
                df = trimmer(df)
                df2 = pd.DataFrame()
                df2["Date"] = df["Date"]
                df2["PriceChangeR"] = df["PriceChangeR"]
                        
                cityprice = city + "P"
                globals()[cityprice] = df2

        citylistp = {"TorontoP", "MontréalP","EdmontonP","QuebecP","LondonP","CalgaryP", "WinnipegP", "SaskatoonP"}

        for city in citylistp:
                outP = pd.DataFrame()
                outP = pd.concat([VancouverP, (globals()[city])])


        plt.figure()


        p = sns.boxplot(data=outP, x="Date", y="PriceChangeR")
        p.set_xticklabels([ "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", '17', "18", "19", "20", "21", "22"])
        p.set(xlabel = "Year", ylabel = "Percentage", title = F"price change difference in cities across canada")
        
        
        return p


def scgraph():
        import pandas as pd
        import seaborn as sns
        import numpy as np
        import os
        import matplotlib.pyplot as plt
        from matplotlib import dates as dates
        import numpy as np

        citylist = {"Vancouver","Toronto", "Montréal","Edmonton","Quebec","London","Calgary", "Winnipeg", "Saskatoon"}

        for city in citylist:
                df = CityProcess(city, 2) 
                df = trimmer(df)
                df2 = pd.DataFrame()
                df2["Date"] = df["Date"]
                df2["ShortfallP"] = df["ShortfallP"]

                cityshort = city + "S"
                globals()[cityshort] = df2


        citylists = {"TorontoS", "MontréalS","EdmontonS","QuebecS","LondonS","CalgaryS", "WinnipegS", "SaskatoonS"}

        for city in citylists:
                outS = pd.DataFrame()
                outS = pd.concat([VancouverS, (globals()[city])])

        plt.figure()

        s = sns.boxplot(data=outS, x="Date", y="ShortfallP")
        s.set_xticklabels([ "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", '17', "18", "19", "20", "21", "22"])
        s.set(xlabel = "Year", ylabel = "Percentage", title = F"shortfall difference in cities across canada")
        
        
        return s


def cgraph():
        import pandas as pd
        import seaborn as sns
        import numpy as np
        import os
        import matplotlib.pyplot as plt
        from matplotlib import dates as dates
        import numpy as np

        citylist = {"Vancouver","Toronto", "Montréal","Edmonton","Quebec","London","Calgary", "Winnipeg", "Saskatoon"}

        for city in citylist:
                
                df = CityProcess(city, 2) 
                df = trimmer(df)
                df2 = pd.DataFrame()
                df2["Date"] = df["Date"]
                df2["PriceChangeR"] = df["PriceChangeR"]
                        
                cityprice = city + "P"
                globals()[cityprice] = df2

        citylistp = {"TorontoP", "MontréalP","EdmontonP","QuebecP","LondonP","CalgaryP", "WinnipegP", "SaskatoonP"}

        for city in citylistp:
                outP = pd.DataFrame()
                outP = pd.concat([VancouverP, (globals()[city])])

        citylist = {"Vancouver","Toronto", "Montréal","Edmonton","Quebec","London","Calgary", "Winnipeg", "Saskatoon"}

        for city in citylist:
                df = CityProcess(city, 2) 
                df = trimmer(df)
                df2 = pd.DataFrame()
                df2["Date"] = df["Date"]
                df2["ShortfallP"] = df["ShortfallP"]

                cityshort = city + "S"
                globals()[cityshort] = df2


        citylists = {"TorontoS", "MontréalS","EdmontonS","QuebecS","LondonS","CalgaryS", "WinnipegS", "SaskatoonS"}

        for city in citylists:
                outS = pd.DataFrame()
                outS = pd.concat([VancouverS, (globals()[city])])


        plt.figure()


        p = sns.boxplot(data=outP, x="Date", y="PriceChangeR")
        p.set_xticklabels([ "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", '17', "18", "19", "20", "21", "22"])
        p.set(xlabel = "Year", ylabel = "Percentage", title = F"price change difference in cities across canada")

        f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        ax1.boxplot(data=outP, x="Date", y="PriceChangeR")
        ax1.set_xticklabels([ "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", '17', "18", "19", "20", "21", "22"])
        ax1.set(xlabel = "Year", ylabel = "Percentage", title = F"price change difference in cities across canada")

        ax2.boxplot(data=outS, x="Date", y="ShortfallP")
        ax2.set_xticklabels([ "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", '17', "18", "19", "20", "21", "22"])
        ax2.set(xlabel = "Year", ylabel = "Percentage", title = F"shortfall difference in cities across canada")
