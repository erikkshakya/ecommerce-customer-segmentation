import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

db_password = 'admin123'
db_name = 'ecommerce_db'
db_user = 'postgres'
db_host = 'localhost'
db_port = 5432

print("Connecting to database.....")
connection_str = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_str)

df = pd.read_sql("SELECT * from customer_rfm", engine)
print(f"Data loaded: {df.shape[0]} rows.")
print(f"Data loaded: {df.head(10)}")

# Scaling
features = ['recency', 'frequency', 'monetary']
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[features])
print(df_scaled)

# K means clustering
print("Running K-Means clustering...")
kmeans = KMeans(n_clusters=4, random_state=42)
df['cluster'] = kmeans.fit_predict(df_scaled)
# print(f"{df.head(10)}")

# Analyse the cluster
summary = df.groupby('cluster')[features].mean().reset_index()
print("\n Cluster Summary")
print(summary)

# Visualization
plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x='recency', y='monetary', hue='cluster', palette='viridis', alpha=0.6)
plt.title('Customer Segments: Recency vs Monetary')
plt.ylim(0, 1000) # Limit y-axis to see the main groups clearly (ignore super-whales)
plt.savefig('cluster_plot.png')

df.to_csv('final_customer_segments.csv', index=False)
print("\n✅ Success! File 'final_customer_segments.csv' saved.")
