import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from utils.screenshot import take_screenshot
import traceback
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    # Set Chrome options to disable notification pop-ups
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })
    
    service = Service("C:/tools/chromedriver.exe")
    # Pass the configured options to the WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_qa_jobs_filter(driver):
    try:
        home_page = HomePage(driver)
        home_page.open()
        # Navigate to the careers page from the menu
        home_page.go_to_careers()

        careers_page = CareersPage(driver)
        # Assert that the careers page is opened successfully
        assert careers_page.is_open(), "Careers page did not open"
        # Assert that the location, teams, and life blocks are visible on the page
        assert careers_page.blocks_are_visible(), "Locations/Teams/Life blocks are not visible"
        
        careers_page.go_to_quality_assurance()

        # Filter the job listings for a specific location and department
        qa_jobs = careers_page.filter_jobs("Istanbul, Turkiye", "Quality Assurance")

        # Verify each job card's position, department, and location
        for job in qa_jobs:
            assert "Quality Assurance" in job.position
            assert job.department == "Quality Assurance"
            assert job.location == "Istanbul, Turkiye"

    except Exception as e:
        print("Test failed. Taking screenshot and saving error log...")
        # Save a screenshot of the failure state
        take_screenshot(driver, "test_failure_screenshot")

        # Write the detailed traceback to a log file
        with open("error_log.txt", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())

        raise e
