from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CareersPage:
    def __init__(self, driver):
        self.driver = driver
        self.see_all_qa_jobs = (By.XPATH, "//a[text()='See all QA jobs']")
        self.job_cards = (By.CLASS_NAME, "position-list-item")

    def go_to_quality_assurance(self):
        self.driver.get("https://useinsider.com/careers/quality-assurance/")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.see_all_qa_jobs)
        ).click()

    def filter_jobs(self, location, department):
        print("Filtering jobs...")

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "select2-filter-by-location-container"))
        ).click()
        time.sleep(1)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[normalize-space(text())='{location}']"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "select2-filter-by-department-container"))
        ).click()
        time.sleep(1)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[normalize-space(text())='{department}']"))
        ).click()

        print(f"Filters applied: {location}, {department}")

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "position-list-item"))
        )
        jobs = self.driver.find_elements(By.CLASS_NAME, "position-list-item")
        print(f"{len(jobs)} job postings found.")
        return [JobCard(job) for job in jobs]

class JobCard:
    def __init__(self, element):
        self.position = element.find_element(By.CLASS_NAME, "position-title").text
        self.department = element.find_element(By.CLASS_NAME, "position-department").text
        self.location = element.find_element(By.CLASS_NAME, "position-location").text

    def __repr__(self):
        return f"{self.position} | {self.department} | {self.location}"
