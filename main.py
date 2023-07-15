import sys
import time

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException



def get_transcript(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        show_more_button = driver.find_element(By.CSS_SELECTOR, ".more-button")
        driver.execute_script("arguments[0].click();", show_more_button)
    except NoSuchElementException:
        print("No 'Show More' button found.")

    try:
        show_more_button = driver.find_element(By.CSS_SELECTOR, ".ytp-button.ytp-subtitles-button")
        show_more_button.click()
    except NoSuchElementException:
        print("No transcription button found!")

    try:
        transcript_element = driver.find_element(By.CSS_SELECTOR, ".ytp-transcript-content")
        transcript = transcript_element.text
        print(transcript)
    except NoSuchElementException:
        print("No transcript found.")

    time.sleep(5)  # wait to let user see what is going on
    time.sleep(10)

def main():
    # function that parses input arguments, calls appropriate methods
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", help="Specify the url for video containing transcript",
                        metavar="URL")
    args = parser.parse_args()

    if args.url is None:
        print("Please specify URL")
        print("Use the -h to see usage information")
        sys.exit(2)
    else:
        url = args.url
        get_transcript(url)


if __name__ == "__main__":
    main()
