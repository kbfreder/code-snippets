import requests
import os
from dotenv import load_dotenv, find_dotenv
import base64


SITE_URL = "https://ultimatehall.org"
wp_url = f"{SITE_URL}/wp-json/"

load_dotenv(find_dotenv)

USERNAME = os.getenv("USERNAME")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# base64_encode( $username . ':' . $password )
un_pw_enc = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}")

header = {
    "Content-Type": "application/json",
    "Authorization": "Basic {un_pw_enc}"
}

response = requests.get(wp_url, headers=header)
output = response.json()

print(output)