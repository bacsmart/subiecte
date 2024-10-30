import os
import requests
from bs4 import BeautifulSoup

# Base URL and range of years
base_url = "https://subiectebac.ro/info/info_"
years = range(2017, 2018)  # 2009 to 2024

# Folder structure definition
folders = {
    "info": ["vara", "toamna", "speciala", "simulare", "model"],
    "stiinte": ["vara", "toamna", "speciala", "simulare", "model"]
}

# Download function
def download_pdf(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Main loop for each year
for year in years:
    # Fetch the HTML page for the given year
    page_url = f"{base_url}{year}.html"
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to retrieve page for {year}")
        continue
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    sections = soup.find_all("h1")

    # Process each category in the page (Mate-Info and Stiintele Naturii)
    for section in sections:
        category = "info" if "Mate-Info" in section.text else "stiinte"
        
        session_links = section.find_next_sibling("ul").find_all("a")
        for link in session_links:
            session_name = link.text.lower()

            # Determine folder name based on session
            session_folder = next((s for s in folders[category] if s in session_name), None)
            if not session_folder:
                continue

            # Define file name based on link text
            file_name = "subiect.pdf" if "barem" not in session_name else "barem.pdf"
            
            # Create the full URL for the PDF and local folder structure
            pdf_url = f"{page_url.rsplit('/', 1)[0]}/{link['href']}"
            folder_path = os.path.join(str(year), category, session_folder)
            os.makedirs(folder_path, exist_ok=True)
            
            # Download the PDF into the correct folder
            download_pdf(pdf_url, os.path.join(folder_path, file_name))
