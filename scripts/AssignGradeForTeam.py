from course import Course
from scripts import Script
from utils import parse_course_id, parse_assignment_id
from pathlib import Path
import pandas as pd
from utils.prompt import for_string

class AssignGradeForTeam(Script):
    def __init__(self, assignment_url: str):
        self.course_id = parse_course_id(assignment_url)
        self.assignment_id = parse_assignment_id(assignment_url)
        self.course = Course(self.course_id)
        self.assignment = self.course.get_assignment(self.assignment_id)
        self.teams = dict()
        self.students = dict()

    def load_groups(self, csv_path: str):
        assert Path(csv_path).exists(), f"File not found: {csv_path}"
        df = pd.read_csv(csv_path).fillna('')
        
        for index, row in df.iterrows():
            if row['group_name'] not in self.teams:
                self.teams[row['group_name']] = list()
            self.teams[row['group_name']].append(row['canvas_user_id'])
            self.students[int(row['canvas_user_id'])] = row['name']
        
            
    def get_group_by_id(self, student_id: str):
        for team in self.teams:
            if student_id in self.teams[team]:
                return team
        return None

    def run(self):
        assert len(self.teams) > 0, "No team loaded"
        assert len(self.students) > 0, "No student loaded"
        score_dict = dict()
        responses = self.assignment.list_submissions()
        for response in responses:
            submissions = response.json()
            for submission in submissions:
                # check if there is attachment
                submitted_by = submission['user_id']
                submitted_by_name = self.students[submitted_by]
                submitted_team = self.get_group_by_id(submitted_by)
                if submitted_team not in score_dict:
                    score_dict[submitted_team] = list()
                score_dict[submitted_team].append(
                    {
                        'id': submitted_by,
                        'name': submitted_by_name,
                        'score': submission['score'],
                        'submitted': 'attachments' in submission and len(submission['attachments']) > 0
                    }
                )
        
        for team in sorted(score_dict):
            if team == '':
                continue
            scores = []
            for member in score_dict[team]:
                if member['score'] is not None:
                    scores.append(member['score'])
                else:
                    scores.append(0)
            max_score = max(scores)
            if any(x != max_score for x in scores):
                print('='*20)
                print("[Warning]: not all members have the same score")
                print(team)
                for member in score_dict[team]:
                    print(f"  {'*' if member['submitted'] else ''}{member['name']}: {member['score']} ")
                x = for_string("Update score for this team", default="n", is_legal=lambda x: x != '' and x in ['Y', 'n'], error_message="Please enter Y or n")
                if (x == 'Y'):
                    print('updating ...')
                    for member in score_dict[team]:
                        if member['score'] is None or member['score'] != max_score:
                            self.assignment.grade_assignment(member['id'], max_score, '')