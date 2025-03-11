from datetime import datetime


def log(level, message):
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    if level == 0:
        print(f"{now}\t\033[0;32mINFO\033[0m\t{message}")
    elif level == 1:
        print(f"{now}\t\033[0;31mWARNING\033[0m\t{message}")
    elif level == 2:
        print(f"{now}\t\033[0;31mERROR\033[0m\t{message}")


# from utils.log import log

# log(0, "info")
# log(1, "debug")
# log(2, "error")
