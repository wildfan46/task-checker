import checks as checks


def get_task_configurations(config):
    """Build the task configuration list using runtime config."""
    return [
        {
            "name": "spot treat weeds",
            "project_id": config["DELANO_HOUSE_PROJECT_ID"],
            "section_id": config["DELANO_HOUSE_MAINTENANCE_SECTION_ID"],
            "checking_function": checks.check_weed_task,
            "weather_to_check": "today"
        },
        {
            "name": "grill dinner tonight",
            "project_id": config["PERSONAL_PROJECT_ID"],
            "section_id": config["PERSONAL_FUN_SECTION_ID"],
            "checking_function": checks.check_grilling_task,
            "weather_to_check": "today"
        },
        {
            "name": "walk",
            "project_id": config["PERSONAL_PROJECT_ID"],
            "section_id": config["PERSONAL_PHYSICAL_HEALTH_SECTION_ID"],
            "checking_function": checks.check_walk_task,
            "weather_to_check": "today"
        },
        {
            "name": "cut grass",
            "project_id": config["DELANO_HOUSE_PROJECT_ID"],
            "section_id": config["DELANO_HOUSE_MAINTENANCE_SECTION_ID"],
            "checking_function": checks.check_grass_task,
            "weather_to_check": "today"
        },
        {
            "name": "clear driveway",
            "project_id": config["DELANO_HOUSE_PROJECT_ID"],
            "section_id": config["DELANO_HOUSE_MAINTENANCE_SECTION_ID"],
            "checking_function": checks.check_driveway_snow_task,
            "weather_to_check": "yesterday"
        },
        {
            "name": "bring in cushions",
            "project_id": config["DELANO_HOUSE_PROJECT_ID"],
            "section_id": config["DELANO_HOUSE_MAINTENANCE_SECTION_ID"],
            "checking_function": checks.check_chair_cushion_task,
            "weather_to_check": "today"
        },
    ]


# map lowercase task name -> days to look back when checking completed tasks
COMPLETED_LOOKBACK = {
    "spot treat weeds": 21,
    "cut grass": 5
}
