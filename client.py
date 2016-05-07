"""
Use function requests.post() to communicate with server.
First, use
    requests.post('http://127.0.0.1:1234', "generate", auth=("name","password"))
to get id, then use it in a URL to get to your exercise. For example:
    requests.post('http://127.0.0.1:1234/123123123', "1->5", auth=("name","password"))
use your auth tuple to get access to your exercise.

Valid datas are:
 x->y (ask if there is one-way connection between these two stations)
 answer: x (to send answer - WARNING - after this you can no longer send your asks etc.)
 
 info (get human-readable info)
 timeout (get time in seconds when the exercise is ending)
 solved (if the right answer was sent)
 solve time (the time of completion)
 close (if the answer was sent - true or false)
"""

import requests

r = requests.post('http://127.0.0.1:1234', "generate")
print r.content
r = requests.post('http://127.0.0.1:1234/'+r.content, "info")
print r.content
