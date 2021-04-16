from api import API
from utils import get_logger


class Discussion:
    def __init__(self, course_id, discussion_id):
        self.course_id = course_id
        self.discussion_id = discussion_id
        self.endpoint = f"https://canvas.eee.uci.edu/api/v1/courses/{course_id}/discussion_topics/{discussion_id}"
        self.api = API.get_instance()
        self.logger = get_logger('Discussion')

        data = self.api.get(self.endpoint).json()
        assert 'title' in data
        self.title = data['title']

    def get_participation(self):
        result = list()
        endpoint = self.endpoint + '/entries'
        params = {
            "per_page": 100
        }
        keys = ['id', 'user_id', 'parent_id', 'created_at', 'user_name', 'message', 'parent_id']

        for response in self.api.get_paginated(endpoint, params):
            for post in response.json():
                result.append({k: str(post[k]) for k in keys})
                if 'has_more_replies' in post and post['has_more_replies']:
                    entry_endpoint = self.endpoint + f"/entries/{post['id']}/replies"
                    for entry_replies in self.api.get_paginated(entry_endpoint, params):
                        for reply in entry_replies.json():
                            result.append({k: str(reply[k]) for k in keys})
                elif 'recent_replies' in post:
                    for reply in post['recent_replies']:
                        result.append({k: str(reply[k]) for k in keys})

        return result
