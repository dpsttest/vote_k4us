from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
from datetime import datetime 
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
load_dotenv()

##### Cron Job #####
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

polls = ['totalpoll-poll-23795', 'totalpoll-poll-23796', 'totalpoll-poll-23800']
id_polls = ['choice-9d82d614-47e4-4216-b3fd-8eaacfb22324-selector', 'choice-d6501067-de0b-47b1-bf84-f84f73305777-selector', 'choice-76cad3be-76e4-406c-80cc-8cb18f1abd75-selector']


options = webdriver.chrome.options.Options()
options.add_argument("--disable-extensions")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disk-cache-size=0")
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")



# def delete_cache(driver):
#     driver.execute_script("window.open('')")  # Create a separate tab than the main one
#     driver.switch_to.window(driver.window_handles[-1])  # Switch window to the second tab
#     driver.get('chrome://settings/clearBrowserData')  # Open your chrome settings.
#     perform_actions(driver, Keys.TAB * 2 + Keys.DOWN * 4 + Keys.TAB * 7 + Keys.ENTER)  # Tab to the time select and key down to say "All Time" then go to the Confirm button and press Enter
#     driver.close()  # Close that window
#     driver.switch_to.window(driver.window_handles[0])  # Switch Selenium controls to the original tab to continue normal functionality.

# def perform_actions(driver, keys):
#     actions = ActionChains(driver)
#     actions.send_keys(keys)
#     time.sleep(2)
#     print('Performing Actions!')
#     actions.perform()
#     time.sleep(5)

def app_vote():
    start_time = datetime.now()
    print('Time start:', str(start_time))
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get('https://k4us.com.br/pak2022')
        print(driver.title)
        driver_status = True
    except:
        print('Connection fails')
        driver_status = False

    if driver_status:
        for i in range(len(polls)):
            element_vote = driver.find_element(By.ID, id_polls[i])
            driver.execute_script("arguments[0].click();", element_vote)
            element_submit = driver.find_element(By.CSS_SELECTOR, f"#{polls[i]} > form > .totalpoll-buttons > button.totalpoll-buttons-vote")
            driver.execute_script("arguments[0].click();", element_submit)
            time.sleep(10)
            try: 
                element_error = driver.find_element(By.CSS_SELECTOR, f"#{polls[i]} > form > .totalpoll-message-error")
                print(element_error.text)
            except:
                print('No error message')
    # driver.execute_script("window.localStorage.clear()")
    # driver.execute_script("window.sessionStorage.clear()")
    driver.delete_all_cookies()
    # delete_cache(driver)
    driver.stop_client()
    driver.close()
    driver.quit()
    end_time = datetime.now()
    print('Time end:', str(end_time))
    print('Time difference:', str(end_time - start_time))

####### Run Cron Job ########

# @sched.scheduled_job('cron', minute=5)
# def vote_job():
#     app_vote()

@sched.scheduled_job('interval', minutes=5)
def time_job():
    app_vote()

sched.start()
