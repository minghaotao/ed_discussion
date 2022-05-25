import requests
import json
from requests.structures import CaseInsensitiveDict
from datetime import datetime
import csv
from slacker import Slacker
import os
import ed_reports
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

headers = CaseInsensitiveDict()

courses = {
    'course_number': 'https://us.edstem.org/api/courses/{course_number}/analytics/discussion_threads.json',
}


def load_json():
    with open("/cred.json", 'r') as f:
        cred = json.load(f)
        return cred


def slack_bot(message):
    cred = load_json()
    bot = Slacker(cred["slack_token_staff"])
    channel = ""
    bot_name = ""

    # bot.chat.post_message(channel, as_user=bot_name,
    #                       text=f"{message}")
    bot.files.upload(channels=channel,
                     file_=f'{message}.png')


def download_file(course, course_url):
    headers["content-type"] = "application/x-www-form-urlencoded"
    data = "_token= {Curl token}"
    r = requests.post(course_url, headers=headers, data=data)
    if r.status_code == 200:
        f_read = json.loads(r.text)

        ed_reports.clear_file(course)
        ed_reports.generate_file(f_read, course)
        data = ed_reports.read_file(course)
        ed_reports.write_file(data, 'reports')


def charts():
    matplotlib.style.use('fivethirtyeight')

    df = pd.read_csv("/course_files/reports.csv")

    ax = df.plot.bar(x="Courses", y=["Total_Threads", "Total_Questions", "Current_Unresolved", "late_24Hours"],
                     fontsize=9, figsize=(10, 7), rot=0)

    for patch in ax.patches:
        ax.text(
            patch.get_x(),
            patch.get_height() + 1,
            " {:,}".format(int(patch.get_height())),
            fontsize=10,
            color='dimgrey',

        )

    plt.title(f"Ed Discussion Report-Week of {ed_reports.filt_week}")

    plt.tight_layout()

    plt.xlabel("Courses")

    plt.savefig('/course_files/ed_report.png')

    ax1 = df.sort_values('Response_Rate%').plot.barh(x="Courses", y="Response_Rate%", fontsize=9, figsize=(10, 7))

    for patch in ax1.patches:
        ax1.text(
            patch.get_width(),
            patch.get_y(),
            " {:,}%".format(patch.get_width()),
            fontsize=10,
            color='dimgrey'
        )

    plt.title(f'late_24Hours_Response_Rate-Week of {ed_reports.filt_week}')

    plt.tight_layout()
    plt.savefig(f'/course_files/response_rate.png')
    # plt.show()


if __name__ == '__main__':
    ed_reports.reset_file("reports")
    header = ["Courses", "Total_Threads", "Total_Questions", "Current_Unresolved", "late_24Hours", "Response_Rate%"]
    ed_reports.write_file(header, 'reports')
    for key, value in courses.items():
        download_file(key, value)

    charts()

    slack_bot('ed_report')
    slack_bot('response_rate')
