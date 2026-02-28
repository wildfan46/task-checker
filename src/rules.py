import checks as checks


def get_task_configurations(config):
    """Build the task configuration list using runtime config."""
    return [
        {
            "name": "spot treat weeds",
            "project_id": config["DELANO_HOUSE_PROJECT_ID"],
            "section_id": config["DELANO_HOUSE_MAINTENANCE_SECTION_ID"],
            "checking_function": checks.check_weed_task
        },
        {
            "name": "grill dinner tonight",
            "project_id": config["PERSONAL_PROJECT_ID"],
            "section_id": config["PERSONAL_FUN_SECTION_ID"],
            "checking_function": checks.check_grilling_task
        },
        {
            "name": "walk",
            "project_id": config["PERSONAL_PROJECT_ID"],
            "section_id": config["PERSONAL_PHYSICAL_HEALTH_SECTION_ID"],
            "checking_function": checks.check_walk_task
        },
        {
            "name": "cut grass",
            "project_id": config["DELANO_HOUSE_PROJECT_ID"],
            "section_id": config["DELANO_HOUSE_MAINTENANCE_SECTION_ID"],
            "checking_function": checks.check_grass_task
        },
        {
            "name": "clear driveway",
            "project_id": config["DELANO_HOUSE_PROJECT_ID"],
            "section_id": config["DELANO_HOUSE_MAINTENANCE_SECTION_ID"],
            "checking_function": checks.check_driveway_snow_task
        },
    ]


# map lowercase task name -> days to look back when checking completed tasks
COMPLETED_LOOKBACK = {
    "spot treat weeds": 21,
    "cut grass": 5
}
