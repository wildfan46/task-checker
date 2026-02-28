import os
import boto3


ssm = boto3.client("ssm")


def get_param(name, decrypt=True):
    return ssm.get_parameter(
        Name=name, WithDecryption=decrypt
    )["Parameter"]["Value"]


def get_config():
    TODOIST_API_TOKEN = get_param(os.environ["TODOIST_PARAM"])
    PIRATE_API_KEY = get_param(os.environ["PIRATE_PARAM"])
    LAT = os.environ["LAT"]
    LON = os.environ["LON"]
    DELANO_HOUSE_PROJECT_ID = os.environ["DELANO_HOUSE_PROJECT_ID"]
    DELANO_HOUSE_MAINTENANCE_SECTION_ID = os.environ[
        "DELANO_HOUSE_MAINTENANCE_SECTION_ID"
    ]
    PERSONAL_PROJECT_ID = os.environ["PERSONAL_PROJECT_ID"]
    PERSONAL_FUN_SECTION_ID = os.environ["PERSONAL_FUN_SECTION_ID"]
    PERSONAL_PHYSICAL_HEALTH_SECTION_ID = os.environ[
        "PERSONAL_PHYSICAL_HEALTH_SECTION_ID"
    ]
    return {
        "TODOIST_API_TOKEN": TODOIST_API_TOKEN,
        "PIRATE_API_KEY": PIRATE_API_KEY,
        "LAT": LAT,
        "LON": LON,
        "DELANO_HOUSE_PROJECT_ID": DELANO_HOUSE_PROJECT_ID,
        "DELANO_HOUSE_MAINTENANCE_SECTION_ID":
            DELANO_HOUSE_MAINTENANCE_SECTION_ID,
        "PERSONAL_PROJECT_ID": PERSONAL_PROJECT_ID,
        "PERSONAL_FUN_SECTION_ID": PERSONAL_FUN_SECTION_ID,
        "PERSONAL_PHYSICAL_HEALTH_SECTION_ID":
            PERSONAL_PHYSICAL_HEALTH_SECTION_ID
    }
