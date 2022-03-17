from app.config.mysqlconnection import connectToMySQL
from flask import flash

class Dojo:
    db='dojo_survey_schema'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.language = data['language']
        self.comments = data['comments']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos ORDER BY created_at DESC;"
        results = connectToMySQL(cls.db).query_db(query)
        dojos = []
        for d in results:
            dojos.append(cls(d))
        return dojos
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM dojos WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO dojos (name, location, language, comments, created_at, updated_at) VALUES (%(name)s, %(location)s, %(language)s, %(comments)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE dojos SET name=%(name)s, location=%(location)s, language=%(language)s, comments=%(comments)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM dojos WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
        
    @staticmethod
    def validate(dojo):
        is_valid = True
        if len(dojo['name']) < 2:
            flash('Name must be at least two characters.')
            is_valid = False
        if len(dojo['location']) < 1 or dojo['location'] == '--Select A Location--':
            flash(f'Location must be selected.', dojo['location'])
            is_valid = False
        if len(dojo['language']) < 1 or dojo['language'] == '--Select A Language--':
            flash(f'Language must be selected.', dojo['language'])
            is_valid = False
        if len(dojo['comments']) < 2:
            flash('Comments must be at least two characters.')
            is_valid = False
        return is_valid