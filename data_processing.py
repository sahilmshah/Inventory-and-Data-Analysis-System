import pandas as pd
import hashlib

# User credentials (simulating a database)
users = {
    "admin": hashlib.sha256("password".encode()).hexdigest()  #username is 'admin' and password is 'password'
}

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user."""
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

# Function to load and preprocess data
def load_and_preprocess():
    product_data = pd.read_csv('product_data.csv')
    mat_data = pd.read_csv('mat_data.csv')
    sales_data = pd.read_csv('sales_data.csv')

    # Reshaping sales data to a long format for easier analysis
    sales_data_long = sales_data.melt(id_vars=['sku', 'name'], 
                                      var_name='date_sale', 
                                      value_name='quantity')
    sales_data_long['date_sale'] = pd.to_datetime(sales_data_long['date_sale'], format='%m/%Y')

    return product_data, mat_data, sales_data_long

# Function for data analysis
def analyze_data(product_data, mat_data, sales_data):
    # Extracting month from the date for seasonality analysis
    sales_data['month'] = sales_data['date_sale'].dt.month

    # Sales analysis
    sales_trends = sales_data.groupby('date_sale')['quantity'].sum().reset_index()
    monthly_sales = sales_data.groupby(sales_data['date_sale'].dt.strftime('%Y-%m'))['quantity'].sum().reset_index(name='quantity')
    monthly_seasonality = sales_data.groupby('month')['quantity'].mean().reset_index(name='quantity')

    # Comparison of on demand vs regular products in terms of sales
    on_demand_vs_regular = product_data.groupby('on_demand')['name'].count().reset_index(name='count')

    return sales_trends, monthly_sales, monthly_seasonality, on_demand_vs_regular

# Function to analyze inventory stock levels
def analyze_stock_levels(product_data, mat_data):
    # Exclude on-demand products
    non_on_demand_products = product_data[product_data['on_demand'] == 'no']

    # Analyzing stock levels for non-on-demand products and materials
    product_stock = non_on_demand_products[['name', 'stock']]
    material_stock = mat_data[['name', 'stock']]

    return product_stock, material_stock

def display_basic_statistics(data):
    statistics = data.describe()
    return statistics