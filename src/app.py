from config import get_config
from weather import get_pirate_forecast
from rules import get_task_configurations
import todoist

from datetime import datetime, timedelta, timezone

def lambda_handler(event, context):
    config = get_config()
    yesterday_utc = datetime.now(timezone.utc) - timedelta(days=1)
    todays_forecast = get_pirate_forecast(
        config['PIRATE_API_KEY'],
        config['LAT'],
        config['LON']
    )
    yesterdays_weather = get_pirate_forecast(
        config['PIRATE_API_KEY'],
        config['LAT'],
        config['LON'],
        date=yesterday_utc.timestamp()
    )

    candidate_tasks = get_task_configurations(config)

    tasks_to_create = []

    if not todays_forecast and not yesterdays_weather:
        tasks_to_create.append({
            "name": "Investigate Weather API Failure",
            "project_id": config['PERSONAL_PROJECT_ID'],
            "section_id": config['PERSONAL_FUN_SECTION_ID'],
        })
    else:
        for task_cfg in candidate_tasks:
            if task_cfg["weather_to_check"] == "today":
                task = task_cfg["checking_function"](
                    todays_forecast,
                    task_cfg["project_id"],
                    task_cfg["section_id"]
                )
            else:
                task = task_cfg["checking_function"](
                    yesterdays_weather,
                    task_cfg["project_id"],
                    task_cfg["section_id"]
                )
            if task:
                tasks_to_create.append(task)

    if not tasks_to_create:
        print("No tasks to create.")
        return {
            'statusCode': 200,
            'body': "No tasks created."
        }

    tasks_created = 0
    print(f"Tasks to create: {tasks_to_create}")
    for task in tasks_to_create:
        print(f"Processing candidate task: {task}")
        if (not isinstance(task, dict)) or ("name" not in task):
            print("Invalid task candidate, skipping.")
            continue

        if todoist.check_active_task_exists(
            config['TODOIST_API_TOKEN'],
            task["name"],
        ):
            print(f"Active task exists: {task['name']}")
            continue
        if "lookback_days" in task:
            if todoist.check_recently_completed(
                config['TODOIST_API_TOKEN'],
                task["name"],
                task["lookback_days"]
            ):
                print(
                    f"Recently completed task found: "
                    f"{task['name']}"
                )
                continue

        todoist.create_todoist_task(
            config['TODOIST_API_TOKEN'],
            task["name"],
            task["project_id"],
            task["section_id"],
            task["due_datetime"] if "due_datetime" in task else None
        )
        tasks_created += 1

    return {
        'statusCode': 200,
        'body': f"Tasks created: {tasks_created}"
    }


if __name__ == "__main__":
    # Example: Run the lambda_handler locally
    print("Running local test of lambda_handler...")
    result = lambda_handler({}, {})
    print("Lambda result:", result)
