"""
Graduate Employment Insights Dashboard
Author: Gowtham
Date: 2025-09-25

This project was created for my personal portfolio and learning purposes only.
Please do not copy, redistribute, or use this code without my explicit permission.
"""

# --- Import required libraries ---
import pandas as pd  # For data manipulation and analysis
import numpy as np   # For numerical operations and random data generation
import matplotlib.pyplot as plt  # For plotting
import seaborn as sns  # For advanced statistical visualizations

# --- Generate synthetic data for 10 years ---
np.random.seed(42)  # For reproducibility
years = np.arange(2016, 2026)  # Years from 2016 to 2025
passed_out = np.random.randint(300, 600, size=len(years))  # Total students passed out each year
placed = np.random.randint(200, passed_out - 50)  # Students placed (random, but less than passed out)
unemployed = passed_out - placed  # Students not placed

# --- Create a DataFrame to store the data ---
data = pd.DataFrame({
    'Year': years,
    'Passed_Out': passed_out,
    'Placed': placed,
    'Unemployed': unemployed
})

# --- Data Preview: Show the first few rows of the dataset ---
print("\nPreview of the data:")
print(data.head())


# --- Set up the visualization style and figure ---
import matplotlib.image as mpimg
from urllib.request import urlopen
from io import BytesIO

sns.set_theme(style="whitegrid")
fig, axs = plt.subplots(2, 2, figsize=(14, 10))  # 2x2 grid of plots

# --- Add a background image to the figure ---
# You can change this URL to any image you prefer
bg_img_url = "https://images.unsplash.com/photo-1503676382389-4809596d5290?auto=format&fit=crop&w=1500&q=80"
try:
    with urlopen(bg_img_url) as file:
        bg_img = mpimg.imread(BytesIO(file.read()), format='jpg')
    fig.figimage(bg_img, xo=0, yo=0, alpha=0.25, zorder=0)
except Exception as e:
    print(f"Could not load background image: {e}")

# --- Bar Chart: Passed Out, Placed, Unemployed per year ---
bar_width = 0.25
x = np.arange(len(years))
axs[0, 0].bar(x - bar_width, data['Passed_Out'], width=bar_width, label='Passed Out', color='#4B8BBE')
axs[0, 0].bar(x, data['Placed'], width=bar_width, label='Placed', color='#306998')
axs[0, 0].bar(x + bar_width, data['Unemployed'], width=bar_width, label='Unemployed', color='#FFE873')
axs[0, 0].set_xticks(x)
axs[0, 0].set_xticklabels(data['Year'])
axs[0, 0].set_title('Yearly College Outcomes')
axs[0, 0].legend()

# --- Line Chart: Placement and Unemployment Trends ---
axs[0, 1].plot(data['Year'], data['Placed'], marker='o', label='Placed', color='#306998', linewidth=2)
axs[0, 1].plot(data['Year'], data['Unemployed'], marker='s', label='Unemployed', color='#FFE873', linewidth=2)
axs[0, 1].set_title('Placement vs Unemployment Trend')
axs[0, 1].legend()

# --- Pie Chart: Placement Distribution for the Last Year ---
last_year = data.iloc[-1]
pie_labels = ['Placed', 'Unemployed']
pie_sizes = [last_year['Placed'], last_year['Unemployed']]
axs[1, 0].pie(pie_sizes, labels=pie_labels, autopct='%1.1f%%', startangle=140, colors=['#306998', '#FFE873'])
axs[1, 0].set_title(f"{last_year['Year']} Placement Distribution")

# --- Heatmap: Correlation between columns ---
corr = data[['Passed_Out', 'Placed', 'Unemployed']].corr()
heatmap = sns.heatmap(corr, annot=True, cmap='coolwarm', ax=axs[1, 1], cbar=True)
axs[1, 1].set_title('Correlation Heatmap')

# --- Main Title and Layout ---
plt.suptitle('College Pass-Outs, Placements & Unemployment Analysis (2016-2025)', fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.96])

# --- Add a visually attractive summary box for best/worst years at the bottom left ---
best_year = data.loc[data['Placed'].idxmax(), 'Year']
best_placed = data['Placed'].max()
worst_year = data.loc[data['Unemployed'].idxmax(), 'Year']
worst_unemp = data['Unemployed'].max()

# --- Add a plain note for best/worst employee year at the bottom (no background) ---
note_text = (
    f"Best Placement Year: {best_year} ({best_placed} placed)\n"
    f"Worst Unemployment Year: {worst_year} ({worst_unemp} unemployed)"
)
plt.gcf().text(
    0.02, 0.01, note_text, fontsize=9, color='#22223b', ha='left', va='bottom', fontweight='bold'
)

# --- Add a custom footer to the dashboard ---
plt.gcf().text(0.5, -0.04, 'Thank you for viewing this dashboard!\nCreated by Gowtham | 2025',
              fontsize=11, color='#4B8BBE', ha='center', va='top',
              bbox=dict(facecolor='#f2e9e4', edgecolor='#4B8BBE', boxstyle='round,pad=0.5'))

# --- Save the dashboard as an image file (save before plt.show) ---
plt.savefig('dashboard_sample.png', bbox_inches='tight')
plt.show()

# --- Extra Visual Enhancements ---
from matplotlib.patches import Rectangle
import matplotlib.patheffects as PathEffects

# Highlight best/worst years on the line chart
best_idx = data['Placed'].idxmax()
worst_idx = data['Unemployed'].idxmax()
axs[0, 1].annotate('Best Placement',
                   xy=(data['Year'][best_idx], data['Placed'][best_idx]),
                   xytext=(data['Year'][best_idx], data['Placed'][best_idx]+20),
                   arrowprops=dict(facecolor='green', shrink=0.05),
                   fontsize=10, color='green', fontweight='bold')
axs[0, 1].annotate('Worst Unemployment',
                   xy=(data['Year'][worst_idx], data['Unemployed'][worst_idx]),
                   xytext=(data['Year'][worst_idx], data['Unemployed'][worst_idx]+20),
                   arrowprops=dict(facecolor='red', shrink=0.05),
                   fontsize=10, color='red', fontweight='bold')

# Add a gradient background to the bar chart
from matplotlib.colors import LinearSegmentedColormap
z = np.linspace(0, 1, 256).reshape(1, -1)
axs[0, 0].imshow(z, aspect='auto', cmap=LinearSegmentedColormap.from_list('bluefade', ['#e0f7fa', '#4B8BBE']), extent=[-0.5, len(years)-0.5, 0, max(data['Passed_Out'])+50], alpha=0.2)

# Custom font and shadow for the main title
plt.suptitle('College Pass-Outs, Placements & Unemployment Analysis (2016-2025)', fontsize=18, fontweight='bold', color='#22223b',
             path_effects=[PathEffects.withStroke(linewidth=3, foreground='white')])


# --- Print summary statistics for the data ---
print("\nSummary Statistics:\n", data.describe())

# --- Calculate average placement and unemployment rates ---
placement_rate = (data['Placed'] / data['Passed_Out']).mean()
unemployment_rate = (data['Unemployed'] / data['Passed_Out']).mean()

# --- Print more detailed insights for the user ---
print(f"\nBest placement year: {best_year}")
print(f"Worst unemployment year: {worst_year}")
print(f"Average placement rate: {placement_rate:.2%}")
print(f"Average unemployment rate: {unemployment_rate:.2%}")
