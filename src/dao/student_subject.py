from model import student_subject,student,subject
from operator import and_,or_



#checking if the student enrolled subject  already ,if not the he can enroll
def subscribe_to_subject(student_id, subject_id, connection):
   check = connection.query(student_subject.StudentSubject.student_id,student_subject.StudentSubject.subject_id,student_subject.StudentSubject.subscription_time).filter(
                            and_(
                                student_subject.StudentSubject.student_id == student_id,
                                student_subject.StudentSubject.subject_id == subject_id
                            )).all()
   if not check:
    #adding new student who enrolled the subject
    obj = student_subject.StudentSubject(student_id=student_id,subject_id=subject_id)
    connection.add(obj)
    connection.commit()
    return {
        'id': obj.id
    }
   else:
    return{
        'status': 'success',
        'message': None,
        'data': "already exits"
    }


def change_student_subject(student_id, old_subject_id, new_subject_id, connection):
    obj = connection.query(student_subject.StudentSubject).filter(
        and_(
            student_subject.StudentSubject.student_id == student_id,
            student_subject.StudentSubject.subject_id == old_subject_id
        )
    ).first()

    if obj is not None:
        obj.subject_id = new_subject_id
        connection.commit()

        return True

    return False

#to delete 
def delete_subscription(connection,student_id,subject_id):
    obj = connection.query(student_subject.StudentSubject).filter(
        and_(
            student_subject.StudentSubject.student_id == student_id,
            student_subject.StudentSubject.subject_id == subject_id
        )
    ).first()
   # for eachrow in obj:
    connection.delete(obj)
    connection.commit()

#to view students
def toviewstudents(subject_id,connection):
    obj = connection.query(student_subject.StudentSubject.id,student_subject.StudentSubject.student_id,student.Student.name,student_subject.StudentSubject.subscription_time
                           ).join(student.Student,student_subject.StudentSubject.student_id == student.Student.id
                          ).filter( student_subject.StudentSubject.subject_id == subject_id).all()
    data=[]
    for row in obj:
        data.append({
            'id' : row.id,
            'student_id':row.student_id,
            'student_name':row.name,
            'subscription_time':str(row.subscription_time)
        })
    return data

#can use the below two methods but theses are not efficient!! for big tables
globData =[]
#get subjects enrolled for specific student
def subjects_enrolled(student_id,connection):
    obj = connection.query(student_subject.StudentSubject.subject_id,subject.Subject.name,student_subject.StudentSubject.id).join(subject.Subject,student_subject.StudentSubject.subject_id == subject.Subject.id
    ).filter(
          student_subject.StudentSubject.student_id == student_id,   
    ).all()
    
    data=[]

    for row in obj:
        globData.append(
            {
                'subject_id':row.subject_id
            }
        )

    for row in obj:
        data.append({
            'subject_id' : row.subject_id,
            'subject_name':row.name,
            'id':row.id
        })
    return data


def subjects_not_enrolled(student_id,connection):
    print(globData)
    res = []
    for idx,sub in enumerate(globData):
        res.append(list(sub.values()))
        
    print("The converted list : " + str(res))

    check_list = []
    for sublist in res: 
       for item in sublist:
           check_list.append(item)
    
    print(check_list)

    result = connection.query(student_subject.StudentSubject.subject_id,subject.Subject.name).join(subject.Subject,student_subject.StudentSubject.subject_id == subject.Subject.id).filter(
                  subject.Subject.id.not_in(check_list)
    ).distinct().all()
    
    data=[]
    for row in result:
        data.append({
            'subject_id' : row.subject_id,
            'subject_name':row.name
        })
    return data
