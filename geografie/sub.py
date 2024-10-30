import os
import requests
from bs4 import BeautifulSoup

# Base URL and year range
base_url = "https://subiectebac.ro/geo/geo_"
years = range(2008, 2025)  # 2009 to 2024

# Define session names based on file types
sessions = {
    "sesiunea de vara": "vara",
    "sesiunea de toamna": "toamna",
    "sesiunea speciala": "speciala",
    "simulare": "simulare",
    "model": "model"
}

# Function to download a PDF
def download_pdf(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Loop through each year
for year in years:
    # Get the HTML for the year page
    page_url = f"{base_url}{year}.html"
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to retrieve page for {year}")
        continue
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    session_links = soup.find("ul", class_="lista").find_all("a")

    # Process each link
    for link in session_links:
        session_name = link.text.lower()
        
        # Identify the session folder
        session_folder = next((folder for key, folder in sessions.items() if key in session_name), None)
        if not session_folder:
            continue

        # Determine file type (subiect or barem)
        file_type = "subiect.pdf" if "barem" not in session_name else "barem.pdf"
        
        # Full URL for the PDF and local folder structure
        pdf_url = f"{page_url.rsplit('/', 1)[0]}/{link['href']}"
        folder_path = os.path.join(str(year), session_folder)
        os.makedirs(folder_path, exist_ok=True)
        
        # Download the PDF into the correct folder
        download_pdf(pdf_url, os.path.join(folder_path, file_type))
