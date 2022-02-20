from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route('/')
def start_page():
    return '<a href="http://127.0.0.1:8080/training/инженер"> Заготовка </a>'


@app.route('/training/<prof>')
def prof_page(prof):
    params = {
        "mars_image_url": url_for('static', filename='img/mars.jpg'),
        "prof": prof
    }
    if 'инженер' in prof or "сторитель" in prof:
        params["training"] = "Инженерные тренажёры"
        params["plan_of_training_image_url"] = url_for('static', filename='img/ES.jpg')
    else:
        params["training"] = "Научные симуляторы"
        params["plan_of_training_image_url"] = url_for('static', filename='img/SS.jpg')
    return render_template("prof.html", **params)


@app.route('/<title>')
def base_page(title):
    return render_template("base.html", image_url=url_for('static', filename='img/mars.jpg'), title=title)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
    print(url_for('static', filename='img/mars.jpg'))