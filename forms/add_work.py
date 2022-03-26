from flask_wtf import FlaskForm
from wtforms import DateTimeField, BooleanField, SubmitField, IntegerField, StringField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Количество рабочих часов', validators=[DataRequired()])
    collaborators = StringField('Номера рабочих', validators=[DataRequired()])
    start_date = DateTimeField('Дата начала работы', format='%d/%m/%y')
    finish_date = DateTimeField('Дата конца работы', format='%d/%m/%y')
    is_finished = BooleanField('Работа завершена')
    team_leader = IntegerField('Номер руководителя', validators=[DataRequired()])
    submit = SubmitField('Добавить')