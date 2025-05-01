
from util import SeleniumActions
import time, json, os, re

if __name__ == "__main__":
    
    try:
        # Starting the selenium webdriver
        SeleniumPlayer = SeleniumActions()
        # Open JSON FILE
        with open("source_xpath.json", "r") as file:
            source_xpath = json.load(file)

        
        SeleniumPlayer.open_url(source_xpath.get("url"))
        SeleniumPlayer.wait_for_element(source_xpath.get("search_box"))
        # Start searching your desired mobile specs
        SeleniumPlayer.fill_and_submit(source_xpath.get("search_box"), "Mobile Phone 32 gb RAM 512 GB ROM 100 GB Camera") 
        # Open a Fiel to store these details
        with open("PhoneData.txt", "a") as file:
            file.write("Data Extracted for the phones are:")
            all_mobile_xpath=source_xpath.get("elements")
            for index in range(1, 10):
                result = SeleniumPlayer.get_text(f"{all_mobile_xpath}[{index}]")
                time.sleep(1)
                file.write(result+"\n\n")
    except Exception as e:
        print("Error during automation:", e)
    finally:
        time.sleep(5)
        SeleniumPlayer.close_browser()
