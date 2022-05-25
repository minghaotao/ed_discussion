from datetime import datetime, timedelta
import csv
from slacker import Slacker
import json
import os
import pandas as pd

current_day = datetime.today().strftime('%Y-%m-%d')
current_day = datetime.strptime(current_day, '%Y-%m-%d')

filt_week = (current_day - timedelta(days=7)).strftime('%Y-%m-%d')


def write_file(rows, course):
    with open(f'/Users/edwardt/PycharmProjects/Upenn_Piazza/ed_discussion/course_files/{course}.csv',
              mode='a', ) as csvfile:
        csvwrite = csv.writer(csvfile, quotechar='"')
        csvwrite.writerow(rows)


def clear_file(course):
    headers = ["url", "post_create_at", "answer_at", "category", "type", "over_24"]
    with open(f'/Users/edwardt/PycharmProjects/Upenn_Piazza/ed_discussion/course_files/{course}.csv',
              mode='w') as csvfile:
        csvwrite = csv.writer(csvfile)
        csvwrite.writerow(headers)


def reset_file(file):
    with open(f'/Users/edwardt/PycharmProjects/Upenn_Piazza/ed_discussion/course_files/{file}.csv',
              mode='w') as csvfile:
        pass


def covert_time_zone(time):
    time_zone = time.split('+')[1].split(':')[0]
    current_time = datetime.strptime(time, f'%Y-%m-%dT%H:%M:%S.%f+{time_zone}:00')
    update_time = (current_time - timedelta(hours=14)).strftime(f'%Y-%m-%dT%H:%M:%S.%f+{time_zone}:00')
    return update_time


def compare_24_hours(time, answer_time=None):
    time_zone = time.split('+')[1].split(':')[0]
    time = datetime.strptime(time, f'%Y-%m-%dT%H:%M:%S.%f+{time_zone}:00')
    one_day_time = (time + timedelta(hours=24)).strftime(f'%Y-%m-%dT%H:%M:%S.%f+{time_zone}:00')
    now = datetime.now()

    current_time = datetime.strftime(now, f'%Y-%m-%dT%H:%M:%S.%f+{time_zone}:00')

    if answer_time:

        if answer_time >= one_day_time:
            return True
        else:
            return False
    else:

        if current_time >= one_day_time:
            return True
        else:
            return False


def update_time_zone(f_read):
    # with open("/Users/edwardt/PycharmProjects/Upenn_Piazza/ed_discussion/CIS5810.json", 'r') as f:
    #     f_read = json.load(f)
    #
    report = []

    for data in f_read:

        if data["type"] == "question":

            if data["answers"]:
                answer_time = data["answers"][0]["created_at"]
                update_answer_time = covert_time_zone(answer_time)
                create_time = data["created_at"]
                update_create_time = covert_time_zone(create_time)

                if compare_24_hours(update_create_time, update_answer_time) == True:

                    feed = f'{data["url"]},{update_create_time},{update_answer_time},{data["category"]},{data["type"]},1'

                    report.append(feed)
                else:
                    feed = f'{data["url"]},{update_create_time},{update_answer_time},{data["category"]},{data["type"]},0'

                    report.append(feed)

            else:

                create_time = data["created_at"]
                update_create_time = covert_time_zone(create_time)

                if compare_24_hours(update_create_time) == True:

                    feed = f'{data["url"]},{update_create_time},NaN,{data["category"]},{data["type"]},1'
                    report.append(feed)
                else:

                    feed = f'{data["url"]},{update_create_time},NaN,{data["category"]},{data["type"]},0'
                    report.append(feed)

        if data["type"] == "post":

            if data["comments"]:
                answer_time = data["comments"][0]["created_at"]
                update_answer_time = covert_time_zone(answer_time)
                create_time = data["created_at"]
                update_create_time = covert_time_zone(create_time)

                feed = f'{data["url"]},{update_create_time},{update_answer_time},{data["category"]},{data["type"]}'

                report.append(feed)
            else:
                create_time = data["created_at"]
                update_create_time = covert_time_zone(create_time)

                feed = f'{data["url"]},{update_create_time},NaN,{data["category"]},{data["type"]}'
                report.append(feed)

    return report


def generate_file(f_read, course):
    report = update_time_zone(f_read)

    for data in report:
        data = data.split(',')
        write_file(data, course)


def read_file(course):
    df = pd.read_csv(f"/Users/edwardt/PycharmProjects/Upenn_Piazza/ed_discussion/course_files/{course}.csv")

    df = df.loc[df["post_create_at"] >= filt_week]

    total_post = df["url"].count()

    total_question = df[(df["type"] == 'question')]["url"].count()

    current_unsolved = df[(df["type"] == 'question') & (df["answer_at"].isnull())]["url"].count()

    late_posts = df[(df["type"] == 'question') & (df["over_24"] == 1)]["url"].count()

    response_rate = (late_posts / total_question) * 100

    response_rate = round(response_rate, 2)

    print(
        f'**{course}** Total_threads: {total_post}, Total_Questions: {total_question}, Current_Unresolved: {current_unsolved}, late_24Hours: {late_posts}, Late_Response_Rate: {response_rate}%')

    # return f'**{course}** Total_threads: {total_post}, Total_Questions: {total_question}, Current_Unresolved: {current_unsolved}, late_24Hours: {late_posts}, Late_Response_Rate: {response_rate}%'
    return course, total_post, total_question, current_unsolved, late_posts, response_rate


if __name__ == '__main__':
    # clear_file()
    # update_time_zone()

    read_file()
