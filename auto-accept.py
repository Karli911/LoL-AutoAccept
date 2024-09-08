import cv2
import numpy as np
import pyautogui
import time
import logging
import os
import json

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

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

def main():
    # Load configuration
    config = load_config()

    template_path = config['template_path'] 
    threshhold = config['threshhold'] 
    retry_interval = config['retry_interval']
    region = config.get('region', None)  # Optionally define a screen region
    max_retries = config.get('max_retries', 10)  # Maximum retries before alert
    debug = config.get('debug', False)  # Enable/disable debugging visualization

    retry_attempts = 0

    try:
        while True:
            if find_accept_button(template_path, threshhold, region, debug):
                retry_attempts = 0
                print("Accept button found and clicked!")
                time.sleep(retry_interval)  # Wait for the retry interval
            else:
                print("Accept button not found. Retrying...")
                retry_attempts += 1
                if retry_attempts > max_retries:
                    logging.error("Max retries reached. Please check the application.")
                    # Add alert mechanism here (e.g., email or desktop notification)

                # Retry with increasing delay (capped at 10 seconds)
                time.sleep(min(10, retry_interval * retry_attempts))

    except KeyboardInterrupt:
        logging.info("Script terminated by user.")
        print("Script terminated by user.")

if __name__ == '__main__':
    main()
