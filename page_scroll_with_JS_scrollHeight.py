from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import NoSuchElementException


def setUpBrowserParameters():
    global driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get("https://intoli.com/blog/scrape-infinite-scroll/demo.html")
    driver.maximize_window()


setUpBrowserParameters()

data = []

# item visited
itemsVisited = 0

# elements to be visited
n = 45

# old element count
oldCount = 0

# Initial page height
oldHeight = driver.execute_script("return document.body.scrollHeight")

while itemsVisited < n:
    # scroll the page
    driver.execute_script("window.scroll(0, document.body.scrollHeight)")

    # Wait for new elements to be visible
    time.sleep(2)

    newHeight = driver.execute_script("return document.body.scrollHeight")
    newCount = len(driver.find_elements(By.XPATH, "//div[@class='box']"))

    if newHeight == oldHeight:
        print('breaking loop...page not scrollable anymore')
        break

    # pick each element and extract data
    for x in range(oldCount, newCount):
        elem = driver.find_element(By.CSS_SELECTOR, "div.box:nth-of-type("+str(x+1)+")").get_attribute('textContent')
        print(elem)
        data.append(str(elem))
        itemsVisited = itemsVisited + 1
        if itemsVisited >= n:
            break
    
    oldCount = newCount


# create DataFrame using Dictionary
# Dictionary uses {} and a key:pair structure
df = pd.DataFrame({'Scraped Data': data})


# export data to desired format
# index is for serial numbers
fileName = "TestFile.xlsx"
df.to_excel(fileName,index=False)

