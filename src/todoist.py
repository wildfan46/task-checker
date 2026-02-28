import requests
from datetime import datetime, timedelta


base_url = "https://api.todoist.com/api/v1"
post_url = f"{base_url}/tasks/completed/by_completion_date"
tasks_url = f"{base_url}/tasks"


def check_recently_completed(
    token: str,
    task_name: str,
    days: int = 21
) -> bool:
    """Return True if task_name is found in completed items in last `days`."""
    headers = {"Authorization": f"Bearer {token}"}
    since = (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z"
    limit = 200
    offset = 0
    while True:
        params = {"since": since, "limit": limit, "offset": offset}
        r = requests.get(post_url, headers=headers, params=params)
        if r.status_code != 200:
            print(f"Todoist API error: {r.status_code}")
            return False
        items = r.json().get("items", [])
        for t in items:
            if task_name.lower() in t["content"].lower():
                return True
        if len(items) < limit:
            break
        offset += limit
    return False


def last_task_older_than(token: str, task_name: str, days: int) -> bool:
    """Return True when no completed task matching `task_name` in `days`."""
    return not check_recently_completed(token, task_name, days)


def create_todoist_task(
    token: str,
    task_name: str,
    project_id: str,
    section_id: str,
    due_datetime: str = None
):
    """Create a task via Todoist REST v2. Returns response object."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "content": task_name,
        "project_id": project_id,
        "section_id": section_id
    }
    if due_datetime:
        data["due_datetime"] = due_datetime
    else:
        data["due_date"] = datetime.utcnow().date().isoformat()
    r = requests.post(tasks_url, headers=headers, json=data)
    if r.status_code not in (200, 201):
        print(f"Todoist create task failed: {r.status_code} {r.text}")
    return r


def check_active_task_exists(token: str, task_name: str) -> bool:
    """Legacy helper: single-task existence check via REST endpoint."""
    print(f"Fetching active tasks for existence check for task '{task_name}'")
    headers = {"Authorization": f"Bearer {token}"}
    tasks = []
    cursor = None
    while True:
        query_params = "query=view%20all&limit=200"
        if cursor:
            query_params += f"&cursor={cursor}"
        r = requests.get(f"{tasks_url}/filter?{query_params}", headers=headers)
        if r.status_code != 200:
            print(f"Todoist tasks fetch failed: {r.status_code}")
            print(f"Error response: {r.text}")
        results = r.json()
        tasks.extend(results.get("results", []))
        next_cursor = results.get("next_cursor")
        if next_cursor:
            cursor = next_cursor
        else:
            break
    return any(task_name.lower() in t["content"].lower() for t in tasks)
