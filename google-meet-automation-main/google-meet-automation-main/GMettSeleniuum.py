from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from collections import Counter
import re
from selenium.webdriver.chrome.service import Service

# Step 1: Setup Selenium WebDriver with a clean Chrome profile
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/sripr/AppData/Local/Google/Chrome/User Data/Profile 7")  # Clean profile for Selenium
options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass automation detection
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-infobars")  # Disable "Chrome is being controlled by automated test software"
options.add_argument("--start-maximized")   # Start maximized for better control

# Initialize WebDriver with the clean profile
driver = webdriver.Chrome(service=Service(executable_path="D:/AbyssOrder/Abyss-Order/ChromeDriver/chromedriver-win64/chromedriver-win64/chromedriver.exe"), options=options)

# Step 2: Open Google Meet (manual login will be required the first time)
driver.get('https://accounts.google.com/signin')

# Allow some time for manual login
input("Press Enter after logging in and completing any authentication steps...")

# Proceed with Google Meet after login
driver.get('https://meet.google.com/')

input("Press Enter after starting the Google Meet and enabling captions...")

# Step 3: Capture live captions (captions appear in the aria-live element)
captions_xpath = '//*[@aria-live="polite"]'
captions_text = ""

# Set up a loop to periodically capture and store the captions
start_time = time.time()
duration = 60 * 30  # Capture for 30 minutes

while time.time() - start_time < duration:
    try:
        # Locate and capture the caption text
        captions = driver.find_element(By.XPATH, captions_xpath).text
        captions_text += captions + " "
        time.sleep(5)  # Adjust delay between captures as needed
    except Exception as e:
        print(f"Error capturing captions: {e}")
        time.sleep(5)

# Step 4: Close the WebDriver
driver.quit()

# Step 5: Process the Captions Text
# Remove special characters and split into words
captions_text = re.sub(r'[^\w\s]', '', captions_text).lower()  # Convert to lowercase and remove punctuation
words = captions_text.split()

# Optionally, remove common stopwords like "the", "is", "and"
stopwords = set(["the", "is", "and", "to", "of", "a", "in", "that", "it", "on", "for", "with", "as", "by", "this", "are", "was", "an", "be", "or", "from", "at", "have", "has", "but", "not", "which", "you", "we"])
filtered_words = [word for word in words if word not in stopwords]

# Step 6: Count Word Frequencies
word_counter = Counter(filtered_words)

# Step 7: Print the Top 10 Most Spoken Words
top_10_words = word_counter.most_common(10)
print("Top 10 most spoken words in the Google Meet:")
for word, count in top_10_words:
    print(f"{word}: {count} occurrences")
