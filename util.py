from flask import session
import copy 

def session_exists():
    return 'user_id' in session

def session_create(user_id, username):
    if session_exists(): return False
    
    session['user_id'] = user_id
    session['username'] = username
    return True

def session_delete():
    if not session_exists(): return False

    session.clear()
    return True

def session_get(key):
    if not session_exists(): return None
    return session[key]

def session_set(key, value):
    if not session_exists(): return False

    session[key] = value
    return True

def session_append(key, element):
    if not session_exists(): return False

    if key not in session or type(session[key]) != type(list()):
        session[key] = list()
    
    session[key] = session[key] + [element]
    return True

def session_dict():
    return dict(session)