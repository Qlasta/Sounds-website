import requests
from api_manager import generate_random_sound, authorize, download_sound
BASE_URL = "https://freesound.org"
user_token = "CMUuZMbE7Ed6az4rnZAQ3OOK8HRmGf"
API_KEY = "X8bWmDASLK2XjTdIY97bFfeo5fJgVR1mrylEPipb"

headers_for_download = {"Authorization": f"Bearer {user_token}"}
# Get the file of the sound
download = requests.get(f"{BASE_URL}/apiv2/sounds/3214/download/", headers=headers_for_download)
# Save downloaded file
with open(f"static/sounds/naujas.wav", "wb") as file:
    file.write(download.content)
    print("done")

print(generate_random_sound())


