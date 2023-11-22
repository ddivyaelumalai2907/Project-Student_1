from sqlalchemy import text
from model import student

def get_student_by_id(id, connection):
    query = text("select id, name, joined_time from training.student where id = :student_id")
    result = connection.execute(query, {'student_id': id})

    for row in result:
        return {
            'id': row.id,
            'name': row.name,
            'joined_time': str(row.joined_time)
        }

    return None

def get_student_by_id_model(id, connection):
    row = connection.query(student.Student).filter(student.Student.id == id).first()
    if row is not None:
        return {
            'id': row.id,
            'name': row.name,
            'joined_time': str(row.joined_time)
        }

    return None

#add new student
def new_student(student_name,connection):
    
    obj = student.Student(name = student_name)
    connection.add(obj)
    connection.commit()
    
    return {
        'id': obj.id
    } 

def change_student_name(old_name, new_name, connection):
    obj = connection.query(student.Student).filter(
            student.Student.name == old_name
    ).first()

    if obj is not None:
        obj.name = new_name
        connection.commit()

        return True

    return False

#student login

def student_login(id,name,connection):

    obj = connection.query(student.Student).filter(
        and_(
            student.Student.id == id,
            student.Student.name == name
        )
    ).first()

    if obj is not None:
        return True
    
    return False
