# Agricultural Production Analysis for County-Level Planning

A MEL and Data Analytics Project

---

## Introduction & Objectives

- **Objective:** To transform raw agricultural and demographic data into strategic insights for improving agricultural sustainability and food security.

- **Part 1:** Data Cleaning and Descriptive Analysis

- **Part 2:** MEL Logic and Policy-Relevant Metrics

---

## Part 1: Data Cleaning & Quality

### Data Quality Issues Identified:

- Inconsistent column names and typos.

- Missing values in critical demographic columns.

- Inclusion of non-county administrative units (forests, parks).

- Incorrect data types for numeric columns.

- Potential for data entry errors and outliers.

### Data Cleaning Steps:

- Standardized all column names to a consistent snake_case format.

- Removed 12 non-county entries to focus the analysis on counties.

- Removed counties with missing population or area data and filled other missing values with 0.

- Converted all relevant columns to numeric data types.

- Validated data integrity by checking for negative values and recalculating population density.

---

## Part 1: Descriptive Analysis: Key Indicators

- **Total Households Engaged in Farming:** 6,354,211

- **Average Household Size:** 4.51 persons/household

- **Average Agricultural Specialization Index:** 60.7% of households engaged in farming.

**Interpretation:** A significant portion of the population across the analyzed counties is engaged in agriculture, highlighting the sector's importance for livelihoods. The average household size is a key demographic factor for food security planning.

---

## Part 1: Descriptive Analysis: Visualizations

### Top 10 Counties by Crop Production Households

![Top 10 Counties by Crop Production Households](https://files.manuscdn.com/user_upload_by_module/session_file/310519663202798138/CWNLpiruPAsEwwmN.png)

### Comparison of Major Agricultural Sub-sectors

![Comparison of Major Agricultural Sub-sectors](https://files.manuscdn.com/user_upload_by_module/session_file/310519663202798138/fuWrqRqeDZCWcbRH.png)

**Interpretation:** Crop production is the dominant agricultural sub-sector, followed by livestock. The top 10 counties in crop production are geographically diverse, indicating widespread engagement. This distribution provides a basis for targeted interventions in the crop sub-sector.

---

## Part 2: Defining a Primary Agricultural Sector

### Transformation Logic:

- A 'Primary Agricultural Sector' was defined for each county based on the dominant sub-sector (Crop, Livestock, Aquaculture, Fishing).

- A sector is considered 'Dominant' if it has at least 50% more households than the next largest sector.

- If the dominant and second-largest sectors are Crop and Livestock and are within 20% of each other, the county is classified as 'Crop-Livestock Mixed'.

- Otherwise, if no single sector is dominant, it's classified as 'Mixed Agriculture'.

### Distribution of Counties:

![Distribution of Counties by Primary Agricultural Sector](https://files.manuscdn.com/user_upload_by_module/session_file/310519663202798138/TwTiQLCsMWzmHIuk.png)

**Interpretation:** The majority of counties have a 'Mixed Agriculture' economy, indicating a diversified agricultural base. 'Crop-Livestock Mixed' is the next most common, suggesting strong integration between these two sub-sectors. This classification helps in designing programs tailored to the specific agricultural profile of each county.

---

## Part 2: Policy-Relevant Metric 1: Crop Yield Potential Intensity

- **Policy Question:** Which counties have the highest crop farming intensity relative to their land area?

- **Metric:** Crop Intensity (Households in Crop Production per sq km)

| County | Crop_Production | Area_sq_km | Crop_Intensity |
| --- | --- | --- | --- |
| VIHIGA | 108522 | 563.8 | 192.483150 |
| KISII | 207400 | 1323.0 | 156.764928 |
| NYAMIRA | 102856 | 897.3 | 114.628329 |
| KAKAMEGA | 321945 | 3020.0 | 106.604305 |
| BUNGOMA | 269979 | 3023.9 | 89.281722 |

**Interpretation:** These counties show a high concentration of crop farming, suggesting intensive land use. This could mean high productivity, but also a risk of land degradation. Policies should focus on sustainable intensification and resource management.

---

## Part 2: Policy-Relevant Metric 2: Agricultural Engagement Rate

- **Policy Question:** How does the level of household farming engagement correlate with population density?

- **Metric:** Agricultural Engagement Rate ((Farming / Total_Households) * 100)

| County | Farming | Total_Households | Agricultural_Specialization_Index | Density_per_sq_km |
| --- | --- | --- | --- | --- |
| KITUI | 215322.0 | 262942 | 81.889542 | 37.338339 |
| BOMET | 152564.0 | 187641 | 81.306324 | 345.999052 |
| VIHIGA | 113753.0 | 143365 | 79.345028 | 1046.493437 |
| MAKUENI | 193531.0 | 244669 | 79.099109 | 120.890719 |
| NYANDARUA | 140854.0 | 179686 | 78.388967 | 194.262714 |

**Interpretation:** The correlation coefficient of -0.589 indicates a negative relationship between agricultural engagement and population density. Counties with higher agricultural engagement rates show that a larger proportion of their population depends on farming for livelihood. Policy should focus on value chain development, market access, and agricultural extension services to improve productivity and incomes for farming households.

---

## Conclusion & Recommendations

- The analysis reveals significant diversity in agricultural engagement and specialization across counties.

- **Recommendation 1:** Develop targeted agricultural support programs based on the 'Primary Agricultural Sector' classification.

- **Recommendation 2:** In counties with high 'Crop Intensity', promote sustainable farming practices to mitigate land degradation.

- **Recommendation 3:** In counties with high 'Agricultural Engagement Rate' but low economic diversification, invest in non-farm employment opportunities.

- **Recommendation 4:** Further research is needed to incorporate data on farm size, income levels, and specific crop yields for a more granular analysis.

