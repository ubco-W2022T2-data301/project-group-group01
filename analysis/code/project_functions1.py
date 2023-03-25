import pandas as pd
import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import dates as dates
import numpy as np



def ProcessData():

        locales = LPE.GEO.unique()

        for city in locales:

                LPE = pd.read_csv("../data/processed/PE_ordered_filtered.csv")
                
                name = city[:(city.find(",")+1) ]
        
                cityname = "../data/processed/PIndex/"+ str(name) +"PIndex.csv"
                citindex = pd.read_csv(cityname)
        
                cityname = "../data/processed/PopEstimate/"+ str(name) +"PopEstimate.csv"
                citpopest = pd.read_csv(cityname)
        
                cityname = "../data/processed/NewInventory/"+ str(name) +"NewInventory.csv"
                citnewinv = pd.read_csv(cityname)

                citnewinvyr = citnewinv.groupby(pd.PeriodIndex(citnewinv["REF_DATE"], freq="Y"))["VALUE"].sum().reset_index()
                citindex = citindex.groupby(pd.PeriodIndex(citindex["REF_DATE"], freq="Y"))["VALUE"].mean().reset_index()
                citpopest["Change"] = citpopest["VALUE"].diff()
                calindex["PDelta"] = calindex["VALUE"].diff()

                shortfall = pd.DataFrame()
                shortfall["PDelta"] = calindex["PDelta"] * 1000
                shortfall["Date"] = calpopest["REF_DATE"]
                shortfall["0"] = (calnewinvyr["VALUE"]  * 0)
                shortfall["2"] =  (calpopest["Change"] - (calnewinvyr["VALUE"]  * 2))

                shortfallgraph = sns.lineplot(x='Date', y='value', hue='variable', 
                        data=pd.melt(shortfall, ['Date']))

                shortfallgraph.set(xlabel = "Date",
                        ylabel = "Shortfall",
                        title = F"Housing shortfall in {city} assuming 2 persons per home"
                        )

                plt.legend(title = "Legend", labels = ["Price Changes\n(exaggerated)","","Zero Line","","Shortfall"])
        
                fig = shortfallgraph.get_figure()
                fig.savefig("out.png")