from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pyautogui


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

# # get the position of the button
# x, y = verify_button.location['x'], verify_button.location['y']
# # get the current position of the mouse
# current_x, current_y = pyautogui.position()
# # calculate the mouse movement
# distance_x = x - current_x
# distance_y = y - current_y
# # move the mouse to the button
# pyautogui.moveTo(current_x + distance_x, current_y + distance_y, duration=5)


# wait for a while
sleep(1)
# use javascript to click the button
driver.execute_script("var evt = document.createEvent('MouseEvents');"
                      "evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);"
                      "arguments[0].dispatchEvent(evt);", verify_button)

# 等待一段时间
sleep(6)

driver.quit()
