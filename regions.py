from db import db
import users, messages

def get_list_region():
    sql = "SELECT R.content, U.username, R.sent_at FROM regions R, users U WHERE R.user_id=U.id AND R.visible=True ORDER BY R.id"
    result = db.session.execute(sql)
    return result.fetchall()

def sent_region(title):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO regions (content, user_id, sent_at, visible) VALUES (:content, :user_id, NOW(), True)"
    result = db.session.execute(sql, {"content":title, "user_id":user_id})
    db.session.commit()
    return True

def get_region_id(region_content,time):
    sql_region_id = "SELECT id FROM regions WHERE content=:content AND sent_at=:time"
    region_id_res = db.session.execute(sql_region_id, {"content":region_content, "time":time})
    list_region_id = region_id_res.fetchone()
    region_id = list_region_id[0]
    return region_id


def get_region_creator_id(region_id):
    sql= "SELECT user_id FROM regions WHERE id=:region_id"
    result = db.session.execute(sql, {"region_id":region_id})
    list_result = result.fetchone()
    region_creator_id = list_result[0]
    return region_creator_id

def get_region_sent(region_content,message_id):
    region_id = messages.get_region_id_with_msg_id(message_id)
    sql = "SELECT sent_at FROM regions WHERE content=:region_content AND id=:region_id"
    result = db.session.execute(sql, {"region_content":region_content,"region_id":region_id})
    list_result = result.fetchone()
    region_sent_at = list_result[0]
    return region_sent_at


def get_region_content(message_id):
    region_id_sql = "SELECT region_id FROM messages WHERE id=:message_id AND visible=True"
    region_id_res = db.session.execute(region_id_sql, {"message_id":message_id})
    list_region_id = region_id_res.fetchone()
    region_id = list_region_id[0]

    region_content_sql = "SELECT content FROM regions WHERE id=:region_id"
    region_conten_red = db.session.execute(region_content_sql, {"region_id":region_id})
    list_region_content = region_conten_red.fetchone()
    region_content = list_region_content[0]
    return region_content
