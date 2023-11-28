from selenium import webdriver
import os
import time
os.environ.PATH = os.environ.get('PATH', "")+":/home/monisha/chromedriver"
# # Path to your web driver (e.g., ChromeDriver or GeckoDriver)
# driver_path = 'path_to_your_webdriver'

# URL of the page where you want to input text and submit
url = 'https://chat.openai.com/'

# Directory containing your text files
directory = 'sample_data'

opts = webdriver.ChromeOptions() 
 
# Adding argument to disable the AutomationControlled flag 
opts.add_argument("--disable-blink-features=AutomationControlled") 
 
# Exclude the collection of enable-automation switches 
opts.add_experimental_option("excludeSwitches", ["enable-automation"]) 
 
# # Turn-off userAutomationExtension 
opts.add_experimental_option("useAutomationExtension", False) 


# Initialize the web driver
driver = webdriver.Chrome(options=opts)
driver.get(url)
input()
# Iterate through files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)

        # Read the content of the file
        with open(file_path, 'r') as file:
            file_content = file.read()

        # Find the textarea and submit button by XPath
        textarea = driver.find_element_by_xpath('//*[@id="prompt-textarea"]')
        submit_button = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/form/div/div[2]/div/button')

        # Clear the textarea, input the file content, and click the submit button
        textarea.clear()
        textarea.send_keys(file_content)
        submit_button.click()

        # Wait for some time if needed (e.g., for page reload, response, etc.)
        time.sleep(2)

# Close the browser when done
driver.quit()
