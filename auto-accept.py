import cv2
import numpy as np
import pyautogui
import time
import logging
import os

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def find_accept_button(template_path, threshhold=0.5):
    # Capture the current screen
    try:

        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Load the template of the "Accept" button
        if not os.path.exists(template_path):
            logging.error(f'Template image not found at path: {template_path}')
            return False
    
        template = cv2.imread(template_path, 0)
        w, h = template.shape[::-1]

        #Match the template to the screenshot
        res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshhold)

        # If the button is found, click it
        if len(loc[0]) > 0:
            for pt in zip(*loc[::-1]):
                pyautogui.click(pt[0] + w/2, pt[1] + h/2)
                logging.info("Accept button found and clicked!")
                return True
            logging.info("Accept button not found.")
            return False
    except Exception as e:
                logging.error(f"Error during button search: {e}")
                return False
    
def main():
    template_path = 'accept_button.png' # Path to the template image

    while True:
        if find_accept_button(template_path):
            print("Accept button found and clicked!")
            time.sleep(2) # Wait for 1 second before searching again
        else:
            print("Accept button not found. Retrying...")
        time.sleep(2)


if __name__ == '__main__':
    main()
