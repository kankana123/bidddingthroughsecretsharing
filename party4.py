import math
import flask
import requests
import Crypto
import rsa
import math
import random
import requests
import numpy as np
import sss3


n=5
t=2

totalbids=3
great=50000000
prime=sss3.get_large_enough_prime((3*great,2))
#print(prime)
pid="p4"
partyno=4
(pubkey,privekey)=rsa.newkeys(512)
#print(pubkey)
a="http://127.0.0.1:5000/postkey/p"+str(partyno)+"/"+str(pubkey)
response=requests.get(a)
bidshare=[]
publickey=[]

 
i=0
while i<n:# get publickey from other parties
        a="http://127.0.0.1:5000/getkey/p"+str(i+1)
        x=sss3.bytestokey((requests.get(a)).content)#here i is taken as a string
        publickey.append(x)
        i=i+1

#print(publickey)

a= "http://127.0.0.1:5000/gethash"
response=requests.get(a)
hashids=sss3.bytestoarr(response.content)
i=0
while i<totalbids:
  a="http://127.0.0.1:5000/getshares/b"+str(hashids[i])+"p"+str(partyno)
  response=requests.get(a)
  a=int((response.content).decode("utf-8"))
  bidshare.append(sss3.decrypt(a,privekey))
  i=i+1
#print("shares are ",bidshare)



least=0
i=1
while i<totalbids:# sorting
  #print("round between ",i,"and ",least)
  j=0
  s=random.randint(0,1000)
  #print("s   ",s)
  sharesofs=sss3.shareformation(n,t,s,prime)# secret of s
  #print("shares given ", sharesofs)
  secret=0
  while j<len(sharesofs):#print shares of s
    b=sss3.encrypt(sharesofs[j][1],publickey[j])
    j=j+1
    a= "http://127.0.0.1:5000/postshares/pg" +str(partyno)+"pr"+str(j)+"p"+str(least+1)+"p" +str(i+1) +"/"+str(b)
    response=requests.get(a)
  j=0
  while j<n:#formation of secret by adding shares
    a="http://127.0.0.1:5000/getshares/pg"+str(j+1)+"pr"+str(partyno)+"p"+str(least+1)+"p"+str(i+1)
    response=requests.get(a)
    #print(response)
    b=(sss3.bytestono(response.content))#write bytestoshares
    v=(sss3.decrypt(b,privekey))
    secret=secret+v
    #print(v)
    j=j+1
  j=0
  toss=0
  a="http://127.0.0.1:5000/postshares/toss"+str(i+1)+str(least+1)+"p"+str(partyno)+"/"+str(random.randint(0,10)%2)
  response=requests.get(a)
  while j<n:#toss
     a="http://127.0.0.1:5000/getshares/toss"+str(i+1)+str(least+1)+"p" +str(j+1)
     response=requests.get(a)
     toss=(toss+sss3.bytestono(response.content))%2
     j=j+1
  #print("toss  ",toss)
  j=0
  
  #print(pow(-1,toss))  
  g=secret*(bidshare[i]-bidshare[least])*pow(-1,toss)
  #print(g)
  a="http://127.0.0.1:5000/postkey/"+str(partyno)+"share"+str(least+1)+str(i+1)+"/"+str(g)#declaring product
  response=requests.get(a)
  sharesproduct=[]#productof bid and secret
  j=0
  while j<n:#gathering all shares of product
    a="http://127.0.0.1:5000/getkey/"+str(j+1)+"share"+str(least+1)+str(i+1)
    response=requests.get(a)
    b=sss3.bytestono(response.content)#write bytestono
    c=(j+1,b)
    sharesproduct.append(c)
    j=j+1
  
  leastold=least
  v=(2*t)-1
  #print(v)
  x=sss3.getmin(n,v,sharesproduct,prime,toss,great)
  if x==0:
     least=i
  print("between",(hashids[i]),"and" ,(hashids[leastold]), "the less is " ,(hashids[least]) )
  i=i+1
