# Food Log Application - User Guide 
Hello! Thanks for downloading my food log app. The main goal of this project is to provide an application that allows you to scan barcodes of food you eat to keep track of it and see the various pieces of information about the food.

## INSTALLING
First, download the app and the various files that come with it. You’ll have to install a package first for the application to be able to run properly. Once you’ve installed these and the project itself, get ready to run the application by launching it in VSCode.
Install the required dependencies using the file ```Package Installation.py``` or 
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
To use the Edamam food database API, you need to obtain an API key and application ID:

1. Sign up for a free API key and application ID at the [Edamam Developer Portal](https://developer.edamam.com/).
2. Create a file named `api_keys.py` in the project directory and add your API key and application ID in the following format:
> [!IMPORTANT]
> An API key file is required to return results from the application.

 ```python
  EDAMAM_APP_ID = 'your_app_id_here'
  EDAMAM_APP_KEY = 'your_api_key_here'
``` 
4. Save the file.

## LAUNCHING THE APPLICATION
The application's goal is to make logging your food easier and to use less cognitive load by not having to keep track of what you eat by memory alone. To use it properly, be sure to do the following first:
- **Barcode**: Have a clear barcode ready to scan (or have the foods packaging on hand to reference back to)
- **Camera**: Have a working camera 
- **Installs**: Have the app open and running with all installs done
Next, do the following:
- **Launch**: Launch the barcode scanner by pressing the run or “play” button in VSCode
- **Permissions**: Allow access to your camera when prompted
- **Get started**: Begin to either type the name of the food, or hold the food item with the barcode facing the camera to scan it to begin using it 

## USING THE APPLICATION
The app has multifaceted options for use cases. For example, upon running the application, the camera will be off by default. If you’d like to turn it on, click “scan barcode.” This will launch your camera. Next, hold the barcode up to the camera. This will scan the barcode and the UPC number will automatically enter into the text field. If you’d like (or if the barcode scanner doesn’t work), you can type in the UPC code manually. Additionally, you can start to type the food name in the text field and you will see food names beginning to auto populate. If you see the food in the autocomplete list, simply click it. If not, continue to type it out until it’s complete. 
Next, now that you have your food inputted, click `log food.`

## CREDITS
Credits go to Edamam Food Database API.
