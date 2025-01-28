import pyautogui
import time
import keyboard
import subprocess
import sys

# Function to install required modules
def install(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install required modules
install("pyautogui")
install("keyboard")

# Define center coordinates
pixelX = 1198
pixelY = 971
searchRadius = 25  # Search within 50 pixels around the center coordinates
orangeColor = (255, 107, 17)  # RGB value for 0xFF6B11
tolerance = 6  # Allow slight variations in color

# Toggle variable
toggle = False

# Function to check if a color is within tolerance
def color_match(color, target_color, tolerance):
    return all(abs(c - t) <= tolerance for c, t in zip(color, target_color))

# Toggle on/off with F8
def toggle_script():
    global toggle
    toggle = not toggle
    if toggle:
        print("Script is ON")
    else:
        print("Script is OFF")

# Register F8 as the toggle hotkey
keyboard.add_hotkey('F8', toggle_script)

try:
    while True:
        # Only run if the toggle is ON
        if toggle:
            # Search for the color within the specified radius
            found = False
            for x in range(pixelX - searchRadius, pixelX + searchRadius + 1):
                for y in range(pixelY - searchRadius, pixelY + searchRadius + 1):
                    # Get the current pixel color
                    color = pyautogui.pixel(x, y)

                    # Debugging: Print the color and coordinates
                    print(f"Color: {color} at X: {x} Y: {y}")

                    # Check if the color matches within tolerance
                    if color_match(color, orangeColor, tolerance):
                        found = True
                        foundX = x
                        foundY = y
                        break  # Exit the inner loop if the color is found
                if found:
                    break  # Exit the outer loop if the color is found

            # If the color is found, perform the action
            if found:
                print("Orange detected! Clicking...")
                pyautogui.moveTo(foundX, foundY)  # Move mouse to the found location
                time.sleep(0.05)  # Short delay to ensure click registers
                pyautogui.click()  # Perform the click
                time.sleep(22)  # Wait 22 seconds
            else:
                print("Searching for orange...")

            # Small delay to reduce CPU usage
            time.sleep(0.1)
        else:
            # If the toggle is OFF, sleep briefly to reduce CPU usage
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Script exited.")