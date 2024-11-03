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
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.amazon.com/")

setUpBrowserParameters()

print("waiting for input...")
x = input()
driver.find_element(By.ID, "captchacharacters").send_keys(x)
print("input succeeded... Passing it as captcha")


# hit Continue button
driver.find_element(By.XPATH, "//form//span//button").click()


#Explicit wait
# change the delivery country
elem1 = "//*[@id='glow-ingress-block']"
elem2 = "//*[@id='GLUXCountryListDropdown']"
WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, elem1))).click()
WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, elem2))).click()


# search for United Kindgom in dropdown
destinations = driver.find_elements(By.XPATH, "//li[@class='a-dropdown-item']")
for i in destinations:
    if "United Kingdom" in i.text:
        i.click()
        break


driver.find_element(By.XPATH, "//span[@class='a-button a-button-primary']/span[@class='a-button-inner']").click()


# Search iPhone 12
time.sleep(3)
elemID3 = "//input[@id='twotabsearchtextbox']"
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, elemID3))).send_keys("iPhone 12")


# hit search btn
driver.find_element(By.XPATH, "//input[@ID='nav-search-submit-button']").click()


isRun = True
count = 1
url = []
title = []
customerReviews = []
stars = []
rating = []
while isRun:
    # Pick all products
    items = driver.find_elements(By.XPATH, "//div[@data-cy='title-recipe']//h2//a")
    original_window = driver.current_window_handle


    # filter for only iPhone 12
    for i in items:
        # if "iphone 12" in i.text.lower() and "case" not in i.text.lower():
        if "iphone 12" in i.text.lower() and not any(x in i.text.lower() for x in ['case','charger','cable','holder','accessory','accessories','replacement','speaker','dummy','protector']):
            print(str(count) + "]")
            print(i.text + "\n")
            href = i.get_attribute("href")
            # Open new tab
            driver.switch_to.new_window('tab')
            # open product in new tab
            driver.get(""+str(href)+"")
            time.sleep(2)

            
            # Get URLs
            x = driver.current_url
            url.append(str(x))


            # Get title
            x = driver.find_element(By.XPATH, "//h1[@id='title']").text
            title.append(str(x))


            # Get rating stars
            # .text method wasn't working
            # so, I used get_attribute('textContent')
            try:
                x = driver.find_element(By.XPATH, "//div[@id='averageCustomerReviews']//a//i//span[1]").get_attribute('textContent')
                stars.append(str(x))
            except NoSuchElementException:
                stars.append('NA')


            # Get total ratings
            try:
                x = driver.find_element(By.ID, 'acrCustomerReviewText').get_attribute('textContent')
                customerReviews.append(str(x))
            except NoSuchElementException:
                customerReviews.append('NA')


            # Get rating value
            try:
                x = driver.find_element(By.XPATH, "//div[@id='averageCustomerReviews']//a//span[1]").get_attribute('textContent')
                rating.append(str(x))
            except NoSuchElementException:
                rating.append('NA')


            driver.close()
            # move back to parent tab
            driver.switch_to.window(original_window)
            count = count + 1
    

    # find the Next Button (with Explicit wait) to tackle pagination
    elem = "//*[contains(@class,'s-pagination-next')]"
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, elem)))
    nextBtn = driver.find_element(By.XPATH, elem)
    nextBtnAttribute = nextBtn.get_attribute("aria-disabled")


    # check if it is disabled or not
    # use lower() for case insensitive string comparision
    if str(nextBtnAttribute).lower() == "None".lower():
        isRun = True
        nextBtn.click()
        time.sleep(3)
    else:
        print("aria-disbaled present")
        isRun = False


# create DataFrame using Dictionary
# Dictionary uses {} and a key:pair structure
df = pd.DataFrame({'URL': url, 'Title': title, 'Stars': stars, 'customerReviews': customerReviews, 'Ratings': rating})


# export data to desired format
# index is for serial numbers
fileName = "TestFile.xlsx"
df.to_excel(fileName,index=False)
