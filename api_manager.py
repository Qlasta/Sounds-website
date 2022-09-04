import requests
import random
from bs4 import BeautifulSoup
import os

# Documentation: https://freesound.org/docs/api/authentication.html#oauth-authentication
BASE_URL = "https://freesound.org"
API_KEY = os.environ["API_KEY"]
CLIENT_ID = os.environ["CLIENT_ID"]
USERNAME = os.environ["FREESOUND_USER"]
PASSW = os.environ["FREESOUND_PASSW"]


def generate_random_sound():
    """ Generates random sound id, authorize to api and gets sound info"""
    headers = {"Authorization": f"Token {API_KEY}"}
    sound_id = random.randint(1,10000)
    response = requests.get(url=f"{BASE_URL}/apiv2/sounds/{sound_id}", headers=headers)
    response.raise_for_status()
    sound_info = response.json()
    print(sound_info["url"])
    print(sound_info["name"])
    print(sound_info["tags"])
    print(sound_info["description"])
    return sound_info


def authorize():
    """ Authorizations steps to get user access token, which will be used for sound download"""
    with requests.session() as client:

        # Step 1 get cookie token and middle token
        r = client.get(f"{BASE_URL}/apiv2/login/")
        soup = BeautifulSoup(r.content, "html.parser")
        csrfmiddlewaretoken = soup.find('input', dict(name='csrfmiddlewaretoken'))['value']
        csrftoken = r.cookies["csrftoken"]
        print(f"Csrf token {csrftoken}")
        print(f"Middle token:{csrfmiddlewaretoken}")


        # Step 2 log in
        params_for_authorization = {"client_id": CLIENT_ID, "response_type": "code"}
        login_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "lt-LT,lt;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Length": "143",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": f"csrftoken={csrftoken}",
        "Host": "freesound.org",
        "Origin": "https://freesound.org",
        "Referer": "https://freesound.org/apiv2/login/",
        "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": 'Windows',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        login_info = {"username": USERNAME, "password": PASSW, "csrfmiddlewaretoken":csrfmiddlewaretoken}
        login_response = client.post(url=f"{BASE_URL}/apiv2/login/", data=login_info, headers=login_headers, allow_redirects=False)
        login_response.raise_for_status()
        login_success = login_response
        csrftoken = login_response.cookies["csrftoken"]
        sessionid = login_response.cookies["sessionid"]
        print(csrftoken, sessionid)
        print(login_success)

        # Step 3 authorize with client and get temp code
        authorize_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "lt-LT,lt;q=0.9",
            "Connection": "keep-alive",
            "Cookie": f"csrftoken={csrftoken}; sessionid={sessionid}",
            "Host": "freesound.org",
            "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "Authorization":f"Token {API_KEY}"
        }

        authorize = requests.get(url=f"{BASE_URL}/apiv2/oauth2/authorize/", params=params_for_authorization, headers=authorize_headers, allow_redirects=False)
        soup2 = BeautifulSoup(authorize.content, "html.parser")
        authorize.raise_for_status()
        temp_code = (authorize.headers["location"]).split("=")[1]
        # https://freesound.org/apiv2/oauth2/authorize/?client_id=3JVrrERUTDF2cPMj7TP1&response_type=code
        print(temp_code)

        # Insert this function if need to give user permissions to get temp code
        def mark_as_allow():
            headers_for_allow = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "lt-LT,lt;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Length": "143",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": f"{csrftoken}; {sessionid}",
            "Host": "freesound.org",
            "Origin": "https://freesound.org",
            "Referer": "https://freesound.org/apiv2/oauth2/authorize/?client_id=3JVrrERUTDF2cPMj7TP1&response_type=code",
            "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": 'Windows',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "Authorization":f"Token {API_KEY}"

            }


            data_allow = {

            "csrfmiddlewaretoken": second_csrf_token,
            "redirect_uri": "https://freesound.org/home/app_permissions/permission_granted/",
            "scope": "read write",
            "client_id": CLIENT_ID,
            "response_type": "code",
            "allow": "Authorize!",
            }
            authorize_allow = requests.post(url=f"{BASE_URL}/apiv2/oauth2/authorize", data=data_allow, headers=headers_for_allow)
            soup3 = BeautifulSoup(authorize_allow.content, "html.parser")
            print(f" Auth content from allow: {soup3}")


        # Step 4 get authorization token
        params_for_redirect = {"code": temp_code}
        params_for_user_token = {"client_id": CLIENT_ID, "client_secret": API_KEY, "grant_type": "authorization_code", "code": temp_code}
        user_token_response = requests.post(url=f"{BASE_URL}/apiv2/oauth2/access_token/", params=params_for_user_token)
        user_token = user_token_response.json()["access_token"]
        print(f"User token {user_token}")
        headers_for_download = {"Authorization": f"Bearer {user_token}"}
        return headers_for_download


def download_sound(sound_id, sound_name, headers_for_download):
    """Downloads sound using generated id and access token, saves file to app directory using original sound name."""
    # Get the file of the sound
    download = requests.get(f"{BASE_URL}/apiv2/sounds/{sound_id}/download/", headers=headers_for_download)
    # Save downloaded file
    with open(f"static/sounds/{sound_name}", "wb") as file:
        file.write(download.content)

