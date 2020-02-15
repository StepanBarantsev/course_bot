# Это файл для меня, тут я буду генерировать отчеты по необходимости
from faunahelper import FaunaHelper
from faunadb.client import FaunaClient
import os

faunakey = os.environ['FAUNAKEY']

faunahelper = FaunaHelper(FaunaClient(faunakey))


def print_all_students(faunahelper):
    for s in faunahelper.get_all_students():
        print('%s: (%s), %s, %s' % (s['name'], s['days'], s['telegram_id'], s['freezed']))


def print_non_freezed_students(faunahelper):
    students = [s for s in faunahelper.get_all_students() if not(s['freezed'])]
    for s in students:
        print('%s: (%s), %s' % (s['name'], s['days'], s['telegram_id']))


def print_freezed_students(faunahelper):
    students = [s for s in faunahelper.get_all_students() if s['freezed']]
    for s in students:
        print('%s: (%s), %s' % (s['name'], s['days'], s['telegram_id']))


print_all_students(faunahelper)