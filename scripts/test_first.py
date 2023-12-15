from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


for i in range(10):

    # create the Safari webdriver
    driver = webdriver.Safari()
    # open the verification page
    driver.get("http://localhost:3000")

    # find the verify button
    verify_button = driver.find_element_by_xpath("//div[@class='border-2 w-8 h-8 rounded-lg cursor-pointer bg-white flex justify-center items-center']")
    # wait for a while to make sure the button is loaded
    sleep(1)

    # check if the button is clickable
    if verify_button.is_enabled() and verify_button.is_displayed(): print("the button is clickable")
    else: print("the button is not clickable")

    # create an ActionChains object
    actions = ActionChains(driver)
    # move the mouse to the button
    actions.move_to_element(verify_button)
    # calculate the mouse movement
    driver.execute_script("arguments[0].click();", verify_button)
    driver.execute_script("arguments[0].click();", verify_button)

    # wait for a while to quit
    sleep(3)
    driver.quit()
