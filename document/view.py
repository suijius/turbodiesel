__author__ = 'SChepurnov'

import couchdb
from django.shortcuts import render_to_response
from django.db import connections
import json

def default(request):
    return render_to_response('administration/couchdb.html', {})

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def mysql2couchdb(request):

    foo = couchdb.Couch('localhost', '5984')
    foo.createDb('nature')

    sql = 'select * from view_catalog'
    cursor = connections['default'].cursor()
    cursor.execute(sql)
    response = dictfetchall(cursor)
    for doc in response:
        foo.saveDoc('nature', json.dumps(doc), str(doc['id']))
    return render_to_response('administration/couchdb.html', {})