import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os

# List of Unsplash URLs to scrape
urls = [
    "https://unsplash.com/s/photos/luxurycars?license=free",
    "https://unsplash.com/s/photos/bmw?license=free",
    "https://unsplash.com/s/photos/rollsroyce?license=free",
    "https://unsplash.com/s/photos/gucci?license=free",
    "https://unsplash.com/s/photos/luxurywatch?license=free",
    "https://unsplash.com/s/photos/villas?license=free",
    "https://unsplash.com/s/photos/superbike?license=free",
    "https://unsplash.com/s/photos/luxurybike?license=free",
    "https://unsplash.com/s/photos/helicopter?license=free",
    "https://unsplash.com/s/photos/privatejet?license=free",
    "https://unsplash.com/s/photos/yacht?license=free",
    "https://unsplash.com/s/photos/luxury-handbags?license=free",
    "https://unsplash.com/s/photos/perfume?license=free",
    "https://unsplash.com/s/photos/luxurybuildings?license=free",
    "https://unsplash.com/s/photos/car-logos?license=free"
]

# Set up the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no browser UI)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Create a directory to save images
os.makedirs("unsplash_images", exist_ok=True)

image_count = 0
max_images = 2500

try:
    for url in urls:
        if image_count >= max_images:
            break
        
        print(f"Opening URL: {url}")
        driver.get(url)
        time.sleep(5)  # Allow time for the page to load

        # Scroll to the bottom to load more images
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(20):  # More scrolling for more images
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

        # Find all image elements
        img_elements = driver.find_elements(By.TAG_NAME, "img")

        # Download images
        for img in img_elements:
            if image_count >= max_images:
                break

            img_url = img.get_attribute("src")
            if img_url and "images.unsplash.com" in img_url:
                try:
                    img_data = requests.get(img_url).content
                    with open(f"unsplash_images/image_{image_count}.jpg", "wb") as img_file:
                        img_file.write(img_data)
                    print(f"Downloaded: image_{image_count}.jpg")
                    image_count += 1
                except Exception as e:
                    print(f"Failed to download image: {e}")

finally:
    driver.quit()

print(f"Downloaded {image_count} images!")
