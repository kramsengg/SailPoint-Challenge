from flask import Flask, render_template

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

import json

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route("/")
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
        body = f"Hi,\n\nHere's the summary of pull requests for the past week:\n\nOpened: {opened}   {open_titles} \nClosed: {closed}  {closed_titles}\nIn progress: {in_progress} {in_progress_titles} \n\nBest regards,\n Ramachandran\n DevOps Engineer - Support"

        fromMail = f"From: {os.getenv('FROM_EMAIL')}"
        toMail = f"To: {os.getenv('TO_EMAIL')}"
        return render_template('pullstats.html', title='Pull Request Statistics',  fromMail=fromMail, toMail=toMail, subject=subject, params=params, opened=opened,open_titles=open_titles,closed=closed,closed_titles=closed_titles,in_progress=in_progress,in_progress_titles=in_progress_titles)
    else:
        print(f"Error: {response.status_code}")
        return f"Error: {response.status_code}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)