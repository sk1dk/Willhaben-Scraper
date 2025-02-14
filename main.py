import requests
import re
import os
import sys
from PIL import Image

base_url = input("Enter the URL: ").strip()
if "?" in base_url:
    base_url = base_url.split("?")[0]

fixed_params = "&rows=1000&periode=2"
price_from = input("Enter minimum price: ").strip()
price_to = input("Enter maximum price: ").strip()
full_url = f"{base_url}?sfId=85ec0b3c-fb9a-4f5b-a646-aeb41554f901&isNavigation=true{fixed_params}&PRICE_FROM={price_from}&PRICE_TO={price_to}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

saved_posts = 0
skipped_posts = 0
exif_removed = 0

def remove_exif(image_path):
    global exif_removed
    try:
        with Image.open(image_path) as img:
            img_without_exif = Image.new(img.mode, img.size)
            img_without_exif.putdata(list(img.getdata()))
            img_without_exif.save(image_path, format="JPEG")
            exif_removed += 1
    except Exception as e:
        print(f"❌ Error removing EXIF: {e}")

response = requests.get(full_url, headers=headers)

if response.status_code == 200:
    page_content = response.text
    ids = re.findall(r'"id":"(\d+)"', page_content)
    seo_urls = {m[0]: m[1] for m in re.findall(r'"id":"(\d+)".*?{"name":"SEO_URL","values":\["(.*?)"\]}', page_content)}
    headings = {m[0]: m[1] for m in re.findall(r'"id":"(\d+)".*?{"name":"HEADING","values":\["(.*?)"\]}', page_content)}
    prices = {m[0]: m[1] for m in re.findall(r'"id":"(\d+)".*?{"name":"PRICE_FOR_DISPLAY","values":\["(.*?)"\]}', page_content)}
    image_urls = {m[0]: m[1] for m in re.findall(r'"id":"(\d+)".*?"mainImageUrl":"(https:[^"]+)"', page_content)}
    all_images_data = {m[0]: m[1] for m in re.findall(r'"id":"(\d+)".*?"name":"ALL_IMAGE_URLS","values":\["(.*?)"\]}', page_content)}
    biographies = {m[0]: m[1] for m in re.findall(r'"id":"(\d+)".*?"name":"BODY_DYN","values":\["(.*?)"\]}', page_content)}

    for item_id in ids:
        if item_id in seo_urls and item_id in headings and item_id in prices and item_id in all_images_data and item_id in biographies:
            heading = headings[item_id]

            if len(heading.split()) < 4:
                skipped_posts += 1
                continue

            seo_url = seo_urls[item_id]
            price = prices[item_id]
            biography = biographies[item_id]
            all_images = all_images_data[item_id].split(";")

            if len(all_images) != 4:
                skipped_posts += 1
                continue

            folder_name = heading.replace("/", "-").replace("\\", "-").strip()
            os.makedirs(folder_name, exist_ok=True)

            info_file_path = os.path.join(folder_name, "information.txt")
            with open(info_file_path, "w", encoding="utf-8") as info_file:
                info_file.write(f"ID: {item_id}\n")
                info_file.write(f"SEO_URL: {seo_url}\n")
                info_file.write(f"PRICE: {price}\n")
                info_file.write(f"Biography: {biography}\n")

            for index, image_path in enumerate(all_images):
                full_image_url = f"https://cache.willhaben.at/mmo/{image_path}"
                image_file_path = os.path.join(folder_name, f"image_{index+1}.jpg")
                
                image_response = requests.get(full_image_url, headers=headers)
                if image_response.status_code == 200:
                    with open(image_file_path, "wb") as img_file:
                        img_file.write(image_response.content)
                    remove_exif(image_file_path)

            saved_posts += 1

        else:
            skipped_posts += 1

        sys.stdout.write(f"\r🔥 Posts saved: {saved_posts} | ⭐️ Posts skipped: {skipped_posts} | 😇 Exif Cleaned: {exif_removed}   ")
        sys.stdout.flush()

else:
    print(f"\n❌ Failed to retrieve data. Status code: {response.status_code}")
