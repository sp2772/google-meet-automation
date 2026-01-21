from xmlrpc.client import MultiCall
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re
import keyboard
from collections import Counter
from meta_ai_api import MetaAI

# Step 1: Setup undetected-chromedriver
options = uc.ChromeOptions()
driver = uc.Chrome(version_main=130)  # Initialize WebDriver

# Step 2: Open Google Meet and Login
driver.get('https://accounts.google.com/signin')

time.sleep(4)
#keyboard.write("sp27venus@gmail.com")
driver.find_element(By.TAG_NAME, 'input').send_keys("sp27venus@gmail.com")
keyboard.send("enter")

time.sleep(4)
keyboard.write("<password>")
keyboard.send("enter")

input("Press Enter after logging in and completing any authentication steps...")
driver.get('https://meet.google.com/')
input("Press Enter after starting the Google Meet and enabling captions...")

def find_button_by_aria_label(driver, aria_label):
    try:
        return WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//button[@aria-label='{aria_label}']"))
        )
    except Exception as e:
        return None
    
# Step 3 (Alternative): Dynamic XPath Finder for Buttons Using aria-label
def find_button_by_aria_label2(driver, aria_label):
    try:
        button = driver.find_element(By.XPATH, f"//button[@aria-label='{aria_label}']")
        return driver.execute_script(
            "function absoluteXPath(element) {"
            "var comp, comps = []; var parent = null; var xpath = '';"
            "var getPos = function(element) {"
            "var position = 1, curNode;"
            "for (curNode = element.previousSibling; curNode; curNode = curNode.previousSibling) {"
            "if (curNode.nodeName == element.nodeName) {++position;}}"
            "return position;};"
            "for (; element && element.nodeType == 1; element = element.parentNode) {"
            "comp = comps[comps.length] = {};"
            "comp.name = element.nodeName.toLowerCase();"
            "comp.position = getPos(element);}"
            "for (var i = comps.length - 1; i >= 0; i--) {"
            "comp = comps[i]; xpath += '/' + comp.name + '[' + comp.position + ']';}"
            "return xpath;} return absoluteXPath(arguments[0]);", button)
    except Exception as e:
        print(f"Error finding button by aria-label '{aria_label}': {e}")
    return None



def find_captions_xpath(driver):
    """
    Searches the Google Meet page dynamically to find the XPath
    of the captions element based on known tag and class attributes.
    """
    try:
        # Locate all 'div' elements with relevant class names
        elements = driver.find_elements(By.TAG_NAME, 'div')
        for element in elements:
            class_name = element.get_attribute('class')
            
            # Check if it matches the known class names for captions
            if 'iOzk7' in class_name:
                xpath = driver.execute_script(
                    "function absoluteXPath(element) {"
                    "var comp, comps = [];"
                    "var parent = null;"
                    "var xpath = '';"
                    "var getPos = function(element) {"
                    "var position = 1, curNode;"
                    "for (curNode = element.previousSibling; curNode; curNode = curNode.previousSibling) {"
                    "if (curNode.nodeName == element.nodeName) {"
                    "++position;"
                    "}"
                    "}"
                    "return position;"
                    "};"
                    "for (; element && element.nodeType == 1; element = element.parentNode) {"
                    "comp = comps[comps.length] = {};"
                    "comp.name = element.nodeName.toLowerCase();"
                    "comp.position = getPos(element);"
                    "}"
                    "for (var i = comps.length - 1; i >= 0; i--) {"
                    "comp = comps[i];"
                    "xpath += '/' + comp.name + '[' + comp.position + ']';"
                    "}"
                    "return xpath;"
                    "} return absoluteXPath(arguments[0]);", element)
                
                print(f"Found captions element XPath: {xpath}")
                return xpath  # Return the first matching element's XPath

    except Exception as e:
        print(f"Error finding captions element: {e}")

    print("Captions element not found. Please enable captions and try again.")
    return None

