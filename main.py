import pandas as pd
import csv
import os
import tkinter as tk
from tkinter import Listbox, Toplevel, messagebox, Scrollbar, Canvas, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data_processing import load_and_preprocess, analyze_data, analyze_stock_levels, verify_password, users
from plotting import create_figures

# GUI Color Scheme and Fonts
BACKGROUND_COLOR = "#f5f5f5"
BUTTON_COLOR = "#0078d7"
TEXT_COLOR = "#ffffff"
FONT = ("Arial", 12)
LARGE_FONT = ("Arial", 14, "bold")

def display_basic_statistics(data):
    statistics = data.describe()
    return statistics

# Function to create a window for visualizations with scroll functionality
def create_visualization_window(figures):
    window = Toplevel()
    window.title("Visualizations")

    # Create a canvas with a scrollbar
    canvas = Canvas(window)
    scrollbar = Scrollbar(window, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Placing the scrollbar in the window
    scrollbar.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)

    # Create a frame inside the canvas which will be scrolled with the scrollbar
    scrollable_frame = Frame(canvas)

    # Clear old figures before drawing new ones
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    for fig in figures:
        figure_canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
        figure_canvas_widget = figure_canvas.get_tk_widget()
        figure_canvas_widget.pack(fill='both', expand=True)
        figure_canvas.draw()

    # Add the scrollable frame to a window in the canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

    # Bind the scrollable frame to the scroll region
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Back button to close the visualization window
    back_button = tk.Button(scrollable_frame, text="Back", command=window.destroy)
    back_button.pack()

# Function to create the main GUI window

def login(user_entry, pass_entry, sales_trends, monthly_sales, monthly_seasonality, on_demand_vs_regular, product_stock, material_stock):
    username = user_entry.get()
    password = pass_entry.get()
    if username in users and verify_password(users[username], password):
        messagebox.showinfo("Login Success", "You have successfully logged in.")
        # Proceed to main application window
        create_gui(sales_trends, monthly_sales, monthly_seasonality, on_demand_vs_regular, product_stock, material_stock)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")


def create_login_window():
    def on_login():
        username = user_entry.get()
        password = pass_entry.get()
        if username in users and verify_password(users[username], password):
            login_window.destroy()  # Close the login window
            create_gui(sales_trends, monthly_sales, monthly_seasonality, on_demand_vs_regular, product_stock, material_stock)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.configure(bg=BACKGROUND_COLOR)  # Set the background color for the login window

    # Username Frame
    username_frame = tk.Frame(login_window, bg=BACKGROUND_COLOR)
    username_frame.pack(fill='x', padx=20, pady=5)
    username_label = tk.Label(username_frame, text="Username", bg=BACKGROUND_COLOR, font=FONT)
    username_label.pack(side='left', padx=10)
    user_entry = tk.Entry(username_frame, font=FONT)
    user_entry.pack(side='right', expand=True, fill='x', padx=10)

    # Password Frame
    password_frame = tk.Frame(login_window, bg=BACKGROUND_COLOR)
    password_frame.pack(fill='x', padx=20, pady=5)
    password_label = tk.Label(password_frame, text="Password", bg=BACKGROUND_COLOR, font=FONT)
    password_label.pack(side='left', padx=10)
    pass_entry = tk.Entry(password_frame, show="*", font=FONT)
    pass_entry.pack(side='right', expand=True, fill='x', padx=10)

    # Login Button
    login_button = tk.Button(login_window, text="Login", command=on_login, bg=BUTTON_COLOR, fg=TEXT_COLOR, font=LARGE_FONT)
    login_button.pack(pady=20)

    login_window.mainloop()

    
