from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd
from tabulate import tabulate

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode to avoid opening a browser window

# Start the chromedriver service
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

url = "https://app.vivatechnology.com/partners?searchtext=&page=73&%24pagegroup=startups"

# Navigate to the URL
driver.get(url)

# Wait for the page to load (you can increase the sleep time if necessary)
time.sleep(20)

# Scroll to the bottom of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

# Get the page source after scrolling to the bottom
page_source = driver.page_source

# Create a BeautifulSoup object
soup = BeautifulSoup(page_source, "html.parser")

# Locate the elements with the specified attributes and exclude those with 'Online Only'
elements = soup.find_all("span", class_="fieldtext", text=lambda text: "Online Only" not in text)

# Extract the text attribute of each element
data = [element.text for element in elements]

# Create a dataframe from the data
df = pd.DataFrame(data, columns=["Partner's"])

# Print the fancy table
table = tabulate(df, headers='keys', tablefmt='fancy_grid')
print(table)

# Save the dataframe as a CSV file
df.to_csv("Viva Technology Python Web Scrape.csv", index=False)

# Close the webdriver
driver.quit()
