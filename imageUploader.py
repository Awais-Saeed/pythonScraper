# Upload image from computer to a website
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import pyautogui


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get('https://www.iloveimg.com/resize-image')
driver.maximize_window()


# click upload btn
uploadBtn = driver.find_element(By.XPATH, "//*[@id='pickfiles']").click()
# uploadBtn.send_keys(r"C:\img.png")
# sometimes, send_keys() will not work.
# For that, we need to use pyautogui.typewrite()
time.sleep(3)
pyautogui.typewrite(r'C:\Users\HP\Downloads\ISUZU Truck Fuel Calibration.png')
pyautogui.press('enter')
