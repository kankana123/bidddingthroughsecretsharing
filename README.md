# bidddingthroughsecretsharing
flask and requests and rsa library required 
n(no of part)=5
t(least no of shares)=2
bidmax=10000
randomnobypartiesmax=1000
great(number to be got back through shres cannot be more than this)=bidmax*randomnobypartiesmax*n
prime=3*great

Here the assumption is taken that each bidder login through a random hashid made by using hash of their sid and bids and every time they login they have to keep a certain amount as security deposit.
