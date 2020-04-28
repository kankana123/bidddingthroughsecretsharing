import random
import numpy
from scipy.interpolate import lagrange
from numpy.polynomial.polynomial import Polynomial
import hashlib
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

def calculate_mersenne_primes():
    """ Returns all the mersenne primes with less than 500 digits.
        All primes:
        3, 7, 31, 127, 8191, 131071, 524287, 2147483647L, 2305843009213693951L,
        618970019642690137449562111L, 162259276829213363391578010288127L,
        170141183460469231731687303715884105727L,
        68647976601306097149...12574028291115057151L, (157 digits)
        53113799281676709868...70835393219031728127L, (183 digits)
        10407932194664399081...20710555703168729087L, (386 digits)
    """
    mersenne_prime_exponents = [
        2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279
    ]
    primes = []
    for exp in mersenne_prime_exponents:
        prime = 1
        for i in range(exp):
            prime *= 2
        prime -= 1
        primes.append(prime)
    return primes

SMALLEST_257BIT_PRIME = (2**256 + 297)
SMALLEST_321BIT_PRIME = (2**320 + 27)
SMALLEST_385BIT_PRIME = (2**384 + 231)
STANDARD_PRIMES = calculate_mersenne_primes() + [
    SMALLEST_257BIT_PRIME, SMALLEST_321BIT_PRIME, SMALLEST_385BIT_PRIME
]
STANDARD_PRIMES.sort()


def get_large_enough_prime(batch):
    """ Returns a prime number that is greater all the numbers in the batch.
    """
    # build a list of primes
    primes = STANDARD_PRIMES
    # find a prime that is greater than all the numbers in the batch
    for prime in primes:
        numbers_greater_than_prime = [i for i in batch if i > prime]
        if len(numbers_greater_than_prime) == 0:
            return prime
    
    return None
#print(get_large_enough_prime((10000000000000,100)))
import numpy as np


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def mod_inverse(k, prime):
    k = k % prime
    if k < 0:
        r = egcd(prime, -k)[2]
    else:
        r = egcd(prime, k)[2]
    return (prime + r) % prime




def shareformation(n,t,s,prime):
    i=0;
    a=[]
    while i<t-1:
       a.append(np.random.randint(0,1234))# coeefeceint of the polynomial
       i=i+1
    shares=[]
    i=1;            
    while i<=n:
       j=0
       k=s
       while j<t-1:
           k=(k+a[j]*pow(i,j+1))%prime
           j=j+1
       shares.append((i,k))
       i=i+1
    return shares   
def modular_lagrange_interpolation(x, points, prime):
    # break the points up into lists of x and y values
    x_values, y_values = zip(*points)
    # initialize f(x) and begin the calculation: f(x) = SUM( y_i * l_i(x) )
    f_x = 0
    for i in range(len(points)):
        # evaluate the lagrange basis polynomial l_i(x)
        numerator, denominator = 1, 1
        for j in range(len(points)):
            # don't compute a polynomial fraction if i equals j
            if i == j:
                continue
            # compute a fraction & update the existing numerator + denominator
            numerator = (numerator * (x - x_values[j])) % prime
            denominator = (denominator * (x_values[i] - x_values[j])) % prime
        # get the polynomial from the numerator + denominator mod inverse
        lagrange_polynomial = numerator * mod_inverse(denominator, prime)
        # multiply the current y & the evaluated polynomial & add it to f(x)
        f_x = (prime + f_x + (y_values[i] * lagrange_polynomial)) % prime
    return f_x    
def points_to_secret_int(points,prime1,great):
    """ Join int points into a secret int.
        Get the intercept of a random polynomial defined by the given points.
    """
    
    x_values, y_values = zip(*points)
    
    free_coefficient = modular_lagrange_interpolation(0, points, prime1)
    secret_int = free_coefficient%prime1  # the secret int is the free coefficient
    
    return fun(prime1,great,secret_int)
def fun(prime,great,secret):
    
    if secret>great:
        
        return (secret-prime)
    return secret
def getmin1(n,t,s,prime,toss,great):
    j=0
    a=[]
    while j<t:
        
        a.append(s[j])
        j=j+1
    x= points_to_secret_int(a,prime,great)
    #print("required is",x)
    if x>0:
            if toss==0:
                   return 1
            else :
                   return 0
    else:
            if toss==0:
                   return 0
            else :
                   return 1
def getmin(n,t,s,prime,toss,great):
    #print("a")
    
    a1=[]
    f=0
    k=0
    while (1):
        b=[]
        c=[]
        j=0
        x=[]
        while (1):
           j=0
           while j<t:
              y=random.randint(0,n-1)
              if y not in x:
                 x.append(y)
                 j=j+1
                 
           x.sort()
           if x not in b:
               b.append(x)
               break
        j=0    
        while j<t:
              c.append(s[x[j]])
              j=j+1
           #print(2)
        no=points_to_secret_int(c,prime,great)
        a1.append(no)
        a1.sort()
        num=0
        j=1
        while j<len(a1):
              num=0
              while (a1[j-1]==a1[j]) :
                  num=num+1
                  if num>=2:
                     required=a1[j]
                     #print("required is",required)
                     if required>0:
                          if toss==0:
                              return 1
                          else :
                              return 0
                     else:
                          if toss==0:
                              return 0
                          else :
                              return 1
                            
                  j=j+1
                  if (j==len(a1)):
                      break
              j=j+1    
                   

def encrypt(m,pb):
   return pow(m,pb.e,pb.n)
def decrypt(m,pk):
   return pow(m,pk.d,pk.n)
def bytestokey(pubkey):
   pubkey=(pubkey).decode("utf-8")
   b=str(pubkey)
   c=0
   a=0
   k=0
   i=0
   while i<len(b):
     if b[i]>="0" and b[i]<="9":
        a=a*10+int(b[i])
        k=1
     elif  k==1:

        break
     i=i+1
   k=0
   while i<len(b)-1:
      if b[i]>="0" and b[i]<="9":
         c=c*10+int(b[i])
         k=1
      elif  k==1:
          break
      i=i+1
   d=rsa.PublicKey(a,c)
   return(d)
def bytestoarr(a):
  a=a.decode("utf-8")
  
  arr=[]
  i=1
  no=0
  m=1
  check=-1
  k=0
  while i <len(a)-1:
     if ((a[i]>="0") and (a[i]<="9")): 
        no=no*10+int(a[i])
        k=1
     elif k==1:
       arr.append(no) 
       no=0
       k=0
     else:
         no=0
     i=i+1
  return arr
def bytestono(a):
  return int((a).decode("utf-8"))
def shareformation(n,t,s,prime):
    i=0;
    a=[]
    while i<t-1:
       a.append(np.random.randint(0,1234))# coeefeceint of the polynomial
       i=i+1
    shares=[]
    i=1;            
    while i<=n:
       j=0
       k=s
       while j<t-1:
           k=(k+a[j]*pow(i,j+1))%prime
           j=j+1
       shares.append((i,k))
       i=i+1
    return shares
#
#
#
#
#
#
#
#
#
#
#
#
#
               
