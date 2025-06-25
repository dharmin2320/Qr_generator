from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, StaleElementReferenceException
import time
import pandas as pd

# --- Chrome options
options = Options()
options.add_argument("--headless")  # comment out to see browser
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

driver.get("https://balmandal.in.baps.org/Default.aspx")
time.sleep(3)



# Wait for login to complete (simple wait + screenshot)
time.sleep(5)
print("🔍 Screenshot saved: 2_after_login_debug.png — check what page loaded")

# Login
driver.find_element(By.XPATH, '/html/body/form/div[3]/div/div[2]/section/div[4]/div[2]/div[1]/div/table/tbody/tr/td/div[1]/input').send_keys("Shaileshbhai477")
driver.find_element(By.XPATH, '/html/body/form/div[3]/div/div[2]/section/div[4]/div[2]/div[1]/div/table/tbody/tr/td/div[2]/input[1]').send_keys("9892560636")
driver.find_element(By.XPATH, '/html/body/form/div[3]/div/div[2]/section/div[4]/div[2]/div[1]/div/table/tbody/tr/td/div[4]/input').click()

# Navigate to list
wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/div[3]/div[1]/div/div[1]/div[2]/div[2]/div/input'))).click()
time.sleep(2)  # slight wait for UI transition
wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/section/div/div[2]/div/div/div[2]/div/div[1]/a/div'))).click()
time.sleep(2)

data = []

list_items = driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/section/div/div[2]/div/div[1]/div[2]/ul/li')
num_items = len(list_items)
print(f"🔢 Total items found: {num_items}")

for i in range(1, num_items + 1):  
    try:
        # Re-locate the image element fresh each time to avoid stale element reference
        xpath_img = f'/html/body/div[1]/div[2]/section/div/div[2]/div/div[1]/div[2]/ul/li[{i}]/div/div[1]/a/img'
        xpath_shlok_count = f'/html/body/div[1]/div[2]/section/div/div[2]/div/div[1]/div[2]/ul/li[{i}]/div/div[1]/span'

        card_img = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_img)))

        shlok_count = driver.find_element(By.XPATH, xpath_shlok_count).text

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card_img)
        time.sleep(0.5)
        card_img.click()

        # Wait for data form to load
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/section/div/div[2]/div/div[1]/div[2]/div/div/div[1]/div[1]/input')))
        
        user_data = {
            'ID': driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/section/div/div[2]/div/div[1]/div[2]/div/div/div[1]/div[1]/input').get_attribute('value'),
            'Sabha Name': driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/section/div/div[2]/div/div[1]/div[2]/div/div/div[1]/div[2]/span/span[1]/span/span[1]').text,
            'First Name': driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/section/div/div[2]/div/div[1]/div[2]/div/div/div[2]/div[1]/div/div[1]/input').get_attribute('value'),
            'Middle Name': driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/section/div/div[2]/div/div[1]/div[2]/div/div/div[2]/div[1]/div/div[2]/input').get_attribute('value'),
            'Surname': driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/section/div/div[2]/div/div[1]/div[2]/div/div/div[2]/div[1]/div/div[3]/input').get_attribute('value'),
            'Shlok Count': shlok_count,
            'Father Mobile': driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/section/div/div[2]/div/div[1]/div[2]/div/div/div[2]/div[1]/div/div[4]/input').get_attribute('value'),
            'Image': driver.find_element(By.XPATH ,'/html/body/div/div[2]/section/div/div[2]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div/img').get_attribute('src')
        }
        data.append(user_data)
        
        # Click "Go Back"
        back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/section/div/div[2]/div/div[1]/div[2]/form/div/div/a')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", back_btn)
        time.sleep(0.5)
        back_btn.click()
        
        # Wait until list reloads (wait for current card_img xpath to appear again)
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_img)))
        
        print(f"✅ Processed item {i}")
    
    except (ElementClickInterceptedException, TimeoutException, StaleElementReferenceException) as e:
        print(f"⚠️ Skipping item {i} due to error: {e}")
        # Optional: try refreshing the page or re-navigating if too many failures
        continue

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("K5_Contact_details.csv", index=False)
print("✅ Data saved to baps_data.csv")

driver.quit()
