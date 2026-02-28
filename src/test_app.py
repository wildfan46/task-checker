import unittest
from datetime import datetime, timezone
import checks


class TestChecks(unittest.TestCase):
    def test_check_weed_task(self):
        forecast = {
            "daily": {
                "data": [
                    {"temperatureHigh": 70, "precipProbability": 0},
                    {"temperatureHigh": 60, "precipProbability": 0},
                    {"temperatureHigh": 80, "precipProbability": 0}
                ]
            }
        }
        res = checks.check_weed_task(
            forecast, "HOUSE_PROJECT_ID", "MAINTENANCE_SECTION_ID"
        )
        self.assertIsInstance(res, dict)
        self.assertEqual(res, {
            "name": "Spot Treat Weeds",
            "project_id": "HOUSE_PROJECT_ID",
            "section_id": "MAINTENANCE_SECTION_ID",
            "lookback_days": 21
        })

    def test_check_grilling_task_creates(self):
        today = checks.datetime.utcnow().date()
        hourly = [
            {
                "time": int(datetime(
                    today.year, today.month, today.day, h,
                    tzinfo=timezone.utc
                ).timestamp()),
                "temperature": 60,
                "windSpeed": 2,
                "precipProbability": 0
            }
            for h in range(16, 20)
        ]
        forecast = {"hourly": {"data": hourly}}
        res = checks.check_grilling_task(
            forecast, "PERSONAL_PROJECT_ID", "PERSONAL_FUN_SECTION_ID"
        )
        self.assertIsInstance(res, dict)
        self.assertEqual(res, {
            "name": "Grill dinner tonight",
            "project_id": "PERSONAL_PROJECT_ID",
            "section_id": "PERSONAL_FUN_SECTION_ID"
        })

    def test_check_walk_task_creates(self):
        today = checks.datetime.utcnow().date()
        hourly = [
            {
                "time": int(
                    checks.datetime(
                        today.year, today.month, today.day, h
                    ).timestamp()
                ),
                "temperature": 70,
                "precipProbability": 0
            }
            for h in range(9, 11)
        ] + [
            {
                "time": int(
                    checks.datetime(
                        today.year, today.month, today.day, h
                    ).timestamp()
                ),
                "temperature": 70,
                "precipProbability": 0
            }
            for h in range(14, 18)
        ]
        forecast = {"hourly": {"data": hourly}}
        res = checks.check_walk_task(
            forecast, "PERSONAL_PROJECT_ID",
            "PERSONAL_PHYSICAL_HEALTH_SECTION_ID"
        )
        self.assertIsInstance(res, dict)
        self.assertIn("name", res)
        self.assertIn("project_id", res)
        self.assertIn("section_id", res)
        self.assertIn("due_datetime", res)


if __name__ == "__main__":
    unittest.main()
