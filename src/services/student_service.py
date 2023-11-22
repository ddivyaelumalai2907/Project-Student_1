import pathlib, sys

root_path = pathlib.Path(__file__).parent.resolve().parent.resolve()
sys.path.append(str(root_path))

import os
from flask import Flask, request
import json, yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dao import student, student_subject,subject
import re,threading,time
import redis

app = Flask(__name__)

def get_db_connection():
    Session = sessionmaker(bind=db_engine)
    return Session()

@app.route('/student/<int:id>', methods=['GET'])
def get_student_details(id):
    res = {
        'status': 'success',
        'message': None,
        'data': None
    }

    try:
        connection = get_db_connection()
        res['data'] = student.get_student_by_id_model(id, connection)

        if res['data'] == None:
            res['status'] = 'failure'
            res['message'] = 'Unable to get the student details'
        else:
            res = {
              'status': 'success',
              'message': None,
              'data':student.get_student_by_id_model(id, connection)
            }
    
    except Exception as e:
        print(str(e))

        res['status'] = 'failure'
        res['message'] = 'Unable to get the student details'

    return json.dumps(res)

@app.route('/student/subscribe', methods=['POST'])
def student_subscribe():
    res = {
        'status': 'success',
        'message': None,
        'data': None
    }

    try:
        input = request.get_json(force=True)
        if 'student_id' not in input:
            res['status'] = 'failure'
            res['message'] = 'No student id given'
        elif not re.match('^\d{1,9}$', str(input['student_id'])):
            res['status'] = 'failure'
            res['message'] = 'Invalid student id given'
        elif 'subject_id' not in input:
            res['status'] = 'failure'
            res['message'] = 'No subject id given'
        elif not re.match('^\d{1,4}$', str(input['subject_id'])):
            res['status'] = 'failure'
            res['message'] = 'Invalid subject id given'
        else:
            connection = get_db_connection()
            res['data'] = student_subject.subscribe_to_subject(
                student_id=int(input['student_id']),
                subject_id=int(input['subject_id']),
                connection=connection
            )
    except Exception as e:
        print(str(e))

        res['status'] = 'failure'
        res['message'] = 'Unable to subscribe the student to the subject'

    return json.dumps(res)

@app.route('/student/subscribe/change', methods=['POST'])
def student_subscribe_change():
    res = {
        'status': 'success',
        'message': None,
        'data': None
    }

    try:
        input = request.get_json(force=True)
        if 'student_id' not in input:
            res['status'] = 'failure'
            res['message'] = 'No student id given'
        elif not re.match('^\d{1,9}$', str(input['student_id'])):
            res['status'] = 'failure'
            res['message'] = 'Invalid student id given'
        elif 'old_subject_id' not in input:
            res['status'] = 'failure'
            res['message'] = 'No old subject id given'
        elif not re.match('^\d{1,4}$', str(input['old_subject_id'])):
            res['status'] = 'failure'
            res['message'] = 'Invalid old subject id given'
        elif 'new_subject_id' not in input:
            res['status'] = 'failure'
            res['message'] = 'No new subject id given'
        elif not re.match('^\d{1,4}$', str(input['new_subject_id'])):
            res['status'] = 'failure'
            res['message'] = 'Invalid new subject id given'
        else:
            connection = get_db_connection()
            res['data'] = student_subject.change_student_subject(
                student_id=int(input['student_id']),
                old_subject_id=int(input['old_subject_id']),
                new_subject_id=int(input['new_subject_id']),
                connection=connection
            )
    except Exception as e:
        print(str(e))

        res['status'] = 'failure'
        res['message'] = 'Unable to subscribe the student to the subject'

    return json.dumps(res)

@app.route('/subject',methods=['GET'])
def all_subjects():
    res= {
        'status' : 'success',
        'message': None,
        'data':None
    }
    try:
        connection = get_db_connection() #creating instance for Session
        s = subject.get_subject(connection)
        res['data'] = s
        
    except Exception as e:
        print(str(e))
        #if failure happens.
        res['status'] = 'failuer'
        res['message'] = 'unable to get the  all subject detail'

    return json.dumps(res)
