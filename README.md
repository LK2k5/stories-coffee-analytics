#Course: EECE490
#Students: Leen Kahwaji and Sarah Tourbah

# stories-coffee-analytics
Data analysis and machine learning project on Stories Coffee sales data to generate business insights and actionable recommendations.

## Business Problem
Stories Coffee provided one year of real sales data across 25 branches in Lebanon but lacks clear visibility into revenue concentration, margin performance, and product mix efficiency.
The objective of this project is to analyze sales, profitability, and product performance in order to provide actionable recommendations that can help increase revenue and profit.
The goal of this analysis is to identify:
- Which branches drive revenue and profitability
- How seasonality impacts demand
- Whether product mix (beverage vs food) affects margins
- Where operational improvements can increase profit

## Data
The project uses four raw CSV exports from the POS system:
- Monthly sales by branch (2025 + Jan 2026)
- Product-level profitability
- Sales by product groups
- Category summary by branch

The raw data contains inconsistencies (repeated headers, inconsistent branch names, formatting issues) which are handled in the data cleaning pipeline.


## Methodology
1. Data cleaning and normalization of raw POS exports  
2. Exploratory data analysis (EDA) on branch performance, seasonality, and category mix  
3. Product-level profitability analysis (menu engineering)  
4. Business insight generation and recommendations  


## Key Findings
- Revenue is concentrated in a small number of flagship branches (Ain El Mreisseh, Zalka, Khaldeh).
- Profit margins are tightly clustered (~70–75%), indicating standardized cost structure across branches.
- Sales are highly seasonal, with a significant peak in March and secondary increases in summer.
- Beverage-heavy branches (Airport, Event Starco) show stronger high-margin product mix.
  

## Visualizations

### Top 10 Branches by Total Sales (2025)
![Top Branches](outputs/figures/top10_branches_2025.png)

### Monthly Sales Trend (2025)
![Seasonality](outputs/figures/seasonality_2025.png)

### Profit Margin by Branch
![Margins](outputs/figures/top_margins.png)

### Beverage Revenue Share by Branch
![Beverage Share](outputs/figures/bev_share.png)



## Key Outputs
- Branch performance and seasonality analysis  
- Identification of high-profit and low-profit products  
- Beverage vs food profitability analysis  
- Actionable recommendations for management  

## Dashboard
The Streamlit dashboard provides an interactive interface to explore branch-level sales, profit margins, monthly trends, and category mix. Users can filter by branch and time to identify high-performing and underperforming locations. The dashboard is connected directly to the cleaned datasets, so it updates automatically when new data is processed. This prototype demonstrates how the solution can be extended to live POS data and advanced analytics (e.g., forecasting, alerts).

## How to Run
1. Clone the repository
```bash
git clone <repo-url>
cd stories-coffee-analytics

2. Create and activate virtual environment
for Windows:
python -m venv .venv
.venv\Scripts\activate
for Mac/Linux:
python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Run the notebooks
jupyter notebook

Then open and execute in order:
notebooks/01_cleaning.ipynb
notebooks/02_analysis.ipynb
All figures will be saved in:
outputs/figures/



