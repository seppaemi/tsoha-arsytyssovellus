from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def user_exists(username):    
    sql = "SELECT users.id FROM users WHERE username=:name"
    result = db.session.execute(sql, {"name":username}).fetchone()
    return result is not None

def allow(user_id, forum_id):
    sql = "INSERT INTO allow(user_id, forum_id) VALUES (:user_id, :forum_id);"
    db.session.execute(sql, {"user_id":user_id, "forum_id":forum_id})
    db.session.commit()

def disallow(user_id, forum_id):
    sql = "DELETE FROM allow WHERE user_id=:user_id AND forum_id=:forum_id;"
    db.session.execute(sql, {"user_id":user_id, "forum_id":forum_id})
    db.session.commit()

def allowed(user_id, forum_id):
    sql = "SELECT 1 FROM allow WHERE user_id=:user_id AND forum_id=:forum_id;"
    result = db.session.execute(sql, {"user_id":user_id, "forum_id":forum_id}).fetchone()
    return result is not None

def get(username):
    sql = "SELECT * FROM users WHERE username=:name"    
    return db.session.execute(sql, {"name":username}).fetchone()

def get_all():
    sql = "SELECT id, administrator, username FROM users;"
    return db.session.execute(sql).fetchall()

def get_allowed_forums(user_id):
    sql = "SELECT forum_id FROM allow WHERE user_id=:user_id;"
    result = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return [r[0] for r in result]

def register(username, password):
    password = generate_password_hash(password)
    sql = "INSERT INTO users (administrator, username, password) VALUES ('false', :name, :password);"
    db.session.execute(sql, {"name":username, "password":password})
    db.session.commit()

def check_password(username, password):
    user_sql = "SELECT password FROM users WHERE username=:username"
    compare = db.session.execute(user_sql, {"username":username}).fetchone()[0]
    if check_password_hash(compare, password):
        return get(username)
    else:
        return None

def promote(user_id):
    sql = "UPDATE users SET administrator='1' WHERE id=:id;"
    db.session.execute(sql, {"id":user_id})
    db.session.commit()

def demote(user_id):
    sql = "UPDATE users SET administrator='0' WHERE id=:id;"
    db.session.execute(sql, {"id":user_id})
    db.session.commit()