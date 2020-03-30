# use apache bench to runsome requests
ab -n 1 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/login 
ab -n 1 -H "Host: user2.att.com" -C 'UserCookie=user2' http://localhost:5000/login
ab -n 10 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/
ab -n 10 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/purchase_a_sword
ab -n 10 -H "Host: user2.att.com" -C 'UserCookie=user2' http://localhost:5000/
ab -n 10 -H "Host: user2.att.com" -C 'UserCookie=user2' http://localhost:5000/purchase_a_sword
ab -n 10 -H "Host: user1.comcast.com" -C 'UserCookie=user1' http://localhost:5000/purchase_a_sword/cool_sword

# read from kafka and check number of events
kafkacat -C -b kafka:29092 -t events -o beginning -e | wc -l

echo "tested requests using apache bench"