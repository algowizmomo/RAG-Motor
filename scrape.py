import os
import requests

# Create the directory if it doesn't exist
if not os.path.exists("notifications_dir"):
    os.makedirs("notifications_dir")

# Read the URLs from urls.txt
with open("urls.txt", "r") as url_file:
    urls = url_file.read().splitlines()

# Download PDFs from the URLs
for url in urls:
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Extract the filename from the URL
            filename = url.split("filename=")[1]
            filename = os.path.join("notifications_dir", filename)
            with open(filename, 'wb') as pdf_file:
                for chunk in response.iter_content(1024):
                    pdf_file.write(chunk)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {url}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

