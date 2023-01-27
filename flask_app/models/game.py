from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app.models import user


class Games:
    def __init__(self, data):
        self.id = data['id']
        self.home_team = data['home_team']
        self.away_team = data['away_team']
        self.location = data['location']
        self.sport = data['sport']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.created_by = None
    db = "sports"


    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM games LEFT JOIN users ON games.user_id = users.id'
        results = connectToMySQL(cls.db).query_db(query)
        game = []
        for row in results:
            userdata = {
                'id': row['id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at'],
            }
            oneGame = cls(row)
            oneGame.created_by = user.User(userdata)
            game.append(oneGame)
        return game

    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM games LEFT JOIN users ON games.user_id = users.id WHERE games.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        oneGame = cls(results[0])
        data = results[0]
        userdata = {
            'id': data['id'],
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
            'email' : data['email'],
            'password' : data['password'],
            'created_at' : data['created_at'],
            'updated_at' : data['updated_at'],
        }
        oneGame.created_by = user.User(userdata)
        return oneGame
    
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO games (home_team, away_team, location, sport, user_id) VALUES(%(home_team)s, %(away_team)s, %(location)s, %(sport)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE games SET home_team=%(home_team)s, away_team=%(away_team)s, location=%(location)s, sport=%(sport)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM games WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def game_user(cls, data):
        query = 'SELECT * FROM games LEFT JOIN users ON games.user_id = users.id WHERE games.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        allGames = []
        for row in results:
            game = cls(results[0])
            userData = {
                'id': row['user.id'],
                'firstName': row['firstName'],
                'lastName': row['lastName'],
                'email': row['email'],
                'password': row['password'],
                'createdAt': row['user.createdAt'],
                'updatedAt': row['user.updatedAt']
            }
            oneUser = user.User(userData)
            game.user = oneUser
            allGames.append(game)
            return allGames
    
    @staticmethod
    def validate_game(data):
        isvalid = True
        if len(data['home_team']) < 1:
            flash("Home team name is required")
            isvalid = False
        if len(data['away_team']) < 1:
            flash("Away team name is required")
            isvalid = False
        if len(data['location']) < 1:
            flash("Location is required")
            isvalid = False
        if len(data['sport']) < 1:
            flash("Sport name is required")
            isvalid= False
        return isvalid
