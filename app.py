from flask import Flask,redirect,url_for
import requests
app = Flask(__name__)

boardpid={}
n=5
totalbids=3
boardbid={}
hashids=[]
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/postkey/<key>/<pubkey>')
def post_kv(key, pubkey):
	boardpid[key] =pubkey
	
	return pubkey
  
@app.route('/posthash/<key>')
def posthash(key):
       if key not in hashids:
	        hashids.append(key)
                
@app.route('/gethash')
def gethash():
    print("1")
    while(1):
        if (len(hashids)==totalbids):
	         return str(hashids)
@app.route('/getkey/<keyother>')
def get_kv(keyother):
       while(1):
            if keyother in boardpid:
                 print("key is",boardpid[keyother])     
                 return boardpid[keyother]
                 break
	        
	

@app.route('/postshares/<key>/<shares>')
def post_shares(key,shares):
    
	boardbid[key]=shares
	return shares

@app.route('/getshares/<keyother>')
def get_shares(keyother):
       while(1):
            if keyother in boardbid:
                 print("shares is",boardbid[keyother])   
                 return boardbid[keyother]
                 break
	
    
if __name__ == '__main__':
    app.run(debug=True)
