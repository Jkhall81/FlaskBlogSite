from flask import Flask, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = '23ydk83%ladkjj4319lasdf'


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


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = open_data('data.json')

    post_index = None
    for index, post in enumerate(blog_posts):
        if post['id'] == post_id:
            post_index = index
            break

    if post_index is not None:
        blog_posts.pop(post_index)

        save_data(blog_posts)
        flash('Post deleted successfully!')
        return redirect(url_for('index'))
    else:
        flash('Post not found')
        return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = open_data('data.json')

    post_index = None
    post = None

    for index, p in enumerate(blog_posts):
        if p['id'] == post_id:
            post_index = index
            post = p
            break

    if request.method == 'POST':
        # grab the posted data
        blog_posts[post_index]['author'] = request.form.get('blog_author')
        blog_posts[post_index]['title'] = request.form.get('blog_title')
        blog_posts[post_index]['content'] = request.form.get('blog_content')

        save_data(blog_posts)
        flash('Post updated successfully!')
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