# Step 4: Use the XPath Finder
captions_xpath = find_captions_xpath(driver)
while True:
    if not captions_xpath:
        print("Failed to find captions element. Retrying...")
        captions_xpath = find_captions_xpath(driver)
    else:
        break

# Step 4 (Alternative): Retrieve XPaths for Mic, Video, and Reactions Buttons Using aria-label
mic_xpath = find_button_by_aria_label(driver, "Turn off microphone")
video_xpath = find_button_by_aria_label(driver, "Turn off camera")
#reaction_xpath = find_button_by_aria_label(driver, "Send a reaction")

while True:
    if not mic_xpath or not video_xpath:
        print("Failed to find one or more button elements using aria-label. Retrying...")
    else:
        break


print(f"Mic XPath: {mic_xpath}")
print(f"Video XPath: {video_xpath}")
#print(f"Reaction XPath: {reaction_xpath}")

# Step 5: Define Toggle Functions
# Step 4: Toggle Button Function
def toggle_button(button):
    try:
        button.click()
        print("Toggled button.")
    except Exception as e:
        print(f"Error toggling button: {e}")

def monitor_button_status(button_xpath, status_class):
    try:
        button = driver.find_element(By.XPATH, button_xpath)
        class_name = button.get_attribute("aria-label")
        return status_class in class_name  # Return True if the button is off
    except Exception as e:
        print(f"Error checking button status: {e}")
        return False

# Step 5: Ensure Mic is On
def ensure_mic_on():
    mic_button = find_button_by_aria_label(driver, "Turn on microphone") or \
                 find_button_by_aria_label(driver, "Turn off microphone")
    if mic_button:
        aria_label = mic_button.get_attribute("aria-label")
        if "Turn on microphone" in aria_label:
            toggle_button(mic_button)
            print("Mic was off. Turned it on.")

# Step 6: Ensure Video is On
def ensure_video_on():
    video_button = find_button_by_aria_label(driver, "Turn on camera") or \
                   find_button_by_aria_label(driver, "Turn off camera")
    if video_button:
        aria_label = video_button.get_attribute("aria-label")
        if "Turn on camera" in aria_label:
            toggle_button(video_button)
            print("Video was off. Turned it on.")




captions_text = ""
try:
    while True:
        try:
            driver.title  # Check if browser is still open
            
            ensure_mic_on()
            ensure_video_on()
            # Capture captions using the dynamic XPath
            captions = driver.find_element(By.XPATH, captions_xpath).text
            captions_text += f" {captions} "
            print(captions)

            time.sleep(5)  # Adjust interval as needed

        except Exception as e:
            print(f"Error capturing captions: {e}")
            if "no such element" in str(e).lower():
                print("Meeting might have ended. Stop caption capture?")
                x = input("(y/n): ")
                if x == 'y':
                    break
            else:
                print("Some problem occurred!")
                x = input("Do you want to end capturing? (y/n): ")
                if x == 'y':
                    break
except KeyboardInterrupt:
    print("Manual interruption detected. Exiting...")
finally:
    driver.quit()

# Step 9: Process Captions and Generate Summary
new_captions_text = re.sub(r'[^\w\s]', '', captions_text).lower()
caption_lines = new_captions_text.split("x999")

cleaned_captions = " ".join(caption_lines)
print("Cleaned Captions:\n", cleaned_captions)

# Step 10: Word Frequency Analysis
words = cleaned_captions.split()
stopwords = set(["hello","you"])
filtered_words = [word for word in words if word.lower() not in stopwords]
word_counter = Counter(filtered_words)

top_20_words = word_counter.most_common(20)
print("\nTop 20 most spoken words:")
for word, count in top_20_words:
    print(f"{word}: {count} occurrences")

# Step 11: Generate Summary and Minutes of Meeting
ai = MetaAI()
response = ai.prompt(
    message=cleaned_captions +
    ".......... FROM THE ABOVE TEXT, SUMMARIZE THE IMPORTANT POINTS AND PROVIDE MINUTES OF MEETING."
)
print("\nSummary:\n", response['message'])

for key, value in response.items():
    print(f"\n{key}:\n{value}\n")