#get all subjects
@app.route('/all/subjects',methods=['GET'])
def all_detailsofsubjects():
    res= {
        'status' : 'success',
        'message': None,
        'data':None
    }
    try:
        connection = get_db_connection() #creating instance for Session
        res['data'] = subject.get_all_subject(connection)
        
    except Exception as e:
        print(str(e))
        #if failure happens.
        res['status'] = 'failuer'
        res['message'] = 'unable to get the  all subject detail'

    return json.dumps(res)

#add student
@app.route('/add/student',methods=['POST'])
def add_student():
    res = {
        'status' : 'success',
        'message' : None,
        'data' : None
    }

    try :
        input =  request.get_json(force=True)

        if 'name' not in  input:
            res['status'] = 'failure'
            res['message'] = 'No student name given'

        else: 

            connection = get_db_connection()
            res['data'] = student.new_student(
                student_name = (input['name']),
                connection = connection
        )

    except Exception as e:
        print(str(e))
        res['status'] = 'failuer'
        res['message'] = 'unable to get the student detail'
    
    return json.dumps(res)

#add new course
@app.route('/add/subject',methods=['POST'])
def add_new_subject():
    res = {
        'status' : 'sucess',
        'message' : None,
        'data' : None
    }

    try :
        input =  request.get_json(force=True)

        if 'subject_name' not in input:
            res['status'] = 'failuer'
            res['message'] = 'No subject name given'
        else: 

            connection = get_db_connection()
            res['data'] = subject.add_subject(
                subject_name = (input['subject_name']),
                connection = connection
        )

    except Exception as e:
        print(str(e))

        res['status'] = 'failuer'
        res['message'] = 'unable to get the subject detail'

    return json.dumps(res)

#delete details in student_subject using DELETE api
@app.route('/quit/course', methods=['DELETE'])
def delete_subscription_details():
    res = {
        'status': 'success',
        'message': None,
        'data': None
    }
    try:
        input = request.get_json(force=True)
        if 'student_id' not in input:
            res['status'] = 'failure'
            res['message'] = 'No student id given'
        elif not re.match('^\d{1,9}$', str(input['student_id'])):
            res['status'] = 'failure'
            res['message'] = 'Invalid student id given'
        elif 'subject_id' not in input:
            res['status'] = 'failure'
            res['message'] = 'No subject id given'
        elif not re.match('^\d{1,4}$', str(input['subject_id'])):
            res['status'] = 'failure'
            res['message'] = 'Invalid subject id given'
        else:
            connection = get_db_connection()
            res['data'] = student_subject.delete_subscription(
                connection,
                student_id=int(input['student_id']),
                subject_id=int(input['subject_id'])
            )
    except Exception as e:
        print(str(e))
        res['status'] = 'failure'
        res['message'] = 'Unable to subscribe the student to the subject'
    return json.dumps(res)

#update subjects using PUT api
@app.route("/update/subjects",methods=['PUT'])
def update_subjects():
    res = {
        'status': 'success',
        'message': None,
        'data': None
    }

    try:
        input = request.get_json(force=True)

        if 'old_subject_id' not in input:
            res['status'] = 'failure'
            res['message'] = 'No old subject id given'
        elif 'new_subject_id' not in input:
            res['status'] = 'failure'
            res['message'] = 'No new subject id given'
        else:
            connection = get_db_connection()
            res['data'] = subject.change_subject(
                old_subject_id=int(input['old_subject_id']),
                new_subject_id=int(input['new_subject_id']),
                connection=connection
            )
    except Exception as e:
        print(str(e))

        res['status'] = 'failure'
        res['message'] = 'Unable to subscribe the student to the subject'

    return json.dumps(res)

