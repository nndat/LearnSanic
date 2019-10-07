from sanic import Sanic, response
from sanic_jinja2 import SanicJinja2
from sanic.response import redirect
from datetime import datetime

import database as db

app = Sanic(__name__)
jinja = SanicJinja2(app)
app.static('/static', './static')


@app.route('/')
@app.route('/index')
async def home(request):
    posts = db.get_all_posts()
    return jinja.render('index.html', request, posts=posts)


@app.route('/post/<id:int>', methods=['GET', 'POST'])
async def post(request, id):
    post = db.get_post(id)
    comments = db.get_comment(id)
    if post is not None:
        return jinja.render('post.html', request, post=post, comments=comments)
    return response.text('no post')


@app.route('/create_post', methods=['GET', 'POST'])
async def create_post(request):
    if len(request.form) > 0:
        title = request.form.get('title')
        content = request.form.get('content')
        post = {
            'create_at': datetime.now(),
            'title': title,
            'content': content
        }
        db.add_post(post)
        return redirect(app.url_for('home'))
    return jinja.render('create_post.html', request)


@app.route('/create_comment/<id:int>', methods=['POST'])
async def create_comment(request, id):
    comment = {
        'post_id': id,
        'content': request.form.get('comment'),
        'create_at': datetime.now()
    }
    db.add_comment(comment)
    return redirect(app.url_for('post', id=id))


@app.route('/manage', methods=['GET', 'POST'])
async def manage(request):
    id = request.form.get('del')
    if id is not None:
        db.delete_post(id)

    id = request.form.get('edit')
    if id is not None:
        return redirect(app.url_for('edit_post', id=id))
    posts = db.get_all_posts()
    return jinja.render('manage.html', request, posts=posts)


@app.route('/edit/<id:int>', methods=['GET', 'POST'])
async def edit_post(request, id):
    if len(request.form) == 0:
        post = db.get_post(id)
        print('*' * 80)
        print(post['content'])
        return jinja.render('edit.html', request, post=post)
    post = {
        'id': id,
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'create_at': datetime.now()
    }
    db.update_post(post)
    return redirect(app.url_for('post', id=post['id']))


@app.route('/about')
async def about(request):
    return jinja.render('about.html', request)


if __name__ == '__main__':
    db.initdb()
    app.run(host='0.0.0.0', port=8000)
