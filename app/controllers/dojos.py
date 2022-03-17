from flask import Flask, session, render_template, redirect, request, flash
from app import app
from app.models.dojo import Dojo
# from app.models import dojo


#home
@app.route('/')
def index():
    return render_template("index.html")

#hidden route - post values to DB
@app.route('/process', methods=['POST'])
def process():
    data = {
        'name' : request.form['name'],
        'location' : request.form['location'],
        'language' : request.form['language'],
        'comments' : request.form['comments']
    }
    if not Dojo.validate(request.form):
        return redirect('/')
    print('Data submitted Successfully!')
    Dojo.save(data)
    return redirect('/result')


@app.route('/result', methods=['GET'])
def result():
    return render_template('result.html', names=Dojo.get_all())

