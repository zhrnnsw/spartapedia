from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests

client = MongoClient('mongodb+srv://riVFerd:test_mongodb@cluster0.rq9u845.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

def get_meta(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0'}

    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    image = soup.select_one('meta[property="og:image"]')['content']
    title = soup.select_one('meta[property="og:title"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']
    
    return {
        'image': image,
        'title': title,
        'desc': desc
    }

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/movie', methods=['POST'])
def movie_post():
    star = request.form['star_give']
    comment = request.form['comment_give']
    meta = get_meta(request.form['url_give'])
    
    image = meta['image']
    title = meta['title']
    desc = meta['desc']
    
    db.movies.insert_one({
        'image': image,
        'title': title,
        'desc': desc,
        'star': star,
        'comment': comment
    })
    
    return jsonify({
        'msg': 'POST request!'
    })

@app.route('/movie', methods=['GET'])
def movie_get():
    movie_list = list(db.movies.find({}, {'_id': False}))
    return jsonify({
        'movies': movie_list,
        'msg': 'GET request!'
    })

if __name__ == '__main__':
    app.run('0.0.0.0', port=5555, debug=True)