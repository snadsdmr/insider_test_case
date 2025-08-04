def take_screenshot(driver, name="test_failed_step"):
    driver.save_screenshot(f"{name}.png")
