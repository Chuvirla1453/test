from flask import Flask, render_template, url_for

app = Flask(__name__)
@app.route('/')
def start_page():
    return '<a href="http://127.0.0.1:8080/Заготовка"> Заготовка </a>'

@app.route('/<title>')
def base_page(title):
    return render_template("base.html", image_url=url_for('static', filename='img/mars.jpg'), title=title)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')