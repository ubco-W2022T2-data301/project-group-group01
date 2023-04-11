# Canadian Housing Project

## Introduction
We are looking at the housing and demographic patterns in Canadian cities. We were interested in looking at the data for this topic because housing affordability and city living is an important part of the narrative of our generation. We wanted to look at the data and see what the trends are behind the prices and also, how different city look and are composed.

## Exploratory Data Analysis
A summary of the highlights of your EDA, where you can show some visualizations of the exploratory data analysis your group did.

* EDA for conducted in Analysis 2: 
    * My EDA focused on determining what datafields would be necessary to include in future cleaned versions of the datasets, and determining the canadian metropolitan areas (CMA's) that should be focused on for our analyses. I did so by first visualizing the datasets and dropping irrelevant columns, then I grouped all the years of data by their geographical region, and created a bar chart of the top 30 CMA's based on population increase.
    ![EDA_pop_barchart](images/EDA_pop_barchart.png)
    
    I then carried these top 30 CMA's forward for the rest of the analysis. 
    * NOTE: EDA for analysis 2 can be found here: [Raw analysis 2](https://github.com/ubco-W2022T2-data301/project-group-group01/blob/8942e9aec2881804cb16acf74ef3e13c48e2ea8e/analysis/ungraded/Logananalysis2_raw.ipynb)


## Question 1 + Results 
* My research question is looking at the correlation between housing prices and shortfall. Housing affordability is a pivotal issue for my generation, and I believe that the oft touted narrative of phantom overseas buyers is only a narrative meant to distract from the fact that the true cause of housing prices is a lack of new housing as compared to population.

### How different are major Canadian cities from each other for construction:
![Shortfall_Distribution](images/shortdiff.png)
* Here we see that between the major cities, there is a significant difference in the shortfalls they experienced. This might be due to two factors. Firstly, all cities used the same occupancy rate, while local constructions might have differed (single family homes vs condos) in the occupancy they targeted. The other factor is that this analysis looks only at percentages, and cities of different sizes have wildly different absolute shortages, which might have different outcomes on price. These limit the confidence of the conclusions, but I think there are still some conclusions that can be drawn. 

### How different are major Canadian cities from each other for Prices:
![Price_Distribution](images/Pricediff.png)
* We see in this plot that prices are much more closely distributed in major Canadian cities. This suggests that there is less connection between how much shortfall is correlated with price increases.

### Question 1 Result:
![Vancouver_Plot](images/VancouverJ.png)
* While the general Canadian trend seems to not support the idea that there is a correlation between shortfall and prices, analysis of individual cities like vancovuer seems to paint a different picture. 
* In Vancouver, we can see that shortfalls are usually followed the next year by price jumps. This pattern provides some support for my hypothesis that shortfalls are more likely responsible for price changes as opposed to the idea that speculation drives up housing price. Though I didn't get to do the stastical analysis to scientifically prove my point, I think my graphs have somewhat helped illustrate my idea.

* This is a brief overview of my analysis, for the more complete look, see the full analysis here: [Analysis 1](https://github.com/ubco-W2022T2-data301/project-group-group01/blob/8942e9aec2881804cb16acf74ef3e13c48e2ea8e/analysis/Jamesanalysis1.ipynb)


## Question 2 + Results
* See the full analysis here: [Analysis 2](https://github.com/ubco-W2022T2-data301/project-group-group01/blob/8942e9aec2881804cb16acf74ef3e13c48e2ea8e/analysis/Logananalysis2.ipynb)
### Exploring the change in housing prices, new housing construction, and population of canadian metropolitan areas over time.
* For my research focus, I wanted to explore how housing in canadian metropolitan areas has changed since 2001, so visualizing the change in housing price, housing construction, and population of CMA's was the central pillar of my analysis. Every step along the way was critical to creating clean datasets that could be used to answer my question, and assist my partners in arriving at their conclusions. 
#### How has population in CMA's changed since 2001?
![pop_change_total](images/total_rate_change_PE_graph.png)
* As seen in the chart, in the 21 years since 2001, the top 30 metropolitan areas in Canada have continued to grow from ~5% to upwards of ~65% depending on the CMA. The fastest growing metropolitan area in Canada is Calgary, AB with Edmonton, AB and Kelowna, BC coming in close behind. 
#### How have housing prices in CMA's changed since 2001?
![price_change_total](images/total_rate_change_NHPI_graph.png)
* As seen in this chart, housing value has increased significantly in Canada in the time period previously specified, the increases ranged from 10% to over 200%. Winnipeg has had the largest increase in housing price over 20 years, with Calgary and Regina coming in 2nd and 3rd place. Interestingly, Calgary had the largest change in population and also a large change in price. Kelowna, which was 3rd in population increase is 20th in housing price increase. I believe this may be due to Kelowna being a lake city, which would have kept the price high even 20 years ago as it is desirable.
#### How has housing construction in CMA's changed since 2001?
![inventory_change_total](images/total_rate_change_NI_graph.png)
* New inventory, otherwise known as new residences entering the market, has varied substantially between CMA's which is due to a number of factors not investigated in my analysis. One can speculate that inventory is controlled by each city's buracracy, housing prices, zoning, and demand for new residences, however how these speculative variables correlate is unknown. 
* However, what can be known about housing inventory is that some areas such as Montreal, Vancouver, Edmonton, and Quebec have had substantial new inventory added to the market over the time period. Montreal had slightly under a 3000% increase whereas the other mentioned areas had between a 500% and 1000% increase in available housing in the metropolitan area. Large inventory increases are indicative of a CMA that stresses the importance of available housing, and probably is indicative of city that expects to have an upwards trend in population. Alternatively, cities with low inventory increases (or even decreases, such as Toronto and some other Ontario CMA's) most likely do not have the space to allocate for new residences, or already have a large number of residences and a high renter pool. These areas can make due with less inventory entering the market, however this will drive up housing prices and further push for a landlord's market. This claim is once again speculative, variables such as renter percentage were not obtained. 
#### Aggregate Scoring - Which CMA's are best in terms of housing?
![aggregate_score_chart](images/aggregated_score_graph.png)
* From the graph it can be seen that Montreal has the highest score of all other metropolitan areas by a significant margin. This is mainly due to its remarkable housing inventory and price percent change. Coming in second is Vancouver, then Edmonton. Wrapping up the top 5 metropolitan areas are Quebec and London. On the other end of things, Toronto has a negative score, due to its decrease in housing inventory percent change, meaning that there are not enough houses reaching the market to keep up with demand. The same can be said for the bottom 5 included in our analysis. Interestingly, the bottom 3 areas are all located in Ontario, which could be resultant in provincial legislation regarding housing construction or possibly just do to geographical limitations resticting increased inventory. Regardless, the worst scored areas are Toronto, Windsor, Guelph, and Greater Sudbury; whereas, the best scored areas are Montreal, Vancouver, Edmonton, and Quebec. 



## Question 3 + Results
* See the full analysis here: [Analysis 3](https://github.com/ubco-W2022T2-data301/project-group-group01/blob/8942e9aec2881804cb16acf74ef3e13c48e2ea8e/analysis/Katrinaanalysis3.ipynb)

## Summary/Conclusion
### Key points
* Population in canadian metropolitan areas has increased across the map, although the rate of increase varies drastically. 
* Since 2001, all regions assessed have increase in housing prices, with the largest increase being in Winnipeg (over 200% increase)
* Most CMA's have had an increase in housing inventory, but some regions (Toronto and other Ontario CMA's) have had a decrease or stable inventory. Having more inventory added is beneficial, therefore higher ranked CMA's must have a significant increase in market availablity. 
* Based on aggregated scoring, Montreal, Vancouver, Edmonton, and Quebec are the top CMA's; Toronto, Windsor, Guelph, and Greater Sudbury are the bottom CMA's of the 30 assessed. 
### Conclusion