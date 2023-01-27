from flask_app import app 
from flask import  render_template, redirect, session, request, flash
from flask_app.models.game import Games
from flask_app.models.user import User
from .users import dashboard



@app.route('/addGame')
def addGame():
    if 'users_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['users_id']
        }
    theUser = User.get_by_id(data)
    return render_template('add_game.html', user=theUser)


@app.route('/createGame', methods=['POST'])
def createGame():
    isValid = Games.validate_game(request.form)
    if not isValid:
        return redirect('/addGame')
    data = {
        'home_team': request.form['home_team'],
        'away_team': request.form['away_team'],
        'location': request.form['location'],
        'sport': request.form['sport'],
        'user_id': session['users_id'],
    }
    print(data)
    Games.save(data)
    return redirect('/dashboard')

@app.route('/game/view/<int:id>')
def viewGame(id):
    data = {
        "id": id
    }
    return render_template('view_game.html', oneGame = Games.get_by_id(data))

@app.route('/game/edit/<int:id>')
def editGame(id):
    if 'users_id' not in session:
        return redirect('/')
    else:
        userdata = {
            'id': session['users_id']
        }
    theUser = User.get_by_id(userdata)
    data = {
        "id" : id
    }
    return render_template('edit_game.html', user = theUser, oneGame = Games.get_by_id(data))


@app.route('/updateGame', methods=['POST'])
def updateGame():
    isValid = Games.validate_game(request.form)
    if not isValid:
        return redirect(f'game/edit/{request.form["id"]}')
    Games.update(request.form)
    return redirect('/dashboard')

@app.route('/game/delete/<int:id>')
def deleteGame(id):
    data = {
        "id" : id
    }
    Games.delete(data)
    return redirect('/dashboard')