"""
Graduate Employment Insights Dashboard
Author: Gowtham
Date: 2025-09-25

This project was created for my personal portfolio and learning purposes only.
Please do not copy, redistribute, or use this code without my explicit permission.
"""


import pandas as pd  
import numpy as np   
import matplotlib.pyplot as plt  
import seaborn as sns  

# --- Generate synthetic data for 10 years ---
np.random.seed(42)  
years = np.arange(2016, 2026)  
passed_out = np.random.randint(300, 600, size=len(years))  
placed = np.random.randint(200, passed_out - 50)  
unemployed = passed_out - placed  


data = pd.DataFrame({
    'Year': years,
    'Passed_Out': passed_out,
    'Placed': placed,
    'Unemployed': unemployed
})


print("\nPreview of the data:")
print(data.head())


# --- Set up the visualization style and figure ---
import matplotlib.image as mpimg
from urllib.request import urlopen
from io import BytesIO

sns.set_theme(style="whitegrid")
fig, axs = plt.subplots(2, 2, figsize=(14, 10)) 


bg_img_url = "https://images.unsplash.com/photo-1503676382389-4809596d5290?auto=format&fit=crop&w=1500&q=80"
try:
    with urlopen(bg_img_url) as file:
        bg_img = mpimg.imread(BytesIO(file.read()), format='jpg')
    fig.figimage(bg_img, xo=0, yo=0, alpha=0.25, zorder=0)
except Exception as e:
    print(f"Could not load background image: {e}")


bar_width = 0.25
x = np.arange(len(years))
axs[0, 0].bar(x - bar_width, data['Passed_Out'], width=bar_width, label='Passed Out', color='#4B8BBE')
axs[0, 0].bar(x, data['Placed'], width=bar_width, label='Placed', color='#306998')
axs[0, 0].bar(x + bar_width, data['Unemployed'], width=bar_width, label='Unemployed', color='#FFE873')
axs[0, 0].set_xticks(x)
axs[0, 0].set_xticklabels(data['Year'])
axs[0, 0].set_title('Yearly College Outcomes')
axs[0, 0].legend()


axs[0, 1].plot(data['Year'], data['Placed'], marker='o', label='Placed', color='#306998', linewidth=2)
axs[0, 1].plot(data['Year'], data['Unemployed'], marker='s', label='Unemployed', color='#FFE873', linewidth=2)
axs[0, 1].set_title('Placement vs Unemployment Trend')
axs[0, 1].legend()

-
last_year = data.iloc[-1]
pie_labels = ['Placed', 'Unemployed']
pie_sizes = [last_year['Placed'], last_year['Unemployed']]
axs[1, 0].pie(pie_sizes, labels=pie_labels, autopct='%1.1f%%', startangle=140, colors=['#306998', '#FFE873'])
axs[1, 0].set_title(f"{last_year['Year']} Placement Distribution")


corr = data[['Passed_Out', 'Placed', 'Unemployed']].corr()
heatmap = sns.heatmap(corr, annot=True, cmap='coolwarm', ax=axs[1, 1], cbar=True)
axs[1, 1].set_title('Correlation Heatmap')


plt.suptitle('College Pass-Outs, Placements & Unemployment Analysis (2016-2025)', fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.96])


best_year = data.loc[data['Placed'].idxmax(), 'Year']
best_placed = data['Placed'].max()
worst_year = data.loc[data['Unemployed'].idxmax(), 'Year']
worst_unemp = data['Unemployed'].max()


note_text = (
    f"Best Placement Year: {best_year} ({best_placed} placed)\n"
    f"Worst Unemployment Year: {worst_year} ({worst_unemp} unemployed)"
)
plt.gcf().text(
    0.02, 0.01, note_text, fontsize=9, color='#22223b', ha='left', va='bottom', fontweight='bold'
)

plt.gcf().text(0.5, -0.04, 'Thank you for viewing this dashboard!\nCreated by Gowtham | 2025',
              fontsize=11, color='#4B8BBE', ha='center', va='top',
              bbox=dict(facecolor='#f2e9e4', edgecolor='#4B8BBE', boxstyle='round,pad=0.5'))

plt.savefig('dashboard_sample.png', bbox_inches='tight')
plt.show()


from matplotlib.patches import Rectangle
import matplotlib.patheffects as PathEffects


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


from matplotlib.colors import LinearSegmentedColormap
z = np.linspace(0, 1, 256).reshape(1, -1)
axs[0, 0].imshow(z, aspect='auto', cmap=LinearSegmentedColormap.from_list('bluefade', ['#e0f7fa', '#4B8BBE']), extent=[-0.5, len(years)-0.5, 0, max(data['Passed_Out'])+50], alpha=0.2)


plt.suptitle('College Pass-Outs, Placements & Unemployment Analysis (2016-2025)', fontsize=18, fontweight='bold', color='#22223b',
             path_effects=[PathEffects.withStroke(linewidth=3, foreground='white')])



print("\nSummary Statistics:\n", data.describe())


placement_rate = (data['Placed'] / data['Passed_Out']).mean()
unemployment_rate = (data['Unemployed'] / data['Passed_Out']).mean()

# --- Print more detailed insights for the user ---
print(f"\nBest placement year: {best_year}")
print(f"Worst unemployment year: {worst_year}")
print(f"Average placement rate: {placement_rate:.2%}")
print(f"Average unemployment rate: {unemployment_rate:.2%}")

