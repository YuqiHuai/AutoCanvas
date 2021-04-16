from api import API


class Assignment:
    def __init__(self, course_id, assignment_id):
        self.course_id = course_id
        self.assignment_id = assignment_id
        self.endpoint = f"https://canvas.eee.uci.edu/api/v1/courses/{course_id}/assignments/{assignment_id}"
        self.api = API.get_instance()

    def grade_assignment(self, student_id: str, grade: float, comment: str):
        endpoint = self.endpoint + f"/submissions/{student_id}"
        data = {
            "comment[text_comment]": comment,
            "submission[posted_grade]": grade
        }
        response = self.api.put(endpoint, data)
        return response

    def delete_submission_comments(self, student_id: str) -> int:
        comments_deleted = 0
        submission_endpoint = self.endpoint + f"/submissions/{student_id}"
        submission = self.api.get(submission_endpoint, {"include": ["submission_comments"]}).json()
        if 'submission_comments' in submission:
            for comment in submission['submission_comments']:
                delete_endpoint = self.endpoint + f"/submissions/{student_id}/comments/{comment['id']}"
                self.api.delete(delete_endpoint)
                comments_deleted += 1
        return comments_deleted
