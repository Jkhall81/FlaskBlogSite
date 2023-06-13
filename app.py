from flask import Flask, render_template, request
import json


app = Flask(__name__)
with open('data.json', 'r') as f:
    blog_posts = json.load(f)


@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # we will fill this in later
        pass
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
