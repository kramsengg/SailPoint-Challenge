from flask import Flask, render_template

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

import json



app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route("/")
def hello_world():
    return  render_template("index.html") 

@app.route("/pullstats")
def pull_statistics():
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

        for pull in pulls:
            if pull["state"] == "open":
                opened += 1
            elif pull["state"] == "closed":
                closed += 1
            else:
                in_progress += 1

        subject = f"Pull request summary for {os.getenv('REPOSITORY_NAME')} ({params['since']} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
        body = f"Hi,\n\nHere's the summary of pull requests for the past week:\n\nOpened: {opened}\nClosed: {closed}\nIn progress: {in_progress}\n\nBest regards,\n Ramachandran\n DevOps Engineer - Support"

        print(f"From: {os.getenv('FROM_EMAIL')}")
        print(f"To: {os.getenv('TO_EMAIL')}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")

        responseContent = f"From: {os.getenv('FROM_EMAIL')}\n" + f"To: {os.getenv('TO_EMAIL')}\n" + f"Subject: {subject}\n" + f"Body: {body}"   
        return responseContent

    else:
        print(f"Error: {response.status_code}")
        return f"Error: {response.status_code}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4545, debug=True)