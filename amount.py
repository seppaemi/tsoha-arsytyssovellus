from db import db
import thread

def increment(thread_id):    
    sql = "UPDATE threads SET messagecount=messagecount+1 WHERE id=:thread_id;"       
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()

    parent_id = thread.parent(thread_id)
    sql = "UPDATE forums SET messagecount=messagecount+1 WHERE id=:forum_id;"    
    db.session.execute(sql, {"forum_id":parent_id})
    db.session.commit()

def decrement(thread_id):
    sql = "UPDATE threads SET messagecount=messagecount-1 WHERE id=:thread_id;"       
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()
    
    parent_id = thread.parent(thread_id)
    sql = "UPDATE forums SET messagecount=messagecount-1 WHERE id=:forum_id;"    
    db.session.execute(sql, {"forum_id":parent_id})
    db.session.commit()

def sub(forum_id, amount):
    sql = f"UPDATE forums SET messagecount=messagecount-{amount} WHERE id=:forum_id;"    
    db.session.execute(sql, {"forum_id":forum_id})
    db.session.commit()

def increment_tc(forum_id):
    sql = "UPDATE forums SET threadcount=threadcount+1 WHERE id=:forum_id;" 
    db.session.execute(sql, {"forum_id":forum_id})
    db.session.commit()

def decrement_tc(forum_id):
    sql = "UPDATE forums SET threadcount=threadcount-1 WHERE id=:forum_id;" 
    db.session.execute(sql, {"forum_id":forum_id})
    db.session.commit()
