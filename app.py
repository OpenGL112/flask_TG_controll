from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {username}'

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    return f'Hello {name}!'

if __name__ == '__main__':
    app.run()

#https://habr.com/ru/articles/783574/ ПРОДОЛЖИТЬ ЧИТАТЬ ОТСЮДА