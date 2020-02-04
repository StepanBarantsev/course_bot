from faunadb import query


class FaunaHelper():

    def __init__(self, clientf):
        self.clientf = clientf

    def get_days_by_telegram_id(self, id):
        result = self.clientf.query(query.get(query.match(query.index('students_by_telegram_id'), id)))
        return result['data']['days']

    def decrement_days_by_telegram_id(self, id):
        days = self.get_days_by_telegram_id(id)
        days -= 1
        self.update_days_by_telegram_id(id, days)

    def update_days_by_telegram_id(self, id, new_number_of_days):
        self.clientf.query(query.update(query.select('ref', query.get(query.match(query.index("students_by_telegram_id"), id))), {'data': {'days': new_number_of_days}}))

    def get_all_students(self):
        result = self.clientf.query(query.map_(query.lambda_("x", query.get(query.var('x'))), query.paginate(query.match((query.index('all_students'))))))
        students = result['data']
        return [(student['data']['telegram_id'], student['data']['days']) for student in students]
