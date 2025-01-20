import sqlite3
from flask import Flask, render_template, request
import requests


conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS preferences (
               id INTEGER PRIMARY KEY,
               genre TEXT,
               favourite_movie TEXT)
               ''')
conn.commit()
conn.close()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')  


@app.route('/recommendations', methods=['POST'])
def recommendations():
    genre = request.form['genre']
    API_KEY = "ccd59db75453c198a99c01446083714a"
    URL = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={genre}"

    response = requests.get(URL)
    movies = response.json()['results']

    
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO preferences (genre) VALUES (?)", (genre,))
    conn.commit()
    conn.close()

    
    return render_template('recommendations.html', movies=movies)  

if __name__ == '__main__':
    app.run(debug=True)
