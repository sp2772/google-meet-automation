from xmlrpc.client import MultiCall
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from collections import Counter
import re
import keyboard
from meta_ai_api import MetaAI

with open("salvo_induction3.txt",'w') as f:
    print("File created")
# Step 1: Setup undetected-chromedriver with a clean Chrome profile
options = uc.ChromeOptions()
driver = uc.Chrome()  # Initialize WebDriver

# Step 2: Open Google Meet (manual login will be required the first time)
driver.get('https://accounts.google.com/signin')

time.sleep(5)

keyboard.write("sp27venus@gmail.com")
keyboard.send("enter")
time.sleep(5)
keyboard.write("<password>")
keyboard.send("enter")

input("Press Enter after logging in and completing any authentication steps...")
driver.get('https://meet.google.com/')
input("Press Enter after starting the Google Meet and enabling captions...")



#captions_xpath = '//*[@id="yDmH0d"]/c-wiz/div/div/div[28]/div[3]/div[3]/div[1]/div[1]/div/div[2]'
#captions_xpath='/html/body/div[1]/c-wiz/div[1]/div/div[31]/div[3]/div[3]/div[1]/div[1]/div/div[2]/div'
captions_xpath='/html/body/div[1]/c-wiz/div/div/div[34]/div[4]/div[3]/div/div[2]/div[1]'
#captions_xpath='/html/body/div[1]/c-wiz/div[1]/div/div[31]/div[3]/div[3]'
captions_text = ""

# Step 4: Monitor captions until the browser closes or Meet ends
try:
    start_time = time.time()
    i = 0  # Optional: Increment to track captions
    with open("salvo_induction2.txt",'a') as f:
        while True:
            try:
                # Check if browser is still open
                driver.title  # This will raise an exception if browser is closed
                captions_element=driver.find_element(By.XPATH, captions_xpath)
                print("Tag name:",captions_element.tag_name,"class name:",captions_element.get_attribute('class'))
                # Capture captions if available
                captions = driver.find_element(By.XPATH, captions_xpath).text
                
                captions_text += f"{captions}\n"
                print(captions)
                if len(captions) !=0:
                    f.write(captions+'\n')
                    f.flush()
                i+=1
                time.sleep(1.9)  # Adjust time interval as needed

            except Exception as e:
                print(f"Error capturing captions: {e}")
                time.sleep(5)

                # Exit if the captions are no longer available (Meet ended)
                if "no such element" in str(e).lower():
                    print("Meeting might have ended. Stopping caption capture?")
                    x=input("(y/n):")
                    if x=='y':
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

# Step 5: Improved Logic to Remove Overlapping Lines
def remove_overlap(line1, line2):
    """
    Removes overlapping part of line2 based on the end of line1.
    """
    min_length = min(len(line1), len(line2))
    for i in range(min_length):
        # Check if the end of line1 matches the start of line2
        if line1[-(i + 1):] == line2[:i + 1]:
            return line2[i + 1:]  # Return line2 without the overlapping part
    return line2  # No overlap found, return original line2

# Step 6: Process the Captions Text
with open('salvo_induction3.txt','r') as f:
    new_captions_text = f.read()
Mycaptionlines = new_captions_text.split("\n")

cleaned_captions = ""
for i in range(len(Mycaptionlines) - 1):
    line1 = Mycaptionlines[i]
    line2 = Mycaptionlines[i + 1]
    cleaned_captions += line1 + " "
    line2 = remove_overlap(line1, line2)  # Remove overlap before appending

# Add the last line (it won’t be compared)
cleaned_captions += Mycaptionlines[-1]

print("Cleaned Captions:")
print(cleaned_captions)

# Step 7: Word Frequency Analysis
words = cleaned_captions.split()
stopwords = set(["hello","the",
"to",
"and",
"that",
"so",
"we",
"have",
"can",
"i",
"a",
"they",
'them',
'like',
'of',
'be',
'if',
'in'])  # Example stopword
filtered_words = [word for word in words if word.lower() not in stopwords]

word_counter = Counter(filtered_words)
top_20_words = word_counter.most_common(40)

print("Top 20 most spoken words in the Google Meet:")
for word, count in top_20_words:
    print(f"{word}: {count} occurrences")

# Step 8: Summarize and Generate Minutes of Meeting
ai = MetaAI()
response = ai.prompt(
    message=cleaned_captions +
    ".......... FROM THE ABOVE COMPLETE TEXT OF A GOOGLE MEET CONVERSATION. "
    "TAKE THE IMPORTANT INFORMATION AS POINTS, SUMMARIZE WHAT HAPPENED IN THE MEET, "
    "AND PROVIDE MINUTES OF MEETING."
)
print(response)



