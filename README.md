# Hello! Thanks for downloading my food log app. The main goal of this project is to provide an application that allows you to scan barcodes of food you eat to keep track of it and see the various pieces of information about the food.

INSTALLING
First, download the app and the various files that come with it. You’ll have to install a package first for the application to be able to run properly. Once you’ve installed these and the project itself, get ready to run the application by launching it in VSCode.
Run the package installation file first (get this from the github folder): “Package Installation.py”
A key part to this is having your own API keys. Go to this link: https://developer.edamam.com/food-database-api and create an account. You can use the free version. You will need an ID and a key to get started. To insert these keys, you will need to edit the run_TkInter.py file, and edit the API key and ID.

LAUNCHING THE APPLICATION
The application's goal is to make logging your food easier and to use less cognitive load by not having to keep track of what you eat by memory alone. To use it properly, be sure to do the following first:
Have a clear barcode ready to scan (or have the foods packaging on hand to reference back to)
Have a working camera 
Have the app open and running with all installs done
Next, do the following:
Launch the barcode scanner by pressing the run or “play” button in VSCode
Allow access to your camera when prompted
Begin to either type the name of the food, or hold the food item with the barcode facing the camera to scan it to begin using it 

USING THE APPLICATION
The app has multifaceted options for use cases. For example, upon running the application, the camera will be off by default. If you’d like to turn it on, click “scan barcode.” This will launch your camera. Next, hold the barcode up to the camera. This will scan the barcode and the UPC number will automatically enter into the text field. If you’d like (or if the barcode scanner doesn’t work), you can type in the UPC code manually. Additionally, you can start to type the food name in the text field and you will see food names beginning to auto populate. If you see the food in the autocomplete list, simply click it. If not, continue to type it out until it’s complete. 
Next, now that you have your food inputted, click ‘log food.’

CREDITS
Credits go to Edamam Food Database API.
