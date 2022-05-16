from datetime import datetime, timedelta

from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
from multiprocessing import Process
from multiprocessing import Pool, cpu_count
import requests
import pickle
import json

LOGIN_TIME_HOUR = 15
LOGIN_TIME_MINUTE = 32
BOOKING_TIME_HOUR = 15
BOOKING_TIME_MINUTE = 33

chrome_driver_path = "F:\Coding\python\chromedriver"
driver = webdriver.Chrome(chrome_driver_path)
action = webdriver.ActionChains(driver)

class Badminton:
    def __init__(self,booking_time):
        # self.chrome_driver_path = "F:\Coding\python\chromedriver"
        # driver = webdriver.Chrome(self.chrome_driver_path)
        # self.action = webdriver.ActionChains(driver)
        self.booking_time = booking_time

    # def login(self):
    #     try:
    #         driver.get(
    #             f"https://wfw.scuec.edu.cn/2021/08/29/book?cdmc=%E7%BE%BD%E6%AF%9B%E7%90%83&date={datetime.today().date()}")
    #         self.get_cookie()
    #         driver.refresh()
    #         time.sleep(3)
    #         print("1111111111111")
    #     except FileNotFoundError or FileExistsError as e:
    #         print(e)
    #         print("start login using username and password")
    #         driver.get(
    #             f"https://wfw.scuec.edu.cn/2021/08/29/book?cdmc=%E7%BE%BD%E6%AF%9B%E7%90%83&date={datetime.today().date()}")
    #         time.sleep(2)
    #         username = driver.find_element(by=By.CSS_SELECTOR, value="#username")
    #         password = driver.find_element(by=By.CSS_SELECTOR, value="#password")
    #         submit = driver.find_element(by=By.CSS_SELECTOR, value="#login_submit")
    #         time.sleep(2)
    #         username.send_keys("3089008")
    #         time.sleep(2)
    #         password.send_keys("liuyang2010")
    #         time.sleep(2)
    #         submit.click()
    #         pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    #         print("cookie saved")
    #         print("login using username and password")
    def login(self):
        driver.get(
            f"https://wfw.scuec.edu.cn/2021/08/29/book?cdmc=%E7%BE%BD%E6%AF%9B%E7%90%83&date={datetime.today().date()}")
        try:
            username = driver.find_element(by=By.CSS_SELECTOR, value="#username")
            password = driver.find_element(by=By.CSS_SELECTOR, value="#password")
            submit = driver.find_element(by=By.CSS_SELECTOR, value="#login_submit")
            time.sleep(2)
            with open("users.json","r") as users_file:
                data = json.load(users_file)
                account = data["0"]["username"]
                pwd = data["0"]["password"]
            username.send_keys(account)
            time.sleep(2)
            password.send_keys(pwd)
            time.sleep(2)
            submit.click()
            print("end login")
        except:
            print("NoSuchElement, it may already sign in")


    def get_cookie(self):
        cookies = pickle.load(open("cookies.pkl","rb"))
        for cookie in cookies:
            cookie_dict={
                "domain":"scuec.edu.cn",
                "name":cookie.get("name"),
                "value":cookie.get("value")
            }
            print(f"domain: {cookie.get('domain')}")
            print(f"name: {cookie.get('name')}")
            print(f"value:{cookie.get('value')}")
            print(cookie.get("expiry"))
            driver.add_cookie(cookie_dict)
        print("load cookies")
        print("login using cookie")


    def get_latest_date(self):
        while not self.is_page_loaded_xpath('//div[@name="YYRQ"]/parent::a'):
            time.sleep(2)
            driver.back()
            driver.refresh()
        other_date = driver.find_element(by=By.XPATH, value='(//div[@name="YYRQ"])[2]/parent::a')
        time.sleep(2)
        other_date.click()
        while not self.is_page_loaded_xpath('//div[@name="YYRQ"]/parent::a'):
            time.sleep(2)
            driver.back()
            driver.refresh()
        latest_date = driver.find_element(by=By.XPATH, value='(//div[@name="YYRQ"])[3]/parent::a')
        time.sleep(2)
        latest_date.click()

    def is_page_loaded_xpath(self, str_xpath):
        page = driver.find_elements(by=By.XPATH, value=str_xpath)
        if len(page) > 0:
            return True
        else:
            return False

    def is_page_loaded_css(self, css_selector):
        page = driver.find_elements(by=By.CSS_SELECTOR, value=css_selector)
        if len(page) > 0:
            return True
        else:
            return False

    def add_friend(self):
        addfriends = driver.find_element(by=By.CSS_SELECTOR, value="tbody .bs-checkbox")
        time.sleep(1)
        addfriends.click()

    def playground_process(self):
        playground = driver.find_elements(by=By.CSS_SELECTOR, value=".reserveCol .canRes")
        driver.fullscreen_window()
        if len(playground) > 0:
            try:
                if playground[self.booking_time].is_displayed():
                    time.sleep(2)
                    playground[self.booking_time].click()
                    time.sleep(2)
                    playground[self.booking_time + 1].click()
                    playground_lock = driver.find_element(by=By.CSS_SELECTOR, value="#submit")
                    time.sleep(2)
                    playground_lock.click()
                    print(f"session id:{driver.session_id}, playground clicked")
                time.sleep(1)
                booking_submit = driver.find_elements(by=By.CSS_SELECTOR, value="#end_submit button")
                confirm = driver.find_elements(by=By.CSS_SELECTOR, value='button[class="confirm"]')
                if len(confirm) > 0:
                    reason = driver.find_element(by=By.XPATH, value="//h2/following-sibling::p")
                    confirm[0].click()
                    # action.key_down(Keys.ENTER).perform()
                    print(f"session id:{driver.session_id}, the reason is:{reason.text} and confirm clicked")
                if booking_submit[0].is_displayed():
                    self.add_friend()
                    time.sleep(1)
                    booking_submit[0].click()
                    print(f"session id:{driver.session_id}, succeed ?!")
            finally:
                pass
        time.sleep(1)

    def booking(self):
        is_login = False
        while True:
            time_now_hour = int(time.strftime("%H", time.localtime()))
            time_now_minute = int(time.strftime("%M", time.localtime()))
            time_now_second = int(time.strftime("%S", time.localtime()))
            print(f"{time_now_hour}:{time_now_minute}:{time_now_second}")
            if time_now_hour == LOGIN_TIME_HOUR and time_now_minute >= LOGIN_TIME_MINUTE and is_login is False:
                self.login()
                is_login = True
            elif time_now_hour == BOOKING_TIME_HOUR and time_now_minute >= BOOKING_TIME_MINUTE and time_now_second >= 0:
                latest_day = datetime.today().date() + timedelta(days=2)
                print(f"https://wfw.scuec.edu.cn/2021/08/29/book?cdmc=%E7%BE%BD%E6%AF%9B%E7%90%83&date={latest_day}")
                driver.get(
                    f"https://wfw.scuec.edu.cn/2021/08/29/book?cdmc=%E7%BE%BD%E6%AF%9B%E7%90%83&date={latest_day}")
                while not self.is_page_loaded_css(".reserveCol .canRes"):
                    time.sleep(1)
                    driver.back()
                    driver.get(
                        f"https://wfw.scuec.edu.cn/2021/08/29/book?cdmc=%E7%BE%BD%E6%AF%9B%E7%90%83&date={latest_day}")
                self.playground_process()
                driver.quit()
                break
            elif time_now_hour == LOGIN_TIME_HOUR and is_login:
                self.get_latest_date()
                print("keep session alive")
                time.sleep(2)
            else:
                time.sleep(10)
