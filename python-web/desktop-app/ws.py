from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to the ChromeDriver executable
chromedriver_path = "chromedriver.exe"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

# Specify the executable path within options
#chrome_options.binary_location = "path_to_chrome_binary"  # Optional, if needed

# Initialize the Chrome web driver with options
driver = webdriver.Chrome()  # You can use other browsers as well

# URL of the page to scrape
url = "https://clutch.co/in/it-services/ahmedabad"

# Open the URL in the browser
driver.get(url)

# Find all the listings on the page
# Wait for listings to be present
wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
listings = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "provider-row")))
print(listings)
# Iterate through each listing and extract relevant information
for listing in listings:
    company_name = listing.find_element(By.CLASS_NAME, "company-name").text.strip()
    services = listing.find_element(By.CLASS_NAME, "services").text.strip()
    location = listing.find_element(By.CLASS_NAME, "location").text.strip()

    print("Company:", company_name)
    print("Services:", services)
    print("Location:", location)
    print("=" * 50)

# Close the browser
driver.quit()
