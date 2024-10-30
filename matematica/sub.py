import os
import requests
from bs4 import BeautifulSoup

# Base URL and year range
base_url = "https://subiectebac.ro/mate/mate_"
years = range(2014, 2025)  # 2009 to 2024

# Define the categories and session folders
categories = {
    "mate-info": ["vara", "toamna", "speciala", "simulare", "model"],
    "stiinte-ale-naturii": ["vara", "toamna", "speciala", "simulare", "model"],
    "tehnologic": ["vara", "toamna", "speciala", "simulare", "model"],
    "pedagogic": ["vara", "toamna", "speciala", "simulare", "model"]
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
    sections = soup.find_all("h1")

    # Process each category section in the page
    for section in sections:
        category = section.text.strip().lower().replace(" ", "-")
        
        # Verify that the category is valid
        if category not in categories:
            continue
        
        # Find all links within this category
        session_links = section.find_next_sibling("ul").find_all("a")
        for link in session_links:
            session_name = link.text.lower()
            
            # Determine session folder based on session name
            session_folder = next((s for s in categories[category] if s in session_name), None)
            if not session_folder:
                continue
            
            # Define file name (subiect or barem) based on link text
            file_name = "subiect.pdf" if "barem" not in session_name else "barem.pdf"
            
            # Full URL for the PDF and local folder structure
            pdf_url = f"{page_url.rsplit('/', 1)[0]}/{link['href']}"
            folder_path = os.path.join(str(year), category, session_folder)
            os.makedirs(folder_path, exist_ok=True)
            
            # Download the PDF into the correct folder
            download_pdf(pdf_url, os.path.join(folder_path, file_name))
