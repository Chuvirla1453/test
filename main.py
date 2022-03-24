from flask import Flask
from data import db_session, users, jobs
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ghjmvghjmnvghjmvnfgc'
USER = {'surname': [None], 'name': [None], 'age': [None],
        'position': [None], 'speciality': [None], 'address': [None],
        'email': [None]}
JOB = {'team_leader': [None], 'job': [None], 'work_size': [None],
       'collaborators': [None], 'start_date': [None],
       'finish_date': [None], 'is_finished': [None]}


def clear_user():
    global USER
    USER = {'surname': None, 'name': None, 'age': None,
            'position': None, 'speciality': None, 'address': None,
            'email': None}


def clear_job():
    global JOB
    JOB = {'team_leader': None, 'job': None, 'work_size': None,
           'collaborators': None, 'start_date': None,
           'finish_date': None, 'is_finished': None}


def add_user(us):
    db_sess = db_session.create_session()
    for i in range(len(us['name'])):
        user = users.User()
        user.surname = us['surname'][i]
        user.name = us['name'][i]
        user.age = us['age'][i]
        user.position = us['position'][i]
        user.speciality = us['speciality'][i]
        user.address = us['address'][i]
        user.email = us['email'][i]
        db_sess.add(user)
    db_sess.commit()


def add_job(j):
    db_sess = db_session.create_session()
    job = jobs.Jobs()
    for i in range(len(j['job'])):
        job.job = j['job'][i]
        job.work_size = j['work_size'][i]
        job.collaborators = j['collaborators'][i]
        job.start_date = j['start_date'][i]
        job.finish_date = j['finish_date'][i]
        job.is_finished = j['is_finished'][i]
        job.team_leader = j['team_leader'][i]
        db_sess.add(job)
        db_sess.commit()


def main():
    db_session.global_init("db/mars_explorer.db")
    USER['surname'] = ['Scott', 'Daniel', 'Sanders', 'Rommel']
    USER['name'] = ['Ridley', 'Jack', 'Teddy', 'Erwin']
    USER['age'] = [21, 32, 45, 50]
    USER['position'] = ['captain', 'flight engineer', 'flight controller', 'doctor']
    USER['speciality'] = ['research engineer', 'flight engineer', 'programmer', 'radiation protection specialist']
    USER['address'] = ['module_1', 'module_2', 'module_1', 'medical_module']
    USER['email'] = ['scott_chief@mars.org', 'jack_daniel@mars.org', 'teddy_sanders@mars.org', 'desert_fox@mars.org']
    add_user(USER)
    JOB['team_leader'] = [1]
    JOB['job'] = ['deployment of residential modules 1 and 2']
    JOB['work_size'] = [15]
    JOB['collaborators'] = ['2, 3, 4']
    JOB['is_finished'] = [False]
    JOB['start_date'] = [datetime.datetime.now()]
    add_job(JOB)
    # app.run()


if __name__ == '__main__':
    main()