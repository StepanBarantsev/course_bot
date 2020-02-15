from faunadb import query
import os

class FaunaHelper():

    def __init__(self, clientf):
        self.clientf = clientf

    def get_days_by_telegram_id(self, id):
        result = self.clientf.query(query.get(query.match(query.index('students_by_telegram_id'), id)))
        return result['data']['days']

    def get_lmsid_by_telegram_id(self, id):
        result = self.clientf.query(query.get(query.match(query.index('students_by_telegram_id'), id)))
        return result['data']['lmsid']

    def decrement_days_by_telegram_id(self, id):
        days = self.get_days_by_telegram_id(id)
        days -= 1
        self.update_days_by_telegram_id(id, days)

    def update_days_by_telegram_id(self, id, new_number_of_days):
        self.clientf.query(query.update(query.select('ref', query.get(query.match(query.index("students_by_telegram_id"), id))), {'data': {'days': new_number_of_days}}))

    def get_all_students(self):
        result = self.clientf.query(query.map_(query.lambda_("x", query.get(query.var('x'))), query.paginate(query.match((query.index('all_students'))))))
        students = result['data']
        students = [student['data'] for student in students]
        return students

    def get_info(self):
        infonumber = os.environ['INFONUMBER']
        result = self.clientf.query(query.get(query.ref(query.collection("Info"), infonumber)))
        return result['data']

    def freeze_student_by_telegram_id(self, telegram_id):
        self.clientf.query(query.update(query.select('ref', query.get(query.match(query.index("students_by_telegram_id"), telegram_id))), {'data': {'freezed': True}}))

    # Для тех, у кого нет tg
    def update_days_by_lms_id(self, id, new_number_of_days):
        self.clientf.query(query.update(query.select('ref', query.get(query.match(query.index("students_by_lms_id"), id))), {'data': {'days': new_number_of_days}}))

    def decrement_days_by_lms_id(self, id):
        days = self.get_days_by_lms_id(id)
        days -= 1
        self.update_days_by_lms_id(id, days)

    def get_days_by_lms_id(self, id):
        result = self.clientf.query(query.get(query.match(query.index('students_by_lms_id'), id)))
        return result['data']['days']
