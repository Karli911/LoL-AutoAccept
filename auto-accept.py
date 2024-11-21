import cv2
import numpy as np
import pyautogui
import time
import logging
import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import keyboard  # Import keyboard for hotkey functionality
import psutil


# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Global variables to control the script and store settings
is_running = False
config = {}

def load_config(config_path="config.json"):
    """Load configuration from JSON file."""
    if not os.path.exists(config_path):
        logging.error(f'Configuration file not found at path: {config_path}')
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

def find_accept_button(template_path, threshhold=0.5, region=None, debug=False):
    """Find and click the 'Accept' button."""
    try:
        # Capture the current screen or a region
        screenshot = pyautogui.screenshot(region=region)
        screenshot = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

        # Load the template of the 'Accept' button
        if not os.path.exists(template_path):
            logging.error(f'Template image not found at path: {template_path}')
            return False
    
        template = cv2.imread(template_path, 0)
        w, h = template.shape[::-1]

        # Match the template to the screenshot
        res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshhold)

        # If the button is found, click it
        if len(loc[0]) > 0:
            for pt in zip(*loc[::-1]):
                pyautogui.click(pt[0] + w/2, pt[1] + h/2)
                logging.info(f"Accept button found at {pt[0]}, {pt[1]} and clicked!")
                
                # For debugging: show where it found the button
                if debug:
                    cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
                    cv2.imshow("Matched Area", screenshot)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

                return True
        logging.info("Accept button not found.")
        return False

    except Exception as e:
        logging.error(f"Error during button search: {e}")
        return False

def start_auto_accept():
    """Start the auto accept loop."""
    global is_running, config
    retry_attempts = 0
    template_path = config['template_path']
    threshhold = config['threshhold']
    retry_interval = config['retry_interval']
    region = config.get('region', None)
    max_retries = config.get('max_retries', 10)
    debug = config.get('debug', False)

    while is_running:
        if find_accept_button(template_path, threshhold, region, debug):
            retry_attempts = 0
            print("Accept button found and clicked!")
            time.sleep(retry_interval)
        else:
            print("Accept button not found. Retrying...")
            retry_attempts += 1
            if retry_attempts > max_retries:
                logging.error("Max retries reached. Please check the application.")

            time.sleep(min(10, retry_interval * retry_attempts))

def stop_auto_accept():
    """Stop the auto accept loop."""
    global is_running
    is_running = False
    print("Auto Accept Stopped")

def start_thread():
    """Start the auto accept process in a new thread."""
    global is_running
    if not config['template_path']:
        messagebox.showerror("Error", "Please select a template image first.")
        return
    is_running = True
    threading.Thread(target=start_auto_accept).start()

def start_auto_accept_hotkey():
    """Function to start auto-accept using hotkey."""
    if not is_running:
        print("Starting auto-accept using hotkey...")
        start_thread()

def stop_auto_accept_hotkey():
    """Function to stop auto-accept using hotkey."""
    if is_running:
        print("Stopping auto-accept using hotkey...")
        stop_auto_accept()

def setup_hotkeys():
    """Setup the hotkeys for start and stop actions."""
    start_hotkey = config.get('start_hotkey', '-')  # Default hotkey for start
    stop_hotkey = config.get('stop_hotkey', '=')  # Default hotkey for stop

    # Bind hotkeys
    keyboard.add_hotkey(start_hotkey, start_auto_accept_hotkey)
    keyboard.add_hotkey(stop_hotkey, stop_auto_accept_hotkey)

    print(f"Hotkeys set: Start ({start_hotkey}), Stop ({stop_hotkey})")

def create_gui():
    """Create the GUI for configuring settings."""
    global config

    root = tk.Tk()
    root.title("Auto Accept Configuration")

    def select_template():
        config['template_path'] = filedialog.askopenfilename(title="Select Template", filetypes=[("PNG files", "*.png")])
        template_label.config(text=f"Template: {os.path.basename(config['template_path'])}")

    def start_button_pressed():
        try:
            config['threshhold'] = float(threshhold_entry.get())
            config['retry_interval'] = float(retry_interval_entry.get())
            config['max_retries'] = int(max_retries_entry.get())
            setup_hotkeys()  # Setup hotkeys when starting
            start_thread()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values.")

    # GUI layout
    template_button = tk.Button(root, text="Select Template", command=select_template)
    template_button.pack(pady=10)

    template_label = tk.Label(root, text="Template: Not Selected")
    template_label.pack(pady=5)

    threshhold_label = tk.Label(root, text="Threshold (0-1):")
    threshhold_label.pack(pady=5)
    threshhold_entry = tk.Entry(root)
    threshhold_entry.insert(0, str(config['threshhold']))
    threshhold_entry.pack(pady=5)

    retry_interval_label = tk.Label(root, text="Retry Interval (seconds):")
    retry_interval_label.pack(pady=5)
    retry_interval_entry = tk.Entry(root)
    retry_interval_entry.insert(0, str(config['retry_interval']))
    retry_interval_entry.pack(pady=5)

    max_retries_label = tk.Label(root, text="Max Retries:")
    max_retries_label.pack(pady=5)
    max_retries_entry = tk.Entry(root)
    max_retries_entry.insert(0, str(config.get('max_retries', 10)))
    max_retries_entry.pack(pady=5)

    start_button = tk.Button(root, text="Start Auto Accept", command=start_button_pressed)
    start_button.pack(pady=10)

    stop_button = tk.Button(root, text="Stop Auto Accept", command=stop_auto_accept)
    stop_button.pack(pady=10)

    root.mainloop()

def main():
    """Main function to start the GUI and load the configuration."""
    global config
    config = load_config()
    create_gui()

if __name__ == '__main__':
    main()