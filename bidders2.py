import math
import flask
import requests
import rsa
import math
import random
import rsa
import numpy as np
import sss3
import requests

n=5
t=2
great=50000000
totalbids=3
prime=sss3.get_large_enough_prime((3*great,2))
bidder=2
bid=random.randint(0,10000)
print("bid is",bid) 
sid=random.randint(0,100)
pid="b2"
sharesun=sss3.shareformation(n,t,bid,prime)
bidderno=hash((sid,bid,bidder))
if bidderno<0:
        bidderno=bidderno*(-1)
print("hashid ",bidderno)

a="http://127.0.0.1:5000/posthash/"+str(bidderno)
response=requests.get(a)
#print("shares is ",sharesun)


i=0
publickey=[]
while i<n:
     
        a="http://127.0.0.1:5000/getkey/p"+str(i+1)
        
        x=sss3.bytestokey((requests.get(a)).content)#here i is taken as a string
        publickey.append(x)
        i=i+1
#print("publickey as recived",publickey)        



i=0
while i<n:
  b=sss3.encrypt(sharesun[i][1],publickey[i])
  a= "http://127.0.0.1:5000/postshares/b"+str(bidderno)+"p"+str(i+1)+"/"+str(b)
  response=requests.get(a)
  #print("response",i ,"is",response)
  i=i+1
#print("done1")

