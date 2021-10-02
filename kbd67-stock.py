from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from winotify import Notification, audio
import time, webbrowser, datetime

# wait for element to load
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Input information here:
fb_username = ''
fb_password = ''
link = '' # Link to open when post is found

def show_notif(link):
    toast = Notification(app_id='Stock Notifier',
                     title='POST FOUND')

    toast.add_actions(label='Open links',
                    link=link)

    toast.set_audio(audio.LoopingAlarm, loop=True)

    toast.build().show()

PATH = 'C:\Program Files (x86)\chromedriver.exe'
CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

# Enter terms to search for:
TERMS = ['KBD67', 'kbd67', 'KBD 67', 'kbd 67']

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(PATH, chrome_options=chrome_options)

driver.get('https://www.facebook.com/')

inpts = driver.find_elements_by_class_name('inputtext')

inpts[0].send_keys(fb_username)
inpts[1].send_keys(fb_password)

login = driver.find_element_by_name('login')
login.click()
time.sleep(1)
driver.get('https://www.facebook.com/rotoboxph')

i = 1
start_time = time.time()
last_iteration = 0
in_stock = False

while not in_stock:

    try:
        element = driver.find_element_by_css_selector('div.k4urcfbm.dp1hu0rb.d2edcug0.cbu4d94t.j83agx80.bp9cbjyn')
        posts = element.find_elements_by_css_selector('div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0')

        for post in posts:
            desc = post.find_element_by_css_selector('div.ecm0bbzt.hv4rvrfc.ihqw7lf3.dati1w0a')
            # print(desc.text)
            # print()

            for TERM in TERMS:
                if TERM in desc.text:
                    in_stock = True
                    break

        if in_stock:
            show_notif(link)
        else:
            time.sleep(15)
            driver.refresh()

        duration = time.time() - start_time
        print('Iterations: {}  |  Duration: {} (+{}s)'.format(i, datetime.timedelta(seconds=int(duration)), round(duration-last_iteration-15, 1)))
        last_iteration = duration
        i += 1

    except Exception as e:
        print('ERROR:', e)
        driver.get('https://www.facebook.com/rotoboxph')
        time.sleep(15)