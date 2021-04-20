import math

from course import Course
from scripts import Script
from utils import get_logger
from utils import parse_course_id, parse_assignment_id


def seconds_to_day(seconds: int) -> float:
    seconds_in_a_day = 24 * 60 * 60
    return round(seconds / seconds_in_a_day, 4)


def calc_penalty(seconds_late: int) -> int:
    return int(math.ceil(seconds_to_day(seconds_late)) ** 2)


class CustomLatePenalty(Script):
    def __init__(self, assignment_url):
        course_id = parse_course_id(assignment_url)
        assignment_id = parse_assignment_id(assignment_url)
        self.course = Course(course_id)
        self.assignment = self.course.get_assignment(assignment_id)
        self.logger = get_logger('CustomLatePenalty')

    def run(self):
        responses = self.assignment.list_submissions()
        for response in responses:
            submissions = response.json()
            for submission in submissions:
                if submission['late']:
                    student_id = submission['user_id']
                    score = submission['score']
                    penalty = calc_penalty(submission['seconds_late'])
                    comment = f'[Late Submission Penalty]: -{penalty}'
                    self.assignment.grade_assignment(student_id, score - penalty, comment)

                    d = seconds_to_day(submission['seconds_late'])
                    self.logger.info(f"{student_id} -> {d} days late = -{penalty}")
