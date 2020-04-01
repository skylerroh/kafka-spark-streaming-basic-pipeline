# use apache bench to runsome requests
# create the users
ab -n 1 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/login 
ab -n 1 -H "Host: user2.att.com" -C 'UserCookie=user2' http://localhost:5000/login
ab -n 1 -H "Host: user3.googlefi.com" -C 'UserCookie=user3' http://localhost:5000/login
ab -n 1 -H "Host: user4.googlefi.com" -C 'UserCookie=user4' http://localhost:5000/login
ab -n 1 -H "Host: user5.comcast.com" -C 'UserCookie=user5' http://localhost:5000/login

# buy/sell some stuff
ab -n 20 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/purchase_a_sword
ab -n 1 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/
ab -n 15 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/purchase_a_sword?sword_type=cool_sword
ab -n 10 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/purchase_a_sword?sword_type=good_sword
ab -n 12 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/sell_a_sword?sword_type=basic_sword
ab -n 6 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/sell_a_sword?sword_type=good_sword
ab -n 3 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/purchase_a_sword?sword_type=better_sword
ab -n 1 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/purchase_a_sword?sword_type=best_sword

# wait 20 sec
sleep 20

ab -n 10 -H "Host: user2.att.com" -C 'UserCookie=user2' http://localhost:5000/purchase_a_sword
ab -n 9 -H "Host: user2.att.com" -C 'UserCookie=user2' http://localhost:5000/sell_a_sword?sword_type=basic_sword
ab -n 1 -H "Host: user2.att.com" -C 'UserCookie=user2' http://localhost:5000/purchase_a_sword?sword_type=best_sword

ab -n 30 -H "Host: user3.googlefi.com" -C 'UserCookie=user3' http://localhost:5000/purchase_a_sword
ab -n 3 -H "Host: user3.googlefi.com" -C 'UserCookie=user3' http://localhost:5000/purchase_a_sword?sword_type=better_sword

ab -n 2 -H "Host: user4.googlefi.com" -C 'UserCookie=user4' http://localhost:5000/purchase_a_sword

ab -n 3 -H "Host: user5.comcast.com" -C 'UserCookie=user5' http://localhost:5000/purchase_a_sword

ab -n 3 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/purchase_a_knife
ab -n 1 -H "Host: user2.att.com" -C 'UserCookie=user2' http://localhost:5000/purchase_a_knife
ab -n 2 -H "Host: user3.googlefi.com" -C 'UserCookie=user3' http://localhost:5000/purchase_a_knife
ab -n 1 -H "Host: user4.googlefi.com" -C 'UserCookie=user4' http://localhost:5000/purchase_a_knife

# join some guilds
ab -n 1 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/join_guild/the_brave
ab -n 1 -H "Host: user2.att.com" -C 'UserCookie=user2' http://localhost:5000/join_guild/the_brave
ab -n 2 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/leave_guild
ab -n 1 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/join_guild/the_brave
ab -n 1 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/join_guild/the_honorable
ab -n 1 -H "Host: user3.googlefi.com" -C 'UserCookie=user3' http://localhost:5000/join_guild/the_brave

# read from kafka and check number of events
kafkacat -C -b kafka:29092 -t events -o beginning -e | wc -l

echo "tested requests using apache bench"