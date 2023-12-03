Inventory-and-Data-Analysis-System
This is the submission for the Final Project of MFG 598 for myself, Sahil Mahesh Shah.

OVERVIEW
--------
Inventory Management and Data Analysis System
This project is designed to manage inventory and perform data analysis for a manufacturing industry or a warehouse setting. It includes functionalities for password-protected user access, inventory management, and statistical analysis of sales and product data. The system is built using Python and is intended for users who need an efficient way to manage stock levels and analyze sales trends.


INSTALLATION AND SETUP REQUIREMENTS
-----------------------------------
Python 3.6 or higher
Libraries: pandas, matplotlib (for data processing and plotting)


INSTALLATION INSTRUCTIONS
-------------------------
Clone the repository: git clone https://github.com/sahilmshah/inventory-and-data-analysis-system.git
Navigate to the project directory: cd inventory-management-system
Install required dependencies: pip install -r requirements.txt


USAGE
-----
To use this system, run main.py. This will start the user interface where you can log in, manage inventory, and view statistical analyses of your data.
You will need credentials to log-in. Use the following, Username: "admin" ; Password: "password" .

FUNCTION DESCRIPTIONS
---------------------

In data_processing.py

hash_password: Hashes a password for secure storage.
verify_password: Verifies a provided password against a stored hash.
load_and_preprocess: Loads CSV data files and preprocesses them for analysis.
analyze_data: Performs general data analysis on sales data.
analyze_stock_levels: Analyzes current stock levels against sales trends.
display_basic_statistics: Displays basic statistics such as mean, median, etc., from the data.

In main.py

display_basic_statistics: Displays basic statistics (similar to data_processing.py).
create_visualization_window: Initiates a window for data visualization.
login: Handles user login functionality.
create_login_window: Creates the GUI for user login.
initialize_inventory: Initializes inventory data structures.
load_inventory_data: Loads inventory data from a file.
save_inventory_data: Saves current inventory data to a file.
add_item_to_inventory: Adds a new item to the inventory.
update_inventory_item: Updates details of an existing inventory item.
remove_item_from_inventory: Removes an item from the inventory.
refresh_inventory_display: Updates the inventory display in the GUI.
reset_inventory_from_product_data: Resets inventory data based on a separate product data file.
show_statistics: Shows various statistics about the inventory.
show_statistics2: Another function for displaying different statistics.
create_inventory_management_panel: Creates the main panel for inventory management in the GUI.
create_gui: Builds the entire graphical user interface for the application.
main: The main entry point of the application.

In plotting.py

create_figures: Generates graphical figures (e.g., charts, graphs) for data visualization.
