from datetime import datetime

import pytz

from course import Course
from scripts import Script
from utils import parse_course_id, parse_discussion_id, get_logger, parse_assignment_id


def grade_student(posts: [int], replies: [int]):
    # 3 posts in 3 different board
    # 8 replies in 3 different board

    score = 10
    comment = "----------\n"

    total_posts = sum(posts)
    total_replies = sum(replies)
    boards_posted_in = sum([1 for x in posts if x > 0])
    boards_replied_in = sum([1 for x in replies if x > 0])

    if total_posts < 3:
        penalty = (3 - total_posts) * 2
        score -= penalty
        comment += f"-{penalty} for making {total_posts}/3 posts\n"
    elif boards_posted_in < 3:
        penalty = (3 - boards_posted_in) * 2
        score -= penalty
        comment += f"-{penalty} for posting in {boards_posted_in}/3 discussion boards\n"

    if total_replies < 8:
        penalty = (8 - total_replies) * 0.5
        score -= penalty
        comment += f"-{penalty} for making {total_replies}/8 replies\n"
    elif boards_replied_in < 3:
        penalty = (3 - boards_replied_in) * 0.5
        score -= penalty
        comment += f"-{penalty} for replying in {boards_replied_in}/3 discussion boards\n"

    comment += f"\nCurrent Score: {score}\n"

    return comment, score


class DiscussionParticipation(Script):

    def __init__(self):
        self.course = Course('12')
        self.discussions = [
            'https://canvas.eee.uci.edu/courses/29209/discussion_topics/400161',
            'https://canvas.eee.uci.edu/courses/29209/discussion_topics/400158',
            'https://canvas.eee.uci.edu/courses/29209/discussion_topics/400160',
            'https://canvas.eee.uci.edu/courses/29209/discussion_topics/400159',
            'https://canvas.eee.uci.edu/courses/29209/discussion_topics/381246'
        ]
        self.assignment = 'https://canvas.eee.uci.edu/courses/29209/assignments/557702'
        self.logger = get_logger('Grader')

    def generate_grade_book(self, students):
        grade_book = dict()
        for user_id in students:
            student = students[user_id]
            grade_book[user_id] = {
                'name': student['name'],
                'login_id': student['login_id'],
                'sortable_name': student['sortable_name'],
                'participation': {
                    'P': [0 for _ in range(len(self.discussions))],
                    'R': [0 for _ in range(len(self.discussions))]
                },
                'report': f"{student['name']}\n{'-' * 10}\nParticipation in each discussion board:\n",
                'score': -1
            }
        return grade_book

    def run(self):
        course_id = parse_course_id(self.discussions[0])
        course = Course(course_id)
        assignment_id = parse_assignment_id(self.assignment)
        assignment = course.get_assignment(assignment_id)

        students = course.get_enrollments()
        self.logger.info(f"Fetched {len(students)} students.")

        grade_book = self.generate_grade_book(students)

        # fetch participation for each discussion board
        for index, discussion_url in enumerate(self.discussions):
            self.logger.info(f"Fetching Discussion #{index}. ({discussion_url})")
            discussion_id = parse_discussion_id(discussion_url)
            discussion = course.get_discussion(discussion_id)

            participation = discussion.get_participation()
            for anything in participation:
                if anything['user_id'] not in grade_book:
                    # student dropped the course
                    continue
                if anything['parent_id'] == 'None':
                    # original post
                    grade_book[anything['user_id']]['participation']['P'][index] += 1
                else:
                    # reply to a post
                    grade_book[anything['user_id']]['participation']['R'][index] += 1

            for user_id in grade_book:
                num_posts = grade_book[user_id]['participation']['P'][index]
                num_replies = grade_book[user_id]['participation']['P'][index]
                grade_book[user_id]['report'] += \
                    f"{discussion.title}\n  Post: {num_posts}; Reply: {num_replies}\n"

        # calculate score for each student
        for user_id in grade_book:
            data = grade_book[user_id]['participation']
            comment, score = grade_student(data['P'], data['R'])
            grade_book[user_id]['report'] += comment

            current_time = datetime.now(pytz.utc)
            time_format = '%Y:%m:%d %H:%M:%S %Z %z'
            grade_book[user_id]['report'] += \
                f"{'-' * 10}\nReported at: {current_time.strftime(time_format)}"
            grade_book[user_id]['score'] = score

        # upload students' grade
        for user_id in grade_book:
            assignment.delete_submission_comments(user_id)
            assignment.grade_assignment(user_id, grade_book[user_id]['score'], grade_book[user_id]['report'])
