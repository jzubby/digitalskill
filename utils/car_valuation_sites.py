import random
from faker import Faker
from utils.elements_locator import RegPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class BaseSite(object):
    """
    Base class housing general routines for testing for all valuation vendor
    """

    def __init__(self):
        self.locator_configs = RegPageLocators()
        self.faker = Faker()

    @property
    def site_locators(self):
        """

        :return:
        """
        return self.locator_configs

    @staticmethod
    def gen_random_mileage():
        """
        Generate random mileage for test
        :return:
        """
        return random.randrange(10000, 200000, 1000)


    def generate_random_name(self):
        """
        generate fake name for testing
        :return:
        """
        return self.faker.name

    @staticmethod
    def get_email():
        """
        :return: generate fake email for testing
        """
        return "faker@faker.com"

    @staticmethod
    def get_telephone_number():
        """
         TODO: check why the sites are not accepting faker generated tel number
        :return: generate fake telephone for testing
        """
        return "07440909779"


class MotorWaySite(BaseSite):
    """
    class encapsulating logic for MotorWaySite
    """

    def __init__(self, driver, reg_number, global_wait_time_out=100):
        super().__init__()
        self.driver = driver
        self.reg_number = reg_number
        self.global_wait_time_out = global_wait_time_out
        self.site_key = "motorway.co.uk"
        self.motorway_site_locators = self.site_locators.get_element_locator(self.site_key)


    def navigate_to_site(self) -> str:
        sub_button = self.motorway_site_locators.get("homepage").get("submitButton")
        self.driver.get("https://" + self.site_key)
        # we need to wait until page load completes
        WebDriverWait(self.driver, self.global_wait_time_out).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, sub_button)))
        return self.driver.title


    def submit_reg_info_on_hope_page(self) -> str:
        """
        homepage resources
        :return:
        """
        h_page_locators = self.motorway_site_locators.get("homepage")
        submit_button = h_page_locators["submitButton"]
        reg_input = h_page_locators["registrationInput"]
        val_ele = h_page_locators["validationElement"]
        self.driver.find_element(By.CSS_SELECTOR, reg_input).send_keys(self.reg_number)
        self.driver.find_element(By.CSS_SELECTOR, submit_button).click()
        WebDriverWait(self.driver, self.global_wait_time_out).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, val_ele)))
        validation_ele_text = self.driver.find_element(By.CSS_SELECTOR, val_ele).text
        return validation_ele_text

    def extract_vehicle_details(self) -> dict[str, str]:
        """
        extract the details we want
        :return:
        """
        vehicle_details = {}
        h_page_locators = self.motorway_site_locators.get("resultPage")
        for k_detail, v_locator in h_page_locators.items():
            ele_value = self.driver.find_element(By.CSS_SELECTOR, v_locator).text
            if k_detail == "make":
                # make is not explicitly given, we need to extract from model info,
                if ele_value:
                    ele_value = ele_value.split(" ", 1).pop(0)
                    vehicle_details[k_detail.upper()] = ele_value
            elif k_detail == "model":
                if ele_value:
                    ele_value = ele_value.split(" ", 1).pop(-1)
                    vehicle_details[k_detail.upper()] = ele_value
            else:
                vehicle_details[k_detail.upper()] = ele_value
        return vehicle_details

    def confirm_mileage_and_add_details(self):
        """
        confirm the mileage and get the valuation details
        """
        m_page_locators = self.motorway_site_locators.get("confirmMillage")
        mileage_input = m_page_locators["millageInput"]
        mileage_button = m_page_locators["millageConfirmButton"]
        self.driver.find_element(By.CSS_SELECTOR, mileage_input).clear()
        self.driver.find_element(By.CSS_SELECTOR, mileage_input).send_keys(self.gen_random_mileage())
        self.driver.find_element(By.CSS_SELECTOR, mileage_button).click()

        d_page_locators = self.motorway_site_locators.get("yourDetails")

        fullname_button = d_page_locators["fullname"]
        email_input = d_page_locators["emailInput"]
        telephone_input = d_page_locators["telephone"]
        submit_button = d_page_locators["submitButton"]
        # wait until page load completes
        WebDriverWait(self.driver, self.global_wait_time_out).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, submit_button)))
        self.driver.find_element(By.CSS_SELECTOR, fullname_button).send_keys(self.generate_random_name())
        self.driver.find_element(By.CSS_SELECTOR, email_input).send_keys(self.get_email())
        self.driver.find_element(By.CSS_SELECTOR, telephone_input).send_keys(self.get_telephone_number())
        self.driver.find_element(By.CSS_SELECTOR, submit_button).click()

    def get_valuation_price(self) -> str:
        """
        Get the valuation
        :return:
        """
        v_page_locators = self.motorway_site_locators.get("valuationDiscovery")
        v_price = v_page_locators["price"]
        WebDriverWait(self.driver, self.global_wait_time_out).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, v_price)))
        price = self.driver.find_element(By.CSS_SELECTOR, v_price).text
        return price



class WeBuyAnyCarSite(BaseSite):
    """
    Example next implementation for new vendor  webuyanycar.com,
    partial implementation, can be completed but dont want to waste more time to submit quicker,
    """
    def __init__(self, driver, reg_number, global_wait_time_out):
        super().__init__()
        self.driver = driver
        self.reg_number = reg_number
        self.global_wait_time_out = global_wait_time_out
        self.site_key = "webuyanycar.com"
        self.we_buy_any_car_site_locators = self.site_locators.get_element_locator(self.site_key)

    def navigate_to_site(self):
        cookies_warning_dismiss = self.we_buy_any_car_site_locators.get("acceptCookies")
        self.driver.get("http://" + self.site_key)
        # we need to wait to dismiss the cookie warning
        WebDriverWait(self.driver, self.global_wait_time_out).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, cookies_warning_dismiss))).click()


    def submit_reg_info_on_hope_page(self, reg_number):
        """
        homepage resources
        :return:
        """
        page_locators = self.we_buy_any_car_site_locators.get("homepage")
        submit_button = page_locators["submitButton"]
        reg_input = page_locators["registrationInput"]
        mileage_input = page_locators["millageInput"]
        # we need to wait to make sure that we can submit
        WebDriverWait(self.driver, self.global_wait_time_out).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, submit_button)))
        self.driver.find_element(By.CSS_SELECTOR, reg_input).send_keys(reg_number)
        self.driver.find_element(By.CSS_SELECTOR, mileage_input).send_keys(self.gen_random_mileage())
        self.driver.find_element(By.CSS_SELECTOR, submit_button).click()

    def needs_other_function_(self):
        """
        Decided not to complete, so as to submit,
        :return:
        """
        pass
