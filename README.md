# **Web Scraper for Image and Data Extraction on Willhaben.at**  

This script extracts item data and images from a specified URL while removing EXIF metadata from downloaded images.  

## **Features**  
- Scrapes item data including ID, post URL, price, and biography.  
- Downloads and organizes images into folders based on item names.  
- Removes EXIF metadata from images for privacy.  
- Provides real-time status updates on saved and skipped posts.  

## **Requirements**  
Make sure you have Python installed along with the required dependencies:  

```sh
pip install requests pillow
```

## **Usage**  

1. **Clone the Repository**  
   ```sh
   git clone (https://github.com/sk1dk/Willhaben-Scraper)
   cd WillHaben-Scraper
   ```

2. **Run the Script**  
   ```sh
   python main.py
   ```

3. **Provide Input**  
   - Enter the base URL when prompted.  
   - Input minimum and maximum price values.  

## **What does it do?**  

- **Extracts** relevant data (ID, Post URL, price, heading, images, biography).  
- **Filters** items based on conditions (e.g., minimum words in the heading, image count).  
- **Downloads & Saves** images into item-specific folders.  
- **Removes EXIF Metadata** from images for privacy.  
- **Displays** real-time stats on saved, skipped posts, and cleaned EXIF images.  

## **Folder Structure**  

```
repository-name/
│-- scraper.py
│-- README.md
│-- requirements.txt
│-- data/  (Each item's folder with images and info file)
```

## **Example Output**  

```
🔥 Posts saved: 10 | ⭐️ Posts skipped: 3 | 😇 Exif Cleaned: 10   
```

## **License**  
Feel free to modify and distribute.  
