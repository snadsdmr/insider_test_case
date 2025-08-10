from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CareersPage:
    def __init__(self, driver):
        self.driver = driver
        self.see_all_qa_jobs = (By.XPATH, "//a[normalize-space()='See all QA jobs']")
        # Locators for blocks
        self._block_locations = (By.XPATH, "//*[contains(normalize-space(.), 'Our Locations')][not(self::script)]")
        self._block_teams     = (By.XPATH, "//*[contains(normalize-space(.), 'See all teams') or contains(normalize-space(.), 'Teams')][not(self::script)]")
        self._block_life      = (By.XPATH, "//*[contains(normalize-space(.), 'Life at Insider')][not(self::script)]")
        self._job_cards = (By.CLASS_NAME, "position-list-item")

    def is_open(self):
        return "Careers" in self.driver.title

    def blocks_are_visible(self, take_screenshots=True) -> dict:
        wait = WebDriverWait(self.driver, 15)
        checks = {
            "Locations": self._block_locations,
            "Teams":     self._block_teams,
            "Life at Insider": self._block_life,
        }
        results = {}

        for name, locator in checks.items():
            try:
                el = wait.until(EC.presence_of_element_located(locator))
                # Bring into view and wait for it to be visible
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                wait.until(EC.visibility_of(el))
                print(f"✓ '{name}' block is visible.")
                results[name] = True
            except Exception:
                print(f"✗ '{name}' block is NOT visible.")
                results[name] = False
                if take_screenshots:
                    safe = name.lower().replace(" ", "_").replace("@", "at")
                    self.driver.save_screenshot(f"missing_block_{safe}.png")
        return results

    def go_to_quality_assurance(self):
        self.driver.get("https://useinsider.com/careers/quality-assurance/")
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.see_all_qa_jobs)
        ).click()

    def filter_jobs(self, location, department):
        print("Filtering jobs...")

        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "select2-filter-by-location-container"))
        ).click()
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[normalize-space()='{location}']"))
        ).click()

        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "select2-filter-by-department-container"))
        ).click()
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[normalize-space()='{department}']"))
        ).click()

        print(f"Filters applied: {location}, {department}")

        WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located(self._job_cards))
        cards = self.driver.find_elements(*self._job_cards)
        print(f"{len(cards)} job postings found.")
        return [JobCard(card) for card in cards]


class JobCard:
    def __init__(self, element):
        self.position = element.find_element(By.CLASS_NAME, "position-title").text
        self.department = element.find_element(By.CLASS_NAME, "position-department").text
        self.location = element.find_element(By.CLASS_NAME, "position-location").text

    def __repr__(self):
        return f"{self.position} | {self.department} | {self.location}"
