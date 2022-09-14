from db import db

def create(topic, hidden):
    if topic.strip():
        sql = "INSERT INTO forums (hide, topic) VALUES (:hide, :topic);"
        db.session.execute(sql, {"hide":hidden, "topic":topic})
        db.session.commit()
        return True
    return False

def delete(forum_id):
    if (forum_id):
        sql = "DELETE FROM forums WHERE forums.id=:id"
        db.session.execute(sql, {"id":forum_id})
        db.session.commit()

def exists(forum_id):
    sql = "SELECT 1 FROM forums WHERE id=:forum_id;"
    result = db.session.execute(sql, {"forum_id":forum_id})
    return result.fetchone() is not None

def get(forum_id):
    sql = "SELECT * FROM forums WHERE id=:id;"
    result = db.session.execute(sql, {"id":forum_id})
    return result.fetchone()

def get_all():
    subquery = f"SELECT forums.id, MAX(messages.sent_at) AT TIME ZONE 'Etc/UTC' AT TIME ZONE 'Europe/Helsinki' AS lastmsg FROM messages " \
    "LEFT JOIN threads ON messages.thread_id=threads.id " \
    "LEFT JOIN forums ON threads.forum_id=forums.id " \
    "GROUP BY forums.id"

    sql = "SELECT forums.*, subq.lastmsg FROM forums " \
    f"LEFT JOIN ({subquery}) AS subq ON subq.id=forums.id " \
    "ORDER BY forums.topic ASC;"
    result = db.session.execute(sql)
    forums = result.fetchall()
    return forums

def get_allowed(forum_id):
    sql = "SELECT user_id FROM allow WHERE forum_id=:forum_id;"
    result = db.session.execute(sql, {"forum_id":forum_id}).fetchall()
    return [r[0] for r in result]