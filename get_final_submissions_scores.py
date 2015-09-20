#! /usr/bin/env python3

import sys
sys.path.append('.')
import os
import traceback
import argparse
import json
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import django
django.setup()

from autograder.models import Course, Submission


def main():
    args = parse_args()

    course = Course.objects.get(name=args.course_name)
    semester = course.semesters.get(name=args.semester_name)
    project = semester.projects.get(name=args.project_name)

    submissions = Submission.get_most_recent_submissions(project)

    json_ = []
    for submission in submissions:
        json_.append({
            'members': submission.submission_group.members,
            'results': [
                result.to_json() for result in
                sorted(submission.results.all(),
                       key=lambda res: res.test_case.name)
            ]
        })

    if args.format == 'json':
        with open(args.output_filename, 'w') as f:
            json.dump(json_, f, indent=4, sort_keys=True)
        return

    test_case_names = [
        res.test_case.name for res in
        sorted(submissions[0].results.all(),
               key=lambda res: res.test_case.name)
    ]
    rows = []
    for item in json_:
        if args.preserve_groups_in_csv:
            new_usernames = ['_'.join(sorted(item['members']))]
        else:
            new_usernames = item['members']

        for username in new_usernames:
            test_scores = [
                res['total_points_awarded'] for res in item['results']
            ]
            total = sum(test_scores)
            rows.append(
                [username] + [total] + test_scores
            )

    with open(args.output_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['username', 'Total'] + test_case_names)
        writer.writerows(rows)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('course_name')
    parser.add_argument('semester_name')
    parser.add_argument('project_name')

    parser.add_argument('format', choices=['json', 'csv'])
    parser.add_argument('output_filename')
    parser.add_argument(
        '--preserve_groups_in_csv', '-p', action='store_true', default=False)

    return parser.parse_args()


if __name__ == '__main__':
    main()
