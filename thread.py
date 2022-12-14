from db import db 
import amount

def create(title, forum_id, user_id):
    if title.strip():
        sql = "INSERT INTO threads(forum_id, created_by, title, created_at) VALUES (:forum_id, :user_id, :title, NOW())"
        db.session.execute(sql, {"forum_id":forum_id, "user_id":user_id, "title":title})
        db.session.commit()
        amount.increment_tc(forum_id)
        return True
    return False

def delete(forum_id, thread_id, admin, user_id):
    count_sql = "SELECT messagecount FROM threads WHERE threads.id=:thread_id;"
    count = db.session.execute(count_sql, {"thread_id":thread_id}).fetchone()[0]
    if admin:
        sql = "DELETE FROM threads WHERE id=:thread_id"
        params = {"thread_id":thread_id}
    else:
        sql = "DELETE FROM threads WHERE id=:thread_id AND created_by=:user_id;"
        params = {"thread_id":thread_id, "user_id":user_id}    
    db.session.execute(sql, params)
    db.session.commit()
    amount.sub(forum_id, count)
    amount.decrement_tc(forum_id)

def edit(thread_id, title, admin, user_id):
    if admin:
        sql = "UPDATE threads SET title=:title WHERE threads.id=:thread_id;"
    else:
        sql = "UPDATE threads SET title=:title WHERE threads.id=:thread_id AND threads.created_by=:user_id;"
    db.session.execute(sql, {"title":title, "thread_id":thread_id, "user_id":user_id})
    db.session.commit()

def get(thread_id):
    sql = "SELECT * FROM threads WHERE id=:id;"    
    result = db.session.execute(sql, {"id": thread_id})
    return result.fetchone()

def get_all(forum_id):
    subquery = f"SELECT threads.id, MAX(messages.sent_at) AT TIME ZONE 'Etc/UTC' AT TIME ZONE 'Europe/Helsinki' AS lastmsg FROM messages " \
    "LEFT JOIN threads ON messages.thread_id=threads.id " \
    "LEFT JOIN forums ON threads.forum_id=forums.id " \
    "GROUP BY threads.id"
    sql = "SELECT threads.id, threads.title, threads.messagecount, users.username, subq.lastmsg FROM threads " \
        "LEFT JOIN users ON threads.created_by=users.id " \
        f"LEFT JOIN ({subquery}) AS subq ON subq.id=threads.id" \
        " WHERE threads.forum_id=:id " \
        "ORDER BY subq.lastmsg DESC;"
    result = db.session.execute(sql, {"id":forum_id})
    return result.fetchall()

def parent(thread_id):
    sql = "SELECT forum_id FROM threads WHERE id=:thread_id;"
    result = db.session.execute(sql, {"thread_id": thread_id})
    return result.fetchone()[0]