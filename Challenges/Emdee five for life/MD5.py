import hashlib
import requests

get_url_info = requests.get('http://docker.hackthebox.eu:32037')

#print(get_url_info.text)
html = get_url_info.text
start = html.find("h3 align='center'>")+18
end = html.find("</h3>")
string = html[start:end]

string = string.encode('utf-8')
print('string : '+ str(string))
hash = hashlib.md5(string)
print('MD5hash : ' + hash.hexdigest())