import subprocess
import sys
 
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
 
# Install packages
install("opencv-python")
install("pyzbar")
install("requests")
install ("ttkbootstrap")