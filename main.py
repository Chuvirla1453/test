from flask import Flask, render_template, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from data import db_session, users, jobs
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from forms.add_work import AddJobForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ghjmvghjmnvghjmvnfgc'

login_manager = LoginManager()
login_manager.init_app(app)
params = {}


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
                       job.is_finished, job.user])
    params['table_data'] = output
    return render_template('work_log.html', **params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, **params)
    return render_template('login.html', title='Авторизация', form=form, **params)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form, **params)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_work', methods=['GET', 'POST'])
def add_work():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = jobs.Jobs(
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            start_date=form.start_date.data,
            finish_date=form.finish_date.data,
            is_finished=form.is_finished.data,
            team_leader=form.team_leader.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect("/")
    return render_template('add_work.html', title='Добавление работы', form=form, **params)


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = AddJobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(jobs.Jobs).filter(jobs.Jobs.id == id,
                                              ((jobs.Jobs.user == current_user) | (current_user.position == 'captain'))
                                          ).first()
        if job:
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.start_date.data = job.start_date
            form.finish_date.data = job.finish_date
            form.is_finished.data = job.is_finished
            form.team_leader.data = job.team_leader
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(jobs.Jobs).filter(jobs.Jobs.id == id,
                                              ((jobs.Jobs.user == current_user) | (current_user.position == 'captain'))
                                              ).first()
        if job:
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.start_date = form.start_date.data
            job.finish_date = form.finish_date.data
            job.is_finished = form.is_finished.data
            job.team_leader = form.team_leader.data
            db_sess.commit()
            return redirect("/")
        else:
            abort(404)

    return render_template('add_work.html',title='Редактирование работы', form=form, **params)


@app.route('/job_delete/<int:id>')
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(jobs.Jobs).filter(jobs.Jobs.id == id,
                                          ((jobs.Jobs.user == current_user) | (current_user.position == 'captain'))
                                          ).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(users.User).get(user_id)


def main():
    db_session.global_init('db/mars_explorer.db')
    app.run()


if __name__ == '__main__':
    main()
    