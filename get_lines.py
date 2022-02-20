from flask import Flask, render_template, url_for
app = Flask(__name__)
params = {}


@app.route('/')
def start_page():
    params["mars_image_url"] = url_for('static', filename='img/mars.jpg')
    return '<a href="http://127.0.0.1:8080/list_prof/ol"> Заготовка </a>'


@app.route('/training/<prof>')
def prof_page(prof):
    params["prof"] = prof
    if 'инженер' in prof or "сторитель" in prof:
        params["training"] = "Инженерные тренажёры"
        params["plan_of_training_image_url"] = url_for('static', filename='img/ES.jpg')
    else:
        params["training"] = "Научные симуляторы"
        params["plan_of_training_image_url"] = url_for('static', filename='img/SS.jpg')
    return render_template("prof.html", **params)


@app.route("/list_prof/<l>")
def list_prof(l):
    params["type_of_list"] = l
    t = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог',
         'врач', 'инженер по терраформированию', 'климатолог',
         'специалист по радиационной защите', 'астрогеолог', 'гляциолог',
         'инженер жизнеобеспечения', 'метеоролог', 'оператор марсохода',
         'киберинженер', 'штурман', 'пилот дронов']
    params["list_of_professions"] = t
    return render_template("prof_list.html", **params)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
    print(url_for('static', filename='img/mars.jpg'))