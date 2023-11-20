import requests
from bs4 import BeautifulSoup

# Function to scrape URLs for videos and photos from different platforms
def scrape_urls(url, platform):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find URLs based on the platform
        if platform == 'example':
            # Find all <img> tags and extract the 'src' attribute
            img_tags = soup.find_all('img')
            img_urls = [img['src'] for img in img_tags]

            # Find all <video> tags and extract the 'src' attribute
            video_tags = soup.find_all('video')
            video_urls = [video['src'] for video in video_tags]

        elif platform == 'instagram':
            # Find all <img> tags within <div> tags with class 'KL4Bh'
            img_tags = soup.select('div.KL4Bh img')
            img_urls = [img['src'] for img in img_tags]

            # Find all <video> tags within <div> tags with class 'tWeCl'
            video_tags = soup.select('div.tWeCl video')
            video_urls = [video['src'] for video in video_tags]

        elif platform == 'tiktok':
            # Find all <img> tags within <div> tags with class 'tiktok-embed'
            img_tags = soup.select('div.tiktok-embed img')
            img_urls = [img['src'] for img in img_tags]

            # Find all <video> tags within <div> tags with class 'tiktok-embed'
            video_tags = soup.select('div.tiktok-embed video')
            video_urls = [video['src'] for video in video_tags]

        else:
            print("Invalid platform.")
            return [], []

        # Return the URLs for videos and photos
        return video_urls, img_urls
    else:
        print("Failed to retrieve webpage.")
        return [], []

# Example usage
url = "https://example.com"
platform = "example"  # Replace with 'instagram' or 'tiktok' to scrape URLs from those platforms
video_urls, img_urls = scrape_urls(url, platform)
print("Video URLs:", video_urls)
print("Image URLs:", img_urls)
