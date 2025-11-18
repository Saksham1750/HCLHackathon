#  Inventory & Store Performance Analysis

This project explores how **store inventory levels** influence **sales**, **customer purchasing behavior**, and **future spending**, using data from *stores*, *products*, and *store_sales_line_items*.

---

## Objectives
- Analyze correlation between inventory and sales success.  
- Predict customer future spend (next quarter/year).  
- Estimate likely discounts/promotions based on loyalty tier & spending.  
- Identify customers who may increase spend with improved inventory.  
- Assess impact of inventory optimization on sales & satisfaction.  
- Build a dashboard showcasing key store performance KPIs.

---

## Dataset
**Entities Used:**  
- `stores`
- `products`  
- `customer`
- `Sales`
- `Inventory`
## Dataset Size Overview

| Table Name   | Description                             | No. of Rows |
|--------------|------------------------------------------|-------------|
| **stores**   | 15 stores (5 chains × 3 branches each)    | **15**      |
| **products** | Product catalog with categories & pricing | **100**     |
| **customers**| Customer info with loyalty tiers          | **2,000**   |
| **sales**    | Transaction-level sales data (2021–2023)  | **20,000**  |
| **inventory**| Monthly opening/closing inventory per store × product | **54,000** |


Data includes inventory levels, product details, sales transactions, customer history, discounts, and loyalty tiers.

---

## Preprocessing
- Cleaned missing/duplicate data  
- Merged store–product–sales tables

---

## Key Analysis
- Inventory vs sales correlation  
- Top-selling products & stockout frequency
- Customer Turnaround Rate
- Store performance comparison  

---

## Predictive Models
- **Future Spend Prediction:** Regression models (Linear Regression)  
- **Promo Discount Likelihood:** Classification models (Logistic Regression)

Metrics used: RMSE, R², Accuracy.

---
## Resposibilities/Goals 
Saksham - What is the estimated future spend of a customer for the next quarter/year based on their previous year's purchase patterns and store performance?

Rohan - Analyze how local store inventory levels correlate with customer purchasing behavior and sales success.

Mayank Bansal - Which customers are most likely to increase their spending if inventory availability improves top-selling products?

Yash Dahiya - How much discount or promotional offers is a customer likely to receive based on their previous spending behavior and loyalty tier?

## Dashboard
Dashboard includes:

- Store KPIs: Sales, inventory turnover, stockouts  
- Customer KPIs: Future spend, loyalty, discount sensitivity  
- Product KPIs: Top sellers, inventory coverage  
- Tech: *Streamlit*

---

## Tech Stack
Python (Pandas, NumPy, Scikit-Learn)
Visualization: Matplotlib, Seaborn, Plotly  
Dashboard tools: Streamlit  

