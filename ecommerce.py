from util import SeleniumActions
import time, json, os, re

class ECommerceDataExtraction:
    """
    Automates the extraction of mobile phone data from an e-commerce website
    using Selenium. It loads XPaths from a JSON file, applies
    filters based on specific criteria, and saves the extracted results to a text file.
    """

    def __init__(self):
        """
        Set up Selenium player and prepare storage for XPath config.
        """
        self.SeleniumPlayer = SeleniumActions()
        self.source_xpath = {}

    def load_json_data(self, file_path="source_xpath.json"):
        """
        Load XPath and URL config from JSON file.

        Args:
            file_path (str): Path to the config JSON file.
        """
        with open(file_path, "r") as file:
            self.source_xpath = json.load(file)

    def setup_browser(self):
        """
        Launches the Selenium-controlled browser and navigates to the URL defined in the JSON data.
        """
        self.SeleniumPlayer.open_url(self.source_xpath.get("url"))

    def apply_search_filters(self):
        """
        Fill search box and apply product filters.
        """
        try:
            self.SeleniumPlayer.wait_for_element(self.source_xpath.get("search_box"))
            # Search for specific mobile specs
            self.SeleniumPlayer.fill_and_submit(self.source_xpath.get("search_box"), 
            "Mobile Phone 32 gb RAM 512 GB ROM 100 GB Camera")
            
            # Select 4-star ratings and above
            self.SeleniumPlayer.click(self.source_xpath.get("rating4"))
            time.sleep(1)

            # Filter by 256 GB storage
            self.SeleniumPlayer.click(self.source_xpath.get("expand_filter").replace('Primary Camera', 'Internal Storage'))
            time.sleep(1)
            self.SeleniumPlayer.click(self.source_xpath.get("Internal_Storage"))
            time.sleep(1)

            # Filter by 64 MP camera
            self.SeleniumPlayer.click(self.source_xpath.get("expand_filter"))
            time.sleep(1)
            self.SeleniumPlayer.click(self.source_xpath.get("Primary_camera"))
        except Exception as e:
            print("Error during Applying Search Filters:", e)
        finally:
            time.sleep(5)
            self.SeleniumPlayer.close_browser()

    def run_settings(self):
        """
        Load config, open browser, and apply filters.
        """
        try:
            self.load_json_data()
            self.setup_browser()
            # Wait for the search box to show up
            self.SeleniumPlayer.wait_for_element(self.source_xpath.get("search_box"))
        except Exception as e:
            print("Error during Search Settings:", e)
        finally:
            time.sleep(5)
            self.SeleniumPlayer.close_browser()

    def extract_data(self, output_file="PhoneData.txt"):
        """
        Extracts product data from the search results and writes it to a text file.

        Args:
            output_file (str): Path to the output file where extracted data will be saved.
        """
        try:
            # Save the results to a text file
            with open(output_file, "a", encoding='utf-8') as file:
                file.write("Data Extracted for the phones are:")
                all_mobile_xpath = self.source_xpath.get("elements")
                for index in range(1, 10):
                    result = self.SeleniumPlayer.get_text(f"({all_mobile_xpath})[{index}]")
                    time.sleep(1)
                    file.write(result + "\n\n")
        except Exception as e:
            print("Error during Data Extraction Process:", e)
        finally:
            time.sleep(5)
            self.SeleniumPlayer.close_browser()
