from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# ===== CONFIG =====
SHEET_NAME = "Planilha Guild Vatoz Lokoz"

# ===== GOOGLE AUTH =====
creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

sheet = client.open(SHEET_NAME).sheet1

# ===== SELENIUM =====
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

driver.get("https://rubinot.com.br/guilds/Vatoz%20Lokoz")

time.sleep(5)

rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

data = []

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 4:
        data.append([
            cols[0].text,
            cols[1].text,
            cols[2].text,
            cols[3].text
        ])

driver.quit()

# ===== ENVIO =====
sheet.clear()
sheet.update("A1", [["Rank", "Points", "Name", "Level"]])
sheet.update("A2", data)

print("Atualizado com sucesso!")
