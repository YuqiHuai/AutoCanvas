from api import API
from course.assignment import Assignment
from course.discussion import Discussion
from utils import get_logger


class Course:
    def __init__(self, course_id):
        self.course_id = course_id
        self.endpoint = f"https://canvas.eee.uci.edu/api/v1/courses/{course_id}"
        self.api = API.get_instance()
        self.logger = get_logger('Course')

    def get_assignment(self, assignment_id):
        return Assignment(self.course_id, assignment_id)

    def get_discussion(self, discussion_id):
        return Discussion(self.course_id, discussion_id)

    def get_enrollments(self):
        result = dict()
        keys = ['id', 'login_id', 'name', 'sortable_name', 'short_name', 'sis_user_id']
        endpoint = self.endpoint + '/enrollments'
        params = {
            'type': 'StudentEnrollment',
            'per_page': 100
        }

        for response in self.api.get_paginated(endpoint, params):
            for student in response.json():
                user = {k: str(student['user'][k]) for k in keys}
                result[user['id']] = user

        return result
