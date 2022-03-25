from flask import Flask, render_template, url_for
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
params = {}


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


@app.route('/')
def work_log():
    global params
    params["mars_image_url"] = url_for('static', filename='img/mars.jpg')
    db_sess = db_session.create_session()

    output = []
    for job in db_sess.query(jobs.Jobs):
        output.append([job.id, job.job, db_sess.query(users.User).filter(users.User.id == job.team_leader)[0].name +
                       ' ' + db_sess.query(users.User).filter(users.User.id == job.team_leader)[0].surname,
                       str(job.work_size) + ' hours', job.collaborators,
                       job.is_finished])
    params['table_data'] = output
    return render_template('work_log.html', **params)


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
    db_session.global_init('db/mars_explorer.db')
    app.run()


if __name__ == '__main__':
    main()