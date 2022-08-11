# Successive Relocation of Marine Species in the Northern Hemisphere from 1970 to 2020
## Data and materials availability
### Data sources and our cleaned versions
>`1. `Data of specific occurrence locations of marine species
>>**Data sources:**OBIS, https://obis.org/data/access/  
**our cleaned versions:The extracted data on the basis of occurrence is available in [release 1](https://github.com/Casey-bit/marine_food_web_research/releases/tag/occurrence_record_1) and [release 2](https://github.com/Casey-bit/marine_food_web_research/releases/tag/occurrence_record_2). And the extracted latitudinal locations is available in [release 3](https://github.com/Casey-bit/marine_food_web_research/releases/tag/latitudinal_location).**

>`2. `Data of the concentration of marine chlorophyll-a in the Northern Hemisphere from 1998 to 2015
>>**Data sources:**NASA, https://www.earthdata.nasa.gov/   

>`3. `Determination criterion of the trophic levels and the biological attributes of marine species
>>**Data sources:**:`(1). `SeaLifeBase, https://www.sealifebase.org/  
       `(2). `Mindat, https://www.mindat.org/  
       `(3). `WRoMS, https://www.marinespecies.org/   
**our cleaned versions:All the biological attributes needed in our analysis are available in [release 4](https://github.com/Casey-bit/marine_food_web_research/releases/tag/attributes).**
### Key codes
`1. `**Preprocessing**
|Preprocessing codes|Remarks|
|:---|:---|
|01_extract_occurrence_records.py|Get the raw data on the basis of occurrence ([release 1](https://github.com/Casey-bit/marine_food_web_research/releases/tag/occurrence_record_1) and [release 2](https://github.com/Casey-bit/marine_food_web_research/releases/tag/occurrence_record_2))|
|02_count_records_for_family.py|Count the records number of each family from 1970 to 2020|
|03_get_latitudinal_records.py|Get the latitudinal records group by family in each year ([release 3](https://github.com/Casey-bit/marine_food_web_research/releases/tag/latitudinal_location))|
|04_get_percentage_3_regions.py|Calculate the distributional percentage in each region for each family in each year|
|05_median_reserve_and_denoising.py|`(1). `Calculate the median of latitudinal records for each family in each year; `(2). `Remove families that does not include records from 1970 to 1979; `(3). `Denoising median curves over time|

`2. `**Main figures**
|Main figures|Remarks|
|:---|:---|
|fig_1|Changes in latitudinal position of marine families in different time periods and changes in total chlorophyll-a concentration with latitude|
|fig_2|Food web consisting of 559 families and the proportion of species in each trophic level by the direction of shift (the materials in available in [release 5](https://github.com/Casey-bit/marine_food_web_research/releases/tag/level))|
|fig_3|Shift of families associated with trophic levels|

`3. `**Supplement figures**
|Supplement figures|Remarks|
|:---|:---|
|fig_S1|Number of marine species for each family|
|fig_S2|Number of families shifting northward or southward from 1970 to 2020 in the Northern Hemisphere|
|fig_S3|The kernel density estimation plots of the distribution of family trajectories (559 families in fig.2)|
|fig_S4|Shift routes of families over time (3 regions)|
|fig_S5|Number of families at each trophic level (1,446 families in total, [release 4 (attributes)](https://github.com/Casey-bit/marine_food_web_research/releases/tag/attributes))|
|fig_S6|Linear regression of fig.3|
|fig_S7|Shift routes at the taxonomic levels of genus and order|
