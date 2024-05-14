from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pytest


class Test_Sauce:
    def setup_method(self):
        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/")

    def teardown_method(self):
        self.driver.quit()

    def succesful_login_decorator(func):
        def login(self):
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='login-button']")))
            username = self.driver.find_element(By.XPATH, "//*[@id='user-name']")
            username.send_keys("standard_user")
            password = self.driver.find_element(By.XPATH, "//*[@id='password']")
            password.send_keys("secret_sauce")
            loginbutton = self.driver.find_element(By.XPATH, "//*[@id='login-button']")
            loginbutton.click()
            func(self)
        return login
    

    def test_password_and_username_empty(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='login-button']")))
        loginbutton = self.driver.find_element(By.XPATH, "//*[@id='login-button']")
        loginbutton.click()
        errormessage = self.driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        assert errormessage.text == "Epic sadface: Username is required"

    def test_only_password_empty(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='user-name']")))
        username = self.driver.find_element(By.XPATH, "//*[@id='user-name']")
        username.send_keys("standard_user")
        loginbutton = self.driver.find_element(By.XPATH, "//*[@id='login-button']")
        loginbutton.click()
        errormessage = self.driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        assert errormessage.text == "Epic sadface: Password is required"


    def test_locked_out_user(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='login-button']")))
        username = self.driver.find_element(By.XPATH, "//*[@id='user-name']")
        username.send_keys("locked_out_user")
        password = self.driver.find_element(By.XPATH, "//*[@id='password']")
        password.send_keys("secret_sauce")
        loginbutton = self.driver.find_element(By.XPATH, "//*[@id='login-button']")
        loginbutton.click()
        errormessage = self.driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        assert errormessage.text == "Epic sadface: Sorry, this user has been locked out."

    @succesful_login_decorator
    def test_count_products(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='item_4_title_link']/div")))
        elements = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(elements) == 6

    @succesful_login_decorator
    def test_cartadd_count(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='item_4_title_link']/div")))
        addcartbutton = self.driver.find_element(By.XPATH, "//*[@id='add-to-cart-sauce-labs-backpack']")
        addcartbutton.click()
        count = self.driver.find_element(By.XPATH, "//*[@id='shopping_cart_container']/a/span")
        assert count.text == "1"

    @succesful_login_decorator
    def test_remove_from_cart(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='item_4_title_link']/div")))
        addcartbutton = self.driver.find_element(By.XPATH, "//*[@id='add-to-cart-sauce-labs-backpack']")
        addcartbutton.click()
        self.driver.find_element(By.XPATH, "//*[@id='shopping_cart_container']/a").click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "remove-sauce-labs-backpack")))
        self.driver.find_element(By.ID, "remove-sauce-labs-backpack").click()
        try:
            self.driver.find_element(By.XPATH, "//*[@id='cart_contents_container']/div/div[1]/div[3]/div[2]/div[1]")
            assert False
        except:
            assert True
        assert True

    @succesful_login_decorator
    def test_logout(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='menu_button_container']/div/div[1]/div")))
        self.driver.find_element(By.XPATH, "//*[@id='menu_button_container']/div/div[1]/div").click()
        sleep(0.3)
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='logout_sidebar_link']")))
        self.driver.find_element(By.XPATH, "//*[@id='logout_sidebar_link']").click()
        sleep(1)
        try:
            self.driver.find_element(By.XPATH, "//*[@id='login-button']")
            assert True
        except:
            assert False
        
        
