from config import *
from utils.log import log
from api.session import Session


class APIClient:
    def __init__(self):
        log(0, "Session creating for client...")
        self.session = Session()

    def get_pisciners(self):
        pisciners = []
        page = 1
        while True:
            users = self.session.make_request(
                f"{BASE_URL}/v2/campus/{CAMPUS_ID}/users",
                {
                    "cursus_id": CURSUS_ID,
                    "sort": "-created_at",
                    "filter[pool_month]": POOL_MONTH,
                    "filter[pool_year]": POOL_YEAR,
                    "page[size]": 100,
                    "page[number]": page,
                },
            )
            if not users:
                break
            log(0, f"Pisciners fetching from page {page}.")
            pisciners.extend(users)
            page += 1

        return pisciners

    def get_pisciner_projects(self, pisciner_login):
        return self.session.make_request(
            f"{BASE_URL}/v2/users/{pisciner_login}/projects_users"
        )
