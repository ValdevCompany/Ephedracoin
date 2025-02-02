from flask import Flask, render_template, request, redirect, url_for
from transformers import pipeline

app = Flask(__name__, template_folder='C:/Users/User/Desktop/Алишер/Ephedra/code', static_folder='C:/Users/User/Desktop/Алишер/Ephedra/static')

todos = []

# Инициализация модели для генерации задач с помощью GPT
generator = pipeline("text-generation", model="gpt2")


def generate_detailed_task(todo):
    # Генерация более конкретной задачи с помощью GPT
    prompt = f"Пожалуйста, помогите описать задачу на основе: {todo}. Опишите задачу в 200 символах или меньше."
    generated_task = generator(prompt, max_length=200, num_return_sequences=1)[0]['generated_text']

    # Обрезаем результат, чтобы он не превышал 200 символов
    return generated_task[:200]


@app.route('/')
def index():
    return render_template('tdi.html', todos=todos)


@app.route('/add', methods=['POST'])
def add_todo():
    todo = request.form.get('todo')

    if todo:
        # Используем ИИ для генерации более детализированной задачи
        detailed_task = generate_detailed_task(todo)
        todos.append(detailed_task)

    return redirect(url_for('index'))


@app.route('/delete/<int:index>')
def delete_todo(index):
    if 0 <= index < len(todos):
        del todos[index]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)