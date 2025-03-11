from config import *
from utils.log import log

import requests
import time


class Session:
    def __init__(self):
        self._session = requests.Session()
        self._token_expiry = 0

        log(0, "Getting access token from API...")
        self._get_access_token()

    def _get_access_token(self):
        response = self._session.post(
            f"{BASE_URL}/oauth/token",
            data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
        )

        if response.status_code != 200:
            raise Exception("API authentication failed")
        data = response.json()
        self._token_expiry = time.time() + data["expires_in"] - 60
        self._session.headers.update(
            {"Authorization": f"Bearer {data['access_token']}"}
        )

    def _is_token_expired(self):
        return time.time() >= self._token_expiry

    def make_request(self, endpoint, params=None, retries=5, backoff_factor=1.0):
        if self._is_token_expired():
            log(0, "Access token is expired. Getting new access token...")
            self._get_access_token()

        attempt = 1
        while attempt < retries + 1:
            try:
                response = self._session.get(endpoint, params=params)
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(
                        f"API request failed with status code {response.status_code}"
                    )
            except Exception as err:
                sleep_time = backoff_factor * (2**attempt)
                log(
                    1,
                    f"API request failed with status code {response.status_code}. Waiting for {sleep_time} seconds. Attempt: {attempt}/{retries}",
                )
                attempt += 1
                time.sleep(sleep_time)

        raise Exception(f"API request failed after {retries} attempts")

    def __del__(self):
        log(0, "Session closing...")
        self._session.close()
