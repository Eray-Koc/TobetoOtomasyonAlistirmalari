from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class TestSauce:
    def __init__(self):
        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/")

    def password_and_username_empty(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='login-button']")))
        loginbutton = self.driver.find_element(By.XPATH, "//*[@id='login-button']")
        loginbutton.click()
        errormessage = self.driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        status = errormessage.text == "Epic sadface: Username is required"
        print(status)

    def only_password_empty(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='user-name']")))
        username = self.driver.find_element(By.XPATH, "//*[@id='user-name']")
        username.send_keys("standard_user")
        loginbutton = self.driver.find_element(By.XPATH, "//*[@id='login-button']")
        loginbutton.click()
        errormessage = self.driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        status = errormessage.text == "Epic sadface: Password is required"
        print(status)


    def locked_out_user(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='login-button']")))
        username = self.driver.find_element(By.XPATH, "//*[@id='user-name']")
        username.send_keys("locked_out_user")
        password = self.driver.find_element(By.XPATH, "//*[@id='password']")
        password.send_keys("secret_sauce")
        loginbutton = self.driver.find_element(By.XPATH, "//*[@id='login-button']")
        loginbutton.click()
        errormessage = self.driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        status = errormessage.text == "Epic sadface: Sorry, this user has been locked out."
        print(status)

    def count_products(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='login-button']")))
        username = self.driver.find_element(By.XPATH, "//*[@id='user-name']")
        username.send_keys("standard_user")
        password = self.driver.find_element(By.XPATH, "//*[@id='password']")
        password.send_keys("secret_sauce")
        loginbutton = self.driver.find_element(By.XPATH, "//*[@id='login-button']")
        loginbutton.click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='item_4_title_link']/div")))
        elements = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        status = len(elements) == 6
        print(status)

    def add_cart(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='login-button']")))
        username = self.driver.find_element(By.XPATH, "//*[@id='user-name']")
        username.send_keys("standard_user")
        password = self.driver.find_element(By.XPATH, "//*[@id='password']")
        password.send_keys("secret_sauce")
        loginbutton = self.driver.find_element(By.XPATH, "//*[@id='login-button']")
        loginbutton.click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='item_4_title_link']/div")))
        addcartbutton = self.driver.find_element(By.XPATH, "//*[@id='add-to-cart-sauce-labs-backpack']")
        addcartbutton.click()
        count = self.driver.find_element(By.XPATH, "//*[@id='shopping_cart_container']/a/span")
        status = count.text == "1"
        print(status)


testclass = TestSauce()
testclass.add_cart()