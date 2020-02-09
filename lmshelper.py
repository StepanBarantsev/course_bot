import requests

class LmsHelper:

    def __init__(self, lmskey):
        self.lmskey = lmskey
        self.courseid = 1040

    def is_task_completed(self, student_lms_id, task_number, gradepass=5):
        task_info = self.get_task_by_number(task_number, student_lms_id)
        return task_info['grades'][0]['grade'] == gradepass

    def get_task_by_number(self, task_number, student_lms_id):
        task_number = str(task_number)
        lst = self.get_all_tasks_for_student(student_lms_id)
        for element in lst:
            tmp_number = LmsHelper.delete_symbols_except_dots_and_digits(element['name'])
            if tmp_number == task_number:
                return element

    def get_task_by_fullname(self, fullname, student_lms_id):
        lst = self.get_all_tasks_for_student(student_lms_id)
        for element in lst:
            if element['name'] == fullname:
                return element

    @staticmethod
    def delete_symbols_except_dots_and_digits(string):
        return ''.join([i for i in string if i == '.' or i.isdigit()])

    def get_all_tasks_for_student(self, student_lms_id):
        request = 'https://software-testing.ru/lms/webservice/rest/server.php?wstoken=%s&wsfunction=core_grades_get_grades&courseid=%s&userids[0]=%s&moodlewsrestformat=json' % (self.lmskey, str(self.courseid), str(student_lms_id))
        result = requests.get(request, headers={"User-Agent": "Mozilla/5.0"})
        return result.json()['items'][1:]

    def return_max_payed_block(self, student_lms_id):
        if self.get_task_by_fullname('Оплата блока 2', student_lms_id)['grades'][0]['grade'] == 5:
            if self.get_task_by_fullname('Оплата блока 3', student_lms_id)['grades'][0]['grade'] == 5:
                if self.get_task_by_fullname('Оплата блока 4', student_lms_id)['grades'][0]['grade'] == 5:
                    return 4
                return 3
            return 2
        return 1