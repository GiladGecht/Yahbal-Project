from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from pathlib import Path
from tqdm import tqdm
import json
import time

base_url = "https://undocs.org/en/A/65/PV.19"
driver = webdriver.Firefox(executable_path=r'/home/gilad/Yahbal/Yahbal-Project/geckodriver')
T1 = time.time()

driver.get(base_url)
iframe = driver.find_element_by_class_name("embed-responsive-item")
driver.switch_to.frame(iframe)
#
page_text = []
try:
    num_pages = len(WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, ("page")))))
    for page_no in range(num_pages):
        if page_no % 2 == 0:
            driver.get(base_url)
            iframe = driver.find_element_by_class_name("embed-responsive-item")
            driver.switch_to.frame(iframe)
            pages = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, ("page"))))
        print(pages[-1*(page_no + 1)].text)
        print("###"*30)
#
    driver.quit()
except Exception as e:
    print(e)
    driver.quit()


