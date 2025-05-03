from ecommerce import ECommerceDataExtraction
import time
def main():
    extractor = ECommerceDataExtraction()
    
    try:
        extractor.load_json_data(file_path="source_xpath.json")
        extractor.setup_browser()
        extractor.apply_search_filters()
        time.sleep(1)
        extractor.extract_data(output_file="PhoneData.txt")
    except Exception as e:
        print("Something went wrong in the runner:", e)

if __name__ == "__main__":
    main()
