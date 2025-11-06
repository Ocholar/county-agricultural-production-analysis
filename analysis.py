import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('/home/ubuntu/upload/project_data_set.csv')

print("\n=== INITIAL DATA EXPLORATION ===")
print(f"Dataset shape: {df.shape}")
print(f"\nColumn names:\n{df.columns.tolist()}")
print(f"\nFirst few rows:\n{df.head()}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nBasic statistics:\n{df.describe()}")

# ============================================================
# PART 1: DATA QUALITY IDENTIFICATION AND CLEANING
# ============================================================

print("\n\n=== DATA QUALITY ISSUES IDENTIFIED ===")

data_quality_issues = []

# Issue 1: Inconsistent column naming
issue1 = "Issue 1: Inconsistent column naming - 'Counties' should be 'County', 'TOTAL HOUSHOLDS' has typo (should be 'HOUSEHOLDS'), column names have mixed case and inconsistent spacing (e.g., 'Exotic cattle 0Dairy' has '0' instead of '-')"
print(issue1)
data_quality_issues.append(issue1)

# Issue 2: Missing values in population and area columns
missing_pop = df['Population (2019)'].isnull().sum()
missing_area = df['Area sq km'].isnull().sum()
missing_density = df['density per sq km'].isnull().sum()
issue2 = f"Issue 2: Missing values detected - Population (2019): {missing_pop} missing, Area sq km: {missing_area} missing, density per sq km: {missing_density} missing"
print(issue2)
data_quality_issues.append(issue2)

# Issue 3: Forest/Park entries mixed with county data
forest_parks = df[df['Counties'].str.contains('FOREST|PARK|NATIONAL', case=False, na=False)]
issue3 = f"Issue 3: Non-county administrative units mixed with county data - {len(forest_parks)} entries are forests/parks/reserves rather than counties: {forest_parks['Counties'].tolist()}"
print(issue3)
data_quality_issues.append(issue3)

# Issue 4: Data type issues - numeric columns may have been read as objects
numeric_cols = df.columns[1:]  # All columns except Counties
non_numeric = []
for col in numeric_cols:
    if df[col].dtype == 'object':
        non_numeric.append(col)
issue4 = f"Issue 4: Data type inconsistencies - Some numeric columns may contain non-numeric values or have incorrect data types"
print(issue4)
data_quality_issues.append(issue4)

# Issue 5: Potential outliers and data validation issues
# Check for negative values in count columns
issue5 = "Issue 5: Potential outliers and data validation - Need to check for negative values, zeros in population/area columns, and extreme outliers that may indicate data entry errors"
print(issue5)
data_quality_issues.append(issue5)

# ============================================================
# DATA CLEANING PROCESS
# ============================================================

print("\n\n=== DATA CLEANING PROCESS ===")

cleaning_steps = []

# Step 1: Fix column names
print("\nStep 1: Fixing column names...")
df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
# First, handle specific renames
column_mapping = {}
for col in df.columns:
    if col == 'Counties':
        column_mapping[col] = 'County'
    elif col == 'TOTAL HOUSHOLDS':
        column_mapping[col] = 'Total_Households'
    elif col == 'Exotic cattle 0Dairy':
        column_mapping[col] = 'Exotic_Cattle_Dairy'
    elif col == 'Exotic cattle 0Beef':
        column_mapping[col] = 'Exotic_Cattle_Beef'
    elif col == 'Population (2019)':
        column_mapping[col] = 'Population_2019'
    elif col == 'Area sq km':
        column_mapping[col] = 'Area_sq_km'
    elif col == 'density per sq km':
        column_mapping[col] = 'Density_per_sq_km'
    else:
        # Standardize other column names
        new_col = col.replace(' ', '_').replace('-', '_').replace('/', '_')
        column_mapping[col] = new_col

df = df.rename(columns=column_mapping)
step1 = "Step 1: Standardized column names - Fixed typos, removed spaces, standardized naming convention to snake_case"
cleaning_steps.append(step1)
print(step1)

