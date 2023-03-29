import os
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

service = ChromeService(executable_path=ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
chrome_options.set_capability(
    "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
)
driver = webdriver.Chrome(options=chrome_options, service=service)

driver.get("https://www.lambdatest.com/")

logo_header = driver.find_element(
    by=By.XPATH, value='//*[@id="header"]/nav/div/div/div[1]/div/div/a'
)
logo_header.click()

platform_header = driver.find_element(by=By.LINK_TEXT, value="Platform")
platform_header.click()

enterprise_header = driver.find_element(by=By.LINK_TEXT, value="Enterprise")
enterprise_header.click()

# resources_header = driver.find_element(by=By.LINK_TEXT, value="Resources")
# developers_header = driver.find_element(by=By.LINK_TEXT, value="Developers")

pricing_header = driver.find_element(by=By.LINK_TEXT, value="Pricing")
pricing_header.click()

login_header = driver.find_element(by=By.LINK_TEXT, value="Login")
login_header.click()

driver.back()
signup_header = driver.find_element(by=By.LINK_TEXT, value="Sign Up")
signup_header.click()

# Get the network logs
logs = driver.get_log("performance")  # list of dictionaries

# Check if the file already exists
if os.path.isfile("../app/static/network_logs.json"):
    # Get the current number of runs from the network logs file
    with open("../app/static/network_logs.json", "r") as logs_file:
        new_logs = json.load(logs_file)
    run_id = len(new_logs) + 1  # Assign a unique ID for this run
else:
    new_logs = []
    run_id = 1

# Filter the logs
filtered_logs = []
for log in logs:
    log_entry = json.loads(log["message"])["message"]
    if (
        "Network.requestWillBeSent" in log_entry["method"]
        or "Network.responseReceived" in log_entry["method"]
    ):
        filtered_logs.append(log_entry["params"])

# Add the logs to the list with the run ID
new_logs.append({"id": run_id, "logs": filtered_logs})

# Write the filtered logs to a JSON file
with open("../app/static/network_logs.json", "w") as logs_file:
    json.dump(new_logs, logs_file, indent=4, default=str)

driver.quit()
