from model import subject,student_subject
from operator import and_
from sqlalchemy import func
from operator import and_,or_

def get_subject(connection):

    obj= connection.query(subject.Subject.id,subject.Subject.name).all()

    data=[]
    for row in obj:

        data.append({
            'id':row.id,
            'name':row.name,
        })

    return data 

#get all details of subjects
def get_all_subject(connection):

    obj= connection.query(subject.Subject.id,subject.Subject.name,
                          func.count(student_subject.StudentSubject.id).label('countofstudent')
                          ).join(student_subject.StudentSubject,student_subject.StudentSubject.subject_id == subject.Subject.id
                          ).group_by(subject.Subject.id)

    data=[]
    for row in obj:

        data.append({
            'id':row.id,
            'name':row.name,
            'countofstudent':row.countofstudent
        })

    return data 

def change_subject(old_subject_id, new_subject_id, connection):
    obj = connection.query(subject.Subject).filter(
            subject.Subject.id == old_subject_id
    ).first()

    if obj is not None:
        obj.id = new_subject_id
        connection.commit()

        return True

    return False

def change_subject_name(old_name, new_name, connection):
    obj = connection.query(subject.Subject).filter(
            subject.Subject.name == old_name
    ).first()

    if obj is not None:
        obj.name = new_name
        connection.commit()

        return True

    return False

#add new subject
def add_subject(subject_name, connection):
    obj = subject.Subject(name = subject_name)
    connection.add(obj)
    connection.commit()

    return {
        'id': obj.id
    }

#delete subject

def delete_subject(connection,subject_id):
    obj = connection.query(subject.Subject).filter(
            subject.Subject.id == subject_id 
    ).first()
   # for eachrow in obj:
    connection.delete(obj)
    connection.commit()

    return {
        'id': obj.id
    }

#student to see the courses he enrolled and not enrolled
def subjects_enrolled(student_id,connection):
    obj = connection.query(subject.Subject.id,subject.Subject.name,student_subject.StudentSubject.id.label("enrolled_id")
                   ).join(student_subject.StudentSubject,and_(subject.Subject.id == student_subject.StudentSubject.subject_id,
                         student_subject.StudentSubject.student_id == student_id),isouter=True).all()
     
    data = []
    for row in obj:
        data.append({
            "subject_id":row.id,
            "subject_name":row.name,
            "enrolled_id":row.enrolled_id
        })
    
    return data
