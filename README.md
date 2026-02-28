# Task Checker Lambda

[![CI/CD](https://github.com/wildfan46/task-checker/actions/workflows/deploy.yml/badge.svg)](https://github.com/wildfan46/task-checker/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AWS Lambda function (deployed via [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)) that creates Todoist tasks based on weather and other criteria. Runs daily, integrating with Pirate Weather and Todoist APIs.

## Features

- **Weather-based tasks:** Automatically creates tasks (weed treatment, grilling, walking, grass cutting, snow clearing) based on forecast data.
- **Todoist integration:** Uses the Todoist API to create/check tasks.
- **Secure config:** Retrieves API keys/config from AWS SSM Parameter Store.
- **Scheduled:** Runs daily at 6:00 AM Central Time via AWS EventBridge.

## Project Structure

- [`src/app.py`](src/app.py): Lambda function code.
- [`template.yaml`](template.yaml): AWS SAM template (resources, env, schedule).
- [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml): GitHub Actions for CI/CD.
- [`src/requirements.txt`](src/requirements.txt): Python dependencies.

## Quick Start (Local Testing)

1. Clone the repo and install dependencies:
    ```sh
    pip install -r src/requirements.txt
    ```
2. Set up environment variables or mock SSM parameters for local testing.
3. Run or test the Lambda handler in [`src/app.py`](src/app.py).

## Deployment

This project uses AWS SAM and GitHub Actions for CI/CD.

### Prerequisites

- AWS account with Lambda, SSM, and KMS permissions.
- SSM parameters:
    - `/task-checker/prod/LAT`
    - `/task-checker/prod/LON`
    - `/task-checker/prod/PIRATE_API_KEY`
    - `/task-checker/prod/TODOIST_API_TOKEN`
    - `/task-checker/prod/API_SPORTS_KEY`
- GitHub repository secrets:
    - `AWS_ROLE_TO_ASSUME`
    - `SAM_STACK_NAME`
    - `SAM_BUCKET`
- Python 3.12

### CI/CD

On push to `main`, [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml):

1. Sets up Python and SAM CLI.
2. Configures AWS credentials via OIDC.
3. Builds and deploys the Lambda using SAM.

## Usage

Triggered daily by schedule. Fetches weather, checks conditions, and creates Todoist tasks as needed.

## Customization

- Edit [`src/app.py`](src/app.py) to change task logic.
- Update [`template.yaml`](template.yaml) for environment, schedule, or permissions.

## License

[MIT](LICENSE)