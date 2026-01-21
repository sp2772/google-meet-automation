from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time

# Step 1: Setup undetected-chromedriver
options = uc.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/sripr/AppData/Local/Google/Chrome/User Data/Profile 7")
driver = uc.Chrome(version_main=130)

# Step 2: Open Google Meet and Login
driver.get('https://accounts.google.com/signin')
time.sleep(4)
driver.find_element(By.TAG_NAME, 'input').send_keys("sp27venus@gmail.com")
time.sleep(4)
driver.find_element(By.TAG_NAME, 'input').send_keys("<password>")
time.sleep(4)

input("Press Enter after logging in and starting the meeting...")

# Step 3: Function to Find Button by aria-label with Explicit Wait
def find_button_by_aria_label(driver, aria_label):
    try:
        return WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//button[@aria-label='{aria_label}']"))
        )
    except Exception as e:
        return None

# Step 4: Toggle Button Function
def toggle_button(button):
    try:
        button.click()
        print("Toggled button.")
    except Exception as e:
        print(f"Error toggling button: {e}")

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

# Step 7: Main Loop
try:
    while True:
        ensure_mic_on()
        ensure_video_on()
        time.sleep(5)
except KeyboardInterrupt:
    print("Manual interruption detected. Exiting...")
finally:
    driver.quit()
