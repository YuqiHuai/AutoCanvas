import numpy as np

from course import Course
from scripts import Script
from utils import parse_course_id, parse_assignment_id, get_logger


class AssignmentScoreAnalyzer(Script):
    def __init__(self, assignment_url: str):
        course_id = parse_course_id(assignment_url)
        assignment_id = parse_assignment_id(assignment_url)
        self.course = Course(course_id)
        self.assignment = self.course.get_assignment(assignment_id)
        self.logger = get_logger('AssignmentScoreAnalyzer')

    def run(self):
        self.logger.info('Fetching submissions')
        responses = self.assignment.list_submissions()
        scores = list()
        for response in responses:
            submissions = response.json()
            for submission in submissions:
                if submission['score']:
                    scores.append(submission['score'])

        print('Grades analyzed:', len(scores))
        print('High:', round(np.max(scores), 2))
        print('Low:', round(np.min(scores), 2))
        print('Average:', round(np.average(scores), 2))
        print('Std:', round(np.std(scores), 2))
