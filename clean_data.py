import pandas as pd

print("Starting data cleaning process...")

# 1. Load raw data
df = pd.read_excel("data/Online Retail.xlsx")
print(f"Original Data - Rows: {len(df)}")

# 2. Inspect cancellations
is_cancelled = df["InvoiceNo"].astype(str).str.startswith("C")
cancelled_df = df[is_cancelled]
normal_df = df[~is_cancelled]

num_cancelled = len(cancelled_df)
num_normal = len(normal_df)
cancelled_revenue = (cancelled_df["Quantity"] * cancelled_df["UnitPrice"]).sum()

print(f"Number of cancelled transactions: {num_cancelled}")
print(f"Number of normal transactions: {num_normal}")
print(f"Revenue associated with cancellations: {cancelled_revenue}")

# 3. Clean the data
# We keep only normal transactions
df_cleaned = normal_df.copy()

# Remove invalid prices and quantities
df_cleaned = df_cleaned[df_cleaned["UnitPrice"] > 0]
df_cleaned = df_cleaned[df_cleaned["Quantity"] > 0]

# Remove duplicates
duplicates_count = df_cleaned.duplicated().sum()
print(f"Duplicates removed: {duplicates_count}")
df_cleaned = df_cleaned.drop_duplicates()

# Missing values info
print(f"Missing CustomerIDs: {df_cleaned['CustomerID'].isnull().sum()}")
print("Keeping missing CustomerIDs because we can still analyze revenue without them.")

# 4. Create calculated column
df_cleaned["Revenue"] = df_cleaned["Quantity"] * df_cleaned["UnitPrice"]

# Extract Date parts
df_cleaned["InvoiceDate"] = pd.to_datetime(df_cleaned["InvoiceDate"])
df_cleaned["YearMonth"] = df_cleaned["InvoiceDate"].dt.to_period("M").astype(str)

print(f"Cleaned Data - Rows: {len(df_cleaned)}")

# 5. Save to CSV
df_cleaned.to_csv("data/cleaned_online_retail.csv", index=False)
print("Saved cleaned data to data/cleaned_online_retail.csv")
