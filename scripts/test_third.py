from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import numpy.random as random


# create the Safari webdriver
driver = webdriver.Safari()
# open the verification page
driver.get("http://localhost:3000")

for _ in range(13):
    # wait for a while to make sure the button is loaded
    wait = WebDriverWait(driver, 1)
    # find the verify button
    verify_button = driver.find_element_by_xpath("//div[@class='border-2 w-8 h-8 rounded-lg cursor-pointer bg-white flex justify-center items-center']")
    # check if the button is clickable
    if verify_button.is_enabled() and verify_button.is_displayed(): print("the button is clickable")
    else: print("the button is not clickable")
    # create an ActionChains object
    driver.execute_script("var evt = document.createEvent('MouseEvents');"
                        "evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);"
                        "arguments[0].dispatchEvent(evt);", verify_button)
    sleep(4)

    # find the verify button for the third verfication
    verify_button = driver.find_element_by_xpath("//div[@class='w-80 h-80 bg-contain relative']")
    # check if the button is clickable
    if verify_button.is_enabled() and verify_button.is_displayed(): print("the button is clickable")
    else: print("the button is not clickable")
    # get the position and size of the button
    location = verify_button.location
    size = verify_button.size
    # compute the center of the button
    center_x = location['x'] + size['width'] / 2
    center_y = location['y'] + size['height'] / 2
    # use javascript to click the button
    for i in range(4):
        # randomly choose one point inside the area of the element
        click_x = center_x + random.randint(-size['width'] / 2, size['width'] / 2)
        click_y = center_y + random.randint(-size['height'] / 2, size['height'] / 2)
        driver.execute_script(f"var evt = document.createEvent('MouseEvents');"
                            f"evt.initMouseEvent('click', true, true, window, 0, 0, 0, {click_x}, {click_y}, false, false, false, false, 0, null);"
                            f"arguments[0].dispatchEvent(evt);", verify_button)

    # wait for the alert to appear
    wait = WebDriverWait(driver, 1)
    alert = wait.until(EC.alert_is_present())
    # accept the alert
    alert = driver.switch_to.alert
    alert.accept()

# wait for a while to quit
sleep(6)
driver.quit()
