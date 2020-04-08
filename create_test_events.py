import numpy as np
import subprocess

# USER TYPES
CHEAP = 'cheap items'
EXPENSIVE = 'expensive items'


def purchase_and_sell(user_type):
    # events are tuples ('purchase'/'sell', item, item_type, quantity)
    events = []
    # cheap items users buy a lot of basic swords and couple cool swords
    if user_type==CHEAP:
        num_basic = int(np.random.poisson(20)) + 1
        num_cool = np.random.random_integers(0, 4)
        # buy some basic_swords
        events.append(('purchase', 'sword', None, num_basic))
        # buy a knife 
        events.append(('purchase', 'knife', None, np.random.choice([0, 1], p=[0.1, 0.9])))
        # buy couple cool_swords
        events.append(('purchase', 'sword', 'cool_sword', num_cool))
        # sell some swords
        events.append(('sell', 'sword', None, np.random.random_integers(0, int(num_basic/4))))
        events.append(('sell', 'sword', 'cool_sword', np.random.random_integers(0, int(num_cool/2))))
    elif user_type==EXPENSIVE:
        num_basic = int(np.random.poisson(3)) + 1
        num_cool = np.random.random_integers(0, 4)
        num_better = max(1, np.ceil(np.random.normal(5, 1)))
        num_best = np.random.random_integers(0, 2)
        # buy some basic_swords
        events.append(('purchase', 'sword', None, num_basic))
        # buy a knife 
        events.append(('purchase', 'knife', None, np.random.choice([0, 1], p=[0.8, 0.2])))
        # buy couple cool_swords
        events.append(('purchase', 'sword', 'cool_sword', num_cool))
        # sell some swords
        events.append(('sell', 'sword', None, np.random.choice([num_basic-1, num_basic])))
        events.append(('sell', 'sword', 'cool_sword', np.random.random_integers(0, num_cool/2)))
        # buy some better swords
        events.append(('purchase', 'sword', 'better_sword', num_better))
        events.append(('purchase', 'sword', 'best_sword', num_best))
    return events
    
                      
def execute_item_event(event_tuple, user_ab):
    transaction, item, item_type, quantity = event_tuple
    if quantity > 0:
        purchase = user_ab + \
                        '-n {} '.format(quantity) + \
                        'http://localhost:5000/{}_a_{}'.format(transaction, item) + \
                        ('?{}_type={}'.format(item, item_type) if item_type else '')
        subprocess.call(purchase, shell=True)
                      

def create_user_and_activity(id):
    host = "user{id}.{provider}.com".format(id=id, provider=np.random.choice(['att', 'comcast', 'sonic', 'googlefi']))
    cookie = "UserCookie=user{id}".format(id=id)
    user_type = np.random.choice([CHEAP, EXPENSIVE], p=[0.3, 0.7])
    
    apache_bench = 'ab -H "Host: {host}" -C "{cookie}" '.format(host=host, cookie=cookie)
    
    # "login" and create user in the redis db
    login = apache_bench + '-n 1 http://localhost:5000/login'
    subprocess.call(login, shell=True)
    
    # buy / sell some stuff
    events = purchase_and_sell(user_type)
    for e in events:
        execute_item_event(e, apache_bench)
    
    # join a guild
    if user_type==CHEAP:
        guild = np.random.choice([None, 'the_brave', 'the_honorable'], p=[0.1, 0.85, 0.05])
        leave = np.random.rand() < 0.1
    elif user_type==EXPENSIVE:
        guild = np.random.choice([None, 'the_brave', 'the_honorable'], p=[0.4, 0.1, 0.5])
        leave = np.random.rand() < 0.23
    if guild:
        subprocess.call(apache_bench + '-n 1 ' + 'http://localhost:5000/join_guild/{}'.format(guild), shell=True)
        if leave:
            subprocess.call(apache_bench + '-n 1 ' + 'http://localhost:5000/leave_guild', shell=True)
    
    
def main():
    np.random.seed(205)
    
    n = 1000
    print('creating {} users'.format(n))
    for i in range(n):
        create_user_and_activity(i)
    print('done: {} users created'.format(n))
    

if __name__ == '__main__':
    main()