# Step 2: Remove forest/park entries (non-county administrative units)
print("\nStep 2: Removing non-county entries...")
df_clean = df[~df['County'].str.contains('FOREST|PARK|NATIONAL', case=False, na=False)].copy()
removed_count = len(df) - len(df_clean)
step2 = f"Step 2: Removed non-county administrative units - Excluded {removed_count} forest/park entries to focus on county-level analysis"
cleaning_steps.append(step2)
print(step2)

# Step 3: Handle missing values
print("\nStep 3: Handling missing values...")
# For missing population and area, we'll check if they can be calculated or need removal
missing_critical = df_clean[df_clean['Population_2019'].isnull() | df_clean['Area_sq_km'].isnull()]
print(f"Counties with missing critical data: {missing_critical['County'].tolist()}")

# Remove rows with missing population or area as these are critical for analysis
df_clean = df_clean.dropna(subset=['Population_2019', 'Area_sq_km'])

# For other missing values in agricultural data, fill with 0 (assuming no activity if not reported)
agricultural_cols = df_clean.columns[1:-3]  # Exclude County and last 3 demographic columns
df_clean[agricultural_cols] = df_clean[agricultural_cols].fillna(0)

step3 = f"Step 3: Handled missing values - Removed {len(missing_critical)} counties with missing critical demographic data; filled missing agricultural data with 0 (assuming no activity if unreported)"
cleaning_steps.append(step3)
print(step3)

# Step 4: Convert data types
print("\nStep 4: Converting data types...")
# Ensure all numeric columns are numeric
for col in df_clean.columns[1:]:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

# Fill any NaN created by coercion with 0
df_clean = df_clean.fillna(0)

step4 = "Step 4: Converted data types - Ensured all numeric columns are properly typed as numeric, coerced any non-numeric values"
cleaning_steps.append(step4)
print(step4)

# Step 5: Validate and handle outliers
print("\nStep 5: Validating data and checking outliers...")
# Check for negative values
negative_counts = (df_clean.select_dtypes(include=[np.number]) < 0).sum().sum()
print(f"Negative values found: {negative_counts}")

# Recalculate density to ensure consistency
df_clean['Density_per_sq_km'] = df_clean['Population_2019'] / df_clean['Area_sq_km']

step5 = "Step 5: Validated data integrity - Checked for negative values, recalculated population density for consistency"
cleaning_steps.append(step5)
print(step5)

print(f"\nCleaned dataset shape: {df_clean.shape}")
print(f"Original dataset shape: {df.shape}")

# Save cleaned dataset
output_path = '/home/ubuntu/agricultural_analysis/cleaned_project_dataset.csv'
df_clean.to_csv(output_path, index=False)
print(f"\nCleaned dataset saved to: {output_path}")

# ============================================================
# DESCRIPTIVE ANALYSIS
# ============================================================

print("\n\n=== DESCRIPTIVE ANALYSIS ===")

# Indicator 1: Total households engaged in farming
total_farming_households = df_clean['Farming'].sum()
print(f"\nIndicator 1 - Total Households Engaged in Farming: {total_farming_households:,.0f}")

# Indicator 2: Average household size (Population / Total Households)
df_clean['Avg_Household_Size'] = df_clean['Population_2019'] / df_clean['Total_Households']
avg_household_size = df_clean['Avg_Household_Size'].mean()
print(f"Indicator 2 - Average Household Size Across Counties: {avg_household_size:.2f} persons/household")

# Indicator 3: Agricultural Specialization Index (Farming households / Total households)
df_clean['Agricultural_Specialization_Index'] = (df_clean['Farming'] / df_clean['Total_Households']) * 100
avg_specialization = df_clean['Agricultural_Specialization_Index'].mean()
print(f"Indicator 3 - Average Agricultural Specialization Index: {avg_specialization:.2f}% (percentage of households engaged in farming)")

# ============================================================
# VISUALIZATIONS
# ============================================================

print("\n\n=== CREATING VISUALIZATIONS ===")

