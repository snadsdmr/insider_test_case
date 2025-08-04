import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from utils.screenshot import take_screenshot
import traceback

@pytest.fixture
def driver():
    service = Service("C:/tools/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_qa_jobs_filter(driver):
    try:
        driver.get("https://useinsider.com/")
        home_page = HomePage(driver)

        driver.get("https://useinsider.com/careers/")
        careers_page = CareersPage(driver)
        careers_page.go_to_quality_assurance()

        qa_jobs = careers_page.filter_jobs("Istanbul, Turkiye", "Quality Assurance")

        for job in qa_jobs:
            assert "Quality Assurance" in job.position
            assert job.department == "Quality Assurance"
            assert job.location == "Istanbul, Turkiye"

    except Exception as e:
        print("Test failed. Taking screenshot and saving error log...")
        take_screenshot(driver, "test_failure_screenshot")

        with open("error_log.txt", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())  # Hatanın detaylı traceback’ini dosyaya yaz

        raise e
