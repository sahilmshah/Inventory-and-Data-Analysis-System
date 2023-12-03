import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates

def create_figures(sales_trends, monthly_sales, monthly_seasonality, on_demand_vs_regular, product_stock, material_stock, selected_month=None):
    
    # Skip filtering if 'All' or 'Reset' is selected
    if selected_month not in [None, 'All', 'Reset']:
        selected_month_value = int(selected_month)
        sales_trends = sales_trends[sales_trends['date_sale'].dt.month == selected_month_value]
        monthly_sales = monthly_sales[monthly_sales['date_sale'].dt.month == selected_month_value]

    figures = []

    # Sales trends figure with statistical annotations
    fig_sales_trends, ax = plt.subplots(figsize=(12, 6))  # Adjusted for better fit
    ax.plot(sales_trends['date_sale'], sales_trends['quantity'], label='Sales Data', color='royalblue')
    # Calculate statistical data
    mean_sales = sales_trends['quantity'].mean()
    median_sales = sales_trends['quantity'].median()
    std_dev_sales = sales_trends['quantity'].std()
    # Add statistical annotations
    ax.axhline(mean_sales, color='green', linestyle='--', label=f'Mean: {mean_sales:.2f}')
    ax.axhline(median_sales, color='red', linestyle='-.', label=f'Median: {median_sales:.2f}')
    # Add a trend line
    z = np.polyfit(mdates.date2num(sales_trends['date_sale']), sales_trends['quantity'], 1)
    p = np.poly1d(z)
    ax.plot(sales_trends['date_sale'], p(mdates.date2num(sales_trends['date_sale'])), linestyle='--', color='orange', label='Trend Line')
    # Annotations for statistical data
    ax.annotate(f'Standard Deviation: {std_dev_sales:.2f}', xy=(0.05, 0.85), xycoords='axes fraction', color='blue')
    # Improve the appearance of the plot
    ax.set_title('Sales Trends Over Time', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Quantity Sold')
    # Adjust plot layout to make space for the legend on the right
    plt.subplots_adjust(right=0.8)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.grid(True)
    # Rotate x-axis labels to prevent overlapping
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    figures.append(fig_sales_trends)
    # Close the plot to avoid displaying it in the current context
    plt.close(fig_sales_trends)

# Monthly Sales figure with statistical annotations
    fig_monthly_sales, ax = plt.subplots(figsize=(12, 6))
    # Ensure 'date_sale' is in datetime format and then format for plotting
    monthly_sales['date_sale'] = pd.to_datetime(monthly_sales['date_sale'])
    monthly_sales_formatted = monthly_sales['date_sale'].dt.strftime('%Y-%m')
    ax.bar(monthly_sales_formatted, monthly_sales['quantity'], color='skyblue')
    # Calculate statistical data
    mean_quantity = monthly_sales['quantity'].mean()
    median_quantity = monthly_sales['quantity'].median()
    # Add statistical annotations
    ax.axhline(mean_quantity, color='green', linestyle='--', label=f'Mean: {mean_quantity:.2f}')
    ax.axhline(median_quantity, color='red', linestyle='-.', label=f'Median: {median_quantity:.2f}')
    # Annotations for statistical data
    ax.annotate(f'Mean: {mean_quantity:.2f}', xy=(0.75, 0.95), xycoords='axes fraction', color='green')
    ax.annotate(f'Median: {median_quantity:.2f}', xy=(0.75, 0.90), xycoords='axes fraction', color='red')
    # Improve the appearance of the plot
    ax.set_title('Monthly Sales', fontsize=14, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Quantity Sold')
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', linewidth=0.5)
    # Rotate x-axis labels to prevent overlapping
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    # Adjust subplot parameters to give the plot more room
    plt.subplots_adjust(bottom=0.15)
    figures.append(fig_monthly_sales)
    # Close the plot to avoid displaying it in the current context
    plt.close(fig_monthly_sales)

    # Monthly Seasonality figure with financial quarter grouping
    fig_monthly_seasonality, ax = plt.subplots(figsize=(12, 6))
    # Define colors for each quarter based on the new financial year structure
    quarter_colors = ['salmon', 'skyblue', 'lightgreen', 'sandybrown']  # Colors for Q4, Q1, Q2, Q3
    # Assign colors to each month based on its quarter
    def assign_color(month):
        if month in [1, 2, 3]:    # Q4
            return quarter_colors[0]
        elif month in [4, 5, 6]:  # Q1
            return quarter_colors[1]
        elif month in [7, 8, 9]:  # Q2
            return quarter_colors[2]
        elif month in [10, 11, 12]: # Q3
            return quarter_colors[3]
    monthly_seasonality['color'] = monthly_seasonality['month'].apply(assign_color)
    # Add bars for each month, colored by quarter
    bars = ax.bar(monthly_seasonality['month'], monthly_seasonality['quantity'],
                  color=monthly_seasonality['color'])
    # Create custom labels for the legend
    custom_labels = [plt.Rectangle((0, 0), 1, 1, color=color) for color in quarter_colors]
    ax.legend(custom_labels, ['Q4', 'Q1', 'Q2', 'Q3'], title='Financial Quarters')
    # Improve the appearance of the plot
    ax.set_title('Monthly Seasonality', fontsize=14, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Average Quantity Sold')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    # Statistical annotations
    average = monthly_seasonality['quantity'].mean()
    ax.axhline(average, color='red', linestyle='--', label=f'Average: {average:.2f}')
    ax.annotate(f'Average: {average:.2f}', xy=(0.75, 0.95), xycoords='axes fraction', color='red')
    ax.grid(True, linestyle='--', linewidth=0.5)
    figures.append(fig_monthly_seasonality)
    # Close the plot to avoid displaying it in the current context
    plt.close(fig_monthly_seasonality)

     # On demand vs regular products figure with statistical annotations
    fig_on_demand_vs_regular = plt.figure(figsize=(8, 5))
    ax = fig_on_demand_vs_regular.add_subplot(111)
    on_demand_vs_regular.plot(kind='bar', ax=ax, color=['skyblue', 'salmon'])
    total_count = on_demand_vs_regular['count'].sum()
    mean_count = on_demand_vs_regular['count'].mean()
    std_dev_count = on_demand_vs_regular['count'].std()
    ax.annotate(f'Total: {total_count}', xy=(0.05, 0.9), xycoords='axes fraction', color='blue')
    ax.annotate(f'Mean: {mean_count:.2f}', xy=(0.05, 0.85), xycoords='axes fraction', color='green')
    ax.annotate(f'Std Dev: {std_dev_count:.2f}', xy=(0.05, 0.8), xycoords='axes fraction', color='red')
    plt.title('On Demand vs Regular Products', fontsize=14, fontweight='bold')
    plt.xlabel('Product Type', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks([0, 1], ['Regular', 'On Demand'], rotation=0)
    plt.grid(True, linestyle='--', linewidth=0.5)
    figures.append(fig_on_demand_vs_regular)

    # Product stock levels figure with statistical annotations
    fig_product_stock = plt.figure(figsize=(10, 6))
    ax = fig_product_stock.add_subplot(111)
    product_stock.loc[:, 'color'] = product_stock['stock'].apply(lambda x: 'green' if x > 50 else ('orange' if x > 20 else 'red'))
    unique_colors = product_stock['color'].unique().tolist()
    sns.barplot(x='name', y='stock', hue='color', data=product_stock, palette=unique_colors, dodge=False, ax=ax)
    ax.get_legend().remove()
    mean_stock = product_stock['stock'].mean()
    median_stock = product_stock['stock'].median()
    std_dev_stock = product_stock['stock'].std()
    ax.axhline(mean_stock, color='blue', linestyle='--', label=f'Mean: {mean_stock:.2f}')
    ax.axhline(median_stock, color='green', linestyle='-.', label=f'Median: {median_stock:.2f}')
    ax.annotate(f'Std Dev: {std_dev_stock:.2f}', xy=(0.7, 0.9), xycoords='axes fraction', color='red')
    plt.title('Product Stock Levels', fontsize=14, fontweight='bold')
    plt.xlabel('Product', fontsize=12)
    plt.ylabel('Stock Level', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, linestyle='--', linewidth=0.5)
    figures.append(fig_product_stock)

    # Material stock levels figure with statistical annotations
    fig_material_stock = plt.figure(figsize=(10, 6))
    ax = fig_material_stock.add_subplot(111)

    # Create a copy of the DataFrame slice to avoid SettingWithCopyWarning
    material_stock = material_stock.copy()
    material_stock['color'] = material_stock['stock'].apply(lambda x: 'green' if x > 100 else ('orange' if x > 50 else 'red'))
    unique_colors_material = material_stock['color'].unique().tolist()
    sns.barplot(x='name', y='stock', hue='color', data=material_stock, palette=unique_colors_material, dodge=False, ax=ax)
    ax.get_legend().remove()
    mean_material_stock = material_stock['stock'].mean()
    median_material_stock = material_stock['stock'].median()
    std_dev_material_stock = material_stock['stock'].std()
    ax.axhline(mean_material_stock, color='blue', linestyle='--', label=f'Mean: {mean_material_stock:.2f}')
    ax.axhline(median_material_stock, color='green', linestyle='-.', label=f'Median: {median_material_stock:.2f}')
    ax.annotate(f'Std Dev: {std_dev_material_stock:.2f}', xy=(0.7, 0.9), xycoords='axes fraction', color='red')
    plt.title('Material Stock Levels', fontsize=14, fontweight='bold')
    plt.xlabel('Material', fontsize=12)
    plt.ylabel('Stock Level', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, linestyle='--', linewidth=0.5)
    figures.append(fig_material_stock)

    return figures