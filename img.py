import os
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Setup
ACCESS_KEY = "oneksKmAl00U7hxyRuHW5mBmMh-rbbRK0hPp-lZwfBJ6xrMk"

# Expanded categories
categories = [
    "luxury-car", "superbike", "jet", "ferrari", "lamborghini", "porsche",
    "bugatti", "rolls-royce", "bmw-m", "audi-rs", "mercedes-amg", 
    "rolex", "patek philippe", "audemars piguet", "richard mille", 
    "luxury-villas", "modern-mansion", "private-jet", "yacht", "superyacht",
    "luxury-watch", "luxury-interior", "exotic-car", "sports-car"
]

num_images = 3000# Number of images to fetch
max_threads = 15   # Parallel downloads

# Create folder to save images
os.makedirs("luxury_images", exist_ok=True)

# Function to download a single image
def download_image(i):
    category = categories[i % len(categories)]
    url = f"https://api.unsplash.com/photos/random?query={category}&client_id={ACCESS_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            image_url = response.json()["urls"]["regular"]
            img_data = requests.get(image_url).content
            with open(f"luxury_images/{category.replace(' ', '_')}_{i+1}.jpg", "wb") as img_file:
                img_file.write(img_data)
            return True
    except Exception as e:
        print(f"Failed to download image {i+1}: {e}")
        return False

# Download images concurrently
with ThreadPoolExecutor(max_threads) as executor:
    results = list(tqdm(executor.map(download_image, range(num_images)), total=num_images, desc="Downloading images"))

print(f"✅ Download completed! {results.count(True)} images downloaded successfully.")
