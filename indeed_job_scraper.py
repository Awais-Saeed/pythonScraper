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
    driver.get("https://pk.indeed.com/")
    driver.maximize_window()

def jobParameters(str1, str2):
    # Search job in desired location
    driver.find_element(By.XPATH, "(//input)[1]").send_keys(str1)
    driver.find_element(By.XPATH, "(//input)[2]").send_keys(str2)
    driver.find_element(By.XPATH, "//button[text()='Find jobs']").click()

    # Date filter (selecting second option)
    driver.find_element(By.XPATH, "//button[@id='filter-dateposted']").click()
    driver.find_element(By.XPATH, "//ul[@id='filter-dateposted-menu']//li[2]").click()


setUpBrowserParameters()
jobParameters("assistant", "Lahore")


title = []
company = []
location = []
salary = []
jobType = []


print("If there is a pop up on screen, close it")
print("Type anything to proceed")
x=input()


count = 0
isRun = True
while isRun:
    # get all jobs
    # pick those <li> which do not have any ancestor <li>.
    # i.e. pick only the direct descendents of <ul>
    items = driver.find_elements(By.XPATH, "//div[contains(@id,'jobResults')]//ul//li[not(ancestor::li)]")
    for ii in items:
        # click jobs one by one
        # There are more elements in the DOM than actually shown on screen.
        # That is why I am using try except block
        try:
            time.sleep(3)   # deliberate delay to avoid captchas
            ii.click()
            count = count + 1

            # get title
            # wait for it to be loaded
            # No need for waiting for subsequent elements
            elem = "//h2[@data-testid='jobsearch-JobInfoHeader-title']//span"
            WebDriverWait(driver,50).until(EC.element_to_be_clickable((By.XPATH, elem)))
            x = driver.find_element(By.XPATH, elem).text
            title.append(str(x))
            print(str(count)+ "] " + str(x))

            # get company name
            x = driver.find_element(By.XPATH, "//div[@data-testid='jobsearch-CompanyInfoContainer']//a").text
            company.append(str(x))

            # get job location
            x = driver.find_element(By.XPATH, "//div[@data-testid='inlineHeader-companyLocation']//div").text
            location.append(str(x))

            # get salary
            try:
                x = driver.find_element(By.XPATH,"//div[@data-testid='jobsearch-OtherJobDetailsContainer']//span").text
                salary.append(str(x))
            except NoSuchElementException:
                salary.append("NA")

            # get job type
            x = driver.find_elements(By.XPATH, "//h3[text()='Job type']//parent::div//div//li")
            cc = []
            for i in x:
                cc.append(str(i.text))
            
            cc = ','.join(cc)
            jobType.append(cc)
        except:
            pass

    try:
        elem = "//a[@aria-label='Next Page']"
        WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, elem)))
        nextBtn = driver.find_element(By.XPATH, elem).click()
        print("Next page")
    except:
        print("Last page reached")
        isRun = False
        pass


# create DataFrame using Dictionary
# Dictionary uses {} and a key:pair structure
df = pd.DataFrame({'Title': title, 'Company': company, 'Location': location, 'Salary': salary, 'Type': jobType})


# export data to desired format
# index is for serial numbers
fileName = "TestFile.xlsx"
df.to_excel(fileName,index=False)