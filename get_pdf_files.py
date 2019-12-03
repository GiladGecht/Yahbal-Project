from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import time



base_url = "https://undocs.org/en/A/{}/PV.{}"
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.add_experimental_option('prefs',  {
    "download.default_directory": r'C:\Users\Gilad Gecht\yahbal\Data',
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True})

driver = webdriver.Chrome(options=chrome_options)

T1 = time.time()
for i in tqdm(range(71, 74)):
    for j in range(4, 28):
        try:
            driver.get(base_url.format(i, j))
            iframe = driver.find_element_by_class_name("embed-responsive-item")
            driver.switch_to.frame(iframe)
            driver.find_element_by_id("open-button").click()
            print("Downloaded: A/{}/PV.{}".format(i, j))
        except:
            print("Unable to find file {}...".format(base_url.format(i, j)))
            next


print("Done in {} seconds...".format(time.time() - T1))

