# Food Log Application
The Food Log Application is a TkInter-based application designed to help users log and track their daily food intake. This repository contains the source code for the application, which is primarily implemented in Python using the TkInter library for the GUI.

## Table of Contents

- [API Key Setup](#api-key-setup)
- [Installation](#installation)
- [Usage](#usage)
- [Main Application](#main-application)
- [Functions and Methods](#functions-and-methods)
- [Contributing](#contributing)
- [License](#license)

## API Key Setup

To use the Edamam food database API, you need to obtain an API key and application ID:

1. Sign up for an API key and application ID at the [Edamam Developer Portal](https://developer.edamam.com/).
2. Create a file named `api_keys.py` in the project directory and add your API key and application ID in the following format:
> [!IMPORTANT]
> An API key file is required to return results from the application.

 ```python
  EDAMAM_APP_ID = 'your_app_id_here'
  EDAMAM_APP_KEY = 'your_api_key_here'
``` 
4. Save the file.

## Installation

To install and run the Food Log Application, follow these steps:

1. Clone the repository:
 ```bash
    git clone https://github.com/jocelyngilbertson/foodlogapp.git
 ``` 
2. Navigate to the project directory:
 ```bash
    cd foodlogapp
 ``` 
3. Install the required dependencies using the file ```Package Installation.py``` or 
 ```python
  import subprocess
  import sys
   
  def install(package):
      subprocess.check_call([sys.executable, "-m", "pip", "install", package])
   
  # Install packages
  install("opencv-python")
  install("pyzbar")
  install("requests")
  install ("ttkbootstrap")
``` 
## Usage

To run the application, execute the following command:

```bash
python run_TkInter.py
``` 

## Main Application

The main application logic is contained within the `run_TkInter.py` file. Below is an overview of its structure and key components:

### `run_TkInter.py`

This is the entry point of the application. It initializes the TkInter GUI and handles user interactions. The key components include:

-   **Initialization**: Sets up the main window and its properties.
-   **Widgets**: Defines and places widgets such as labels, entry fields, buttons, and listboxes.
-   **Event Handling**: Contains functions to handle events like button clicks and listbox selections.
-   **Data Management**: Includes functions to manage food log entries, such as adding, editing, and deleting entries.

```python
# Example snippet from run_TkInter.py
import tkinter as tk
from tkinter import messagebox

def main():
    root = tk.Tk()
    app = FoodLogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
``` 

## Functions and Methods

Here's a detailed list of the key functions and methods in `run_TkInter.py`:

### Initialization and Setup

-   `__init__(self, root)`: Initializes the main application window and its widgets.
    -   **UI Elements**: Sets up the main window with input fields for food name, calories, and date, as well as buttons for adding, editing, and deleting entries, and a listbox for displaying the food log.
        

### Data Management

-   `create_table`: Creats a table for the food log.
    
    -   **Description**: Stores the input from the entry fields of the food log.

-   `setup_widgets`: Sets application structure.
    
    -   **Description**: Sets up the tkinter grid structure with labels fields and buttons.

-   `preview_camera`: Sets up and initalizes the camera function.
    
    -   **Description**: Sets up the application to pull back the provided camera for barcode scanning.
  
-   `lookup_food`: Send the API request to have the food returned with servings from EDAMAM.
    
    -   **Parameters**: Barcode
    -   **Returns**: JSON of the food and its servings
    -   **Description**: Retrieves the information from the API and appends it to the appropriate text fields.
        
-   `log_food`: Adds a food entry.
    
    -   **Parameters**: Food Name, Serving, Barcode
    -   **Description**: Adds the selected food entry based on the user's input in the entry fields.
    -   **UI Interaction**: When the user selects an entry from the listbox, edits the details, and clicks the "Log Food" button.
        
-   `remove_item`: Deletes a selected food entry.

    -   **Description**: Removes the selected entry from the food log.
    -   **UI Interaction**: When the user selects an entry from the listbox and clicks the "Remove Selected Item" button.

-   `autocomplete_food_name`: returns a lits of food names (must have 3 or more characters).
  
    -   **Parameters**: Food Name
    -   **Returns**: JSON of the food name listing from EDAMAM
    -   **Description**: Removes the disabled state of the button.

-   `enable_lookup_button`: enables the Lookup Barcode Butoon.
    
    -   **Description**: Removes the disabled state of the button.
        
-   `export_all_to_file(self)`: Saves the food log to a file.
    
    -   **Description**: Writes the current food log to a specified file for persistent storage.
    -   **UI Interaction**: When the user clicks the "Save" button.
            
-   `load_entries`: Loads the food log from a file.
    
    -   **Description**: Reads a previously saved food log from a specified file.
    -   **UI Interaction**: When the user clicks the "Load" button.        
        
## Contributing

Contributions are welcome! To contribute to the project, follow these steps:

1.  Fork the repository.
2.  Create a new branch:
    
```bash
    `git checkout -b feature-branch`
```
    
3.  Make your changes.
4.  Commit your changes:
    
```bash
    `git commit -m "Description of your changes"`
```
    
5.  Push to the branch:
    
```bash
    `git push origin feature-branch`
```
    
6.  Create a pull request.

Please ensure your code follows the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
