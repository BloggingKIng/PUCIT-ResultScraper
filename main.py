import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def fetchWebsite():
    options = Options()
    options.add_argument("--start-maximized")
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://pu.edu.pk/splash/admissiontestresults")
    time.sleep(3)
    return driver

def fetchData(driver, starting_roll, ending_roll):
    dataArray = []
    for i in range(starting_roll, ending_roll+1):
        try:
            input_roll = driver.find_element(By.XPATH, "//input[@name='roll_no']")
            input_roll.click()
            for _ in range(20):
                ActionChains(driver).send_keys(Keys.BACKSPACE).perform()
            input_roll.send_keys(i)
            input_roll.send_keys(Keys.RETURN)
            time.sleep(1)
            table = driver.find_elements(By.XPATH, "//div[@id='livesearch']//table[@class!='table']")
            table = table[1]
            html = table.get_attribute('outerHTML')
            df = pd.read_html(html)[0]
            data  = {}
            data ['Roll Number'] = i
            for x in range(len(df)):
                data[df[x][0]] = df[x][1]
            dataArray.append(data)
        except:
            pass
    print(dataArray)
    df = pd.DataFrame(dataArray)
    df.to_csv("pucit_result.csv")
    print(dataArray)



if __name__ == "__main__":
    driver = fetchWebsite()
    fetchData(driver,1,1000)