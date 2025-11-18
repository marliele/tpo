from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

#Настройка драйвера, подключение Хрома
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--ignore-certificate-errors')

#service = Service(ChromeDriverManager().install())
#driver = webdriver.Chrome(service=service, options=options)
driver_path = '/usr/bin/chromedriver'
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options) 

driver.implicitly_wait(10)

#Страница авторизации OpenBMC
openbmc_url = "https://localhost:2443/?next=/login#/login"

#test_1
driver.get(openbmc_url)
#Т.к. в ссылке используется https, то автоматизирую страницу о предупреждении
details_button = driver.find_element(By.ID, "details-button")
details_button.click()

proceed_link = driver.find_element(By.ID, "proceed-link")
proceed_link.click()

username_field = driver.find_element(By.ID, "username")
username_field.send_keys("root")

password_field = driver.find_element(By.ID, "password")
password_field.send_keys("0penBmc")

login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

user_button = driver.find_element(By.ID, "app-header-user")
user_button.click()

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@data-test-id='appHeader-link-logout']"))
    )
    print("ТЕСТ УСПЕШНОЙ АВТОРИЗАЦИИ (1): ПРОЙДЕН")
except:
    print("ТЕСТ УСПЕШНОЙ АВТОРИЗАЦИИ (1): ПРОВАЛЕН")
#test_1 end

#test_2
driver.get(openbmc_url)
username_field = driver.find_element(By.ID, "username")
username_field.send_keys("root")

password_field = driver.find_element(By.ID, "password")
password_field.send_keys("wrong_password")

login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

try:
    WebDriverWait(driver, 10).until(
        lambda d: any("401" in entry['message'] for entry in d.get_log('browser') 
                     if 'message' in entry)
    )
    print("ТЕСТ НЕВЕРНЫХ ДАННЫХ (2): ПРОЙДЕН (обнаружена ошибка 401)")
except:
    print("ТЕСТ НЕВЕРНЫХ ДАННЫХ (2): ПРОВАЛЕН (ошибка 401 не обнаружена)")

#test_2 end

#test_3
driver.get(openbmc_url)
account_lock = False
for i in range(10):
    username_field = driver.find_element(By.ID, "username")
    username_field.clear()
    username_field.send_keys("root-wrong")

    password_field = driver.find_element(By.ID, "password")
    password_field.clear()
    password_field.send_keys("wrong_password")
    
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    try:
        WebDriverWait(driver, 10).until(
            lambda d: any("405" in entry['message'] for entry in d.get_log('browser') 
                         if 'message' in entry)
    )
        print("ТЕСТ БЛОКИРОВКИ (3): ПРОЙДЕН (обнаружена ошибка 405)")
        account_lock = True
        break
    except:
        continue
if not account_lock:
    print("ТЕСТ БЛОКИРОВКИ (3): ПРОВАЛЕН (ошибка 405 не обнаружена)")
#test_3 end

#test_4
driver.get(openbmc_url)
username_field = driver.find_element(By.ID, "username")
username_field.send_keys("root")

password_field = driver.find_element(By.ID, "password")
password_field.send_keys("0penBmc")

login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

power_button = driver.find_element(By.XPATH, "//*[@data-test-id='appHeader-container-power']")
power_button.click()

try:
    poweron_button = driver.find_element(By.XPATH, "//*[@data-test-id='serverPowerOperations-button-powerOn']")
    poweron_button.click()
except:
    print("НЕПРАВИЛЬНОЕ СОСТОЯНИЕ OPENBMC: ОТСУТСТВУЕТ КНОПКА POWERON")

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@role='alert']"))
    )
    print("ТЕСТ POWERON (4): ПРОЙДЕН")
except:
    print("ТЕСТ POWERON (4): ПРОВАЛЕН")
#test_4 end

#test_5
driver.get(openbmc_url)
username_field = driver.find_element(By.ID, "username")
username_field.send_keys("root")

password_field = driver.find_element(By.ID, "password")
password_field.send_keys("0penBmc")

login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

try:
    nav_button = driver.find_element(By.ID, "app-header-trigger")
    nav_button.click()
    hardware_status_button = driver.find_element(By.XPATH, "//*[@data-test-id='nav-button-hardware-status']")
    hardware_status_button.click()
except:
    hardware_status_button = driver.find_element(By.XPATH, "//*[@data-test-id='nav-button-hardware-status']")
    hardware_status_button.click()

sensors_button = driver.find_element(By.XPATH, "//*[@data-test-id='nav-item-sensors']")
sensors_button.click()

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@class='table b-table b-table-no-border-collapse b-table-selectable b-table-select-multi b-table-selectable-no-click']"))
    )
    print("ТЕСТ SENSORS VISIBLE (5): ПРОЙДЕН")
except:
    print("ТЕСТ SENSORS VISIBLE (5): ПРОВАЛЕН")
#test_5 end
driver.quit()
