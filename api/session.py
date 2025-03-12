from config import *
from utils.log import log

import requests
import time


class Session:
    def __init__(self):
        self._session = requests.Session()
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
        self._session.headers.update(
            {"Authorization": f"Bearer {data['access_token']}"}
        )

    def _refresh_token(self, response):
        if response.status_code == 401:
            log(0, "Access token expired. Refreshing...")
            self._get_access_token()
            return True
        return False

    def make_request(self, endpoint, params=None, retries=50, sleep_time=10):
        for attempt in range(retries):
            try:
                response = self._session.get(endpoint, params=params)

                if self._refresh_token(response):
                    continue
                if response.status_code == 200:
                    return response.json()
                log(
                    2,
                    f"Request failed (status {response.status_code}). Retrying {attempt + 1}/{retries}...",
                )
            except Exception as err:
                log(
                    2,
                    f"Request failed due to {err}. Retrying {attempt + 1}/{retries}...",
                )
            time.sleep(sleep_time)

        raise Exception("API request failed after multiple attempts.")

    # def __del__(self):
    #     log(0, "Session closing...")
    #     self._session.close()
