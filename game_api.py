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
    user_info = get_user_state(user)
    return user_info['inventory']

def get_user_guild():
    user_info = get_user_state(user)
    return user_info['guild']

def log_to_kafka(topic, event):
    user = get_user()
    event.update(request.headers)
    event.update({'username': user})
    producer.send(topic, json.dumps(event).encode())


@app.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "This is the default response!\n"


@app.route("/login")
def set_user():
    user = get_user()
    session['username'] = user
    return "Current User: {}\n".format(session.get('username'))


@app.route("/logout")
def remove_user():
    session.pop('username', None)
    return "Logged Out\n"


@app.route("/purchase_a_sword")
def purchase_basic_sword():
    return purchase_a_sword('basic_sword')


@app.route("/purchase_a_sword/<sword_type>")
def purchase_a_sword(sword_type):
    purchase_sword_event = {'event_type': 'purchase_sword',
                            'sword_type': sword_type}
    log_to_kafka('events', purchase_sword_event)
    return "Sword Purchased: {}!\n".format(sword_type)


@app.route("/purchase_a_knife")
def purchase_a_knife():
    purchase_knife_event = {'event_type': 'purchase_knife',
                            'description': 'very sharp knife'}
    log_to_kafka('events', purchase_knife_event)
    return "Knife Purchased!\n"


@app.route("/join_guild/<guild_name>")
def join_guild(guild_name):
    user = get_user()
    guild = get_user_guild(user)
    if user_info.get('Guild'):
        status = "Failed: Already part of a guild"
    else:
        status = "Success: Joined {}".format(guild_name)
    join_guild_event = {'event_type': 'join_guild',
                        'guild_name': guild_name,
                        'status': status}
    log_to_kafka('events', join_guild_event)
    return "Joined Guild: {}!\n".format(guild_name)


@app.route("/leave_guild")
def leave_guild(guild_name):
    user = get_user()
    guild = get_user_guild(user)
    if guild:
        status = "Success: Left guild {}".format(guild)
    else: 
        status = "Failed: Not currently part of a guild"
        
    leave_guild_event = {'event_type': 'left_guild',
                         'guild_name': guild_name,
                         'status': status}
    log_to_kafka('events', leave_guild_event)
    return "Left Guild: {}!\n".format(guild_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0')