@app.route("/update/student_name",methods=['PUT'])
def update_student_name():
    res = {
        'status': 'success',
        'message': None,
        'data': None
    }

    try:
        input = request.get_json(force=True)

        if 'old_name' not in input:
            res['status'] = 'failure'
            res['message'] = 'No old name given'
        elif 'new_name' not in input:
            res['status'] = 'failure'
            res['message'] = 'No new name given'
        else:
            connection = get_db_connection()
            res['data'] = student.change_student_name(
                old_name=(input['old_name']),
                new_name=(input['new_name']),
                connection=connection
            )
    except Exception as e:
        print(str(e))

        res['status'] = 'failure'
        res['message'] = 'Unable to subscribe the student to the subject'

    return json.dumps(res)
#delete subject
@app.route('/remove/course', methods=['DELETE'])
def delete_subjects():
    res = {
        'status': 'success',
        'message': None,
        'data': None
    }
    try:
        input = request.get_json(force=True)
        if 'subject_id' not in input:
            res['status'] = 'failure'
            res['message'] = 'No student id given'
        elif not re.match('^\d{1,9}$', str(input['subject_id'])):
            res['status'] = 'failure'
            res['message'] = 'Invalid student id given'
        else:
            connection = get_db_connection()
            res['data'] = subject.delete_subject(
                connection,
                subject_id=int(input['subject_id'])
            )
    except Exception as e:
        print(str(e))
        res['status'] = 'failure'
        res['message'] = 'Unable to delete the subject'
    return json.dumps(res)

#updating subject name using PATCH api
@app.route("/update/subject",methods=['PUT'])
def update_students():
    res = {
        'status': 'success',
        'message': None,
        'data': None
    }

    try:
        input = request.get_json(force=True)

        if 'old_name' not in input:
            res['status'] = 'failure'
            res['message'] = 'No old name given'
        elif 'new_name' not in input:
            res['status'] = 'failure'
            res['message'] = 'No new name given'
        else:
            connection = get_db_connection()
            res['data'] = subject.change_subject_name(
                old_name=(input['old_name']),
                new_name=(input['new_name']),
                connection=connection
            )
    except Exception as e:
        print(str(e))

        res['status'] = 'failure'
        res['message'] = 'Unable to change the subject name'

    return json.dumps(res)

@app.route("/view/students/<id>",methods=['GET'])
def viewstudents(id):
    res = {
        'status': 'success',
        'message': None,
        'data': None
    }
    try:
        connection = get_db_connection()
        res['data'] = student_subject.toviewstudents(id,connection)

    except Exception as e:
        res['status'] = 'failure'
        res['message'] = 'Unable to get the student details'

    return json.dumps(res)

#to get enrolled subjects
@app.route("/enrolled/subjects/<id>",methods=['GET'])
def enrolled_subjects(id):
    res={
        'status':'success',
        'message':None,
        'data':None            
    }
    try:
        connection = get_db_connection()
        res['data'] = subject.subjects_enrolled(id,connection)

    except Exception as e:
        print(str(e))
        res['status'] = 'failure'
        res['message'] = 'Unable to get the student details'

    return json.dumps(res)

@app.route("/explore/subjects/<id>",methods=['GET'])
def explore_subjects(id):
    res={
        'status':'success',
        'message':None,
        'data':None            
    }
    try:
        connection = get_db_connection()
        res['data'] = student_subject.subjects_not_enrolled(id,connection)

    except Exception as e:
        print(str(e))
        res['status'] = 'failure'
        res['message'] = 'Unable to get the student details'

    return json.dumps(res)


file_config = yaml.load(open(os.path.join(root_path, "..", "conf", "config.yml")))
db_engine = create_engine(file_config['db_connection_string'], pool_size=50, isolation_level="READ COMMITTED")

'''
def test():
    print ("Hello")

def test1():
    print("on branch rushok")

def a(n=0):
    while True:
        n=n+1
        print(n)
        time.sleep(1)
        redisConn.publish('my_channel',str(n)) #connecting redis and without str also works,the str is maily used while passing obj
'''


redisConn = redis.Redis('localhost',6379)#decalring redis with hostname,port number
#redisConn.set('demo','works')
#print(redisConn.get('demo'))

'''def dec():
    for i in range(10):
        print(i)
        time.sleep(1)

t = threading.Thread(target=a,args=(100,))
t.daemon=False
t.start()
#dec()'''
app.run('localhost', 5000)
