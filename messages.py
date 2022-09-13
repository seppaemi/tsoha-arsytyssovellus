from db import db
import users,regions

def get_list_message(region_content,time):
    region_id = regions.get_region_id(region_content,time)
    sql = "SELECT M.content, U.username, M.sent_at, M.id FROM messages M, users U, regions R WHERE M.user_id=U.id AND M.region_id = R.id AND R.id=:region_id AND M.region_id=:region_id AND M.visible=True AND R.sent_at=:region_creation_time ORDER BY M.id"
    result = db.session.execute(sql, {"region_id":region_id, "region_creation_time":time})
    return result.fetchall()

def search(query):
    sql = "SELECT M.content, R.content, U.username, M.sent_at, M.id FROM messages M, regions R, users U WHERE M.content LIKE :query AND M.region_id = R.id AND R.visible=True AND M.visible=True and M.user_id=U.id"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    messages = result.fetchall()
    return messages

def get_list_info():
    sql = "SELECT day, time, message_id, location FROM info"
    result = db.session.execute(sql)
    return result.fetchall()    

def send_message(message_content,region_content,time,info_date,info_time,location):
    user_id = users.user_id()
    region_id = regions.get_region_id(region_content,time)
    if user_id == 0:
        return False
    sql_messages = "INSERT INTO messages (content, user_id, region_id, sent_at, visible) VALUES (:content, :user_id, :region_id, NOW(), True) RETURNING id"
    result = db.session.execute(sql_messages, {"content":message_content, "user_id":user_id, "region_id":region_id})
    db.session.commit()
    message_id = result.fetchone()[0]
    sql_info = "INSERT INTO info (day,time,message_id,location) VALUES (:info_date, :info_time, :message_id, :location)"
    db.session.execute(sql_info, {"info_date":info_date, "info_time":info_time, "message_id":message_id, "location":location})
    db.session.commit()
    return message_id

def get_message(message_id):
    sql = "SELECT content FROM messages WHERE id=:message_id AND visible=True"
    result = db.session.execute(sql, {"message_id":message_id})
    list_res = result.fetchone()
    message_content = list_res[0]
    return message_content

def get_message_creator_id(message_id):
    sql= "SELECT user_id FROM messages WHERE id=:message_id"
    result = db.session.execute(sql, {"message_id":message_id})
    list_res = result.fetchone()
    msg_creator_id = list_res[0]
    return msg_creator_id

def get_message_creator_name(message_id):
    sql= "SELECT username FROM messages M, users U WHERE M.id=:message_id and U.id=M.user_id"
    result = db.session.execute(sql, {"message_id":message_id})
    list_res = result.fetchone()
    msg_creator_id = list_res[0]
    return msg_creator_id

def edit_message(message_id, edited_message):
    sql= "UPDATE messages SET content=:edited_message WHERE id=:message_id"
    db.session.execute(sql, {"edited_message":edited_message, "message_id":message_id,})
    db.session.commit()
    return True

def delete_message(message_id):
    sql = "UPDATE messages SET visible=False WHERE id=:message_id"
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return True

def ger_region_id_with_msg_id(message_id):
    sql= "SELECT region_id FROM messages WHERE id=:message_id"
    result = db.session.execute(sql, {"message_id":message_id})
    list_res = result.fetchone()
    region_id = list_res[0]
    return region_id