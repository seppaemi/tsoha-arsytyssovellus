from app import db
from amount import decrement, increment

def create(text, thread_id, user_id):
    if text.strip():
        sql = "INSERT INTO messages (thread_id, user_id, content, sent_at) VALUES (:thread_id, :user_id, :content, NOW());"
        db.session.execute(sql, {"thread_id":thread_id, "user_id":user_id, "content":text})
        db.session.commit()

        increment(thread_id)

        return True
    return False

def delete(message_id, admin, user_id, thread_id):
    if admin:
        sql = "DELETE FROM messages WHERE id=:message_id"
        params = {"message_id":message_id}
    else:
        sql = "DELETE FROM messages WHERE id=:message_id AND user_id=:user_id;"
        params = {"message_id":message_id, "user_id":user_id}

    db.session.execute(sql, params)
    db.session.commit()

    decrement(thread_id)

def edit(message_id, content, admin, user_id):
    if admin:
        sql = "UPDATE messages SET content=:content WHERE id=:message_id;"
    else:
        sql = "UPDATE messages SET content=:content WHERE id=:message_id AND user_id=:user_id;"
    
    db.session.execute(sql, {"content":content, "message_id":message_id, "user_id":user_id})
    db.session.commit()

def get_all(thread_id):
    sql = f"SELECT messages.id, messages.thread_id, messages.content, messages.sent_at AT TIME ZONE 'Etc/UTC' AT TIME ZONE 'Europe/Helsinki' as sent_at, users.username FROM messages " \
    "LEFT JOIN users ON messages.user_id=users.id WHERE thread_id=:id " \
    "ORDER BY sent_at ASC;"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchall()

def search(query):
    sql = f"SELECT messages.id, messages.thread_id, messages.content, messages.sent_at AT TIME ZONE 'Etc/UTC' AT TIME ZONE 'Europe/Helsinki' AS sent_at, users.username, threads.title, threads.forum_id, forums.hide FROM messages " \
    "LEFT JOIN threads ON threads.id=messages.thread_id " \
    "LEFT JOIN forums ON threads.forum_id=forums.id " \
    "LEFT JOIN users ON users.id=messages.user_id " \
    "WHERE messages.content ILIKE :query;"

    result = db.session.execute(sql, {"query":f"%{query}%"})
    return result.fetchall()