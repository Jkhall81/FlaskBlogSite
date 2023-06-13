from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)


def open_data(filename):
    with open(filename, 'r') as f:
        blog_posts = json.load(f)
        return blog_posts


def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)


def generate_new_id(blog_posts):
    if blog_posts:
        last_post = blog_posts[-1]['id']
        new_id = last_post + 1
    else:
        new_id = 1
    return new_id


@app.route('/')
def index():
    blog_posts = open_data('data.json')
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # grab the posted data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        blog_posts = open_data('data.json')

        new_id = generate_new_id(blog_posts)

        # create new post entry
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        # append new post
        blog_posts.append(new_post)

        # save json
        save_data(blog_posts)

        return redirect('/')

    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)
