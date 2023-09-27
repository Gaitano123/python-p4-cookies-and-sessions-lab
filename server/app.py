#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    list = []
    for article in articles:
        atricle_dict = {
            "id": article.id,
            "author": article.author,
            "title": article.title,
            "content": article.content,
            "preview": article.preview,
            "minutes_to_read": article.minutes_to_read,
            "date": article.date,
            "user_id": article.user_id  
        }
        list.append(atricle_dict)
    return make_response(jsonify(list), 200)

@app.route('/articles/<int:id>')
def show_article(id):
    session ['page_views'] = session.get('page_views', 0)
    
    session['page_views'] += 1
     
    if session['page_views'] > 3:
        return make_response(jsonify({'message' : 'Maximum pageview limit reached'}), 401)
    
    article = Article.query.filter(Article.id == id).first()
    article_dict ={
            "id": article.id,
            "author": article.author,
            "title": article.title,
            "content": article.content,
            "preview": article.preview,
            "minutes_to_read": article.minutes_to_read,
            "date": article.date,
            "user_id": article.user_id 
    }
    
    return make_response(jsonify(article_dict), 200)

if __name__ == '__main__':
    app.run(port=5555)
