import pandas as pd 
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# --- Data Loading ---
sales_df = pd.read_csv(r"C:\Users\bansa\Downloads\sales_20k_final_FINAL.csv")
inventory_df = pd.read_csv(r"C:\Users\bansa\Downloads\inventory_2021_2023_monthly.csv")
customers_simple_ids = pd.read_csv(r"C:\Users\bansa\Downloads\customers_simple_ids.csv")
products_df = pd.read_csv(r"C:\Users\bansa\Downloads\real_products_100.csv")

# --- Step 1: Feature Engineering ---

# 1a. Calculate Total Spend and Identify Top 10 Sellers
sales_df['total_spend'] = sales_df['quantity'] * sales_df['price'] * (1 - sales_df['discount'] / 100)
top_products_sales = sales_df.groupby('product_id')['quantity'].sum().nlargest(10).reset_index()
TOP_PRODUCT_IDS = top_products_sales['product_id'].tolist() # [77, 40, 33, 66, 46, 26, 69, 24, 75, 95]

# 1b. Identify High Inventory Risk Products among Top Sellers (Bottom 30% stock)
inventory_top_sellers = inventory_df[inventory_df['product_id'].isin(TOP_PRODUCT_IDS)]
avg_stock_top_sellers = inventory_top_sellers.groupby('product_id')['closing_stock'].mean().reset_index()
stock_low_threshold = avg_stock_top_sellers['closing_stock'].quantile(0.3)

HIGH_RISK_TOP_SELLER_IDS = avg_stock_top_sellers[
    avg_stock_top_sellers['closing_stock'] <= stock_low_threshold
]['product_id'].tolist()
# This yields IDs: [24, 66, 77] (Maida, Cooking Oil, Pasta)

# 1c. Calculate Customer Features
sales_target = sales_df[sales_df['product_id'].isin(TOP_PRODUCT_IDS)].copy()
sales_frustration = sales_df[sales_df['product_id'].isin(HIGH_RISK_TOP_SELLER_IDS)].copy()

# Feature 1: Total Spend on Top 10 Products
customer_spend = sales_target.groupby('customer_id')['total_spend'].sum().reset_index()
customer_spend.rename(columns={'total_spend': 'Total_Top_Spend'}, inplace=True)

# Feature 2: Quantity Purchased of High-Risk Top Seller Items (Frustration)
customer_frustration = sales_frustration.groupby('customer_id')['quantity'].sum().reset_index()
customer_frustration.rename(columns={'quantity': 'Qty_High_Risk_Purchased'}, inplace=True)

# Feature 3: Spending Frequency on Top 10 Products
sales_target['sale_date_only'] = pd.to_datetime(sales_target['sale_date']).dt.date
customer_frequency = sales_target.groupby('customer_id')['sale_date_only'].nunique().reset_index()
customer_frequency.rename(columns={'sale_date_only': 'Top_Product_Frequency'}, inplace=True)

# Merge features
customer_features = customer_spend.merge(customer_frustration, on='customer_id', how='outer')
customer_features = customer_features.merge(customer_frequency, on='customer_id', how='outer').fillna(0)

# --- Step 2: Clustering (K-Means) ---

# Prepare data
X = customer_features[['Total_Top_Spend', 'Qty_High_Risk_Purchased', 'Top_Product_Frequency']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit K-Means (Optimal K was found to be 4)
K_OPTIMAL = 4
kmeans_model = KMeans(n_clusters=K_OPTIMAL, random_state=42, n_init=10)
customer_features['Cluster'] = kmeans_model.fit_predict(X_scaled)

# --- Step 3: Identification of Target Customers (Cluster Analysis) ---

# Find Centroids (Unscaled for interpretation)
centroids_scaled = kmeans_model.cluster_centers_
centroids_original = scaler.inverse_transform(centroids_scaled)
centroids_df = pd.DataFrame(centroids_original, columns=X.columns)

# Based on centroid analysis (executed previously):
# The cluster with the highest Total_Top_Spend AND Qty_High_Risk_Purchased is Cluster 3.
# Cluster 3: Avg Spend ~2865, Avg High-Risk Qty ~5.76
TARGET_CLUSTER = 3

# Filter the Target Customers
target_customers = customer_features[customer_features['Cluster'] == TARGET_CLUSTER].copy()

# Merge with Loyalty Tier for description
#target_customers = target_customers.merge(
#    customers_simple_ids[['customer_id', 'loyalty_tier']],
#    on='customer_id',
#    how='left'
#)
# Merge with Loyalty Tier for description
target_customers = target_customers.merge(
    customers_simple_ids[['customer_id', 'loyalty_tier']],
    on='customer_id',
    how='left'
)

# Remove Bronze customers
target_customers = target_customers[target_customers['loyalty_tier'] != 'Bronze']

# Final output
#final_customer_list = target_customers[['customer_id', 'loyalty_tier', 'Total_Top_Spend', 'Qty_High_Risk_Purchased', 'Top_Product_Frequency']]
#final_customer_list = final_customer_list.sort_values(by='Total_Top_Spend', ascending=False)

# The full list of target customer IDs is saved to a CSV file.
#final_customer_list.to_csv("target_customers_cluster3.csv", index=False)


#df = pd.read_csv(r"C:\Users\bansa\target_customers_cluster3.csv")
#df.head()
# Final output
final_customer_list = target_customers[['customer_id', 'loyalty_tier', 'Total_Top_Spend', 
                                        'Qty_High_Risk_Purchased', 'Top_Product_Frequency']]
final_customer_list = final_customer_list.sort_values(by='Total_Top_Spend', ascending=False)

# ⭐ FILTER: Only customers who will increase spending when inventory improves
final_customer_list = final_customer_list[final_customer_list['Qty_High_Risk_Purchased'] > 0]

print(final_customer_list.head())