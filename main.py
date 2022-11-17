from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
from datetime import datetime
import time

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

polls = ['totalpoll-poll-23795', 'totalpoll-poll-23796', 'totalpoll-poll-23800']
id_polls = ['choice-9d82d614-47e4-4216-b3fd-8eaacfb22324-selector', 'choice-d6501067-de0b-47b1-bf84-f84f73305777-selector', 'choice-76cad3be-76e4-406c-80cc-8cb18f1abd75-selector']

start_time = datetime.now()
print('Time start:', str(start_time))

try:
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome() # run on your computer
    driver.get('https://k4us.com.br/pak2022')
    print(driver.title)
except:
    print('Connection fails')

for i in range(len(polls)):
    element_vote = driver.find_element(By.ID, id_polls[i])
    driver.execute_script("arguments[0].click();", element_vote)
    element_submit = driver.find_element(By.CSS_SELECTOR, f"#{polls[i]} > form > .totalpoll-buttons > button.totalpoll-buttons-vote")
    driver.execute_script("arguments[0].click();", element_submit)
    time.sleep(10)
    try: 
        element_error = driver.find_element(By.CSS_SELECTOR, f"#{polls[i]} > div.totalpoll-message.totalpoll-message-error")
        print(element_error.text)
    except:
        print('No error message')
end_time = datetime.now()
print('Time end:', str(end_time))
print('Time difference:', str(end_time - start_time))
driver.quit()
