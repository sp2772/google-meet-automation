from xmlrpc.client import MultiCall
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time
from collections import Counter
import re
import keyboard
from meta_ai_api import MetaAI

# Step 1: Setup undetected-chromedriver
options = uc.ChromeOptions()
driver = uc.Chrome(version_main=130)  # Initialize WebDriver

# Step 2: Open Google Meet and Login
driver.get('https://accounts.google.com/signin')

time.sleep(4)
keyboard.write("sp27venus@gmail.com")
keyboard.send("enter")

time.sleep(4)
keyboard.write("<password>")
keyboard.send("enter")

input("Press Enter after logging in and completing any authentication steps...")
driver.get('https://meet.google.com/')
input("Press Enter after starting the Google Meet and enabling captions...")

# Step 3: Updated Function to Automatically Find the Captions Element
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
            if 'iOzk7' in class_name and 'XDPoIe' in class_name:
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
if not captions_xpath:
    print("Failed to find captions element. Exiting...")
    driver.quit()
    exit()

print(f"Using XPath: {captions_xpath}")


# mic_xpath = "/html/body/div[1]/c-wiz/div/div/div[31]/div[3]/div[10]/div/div/div[2]/div/div[1]/div/div[2]/span/button/div"

#     # Function to toggle microphone
# def toggle_microphone():
#     mic_button = driver.find_element(By.XPATH, mic_xpath)
#     mic_button.click()  # Click to toggle
#     print("Toggled microphone.")

# # Example usage: Toggle microphone on and off every 5 seconds for demonstration
# for _ in range(7):  # Toggle 3 times
#     toggle_microphone()
#     time.sleep(5)  


# Step 5: Monitor and Capture Captions
captions_text = ""
try:
    while True:
        try:
            driver.title  # Check if browser is still open

            # Capture captions using the dynamic XPath
            captions = driver.find_element(By.XPATH, captions_xpath).text
            captions_text += f" {captions} "
            print(captions)

            time.sleep(10)  # Adjust interval as needed

        except Exception as e:
            print(f"Error capturing captions: {e}")
            if "no such element" in str(e).lower():
                print("Meeting might have ended. Stop caption capture?")
                x=input("(y/n):")
                if x=='y':
                    break
                break
            else:
                print("Some problem occured!")
                x=input("Do you want to end capturing:(y/n)")
                if(x=='y'):
                    break
except KeyboardInterrupt:
    print("Manual interruption detected. Exiting...")
finally:
    driver.quit()  # Ensure browser closes

# Step 6: Process the Captions Text
new_captions_text = re.sub(r'[^\w\s]', '', captions_text).lower()
Mycaptionlines = new_captions_text.split("x999")

def remove_overlap(line1, line2):
    min_length = min(len(line1), len(line2))
    for i in range(min_length):
        if line1[-(i + 1):] == line2[:i + 1]:
            return line2[i + 1:]
    return line2

def remove_overlap(line1, line2):
    """
    Removes overlapping words between two consecutive lines.
    Finds the longest suffix of line1 that matches the prefix of line2.
    """
    words1 = line1.split()
    words2 = line2.split()

    # Find the maximum overlap by comparing suffix of line1 with prefix of line2
    for i in range(len(words1)):
        if words1[i:] == words2[:len(words1) - i]:
            # If overlap found, return the non-overlapping part of line2
            return " ".join(words2[len(words1) - i:])
    
    # If no overlap, return line2 as is
    return line2

cleaned_captions = ""
for i in range(len(Mycaptionlines) - 1):
    line1 = Mycaptionlines[i]
    line2 = Mycaptionlines[i + 1]
    
    # Add the current line1 to the cleaned captions
    cleaned_captions += line1 + " "

    # Remove overlap from line2 and continue
    Mycaptionlines[i + 1] = remove_overlap(line1, line2)

# Add the final line
cleaned_captions += Mycaptionlines[-1]

print("Cleaned Captions:")
print(cleaned_captions)


# Step 7: Word Frequency Analysis
words = cleaned_captions.split()
stopwords = set(["hello"])
filtered_words = [word for word in words if word.lower() not in stopwords]
word_counter = Counter(filtered_words)

top_20_words = word_counter.most_common(20)
print("\nTop 20 most spoken words in the Google Meet:")
for word, count in top_20_words:
    print(f"{word}: {count} occurrences")

# Step 8: Generate Summary and Minutes of Meeting
ai = MetaAI()
response = ai.prompt(
    message=cleaned_captions +
    ".......... FROM THE ABOVE COMPLETE TEXT OF A GOOGLE MEET CONVERSATION. "
    "TAKE THE IMPORTANT INFORMATION AS POINTS, SUMMARIZE WHAT HAPPENED, "
    "AND PROVIDE MINUTES OF MEETING."
)
print("\nMessage:\n",response['message'])


for key,value in response.items():
    print("/n",key,"/n/n",value,"\n")

