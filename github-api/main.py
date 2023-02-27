import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

import json

load_dotenv()

url = "https://api.github.com/repos/pypa/sampleproject/pulls"
headers = {"Authorization": f"Token {os.getenv('GH_SP_PAT_TOKEN')}"}
params = {
    "state": "all",
    "sort": "updated",
    "direction": "desc",
    "since": (datetime.now() - timedelta(days=7)).isoformat()
}

response = requests.get(url, headers=headers, params=params)

if response.ok:
    pulls = response.json()

    opened = 0
    closed = 0
    in_progress = 0
    open_titles = []
    closed_titles = []
    in_progress_titles = []
    for pull in pulls:
        if pull["state"] == "open":
            opened += 1
            open_titles.append(pull['title'])
        elif pull["state"] == "closed":
            closed += 1
            closed_titles.append(pull['title'])
        else:
            in_progress += 1
            in_progress_titles.append(pull['title'])

    subject = f"Pull request summary for {os.getenv('REPOSITORY_NAME')} ({params['since']} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
    body = f"Hi,\n\nHere's the summary of pull requests for the past week:\n\nOpened: {opened} \nClosed: {closed}\nIn progress: {in_progress}\n\nBest regards,\n Ramachandran\n DevOps Engineer - Support"

    print(f"From: {os.getenv('FROM_EMAIL')}")
    print(f"To: {os.getenv('TO_EMAIL')}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
else:
    print(f"Error: {response.status_code}")