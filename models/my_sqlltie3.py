import sqlite3



async def db_connect():
    global db, cur
    db = sqlite3.connect('events.db')
    cur = db.cursor()


    cur.execute("CREATE TABLE IF NOT EXISTS events(name TEXT,cost_event INT, weekday TEXT,time TEXT, additional_info TEXT, places INT, rows INT)")    
    db.commit()


async def db_create_event(data):
    cur.execute("INSERT INTO events (name, cost_event, weekday, time, additional_info,places, rows) VALUES (?, ?, ?, ?, ?, ?, ?)", 
               (data['name_event'], data['cost_ticket'], data['weekday_event'], data['time_event'],data['add_info_event'] ,data['places_event'], data['rows_event']))
    db.commit()

async def db_check_all():
    cur.execute("SELECT * FROM events")
    rows = cur.fetchall()
    return rows
    
    
async def db_check_names(name_event):
    cur.execute("SELECT name FROM events")
    names = cur.fetchall()
    return [name[0] for name in names if name[0] == name_event]

async def db_get_price(name_event):
    cur.execute("SELECT cost_event FROM events WHERE name=?", (name_event,))
    event_info = cur.fetchone()
    return event_info



async def db_book_place(name_event):
    cur.execute("SELECT places FROM events WHERE name=?", (name_event,))
    seats_available = cur.fetchone()[0]
    if seats_available > 0:
        seats_available -= 1
        cur.execute("UPDATE events SET places=? WHERE name=?", (seats_available, name_event))
        db.commit()
        return True
    else:
        return False
    
    
async def db_get_data_by_name(name_event):
    cur.execute("SELECT * FROM events WHERE name = ?", (name_event,))
    event = cur.fetchone()  
    if event:
        event = list(event)  
        event_str = ', '.join(str(e) for e in event)  
        return event_str
    else:
        return None  





async def db_update_value(changing_column, name, new_value):
    cur.execute(f"UPDATE events SET {changing_column}=? WHERE name=?", (new_value, name))
    db.commit()

async def db_weekday_check(current_weekday):
    cur.execute("SELECT weekday, name FROM events WHERE weekday = ?", (current_weekday,))
    events = cur.fetchall()
    event_names = [event[1] for event in events]
    return event_names


async def db_delete_event(name_event):
    cur.execute("DELETE FROM events WHERE name=?", (name_event,))
    db.commit()
        
