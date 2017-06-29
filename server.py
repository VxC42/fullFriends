from flask import Flask, request, redirect, render_template, session, flash
from validations import formIsValid
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key="secretsrunsdeep"

mysql = MySQLConnector(app, 'fullFriends')

@app.route('/')
def index():
    friends = mysql.query_db("SELECT * FROM friends")
    return render_template('/index.html', all_friends = friends)


@app.route('/submit', methods=['POST'])
def create():
    state = formIsValid(request.form)
    if (state['isValid']):
        query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email': request.form['email']
            }
        mysql.query_db(query, data)
        return redirect('/')
    else:
        print "error"
        for error in state['errors']:
            flash(error)
            return redirect('/')

@app.route('/edit/<id>', methods=['POST'])
def show(id):
    query = "SELECT * FROM friends WHERE id = :id"
    data = {'id': id}
    friends = mysql.query_db(query, data)
    return render_template('edit.html', one_friend = friends[0])

@app.route('/update/<id>', methods=['POST'])
def update(id):
    query ="UPDATE friends SET first_name = :first_name, last_name = :last_name, email = :email WHERE id = :id"
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email': request.form['email'],
        'id':id
        }
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    query = "DELETE FROM friends WHERE id=:id"
    data = {
        'id':id
        }
    mysql.query_db(query, data)
    return redirect('/')




app.run(debug=True)
