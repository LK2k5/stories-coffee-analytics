# stories-coffee-analytics
Data analysis and machine learning project on Stories Coffee sales data to generate business insights and actionable recommendations.
## Business Problem
Stories Coffee provided one year of real sales data across 25 branches in Lebanon.  
The objective of this project is to analyze sales, profitability, and product performance in order to provide actionable recommendations that can help increase revenue and profit.

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

## Key Outputs
- Branch performance and seasonality analysis  
- Identification of high-profit and low-profit products  
- Beverage vs food profitability analysis  
- Actionable recommendations for management  

## How to Run
1. Install dependencies:
```bash
pip install -r requirements.txt
