import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time

lock = threading.Lock()

def fetchWebsite():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://pu.edu.pk/splash/admissiontestresults")
    time.sleep(3)
    return driver

initialValue = ""

def condition(driver):
    try:
        roll_no = driver.find_element(By.XPATH, "//table[@class='table']").find_element(By.XPATH, '//tr').text
        global initialValue
        return_ = roll_no != initialValue
        initialValue = roll_no
        return return_
    except Exception as e:
        return False

def fetchData(starting_roll, ending_roll):
    driver = fetchWebsite()
    dataArray = []
    for i in range(starting_roll, ending_roll + 1):
        try:
            input_roll = driver.find_element(By.XPATH, "//input[@name='roll_no']")
            input_roll.click()
            for _ in range(20):
                ActionChains(driver).send_keys(Keys.BACKSPACE).perform()
            input_roll.send_keys(i)
            input_roll.send_keys(Keys.RETURN)
            WebDriverWait(driver, 10).until(condition)
            table = driver.find_elements(By.XPATH, "//div[@id='livesearch']//table[@class!='table']")
            table = table[1]
            html = table.get_attribute('outerHTML')
            df = pd.read_html(html)[0]
            data = {}
            data['Roll Number'] = i
            for x in range(len(df)):
                data[df[x][0]] = df[x][1]
            dataArray.append(data)
        except:
            pass

        if ( i % 100 ) == 0:
            print(f"{i} Completed")
    driver.quit()

    with lock:
        try:
            existing_df = pd.read_csv("results/pucit_result.csv")
        except FileNotFoundError:
            existing_df = pd.DataFrame()

        new_df = pd.DataFrame(dataArray)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)

        combined_df.to_csv("results/pucit_result.csv", index=False)
        print(f"Processed range {starting_roll} to {ending_roll}")
        print(dataArray)

if __name__ == "__main__":
    roll_ranges = [(i, i + 999) for i in range(20000, 41000, 1000)]
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetchData, start, end) for start, end in roll_ranges]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f"Generated an exception: {exc}")
