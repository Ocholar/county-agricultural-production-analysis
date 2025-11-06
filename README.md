Agricultural Production Analysis for County-Level Planning

A comprehensive MEL (Monitoring, Evaluation, and Learning) and Data Analytics project focused on transforming raw agricultural and demographic data into strategic insights for improving agricultural sustainability and food security at the county level.

📋 Project Overview

This project demonstrates advanced data cleaning, descriptive analysis, strategic data restructuring, and the application of MEL principles in a public sector/development program context. The analysis focuses on agricultural productivity and county-level planning using real agricultural and demographic data.

🎯 Objectives

• Part 1: Ensure data quality through rigorous cleaning and extract foundational insights on agricultural engagement across counties

• Part 2: Structure data to define strategic priorities and develop key performance indicators (KPIs) for agricultural programs

📊 Key Findings

Descriptive Indicators

• Total Farming Households: 6,354,211 households engaged in agricultural activities

• Average Household Size: 4.51 persons per household

• Agricultural Specialization Index: 60.7% average engagement rate across counties

Primary Agricultural Sector Classification

• 28 counties: Mixed Agriculture (diversified agricultural economy)

• 10 counties: Crop-Livestock Mixed (strong integration between sectors)

• 9 counties: Livestock Dominant

Policy-Relevant Metrics

Metric 1: Crop Yield Potential Intensity

Measures the number of households engaged in crop production per square kilometer of county area.

Top 5 Counties:

1. Vihiga: 192.48 households/sq km

2. Kisii: 156.76 households/sq km

3. Nyamira: 114.63 households/sq km

4. Kakamega: 106.60 households/sq km

5. Bungoma: 89.28 households/sq km

Metric 2: Agricultural Engagement Rate

Measures the percentage of total households engaged in farming activities.

Correlation with Population Density: -0.589 (p < 0.0001)

Top 5 Counties:

1. Kitui: 81.9%

2. Bomet: 81.3%

3. Vihiga: 79.3%

4. Makueni: 79.1%

5. Nyandarua: 78.4%

🗂️ Repository Structure

Plain Text
agricultural_analysis/
├── README.md                           # Project documentation
├── analysis.py                         # Main analysis script
├── cleaned_project_dataset.csv         # Cleaned dataset (deliverable)
├── summary_statistics.txt              # Summary of findings
├── presentation/                       # Slide presentation files
│   ├── title_slide.html
│   ├── data_cleaning.html
│   ├── descriptive_indicators.html
│   ├── crop_production_analysis.html
│   ├── crop_production_analysis_cont.html
│   ├── subsector_comparison.html
│   ├── primary_sector_classification.html
│   ├── metric_crop_intensity.html
│   ├── metric_engagement_rate.html
│   ├── metric_engagement_rate_cont.html
│   └── conclusion.html
├── viz1_top10_crop_production.png      # Visualization: Top 10 counties
├── viz2_subsector_comparison.png       # Visualization: Sub-sector comparison
├── viz3_specialization_index.png       # Visualization: Specialization index
├── viz4_primary_sector_distribution.png # Visualization: Sector distribution
└── viz5_engagement_vs_density.png      # Visualization: Engagement vs density

🛠️ Technologies Used

• Python 3.11: Core programming language

• pandas: Data manipulation and cleaning

• numpy: Numerical operations

• matplotlib: Data visualization

• seaborn: Statistical data visualization

• scipy: Statistical analysis and correlation

📈 Data Quality Issues Identified

1. Inconsistent column naming: Mixed case, typos (e.g., 'TOTAL HOUSHOLDS'), and spacing issues

2. Missing values: Critical demographic columns had missing data

3. Non-county entries: 12 forest/park entries mixed with county data

4. Data type inconsistencies: Numeric columns containing non-numeric values

5. Potential outliers: Data validation issues requiring verification

🧹 Data Cleaning Process

1. Standardized column names to consistent snake_case format

2. Removed 12 non-county entries (forests/parks) to focus on county-level analysis

3. Handled missing values by removing counties with missing critical data and filling agricultural data gaps with 0

4. Converted data types to ensure all numeric columns are properly typed

5. Validated data integrity by checking for negative values and recalculating population density

🔍 Methodology

Primary Agricultural Sector Classification Logic

1. Compare four main sub-sectors (Crop, Livestock, Aquaculture, Fishing) by household count

2. Identify the dominant sector with the highest number of engaged households

3. Apply threshold: dominant sector must have ≥50% more households than second-largest

4. If threshold not met, classify as 'Mixed Agriculture'

5. Special case: If Crop and Livestock are within 20% of each other, classify as 'Crop-Livestock Mixed'

Policy Metric Definitions

Crop Yield Potential Intensity

• Formula: Crop Production Households / Area (sq km)

• Unit: Households per sq km

• Interpretation: Higher values indicate more intensive crop farming activity relative to land area

Agricultural Engagement Rate

• Formula: (Farming Households / Total Households) × 100

• Unit: Percentage (%)

• Interpretation: Measures the extent to which a county's population depends on agriculture for livelihood

💡 Key Recommendations

1. Targeted Agricultural Support Programs: Develop differentiated support based on Primary Agricultural Sector classification

2. Sustainable Farming Practices: Promote sustainable intensification in high Crop Intensity counties

3. Economic Diversification: Invest in value chain development and non-farm employment in high Agricultural Engagement Rate counties

4. Further Research: Incorporate data on farm sizes, income levels, and actual crop yields for more precise targeting

🚀 Getting Started

Prerequisites

Bash


pip install pandas numpy matplotlib seaborn scipy


Running the Analysis

Bash


python3.11 analysis.py


Viewing the Presentation

Open any of the HTML files in the presentation/ directory in a web browser to view the slides.

📊 Visualizations

The project includes five comprehensive visualizations:

1. Top 10 Counties by Crop Production: Horizontal bar chart showing household engagement

2. Agricultural Sub-Sectors Comparison: Bar and pie charts comparing the four major sub-sectors

3. Agricultural Specialization Index: Top 15 counties by percentage of households engaged in farming

4. Primary Agricultural Sector Distribution: Bar chart showing county distribution across sector categories

5. Agricultural Engagement vs Population Density: Scatter plot with trend line showing correlation

📝 Limitations

• Does not distinguish between subsistence and commercial farming

• No information on farm sizes or actual productivity levels

• Does not account for land quality, climate suitability, or actual crop yields

• Data represents a snapshot and does not capture seasonal variations

• Counties with smaller total areas may appear more intensive even with moderate farming activity

👥 Author

Reagan Ochola 

📄 License

This project is for educational and purposes.

🙏 Acknowledgments

• Data source: County-level agricultural and demographic data (2019)

• Analysis framework: MEL principles for development program evaluation

• Design aesthetic: Agricultural Data Cartography with earthy terracotta and forest green color palette




Project Status: ✅ Complete

Last Updated: November 2025




