# pages/home_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        
        # Most reliable method: find the correct Company menu using XPATH with text content
        self.company_menu = (By.XPATH, "//a[contains(@class, 'nav-link') and contains(., 'Company')]")
        
        # Dropdown item with /careers/ in its href
        self.careers_link = (By.CSS_SELECTOR, "a.dropdown-sub[href*='/careers/']")
        
        # To check if the dropdown menu is open
        self.dropdown_menu_shown = (By.CSS_SELECTOR, ".dropdown-menu.show")

    def open(self):
        self.driver.get("https://useinsider.com/")
        print("Home page opened.")

    def go_to_careers(self):
        wait = WebDriverWait(self.driver, 15)

        # Close the cookie pop-up 
        try:
            cookie_accept_btn = wait.until(EC.element_to_be_clickable((By.ID, "wt-cli-accept-all-btn")))
            cookie_accept_btn.click()
            time.sleep(1)
        except:
            pass

        # 1) Find the "Company" menu and click 
        try:
            company = wait.until(EC.element_to_be_clickable(self.company_menu))
            self.driver.execute_script("arguments[0].click();", company)
            print("Company menu clicked with JavaScript.")
        except Exception as e:
            print(f"Company menu could not be clicked: {e}")
            raise

        # 2) Wait for the dropdown menu to open
        try:
            # aria-expanded check
            wait.until(lambda d: company.get_attribute("aria-expanded") == "true")
            print("Dropdown menu opened via aria-expanded.")
        except:
            # Or wait for the .show class to be present
            wait.until(EC.presence_of_element_located(self.dropdown_menu_shown))
            print("Dropdown menu opened via .show class.")

        # 3) Find the 'Careers' link, wait for it to be clickable, and click
        careers = wait.until(EC.element_to_be_clickable(self.careers_link))
        self.driver.execute_script("arguments[0].click();", careers)
        print("Careers link clicked from dropdown.")
