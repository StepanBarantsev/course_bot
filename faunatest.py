from settings import faunakey
from faunadb import query
from faunadb.objects import Ref
from faunadb.client import FaunaClient

clientf = FaunaClient(secret=faunakey)

result = clientf.query(query.map_(query.lambda_("x", query.get(query.var("x"))), query.paginate(query.match(query.index("all_students")))))['data']

for i in result:
    print(i['data'])

result = clientf.query(query.get(query.match(query.index('telegram_id'), 821086704)))

print(result['data'])

clientf.query(query.create(query.collection('students'), {'data': {'test': 'test'}}))

clientf.query(query.update(query.select('ref', query.get(query.match(query.index('telegram_id'), 821086704))), {'data': {'days': 29}}))