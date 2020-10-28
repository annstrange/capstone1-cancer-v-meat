# capstone1-cancer-v-meat


Capstone I Proposal - Ann Strange
22 Oct 2020
“Forks Over Knives” Debunked?

## Background & Motivation
“The Emperor of All Maladies” points out that cancer has been around for all recorded human history.  We now know it’s a disease of genetic mutation, and also that environment can play a huge role, e.g. smoking with lung cancer or sun exposure with melanoma.  People close to me have suffered from cancer, leading me to be interested in ways to avoid this form of human suffering.   The documentary, “Forks Over Knives” promotes evidence from their study that a whole-foods based diet very significantly affects your likelihood of not getting cancer, particularly pointing to the consumption of animal products as having a direct correlation with cancer rates.  They contend that reducing the consumption of animal products including meat, fish, and dairy to below 5% of your diet will dramatically change your prognosis: actually preventing cancer as well as slowing its development.  I would like to analyze global cancer data by country compared with animal product consumption to see if I can find correlations that might support this claim.  If this claim is true, we should find that countries that eat less animal products are having lower instances of cancer.  As there are many confounders in the causes for cancer, any results will not prove/disprove the documentary, but the failure to find any correlations would make it difficult to support their claim.

## Exploratory Data Analysis
The World Health Organization (WHO) supplies a database called CI5, Cancer Incidence in Five Continents Volume XI. The CI5 database contains incidence rates from 343 cancer registries in 65 countries for cancers diagnosed from 2008 to 2012, for all cancers and 28 major types. The download of summary data provides a set of csv files. There is one with population metrics, and one for the cancer cases reported.  Population data includes columns for Registry (reporting location), Year, Sex, Total population, and remaining columns are the breakdowns by age range (every 5 years).  The Case files include columns to indicate the Registry, Year, Sex, Cancer type code, and the same 5 year age range counts. Additional files provide code definitions. 

The Our World in Data site provides a chart and downloadable .csv of meat/dairy/etc supply metrics per country and year, originally sourced from the Food and Agriculture Organization of the United Nations (FAOSTAT).  The column title is like “Meat food supply quantity (kg/capita/yr)”, a float to 2 decimal places.  Meat, fish, dairy, etc need to be downloaded as separate metrics but have the same file format.  We’ll use 2008 to be able to correspond with the time period available in C15.  




### Cancer by Country

    <base bar? chart, top and bottom 5>

    map

### Animal Consumption Per Capita

    <base chart top and bottom 5>
    map


## Let's look at the Correlation

    map together

    stats


## Confounders
* Age and Cancer
* Strength of reporting systems
* Meat consumption and wealth are strongly correlated



## Interesting Findings
* Our World in Data points out that Meat consumption and wealth are strongly positively correlated.  We can see that the countries with very little cancer reporting are likely also poor, to not participate as heavily in academic pursuits such as data collection.  Most of Africa has not reported in one or both categories so they are excluded.
* We were able to consolidate and match data for 58 countries.
* Note that a typical kg consumed per person per day under healthy conditions is 2 kg/day.  Countries which consume more than/less than 5% /day are ______
* We have not taken into account the major 

