from flask import Flask, render_template
import random

app = Flask(__name__, template_folder='C:/Users/User/Desktop/Алишер/Ephedra/code', static_folder='C:/Users/User/Desktop/Алишер/Ephedra/static')

# Массив с иконками животных
animal_icons = [
    '🐶', # Собака
    '🐱', # Кошка
    '🐭', # Мышь
    '🐹', # Хомяк
    '🐰', # Кролик
    '🦊', # Лиса
    '🐻', # Медведь
    '🐼', # Панда
    '🐯', # Тигр
    '🦁', # Лев
    '🐨', # Коала
    '🐧', # Пингвин
]

@app.route('/')
def index():
    return render_template('cc.html')

@app.route('/account')
def account():
    animal_icon = random.choice(animal_icons)
    return render_template('account.html', animal_icon=animal_icon)

@app.route('/flip')
def flip():
    return render_template('coinflip.html')

@app.route('/cube')
def cube():
    return render_template('cube.html')

@app.route('/avtomat')
def avtomat():
    return render_template('baraban.html')

@app.route('/acc')
def acc():
    return render_template('acc.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
