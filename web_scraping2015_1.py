import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


chrome_options = Options()
download_dir = "C:\\Users\\1\\Desktop\\Sabancı\\Yeni\\Ens491"  # replace with the path to your download directory

# Set preferences for file download
chrome_options.add_experimental_option("prefs", {
  "download.default_directory": download_dir,
  "download.prompt_for_download": False,  # To auto download the file
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True  # To disable the safebrowsing feature

})


# Set up the webdriver and url
driver = webdriver.Chrome(options=chrome_options)
url = "https://sonuc.ysk.gov.tr/sorgu"
driver.get(url)


# File name to save
election_number = ""
election_year = ""
city = ""
district = ""


# Function for file rename
def wait_for_download_and_rename(new_filename):
    print("Waiting for download to complete...")
    while any([filename.endswith(".crdownload") for filename in os.listdir(download_dir)]):
        time.sleep(1)  # wait for download to finish
    print("Download completed.")

    # Find the latest downloaded file in the download directory
    list_of_files = os.listdir(download_dir)
    paths = [os.path.join(download_dir, basename) for basename in list_of_files]
    latest_file = max(paths, key=os.path.getctime)

    # Define the new filename with path
    new_file_path = os.path.join(download_dir, new_filename)

    # Rename the file
    os.rename(latest_file, new_file_path)
    print(f"Renamed file to: {new_file_path}")



# Locate the button by its text
wait = WebDriverWait(driver, 10)
button = driver.find_element(By.XPATH, "//button[contains(., 'Seçim Adı ile Sorgula')]")
button.click()
time.sleep(0.5)

# Open dropdown
dropdown = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".ng-select-container"))
)
dropdown.click()
time.sleep(0.5)


# Find all dropdown options and click the last option
dropdown_options = driver.find_elements(By.CLASS_NAME, "ng-option")
first_option = dropdown_options[-4]
first_option.click()
time.sleep(0.5)
election_year = "2015_1"


# Select Yurt İçi
yurt_ici_radio = driver.find_element(By.XPATH, "//input[@value='1' and @formcontrolname='sandikTuru']")
yurt_ici_radio.click()
time.sleep(0.5)


# Devam Et
continue_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-success.rounded-0.mr-5'))
)
continue_button.click()
time.sleep(1)


# Open İl (City) dropdown
city_dropdown = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//label[text()='İl']/following::ng-select"))
)
city_dropdown.click()


# Wait for the presence of all the city options in the dropdown
city_options = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "ng-option"))
)
start_index = 12

# Loop through each city starting from the specified index
for index in range(start_index, len(city_options)):

    # Click the city dropdown for every iteration
    time.sleep(1)
    city_dropdown.click()

    # Re-identify the city options since the DOM may have been refreshed
    city_options = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "ng-option"))
    )

    # Save city name to a variable
    city = city_options[index].text

    city_options[index].click()
    time.sleep(2)

    # Open İlçe (District) dropdown
    district_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//label[text()='İlçe']/following::ng-select"))
    )
    district_dropdown.click()
    time.sleep(1)

    # Wait for the presence of all the district options in the dropdown
    district_options = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "ng-option"))
    )

    # Loop through each district for the current city
    for district_index in range(len(district_options)):
        time.sleep(1.5)
        # Re-identify the district dropdown and options since the DOM may have been refreshed
        district_dropdown.click()
        time.sleep(1)

        district_options = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ng-option"))
        )

        district = district_options[district_index].text

        district_options[district_index].click()
        time.sleep(4)

        # Click Sorgula
        button = driver.find_element(By.XPATH, "//button[contains(text(), 'Sorgula')]")
        button.click()
        time.sleep(5)

        # Wait and locate the button by its text content "Tabloyu Kaydet"
        tabloyu_kaydet_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Tabloyu Kaydet')]"))
        )
        tabloyu_kaydet_button.click()


        time.sleep(2)
        # Click Kabul Ediyorum
        kabul_ediyorum_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Kabul Ediyorum')]"))
        )
        kabul_ediyorum_button.click()

        time.sleep(2)

        file_name = election_year+"_"+city+"_"+district+".xlsx"
        wait_for_download_and_rename(file_name)

        time.sleep(3)


    # Wait a bit before starting the next iteration for cities
    time.sleep(2)






