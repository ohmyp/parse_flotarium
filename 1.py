from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import requests

day = input('На какую дату смотреть запись: ')
token = ''
user_id = 
driver = webdriver.Chrome(executable_path='/Users/ohmyp/PycharmProjects/flotarium/chromedriver')
url = 'https://n164188.yclients.com/company:169354/idx:0/time?o=s2485675#2021-'+day
timeout = 15
while True:
    driver.get(url)
    
    try:
        element_present = EC.presence_of_element_located((By.ID, 'main'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print(' ')
    finally:
        print(time.ctime())

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    if text.find('На выбранный день нет свободных сеансов') != -1:
        print('Нет свободного времени')
    else:
        print("Появилась свободное время")
        timeToGo = ''
        for button in soup.find_all('button', {"class": "y-button y-button_transparent time-slot ng-binding"}):
            print(button.get_text(), sep=' ')
            timeToGo += button.get_text()

        message = 'Открыта запись на {}, время - {}\n\n{}'.format(url[-10:], timeToGo, url)
        sendMessage = requests.get('https://api.vk.com/method/messages.send', params={'user_id': user_id,
                                                                                      'message': message,
                                                                                      'random_id': 0,
                                                                                      'v': 5.111,
                                                                                      'access_token': token,
                                                                                      })
        print('Message:', sendMessage)
        time.sleep(7200)

    time.sleep(60)
