#!/usr/bin/env python
import redis
import json
import os
from kafka import KafkaProducer
from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = os.urandom(16)
producer = KafkaProducer(bootstrap_servers='kafka:29092')
r = redis.Redis(host='redis', port='6379')

def get_user():
    return request.cookies.get('UserCookie', 'unknown')


def get_user_state(user):
    return json.loads(r.get(user))


def get_user_inventory(user):
    user = user
    user_info = get_user_state(user)
    return user_info['inventory']


def get_user_guild(user):
    user = user
    user_info = get_user_state(user)
    return user_info['guild']


def update_user_state(user, attribute):
    '''
    user_id: user id string
    attribute: either guild or inventory dict to update
    '''
    user_state = get_user_state(user)
    user_state.update(attribute)
    r.set(user, json.dumps(user_state).encode())


def log_to_kafka(topic, event):
    user = get_user()
    event.update(request.headers)
    event.update({'username': user})
    producer.send(topic, json.dumps(event).encode())
    
    
def change_inventory(user, item_category, quantity, item_type='basic'):
    if quantity == 0:
        return
    
    inventory = get_user_inventory(user)
    category = inventory.get(item_category, {})
    cur_quantity = category.get(item_type, 0)
    if quantity < 0:
        status = 'Failed: Do not have that item to sell' if cur_quantity == 0 else 'Success'
    else:
        status = 'Success'
    
    category[item_type] = max(cur_quantity + quantity, 0)
    inventory[item_category] = category
    update_user_state(user, {'inventory': inventory})
    inventory_event = {'event_type': '{}_transaction'.format(item_category),
                       'transaction_type': 'purchase' if quantity > 0 else 'sell',
                       'item_name': item_type,
                       'status': status}
    log_to_kafka('events', inventory_event)
    return inventory_event
    

@app.route("/")
def default_response():
#     default_event = {'event_type': 'default'}
    default_event = {'keys': r.keys('*'), 'user': r.get('user1')}
    log_to_kafka('events', default_event)
    return "This is the default response!\n"


@app.route("/login")
def set_user():
    user = get_user()
    if not r.get(user):
        r.set(user, json.dumps({"guild": None, "inventory": {}}).encode())
    session['username'] = user
    return "Current User: {}\n".format(session.get('username'))


@app.route("/purchase_a_sword")
def purchase_a_sword():
    sword_type = request.args.get('sword_type', 'basic_sword')
    quantity = request.args.get('quantity', 1)
    user = get_user()
    event = change_inventory(user=user, item_category='sword', item_type=sword_type, quantity=quantity)
    return "Sword Purchased: {}!\n".format(sword_type)


@app.route("/purchase_a_knife")
def purchase_a_knife():
    user = get_user()
    knife_type = 'very_sharp_knife'
    event = change_inventory(user=user, item_category='knife', item_type=knife_type, quantity=1)
    return "Knife Purchased!\n"


@app.route("/sell_a_sword")
def sell_a_sword():
    sword_type = request.args.get('sword_type', 'basic_sword')
    quantity = request.args.get('quantity', 1)
    user = get_user()
    event = change_inventory(user=user, item_category='sword', item_type=sword_type, quantity=-quantity)
    return "Sword Sold: {}!\n".format(sword_type)


@app.route("/sell_a_knife")
def sell_a_knife():
    user = get_user()
    event = change_inventory(user=user, item_category='knife', item_type='very sharp knife', quantity=-1)
    return "Knife Sold!\n"


@app.route("/join_guild/<guild_name>")
def join_guild(guild_name):
    user = get_user()
    guild = get_user_guild(user)
    if guild:
        status = "Failed: Already part of a guild"
    else:
        update_user_state(user, {'Guild': guild_name})
        status = "Success: Joined {}".format(guild_name)
    join_guild_event = {'event_type': 'join_guild',
                        'guild_name': guild_name,
                        'status': status}
    log_to_kafka('events', join_guild_event)
    return "Joined Guild: {}!\n".format(guild_name)


@app.route("/leave_guild")
def leave_guild():
    user = get_user()
    guild = get_user_guild(user)
    if guild:
        update_user_state(user, {"guild": None})
        status = "Success: Left guild {}".format(guild)
    else: 
        status = "Failed: Not currently part of a guild"
        
    leave_guild_event = {'event_type': 'left_guild',
                         'guild_name': guild,
                         'status': status}
    log_to_kafka('events', leave_guild_event)
    return "Left Guild: {}!\n".format(guild)


if __name__ == '__main__':
    app.run(host='0.0.0.0')