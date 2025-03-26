from api import APIClient
from database import Database
from utils.log import log
from utils.email import send_emails

import os
import time

db_path = "database.db"
db = Database(db_path)
client = APIClient()


def get_pisciners():
    log(0, "Pisciners fetching...")
    if not os.path.getsize(db_path) > 0:
        pisciners = client.get_pisciners()
        db.insert_multiple("pisciners", pisciners)
    else:
        pisciners = db.get_all("pisciners")

    return pisciners


def monitor_projects(pisciners, monitor_delay, project_delay):
    while True:
        for pisciner in pisciners:
            login = pisciner["login"]
            log(0, f"Projects fetching for {login}.")
            projects = client.get_pisciner_projects(login)

            user_record = db.find("projects", {"login": login})
            existing_projects = (
                set(user_record[0]["projects"]) if user_record else set()
            )
            new_projects = set()

            for project in projects:
                project_slug = project["project"]["slug"]
                project_status = project["status"]

                if project_status == "finished" and project_slug in existing_projects:
                    log(0, f"{login} finished {project_slug} project.")
                    existing_projects.remove(project_slug)

                if (
                    project_status == "waiting_for_correction"
                    and project_slug not in existing_projects
                ):
                    log(0, f"{login} waiting evaluation for {project_slug} project.")
                    send_emails(login, project_slug)
                    new_projects.add(project_slug)

            updated_projects = existing_projects | new_projects
            if user_record:
                db.update(
                    "projects", {"login": login}, {"projects": list(updated_projects)}
                )
            elif new_projects:
                db.insert_data(
                    "projects", {"login": login, "projects": list(new_projects)}
                )

            time.sleep(project_delay)

        log(0, f"Waiting for next check in {monitor_delay} seconds.")
        time.sleep(monitor_delay)


if __name__ == "__main__":
    pisciners = get_pisciners()
    monitor_projects(pisciners, 60 * 10, 1)