# Visualization 1: Top 10 Counties by Crop Production
print("\nCreating Visualization 1: Top 10 Counties by Crop Production...")
top10_crop = df_clean.nlargest(10, 'Crop_Production')[['County', 'Crop_Production']]
print(top10_crop)

fig1, ax1 = plt.subplots(figsize=(12, 6))
bars = ax1.barh(top10_crop['County'], top10_crop['Crop_Production'], color='#2E7D32')
ax1.set_xlabel('Number of Households Engaged in Crop Production', fontsize=12, fontweight='bold')
ax1.set_ylabel('County', fontsize=12, fontweight='bold')
ax1.set_title('Top 10 Counties by Households Engaged in Crop Production', fontsize=14, fontweight='bold', pad=20)
ax1.invert_yaxis()
# Add value labels
for i, (idx, row) in enumerate(top10_crop.iterrows()):
    ax1.text(row['Crop_Production'], i, f" {row['Crop_Production']:,.0f}", 
             va='center', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('/home/ubuntu/agricultural_analysis/viz1_top10_crop_production.png', dpi=300, bbox_inches='tight')
print("Saved: viz1_top10_crop_production.png")
plt.close()

# Visualization 2: Comparison of Major Agricultural Sub-sectors
print("\nCreating Visualization 2: Agricultural Sub-sectors Comparison...")
subsector_totals = {
    'Crop Production': df_clean['Crop_Production'].sum(),
    'Livestock Production': df_clean['Livestock_Production'].sum(),
    'Aquaculture': df_clean['Aquaculture'].sum(),
    'Fishing': df_clean['Fishing'].sum()
}
print(subsector_totals)

fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(14, 6))

# Bar chart
subsector_df = pd.DataFrame(list(subsector_totals.items()), columns=['Sub-sector', 'Households'])
colors = ['#2E7D32', '#F57C00', '#0277BD', '#C62828']
bars = ax2a.bar(subsector_df['Sub-sector'], subsector_df['Households'], color=colors)
ax2a.set_ylabel('Total Households', fontsize=12, fontweight='bold')
ax2a.set_title('Total Households by Agricultural Sub-sector', fontsize=13, fontweight='bold')
ax2a.tick_params(axis='x', rotation=45)
# Add value labels
for bar in bars:
    height = bar.get_height()
    ax2a.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:,.0f}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