def initialize_inventory():
    global inventory_data
    inventory_file = 'inventory.csv'
    if not os.path.exists(inventory_file):
        inventory_data = [
            {"Item Name": "Item A", "Quantity": 100, "Reorder Level": 20},
            {"Item Name": "Item B", "Quantity": 50, "Reorder Level": 10},
            {"Item Name": "Item C", "Quantity": 75, "Reorder Level": 15}
        ]
        with open(inventory_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Item Name", "Quantity", "Reorder Level"])
            writer.writeheader()
            writer.writerows(inventory_data)
        print("Inventory CSV file created successfully.")
    else:
        print("Inventory CSV file already exists.")

def load_inventory_data():
    global inventory_data
    inventory_file = 'inventory.csv'
    try:
        return pd.read_csv(inventory_file)
    except FileNotFoundError:
        print("Inventory file not found. Creating an empty DataFrame.")
        return pd.DataFrame(columns=["Item Name", "Quantity", "Reorder Level"])

def save_inventory_data(df):
    global inventory_data
    inventory_file = 'inventory.csv'
    df.to_csv(inventory_file, index=False)
    print("Inventory data saved successfully.")

def add_item_to_inventory(df, item_name, quantity, reorder_level):
    if item_name not in df['Item Name'].values:
        new_row = pd.DataFrame([[item_name, quantity, reorder_level]], columns=['Item Name', 'Quantity', 'Reorder Level'])
        df = pd.concat([df, new_row], ignore_index=True)
        print(f"Item '{item_name}' added to inventory.")
    else:
        print(f"Item '{item_name}' already exists in inventory.")
    return df

def update_inventory_item(df, item_name, new_quantity):
    if item_name in df['Item Name'].values:
        df.loc[df['Item Name'] == item_name, 'Quantity'] = new_quantity
        print(f"Item '{item_name}' updated in inventory.")
    else:
        print(f"Item '{item_name}' not found in inventory.")
    return df

def remove_item_from_inventory(df, item_name):
    if item_name in df['Item Name'].values:
        df = df[df['Item Name'] != item_name]
        print(f"Item '{item_name}' removed from inventory.")
    else:
        print(f"Item '{item_name}' not found in inventory.")
    return df

def refresh_inventory_display(inventory_listbox, inventory_data):
    inventory_listbox.delete(0, tk.END)  # Clear the current list
    for index, row in inventory_data.iterrows():
        inventory_listbox.insert(tk.END, f"{row['Item Name']} - Qty: {row['Quantity']} - Reorder Level: {row['Reorder Level']}")
        
def reset_inventory_from_product_data(inventory_listbox):
    global inventory_data
    confirmation = messagebox.askyesno("Reset Inventory Confirmation", "Are you sure you want to reset the inventory?")
    if confirmation:
        try:
            # Load product data
            product_data = pd.read_csv('product_data.csv')

            # Transform product data to match inventory format
            reset_inventory = pd.DataFrame({
                "Item Name": product_data['sku'],
                "Quantity": product_data['stock'],
                "Reorder Level": 0  # Setting reorder level to 0 for all items
            })
            # Save the transformed data to Inventory CSV
            save_inventory_data(reset_inventory)

            # Update the inventory data variable
            inventory_data = reset_inventory.copy()

            # Refresh display
            refresh_inventory_display(inventory_listbox, inventory_data)  # This line is updated

            messagebox.showinfo("Reset Successful", "Inventory has been reset with product data.")

        except Exception as e:
            messagebox.showerror("Reset Error", str(e))


def show_statistics():
    try:
        data = pd.read_csv('sales_data.csv')  # Adjust the path and DataFrame as needed
        stats = display_basic_statistics(data)
        messagebox.showinfo("Sales Statistics", str(stats))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_statistics2():
    try:
        data2 = pd.read_csv('mat_data.csv')  # Adjust the path and DataFrame as needed
        stats2 = display_basic_statistics(data2)
        messagebox.showinfo("Material Statistics", str(stats2))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_inventory_management_panel():
    global inventory_data
    inventory_window = Toplevel()
    inventory_window.title("Inventory Management")

    tk.Label(inventory_window, text="Item Name").pack()
    item_name_entry = tk.Entry(inventory_window)
    item_name_entry.pack()

    tk.Label(inventory_window, text="Quantity").pack()
    quantity_entry = tk.Entry(inventory_window)
    quantity_entry.pack()

    tk.Label(inventory_window, text="Reorder Level").pack()
    reorder_level_entry = tk.Entry(inventory_window)
    reorder_level_entry.pack()

    inventory_listbox = tk.Listbox(inventory_window)
    inventory_listbox.pack()
    inventory_data = load_inventory_data()
    refresh_inventory_display(inventory_listbox, inventory_data)

    initialize_inventory()
    def add_item():
        global inventory_data
        try:
            item_name = item_name_entry.get().strip()
            quantity_str = quantity_entry.get().strip()
            reorder_level_str = reorder_level_entry.get().strip()

            if not item_name:
                raise ValueError("Item name cannot be empty.")

            if not quantity_str.isdigit() or not reorder_level_str.isdigit():
                raise ValueError("Quantity and reorder level must be integers.")

            quantity = int(quantity_str)
            reorder_level = int(reorder_level_str)

            if quantity < 0 or reorder_level < 0:
                raise ValueError("Quantity and reorder level must be non-negative.")

            inventory_data = add_item_to_inventory(inventory_data, item_name, quantity, reorder_level)
            refresh_inventory_display(inventory_listbox, inventory_data)
            save_inventory_data(inventory_data)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def update_item():
        global inventory_data  # Access the global inventory_data
        item_name = item_name_entry.get()
        new_quantity = int(quantity_entry.get())
        inventory_data = update_inventory_item(inventory_data, item_name, new_quantity)
        refresh_inventory_display(inventory_listbox, inventory_data)
        save_inventory_data(inventory_data)

    def remove_item():
        global inventory_data
        item_name = item_name_entry.get()
        inventory_data = remove_item_from_inventory(inventory_data, item_name)
        refresh_inventory_display(inventory_listbox, inventory_data)
        save_inventory_data(inventory_data)
    
    def on_listbox_select(event):
        global index
        w = event.widget
        if w.curselection():
            index = int(w.curselection()[0])
        value = w.get(index)
        try:
            item_name, rest = value.split(" - Qty: ")
            quantity_str, reorder_level_str = rest.split(" - Reorder Level: ")
            quantity = int(quantity_str)
            reorder_level = int(reorder_level_str)

            item_name_entry.delete(0, tk.END)
            item_name_entry.insert(0, item_name)
            quantity_entry.delete(0, tk.END)
            quantity_entry.insert(0, quantity)
            reorder_level_entry.delete(0, tk.END)
            reorder_level_entry.insert(0, reorder_level)
        except ValueError:
            messagebox.showerror("Selection Error", "Error in parsing the selected item.")


    inventory_listbox.bind('<<ListboxSelect>>', on_listbox_select)
    button_width = 20  # Width in characters

    remove_button = tk.Button(inventory_window, text="Remove Item", command=remove_item)
    remove_button.pack()

    add_button = tk.Button(inventory_window, text="Add Item", command=add_item)
    add_button.pack()

    update_button = tk.Button(inventory_window, text="Update Item", command=update_item)
    update_button.pack()

    reset_button = tk.Button(inventory_window, text="Reset Inventory", command=lambda: reset_inventory_from_product_data(inventory_listbox), bg=BUTTON_COLOR, fg=TEXT_COLOR, font=LARGE_FONT, width=button_width)
    reset_button.pack(pady=5)


def create_gui(sales_trends, monthly_sales, monthly_seasonality, on_demand_vs_regular, product_stock, material_stock):
    root = tk.Tk()
    root.title("Inventory Management System")
    root.state('zoomed')  # For Windows to start maximized
    # root.attributes('-fullscreen', True)  # Uncomment this line for Linux or macOS

    root.configure(bg=BACKGROUND_COLOR)  # Set the background color for the main window

    figures = create_figures(sales_trends, monthly_sales, monthly_seasonality, on_demand_vs_regular, product_stock, material_stock)
    # Dropdown for selecting month or resetting
    months = ['All'] + list(range(1, 13))  # Adding 'All' to the list
    selected_month = tk.StringVar(root)
    selected_month.set('All')  # default value to 'All'
    month_dropdown = tk.OptionMenu(root, selected_month, *months)
    month_dropdown.pack()

    def update_plots():
        selected_month_value = selected_month.get()
        figures = create_figures(sales_trends, monthly_sales, monthly_seasonality, on_demand_vs_regular, product_stock, material_stock, selected_month_value)
        create_visualization_window(figures)

    update_button = tk.Button(root, text="Update Plots", command=update_plots, bg=BUTTON_COLOR, fg=TEXT_COLOR, font=LARGE_FONT)
    update_button.pack(pady=10)

    plots_button = tk.Button(root, text="Plots and Graphs", command=lambda: create_visualization_window(figures), bg=BUTTON_COLOR, fg=TEXT_COLOR, font=LARGE_FONT)
    plots_button.pack(pady=10)

    inventory_button = tk.Button(root, text="Inventory Management", command=create_inventory_management_panel, bg=BUTTON_COLOR, fg=TEXT_COLOR, font=LARGE_FONT)
    inventory_button.pack(pady=10)

    logout_button = tk.Button(root, text="Log Out", command=root.destroy, bg=BUTTON_COLOR, fg=TEXT_COLOR, font=LARGE_FONT)
    logout_button.pack(pady=10)

    stats_frame = tk.Frame(root, bg=BACKGROUND_COLOR, pady=5)
    stats_frame.pack(fill='x')  # fill='x' makes the frame fill the entire width of the window

    stats_button = tk.Button(stats_frame, text="Sales Statistics", command=show_statistics, bg=BUTTON_COLOR, fg=TEXT_COLOR, font=LARGE_FONT, width=20)
    stats_button.pack(side='left', padx=10)  # side='left' aligns the button to the left

    stats2_button = tk.Button(stats_frame, text="Material Statistics", command=show_statistics2, bg=BUTTON_COLOR, fg=TEXT_COLOR, font=LARGE_FONT, width=20)
    stats2_button.pack(side='left', padx=10)  # side='left' aligns the button to the left


    root.mainloop()

# Main function to run the project
def main():
    global inventory_data
    initialize_inventory()
    inventory_data = load_inventory_data()
    save_inventory_data(inventory_data)
    product_data, mat_data, sales_data = load_and_preprocess()
    sales_trends, monthly_sales, monthly_seasonality, on_demand_vs_regular = analyze_data(product_data, mat_data, sales_data)
    product_stock, material_stock = analyze_stock_levels(product_data, mat_data)
    create_gui(sales_trends, monthly_sales, monthly_seasonality, on_demand_vs_regular, product_stock, material_stock)

if __name__ == "__main__":
    product_data, mat_data, sales_data = load_and_preprocess()
    sales_trends, monthly_sales, monthly_seasonality, on_demand_vs_regular = analyze_data(product_data, mat_data, sales_data)
    product_stock, material_stock = analyze_stock_levels(product_data, mat_data)
    create_login_window()