from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.company_menu = (By.ID, "navbarDropdownMenuLink")
        self.careers_xpath = (By.XPATH, "//a[contains(@href, '/careers') and contains(@class, 'dropdown-sub')]")

    def go_to_careers(self):
        print("🔍 Sayfa başlığı:", self.driver.title)
        time.sleep(2)

        company_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.company_menu)
        )
        company_element.click()
        print("🧭 Company menüsü tıklandı.")
        time.sleep(3)

        try:
            careers_element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.careers_xpath)
            )
            print("👀 Careers görünür durumda. Tıklanıyor...")
            self.driver.execute_script("arguments[0].click();", careers_element)
            print("✅ JS ile Careers linkine tıklandı.")
        except Exception as e:
            print("❌ Careers linki görünmedi veya tıklanamadı.")
            self.driver.save_screenshot("final_careers_fail.png")
            raise e