# Pie chart
ax2b.pie(subsector_df['Households'], labels=subsector_df['Sub-sector'], autopct='%1.1f%%',
         colors=colors, startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
ax2b.set_title('Distribution of Households Across Sub-sectors', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('/home/ubuntu/agricultural_analysis/viz2_subsector_comparison.png', dpi=300, bbox_inches='tight')
print("Saved: viz2_subsector_comparison.png")
plt.close()

# Additional visualization: Agricultural Specialization by County (Top 15)
print("\nCreating Additional Visualization: Agricultural Specialization Index...")
top15_spec = df_clean.nlargest(15, 'Agricultural_Specialization_Index')[['County', 'Agricultural_Specialization_Index']]

fig3, ax3 = plt.subplots(figsize=(12, 7))
bars = ax3.barh(top15_spec['County'], top15_spec['Agricultural_Specialization_Index'], 
                color='#1565C0')
ax3.set_xlabel('Agricultural Specialization Index (%)', fontsize=12, fontweight='bold')
ax3.set_ylabel('County', fontsize=12, fontweight='bold')
ax3.set_title('Top 15 Counties by Agricultural Specialization Index\n(% of Households Engaged in Farming)', 
              fontsize=14, fontweight='bold', pad=20)
ax3.invert_yaxis()
# Add value labels
for i, (idx, row) in enumerate(top15_spec.iterrows()):
    ax3.text(row['Agricultural_Specialization_Index'], i, 
             f" {row['Agricultural_Specialization_Index']:.1f}%", 
             va='center', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig('/home/ubuntu/agricultural_analysis/viz3_specialization_index.png', dpi=300, bbox_inches='tight')
print("Saved: viz3_specialization_index.png")
plt.close()

# ============================================================
# PART 2: PRIMARY AGRICULTURAL SECTOR CLASSIFICATION
# ============================================================

print("\n\n=== PART 2: PRIMARY AGRICULTURAL SECTOR CLASSIFICATION ===")

# Define Primary Agricultural Sector based on dominant activity
print("\nDefining Primary Agricultural Sector...")

def classify_primary_sector(row):
    """
    Classify county's primary agricultural sector based on household engagement.
    
    Logic:
    1. Compare the four main sub-sectors: Crop, Livestock, Aquaculture, Fishing
    2. Identify the dominant sector (highest household count)
    3. Apply threshold: dominant sector must have at least 50% more households than second-largest
    4. If threshold not met, classify as 'Mixed Agriculture'
    5. Special case: If Crop and Livestock are close (within 20%), classify as 'Crop-Livestock Mixed'
    """
    crop = row['Crop_Production']
    livestock = row['Livestock_Production']
    aquaculture = row['Aquaculture']
    fishing = row['Fishing']
    
    sectors = {
        'Crop': crop,
        'Livestock': livestock,
        'Aquaculture': aquaculture,
        'Fishing': fishing
    }
    
    # Sort sectors by household count
    sorted_sectors = sorted(sectors.items(), key=lambda x: x[1], reverse=True)
    dominant = sorted_sectors[0]
    second = sorted_sectors[1]
    
    # If dominant sector has at least 50% more households than second
    if dominant[1] > 0 and second[1] > 0:
        ratio = dominant[1] / second[1]
        
        # Special case: Crop and Livestock are close
        if dominant[0] in ['Crop', 'Livestock'] and second[0] in ['Crop', 'Livestock']:
            if ratio < 1.2:  # Within 20% of each other
                return 'Crop-Livestock Mixed'
        
        # Dominant sector is clearly leading
        if ratio >= 1.5:
            return f'{dominant[0]} Dominant'
        else:
            return 'Mixed Agriculture'
    elif dominant[1] > 0:
        return f'{dominant[0]} Dominant'
    else:
        return 'No Agriculture'

df_clean['Primary_Agricultural_Sector'] = df_clean.apply(classify_primary_sector, axis=1)

# Display distribution
sector_distribution = df_clean['Primary_Agricultural_Sector'].value_counts()
print("\nPrimary Agricultural Sector Distribution:")
print(sector_distribution)

# Create visualization for sector distribution
print("\nCreating visualization for Primary Agricultural Sector distribution...")
fig4, ax4 = plt.subplots(figsize=(10, 6))
bars = ax4.bar(sector_distribution.index, sector_distribution.values, 
               color=['#2E7D32', '#F57C00', '#0277BD', '#7B1FA2'])
ax4.set_ylabel('Number of Counties', fontsize=12, fontweight='bold')
ax4.set_xlabel('Primary Agricultural Sector', fontsize=12, fontweight='bold')
ax4.set_title('Distribution of Counties by Primary Agricultural Sector', fontsize=14, fontweight='bold', pad=20)
ax4.tick_params(axis='x', rotation=45)
# Add value labels
for bar in bars:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('/home/ubuntu/agricultural_analysis/viz4_primary_sector_distribution.png', dpi=300, bbox_inches='tight')
print("Saved: viz4_primary_sector_distribution.png")
plt.close()

# ============================================================
# POLICY-RELEVANT METRICS
# ============================================================

print("\n\n=== POLICY-RELEVANT METRICS ===")

# METRIC 1: Crop Yield Potential Intensity (Households per sq km)
print("\n--- METRIC 1: Crop Yield Potential Intensity ---")
print("Definition: Number of households engaged in crop production per square kilometer of county area")
print("Formula: Crop_Production / Area_sq_km")
print("Unit: Households per sq km")
print("Interpretation: Higher values indicate more intensive crop farming activity relative to land area")

df_clean['Crop_Intensity'] = df_clean['Crop_Production'] / df_clean['Area_sq_km']
top5_crop_intensity = df_clean.nlargest(5, 'Crop_Intensity')[['County', 'Crop_Production', 'Area_sq_km', 'Crop_Intensity']]

print("\nTop 5 Counties by Crop Yield Potential Intensity:")
print(top5_crop_intensity.to_string(index=False))

print("\nInterpretation for Policy Audience:")
print("These counties demonstrate the highest concentration of crop farming households relative to their land area.")
print("This suggests intensive agricultural land use, which may indicate: (1) high agricultural productivity potential,")
print("(2) limited land availability requiring efficient use, or (3) high population pressure on agricultural land.")
print("Policy interventions should focus on sustainable intensification, soil health management, and access to")
print("improved seeds and farming technologies to maximize yields while preserving land quality.")

print("\nLimitation: This metric does not account for land quality, climate suitability, or actual crop yields.")
print("Counties with smaller total areas may appear more intensive even with moderate farming activity.")

# METRIC 2: Agricultural Engagement vs Population Density
print("\n\n--- METRIC 2: Agricultural Engagement Rate ---")
print("Definition: Percentage of total households engaged in farming activities")
print("Formula: (Farming / Total_Households) * 100")
print("Unit: Percentage (%)")
print("Interpretation: Measures the extent to which a county's population depends on agriculture for livelihood")

# We already calculated this as Agricultural_Specialization_Index
# Now let's analyze correlation with population density

from scipy import stats

# Calculate correlation
correlation = stats.pearsonr(df_clean['Agricultural_Specialization_Index'], df_clean['Density_per_sq_km'])
print(f"\nCorrelation between Agricultural Engagement Rate and Population Density:")
print(f"Pearson correlation coefficient: {correlation[0]:.3f}")
print(f"P-value: {correlation[1]:.4f}")

# Top 5 by Agricultural Engagement Rate
top5_engagement = df_clean.nlargest(5, 'Agricultural_Specialization_Index')[
    ['County', 'Farming', 'Total_Households', 'Agricultural_Specialization_Index', 'Density_per_sq_km']
]

print("\nTop 5 Counties by Agricultural Engagement Rate:")
print(top5_engagement.to_string(index=False))

print("\nInterpretation for Policy Audience:")
print(f"The correlation coefficient of {correlation[0]:.3f} indicates a {'negative' if correlation[0] < 0 else 'positive'} relationship")
print("between agricultural engagement and population density. Counties with higher agricultural engagement rates")
print("show that a larger proportion of their population depends on farming for livelihood. These counties may have:")
print("(1) limited alternative employment opportunities, (2) strong agricultural traditions, or (3) favorable")
print("conditions for farming. Policy should focus on value chain development, market access, and agricultural")
print("extension services to improve productivity and incomes for farming households.")

print("\nLimitation: This metric does not distinguish between subsistence and commercial farming, nor does it")
print("account for farm sizes or income levels. High engagement rates may indicate either thriving agricultural")
print("economies or lack of economic diversification.")

# Create scatter plot for correlation
print("\nCreating scatter plot for Agricultural Engagement vs Population Density...")
fig5, ax5 = plt.subplots(figsize=(10, 7))
scatter = ax5.scatter(df_clean['Density_per_sq_km'], 
                      df_clean['Agricultural_Specialization_Index'],
                      s=100, alpha=0.6, c=df_clean['Farming'], cmap='YlGn', edgecolors='black', linewidth=0.5)
ax5.set_xlabel('Population Density (persons per sq km)', fontsize=12, fontweight='bold')
ax5.set_ylabel('Agricultural Engagement Rate (%)', fontsize=12, fontweight='bold')
ax5.set_title(f'Agricultural Engagement vs Population Density\n(Correlation: {correlation[0]:.3f})', 
              fontsize=14, fontweight='bold', pad=20)

# Add trend line
z = np.polyfit(df_clean['Density_per_sq_km'], df_clean['Agricultural_Specialization_Index'], 1)
p = np.poly1d(z)
ax5.plot(df_clean['Density_per_sq_km'], p(df_clean['Density_per_sq_km']), 
         "r--", alpha=0.8, linewidth=2, label=f'Trend line')

# Add colorbar
cbar = plt.colorbar(scatter, ax=ax5)
cbar.set_label('Number of Farming Households', fontsize=11, fontweight='bold')

ax5.legend(fontsize=10)
ax5.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/home/ubuntu/agricultural_analysis/viz5_engagement_vs_density.png', dpi=300, bbox_inches='tight')
print("Saved: viz5_engagement_vs_density.png")
plt.close()

# ============================================================
# SUMMARY STATISTICS FOR PRESENTATION
# ============================================================

print("\n\n=== SUMMARY STATISTICS ===")

summary_stats = {
    'Total Counties Analyzed': len(df_clean),
    'Total Farming Households': f"{df_clean['Farming'].sum():,.0f}",
    'Total Population (2019)': f"{df_clean['Population_2019'].sum():,.0f}",
    'Average Agricultural Engagement Rate': f"{df_clean['Agricultural_Specialization_Index'].mean():.1f}%",
    'Total Crop Production Households': f"{df_clean['Crop_Production'].sum():,.0f}",
    'Total Livestock Production Households': f"{df_clean['Livestock_Production'].sum():,.0f}",
    'Total Aquaculture Households': f"{df_clean['Aquaculture'].sum():,.0f}",
    'Total Fishing Households': f"{df_clean['Fishing'].sum():,.0f}",
}

print("\nKey Summary Statistics:")
for key, value in summary_stats.items():
    print(f"{key}: {value}")

# Save summary to file
with open('/home/ubuntu/agricultural_analysis/summary_statistics.txt', 'w') as f:
    f.write("AGRICULTURAL PRODUCTION ANALYSIS - SUMMARY STATISTICS\n")
    f.write("="*60 + "\n\n")
    
    f.write("DATA QUALITY ISSUES IDENTIFIED:\n")
    for i, issue in enumerate(data_quality_issues, 1):
        f.write(f"{i}. {issue}\n\n")
    
    f.write("\n" + "="*60 + "\n\n")
    f.write("CLEANING STEPS TAKEN:\n")
    for i, step in enumerate(cleaning_steps, 1):
        f.write(f"{i}. {step}\n\n")
    
    f.write("\n" + "="*60 + "\n\n")
    f.write("KEY DESCRIPTIVE INDICATORS:\n")
    for key, value in summary_stats.items():
        f.write(f"{key}: {value}\n")
    
    f.write("\n" + "="*60 + "\n\n")
    f.write("PRIMARY AGRICULTURAL SECTOR CLASSIFICATION LOGIC:\n")
    f.write("1. Compare four main sub-sectors: Crop, Livestock, Aquaculture, Fishing\n")
    f.write("2. Identify dominant sector with highest household count\n")
    f.write("3. Apply threshold: dominant sector must have ≥50% more households than second-largest\n")
    f.write("4. If threshold not met, classify as 'Mixed Agriculture'\n")
    f.write("5. Special case: If Crop and Livestock within 20%, classify as 'Crop-Livestock Mixed'\n\n")
    
    f.write("SECTOR DISTRIBUTION:\n")
    f.write(sector_distribution.to_string())
    
    f.write("\n\n" + "="*60 + "\n\n")
    f.write("POLICY-RELEVANT METRICS:\n\n")
    f.write("METRIC 1: Crop Yield Potential Intensity\n")
    f.write("Top 5 Counties:\n")
    f.write(top5_crop_intensity.to_string(index=False))
    
    f.write("\n\nMETRIC 2: Agricultural Engagement Rate\n")
    f.write("Top 5 Counties:\n")
    f.write(top5_engagement.to_string(index=False))
    f.write(f"\n\nCorrelation with Population Density: {correlation[0]:.3f} (p={correlation[1]:.4f})")

print("\nSummary statistics saved to: summary_statistics.txt")

print("\n\n=== ANALYSIS COMPLETE ===")
print("All outputs saved to /home/ubuntu/agricultural_analysis/")
