import os
import requests
from bs4 import BeautifulSoup

# HTML content
html_content = """<div class="content">
        <h2>2019</h2>
        <h1>Mate-Info</h1>
        <ul class="lista">
            <li><a href="2019/E_d_Informatica_2019_sp_MI_C_var_04_LRO.pdf" class="link" target="_blank">Sesiunea de vara</a></li>
            <li><a href="2019/E_d_Informatica_2019_sp_MI_bar_04_LRO.pdf" class="link" target="_blank">Barem Sesiunea de vara</a></li><br><br>
            <li><a href="2019/E_d_Informatica_2019_sp_MI_C_var_02_LRO.pdf" class="link" target="_blank">Sesiunea de toamna</a></li>
            <li><a href="2019/E_d_Informatica_2019_sp_MI_bar_02_LRO.pdf" class="link" target="_blank">Barem Sesiunea de toamna</a></li><br><br>
            <li><a href="2019/E_d_Informatica_2019_sp_MI_C_var_01_LRO.pdf" class="link" target="_blank">Sesiunea speciala</a></li>
            <li><a href="2019/E_d_Informatica_2019_sp_MI_bar_01_LRO.pdf" class="link" target="_blank">Barem Sesiunea speciala</a></li><br><br>
            <li><a href="2019/E_d_Informatica_2019_sp_MI_C_var_simulare_LRO.pdf" class="link" target="_blank">Simulare Clasa a XII-a</a></li>
            <li><a href="2019/E_d_Informatica_2019_sp_MI_bar_simulare_LRO.pdf" class="link" target="_blank">Barem Simulare Clasa a XII-a</a></li><br><br>
            <li><a href="2019/E_d_Informatica_2019_sp_MI_C_var_model_LRO.pdf" class="link" target="_blank">Model</a></li>
            <li><a href="2019/E_d_Informatica_2019_sp_MI_bar_model_LRO.pdf" class="link" target="_blank">Barem Model</a></li>
        </ul><br><br>
        <h1>Stiintele naturii</h1>
        <ul class="lista">
            <li><a href="2019/E_d_Informatica_2019_sp_SN_C_var_04_LRO.pdf" class="link" target="_blank">Sesiunea de vara</a></li>
            <li><a href="2019/E_d_Informatica_2019_sp_SN_bar_04_LRO.pdf" class="link" target="_blank">Barem Sesiunea de vara</a></li><br><br>
            <li><a href="2019/E_d_Informatica_2019_sp_SN_C_var_02_LRO.pdf" class="link" target="_blank">Sesiunea de toamna</a></li>
            <li><a href="2019/E_d_Informatica_2019_sp_SN_bar_02_LRO.pdf" class="link" target="_blank">Barem Sesiunea de toamna</a></li><br><br>
            <li><a href="2019/E_d_Informatica_2019_sp_SN_C_var_01_LRO.pdf" class="link" target="_blank">Sesiunea speciala</a></li>
            <li><a href="2019/E_d_Informatica_2019_sp_SN_bar_01_LRO.pdf" class="link" target="_blank">Barem Sesiunea speciala</a></li><br><br>
            <li><a href="2019/E_d_Informatica_2019_sp_SN_C_var_simulare_LRO.pdf" class="link" target="_blank">Simulare Clasa a XII-a</a></li>
            <li><a href="2019/E_d_Informatica_2019_sp_SN_bar_simulare_LRO.pdf" class="link" target="_blank">Barem Simulare Clasa a XII-a</a></li><br><br>
            <li><a href="2019/E_d_Informatica_2019_sp_SN_C_var_model_LRO.pdf" class="link" target="_blank">Model</a></li>
            <li><a href="2019/E_d_Informatica_2019_sp_SN_bar_model_LRO.pdf" class="link" target="_blank">Barem Model</a></li>
        </ul><br><br>
    </div>"""  # Replace this with the full HTML content

# Parsing HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Base URL to prepend to links if needed
base_url = "https://subiectebac.ro/info/"  # Replace with actual base URL

# Define folder structure for each category and session
folders = {
    "info": {
        "vara": [],
        "toamna": [],
        "speciala": [],
        "simulare": [],
        "model": []
    },
    "stiinte": {
        "vara": [],
        "toamna": [],
        "speciala": [],
        "simulare": [],
        "model": []
    }
}


# Helper function to create folder and download file
def download_pdf(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we get a valid response
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {save_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")


# Organize links based on sessions and categories
for section in soup.find_all("h1"):
    category = "info" if section.text == "Mate-Info" else "stiinte"

    session_links = section.find_next_sibling("ul").find_all("a")
    for link in session_links:
        session_name = link.text.lower()

        # Determine folder name based on session
        if "vara" in session_name:
            session_folder = "vara"
        elif "toamna" in session_name:
            session_folder = "toamna"
        elif "speciala" in session_name:
            session_folder = "speciala"
        elif "simulare" in session_name:
            session_folder = "simulare"
        elif "model" in session_name:
            session_folder = "model"
        else:
            continue  # Skip any unexpected link

        # Define the file name (subiect.pdf or barem.pdf) based on the link text
        file_name = "subiect.pdf" if "barem" not in session_name else "barem.pdf"

        # Construct full URL for downloading
        pdf_url = base_url + link['href']

        # Create directories
        folder_path = os.path.join(category, session_folder)
        os.makedirs(folder_path, exist_ok=True)

        # Download the PDF into the correct folder
        download_pdf(pdf_url, os.path.join(folder_path, file_name))
