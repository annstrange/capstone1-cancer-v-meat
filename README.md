# capstone1-cancer-v-meat


Capstone I Proposal - Ann Strange
22 Oct 2020
“Forks Over Knives” Debunked?

## Background & Motivation
“The Emperor of All Maladies” (an uplifting read) points out that cancer has been around for all recorded human history.  We now know it’s a disease of genetic mutation, and also that environment can play a huge role, e.g. smoking with lung cancer or sun exposure with melanoma.  People close to me have suffered from cancer, leading me to be interested in ways to avoid this form of human suffering.   The documentary, “Forks Over Knives” promotes evidence from their study that a whole-foods based diet very significantly affects your likelihood of not getting cancer, particularly pointing to the consumption of animal products as having a direct correlation with cancer rates.  They contend that reducing the consumption of animal products including meat, fish, eggs, and dairy to below 5% of your diet will dramatically change your prognosis: actually preventing cancer as well as slowing its development.  Here let's analyze global cancer data by country compared with animal product consumption to see if we can find correlations that might support this claim.  If this claim is true, we should find that countries that eat less animal products are having lower instances of cancer.  As there are many confounders in the causes for cancer, any results will not prove/disprove the documentary, but the failure to find any correlations would make it difficult to support their claim.

## Exploratory Data Analysis
The World Health Organization (WHO) supplies a database called CI5, Cancer Incidence in Five Continents Volume XI. The CI5 database contains incidence rates from 343 cancer registries in 65 countries for cancers diagnosed from 2008 to 2012, for all cancers and 28 major types. The download of summary data provides a set of csv files. There is one with population metrics, and one for the cancer cases reported.  Population data includes columns for Registry (reporting location), Year, Sex, Total population, and remaining columns are the breakdowns by age range (every 5 years).  The Case files include columns to indicate the Registry, Year, Sex, Cancer type code, and the same 5 year age range counts. Additional files provide code definitions. 

The Our World in Data site provides a chart and downloadable .csv of meat/dairy/etc supply metrics per country and year, originally sourced from the Food and Agriculture Organization of the United Nations (FAOSTAT).  The column title is like “Meat food supply quantity (kg/capita/yr)”, a float to 2 decimal places.  Meat, fish, dairy, etc need to be downloaded as separate metrics but have the same file format.  We’ll use 2008 to be able to correspond with the time period available in C15.  

## Data Munging 
1. Cancer statistics are reported regionally by "registry".  Some areas such as the US have many sub-classifications of cancer statistics, which can be reported on multiple levels.  The data set was reduced in these case to only inlude national level data, to avoid double counting.  Other countries such as Canada do not have a total category, so sums by region were done.
2.  The most complete set of cancer data I could identify was for the five year range from 2008-2012 so this was selected and divided by 5 for an annual average for this time period.
3. Meat, Egg, and Dairy were aggregated by country for 2008.
4. Weighted averages were used for the cancer case means, by population sample size.
5. The population was divided into top 5/6 and bottom 1/6 for comparison.

## Assumptions/Disclaimers
1. There is a strong correlation between wealth and meat consumption.  Wealth may be a confounder.
2. Some countries do not tend to report cancer statistics as thoroughly as other countries.  Countries without screening may detect cancer later.
3. Only 60 countries were compared in this analysis where adequate data existed for both cancer stats and animal product consumption. 
4. Age is a big cancer stats confounder as the probability of getting cancer increases exponentially as people age, and the WHO strongly recommends using an Age Adjusted average for any country to country comparisons.  Instead I limited the sample to young people, between age 20 and 49.
6. To compare animal product consuming populations with non-animal consuming populations using the Two Sample Approximate Test of Population Proportions, there is an assumption required on the independence of each "Binimial trial" i.e. each incidence of cancer in independent of the others, and this is likely to not hold true.  It would be interesting to conduct this test exluding regions such as Chernobyl and Hiroshima, or exclude types of cancer with known causes such as smoking where external and regional factors are certainly contributing to cancer rates.
7. To represent the lowest animal product consumption, I've selected the lowest 10 countries in our set (1/6 our sample) with lower than 115 kg/capita which we'll use to represent "low" consumption.  If the average person consumes 2 kg/food and water per day, and we account for some waste**, this would come out to < 10% daily animal product consumption. For "high" consumption countries, the ratio would be closer to 25-30% of diets. 

     **[wasted food report](https://en.reset.org/knowledge/global-food-waste-and-its-environmental-impact-09122018) 



### Cancer by Country

Sample data

![](images/CancerData.png)

After Munging

![](images/CancerDataAfterMunging.png)

Cancer Incidence Age 20-49 (2008-2012) for Our 60 Comparison Countries, Ranked by Probability

![](images/cancer_percapita.png)

### Animal Consumption Per Capita


Our 60 Countries Ranked by Animal Consumption Per Capita, 2008 (Meat, Egg, Milk)

![](images/animal_consumption2.png)



## Does It Look Like There's Correlation?

    df_combo[['country_name','Incidence Per Age Capita', 'animal_product_kg_cap_yr']].corr(method='pearson')

![](images/CorrelationOfMeasures2.png)



## Hypothesis Test

We would like to test the "Forks Over Knives" claim that consuming less animal products reduces your change of developing cancer.  

Our Null Hypothesis is that the chance of getting cancer in a low meat/dairy country would fall within normal probabilities for getting cancer, within a significance of 5%.  Our alternate hypothesis is that there is a significant difference in the probabilies, within a significance of 5%. 

![](images/NullHypothesis.png)

I usesd the * Two Sample Approximate Test of Population Proportions to analyze this *. 


#### Probablistic Model of the Stiuation Assuming the Null Hypothesis is True Using Frequencies and Two Samples

Assuming that each cancer incidence is independent of all the rest (not actually true), the number of cancer incidents per year for age 20-49 are Binomially distributed. 

Our sample populations are:
Population in animal eating countries age 20-49: approx 324 million 
Population in vegan countries age 20-49: approx 77 million

We'll use frequency in the test so we can account for the population differences.  Our hypothesis test and probablistic model for the difference in sample frequencies can be represented as 


![](images/HypothesisTestLaTex.png)


**Results** 
The p-value from this calculation is effectively zero. (is this likely?)

|  |  |
|----------|:-------------|  
|**mean (cancer probability worldwide)**| 0.1320 % |
|**mean (animal consumers)**| 0.1446 % |
|**mean (non animal consumers)**|  0.0790 % |


** Means are also calculated as Weighted Averages, by the sample population sizes.

Observations: The population sizes are so large and the variances so small, our standard deviation and standard error are therefore extremely narrow.  However, even looking at the data as if the population instances were each country (n = 50 and 10), the distributions are extremely narrow, with effectively zero overlap in the PMF curves. 



## Conclusions
Based on this analysis, our p-value is far below alpha, I therefore reject the Null Hypothesis and conclude I cannot disagree with the claims made in "Forks Over Knives" that animal consumption has a correlation with cancer incidence.  Due to the many assumptions required for this type of statistical analysis to be accurate, many of which do not hold true, this should not be considered conclusive evidence, but perhaps may prompt additional study.

