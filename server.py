print """
I recommend to open server in explorer (use address of server), you will get page with simple client file.
Server can also save and load status!
"""

import SimpleHTTPServer
from time import time
import base64
import os
import random
games = {}

def process(data, path="/", auth=""):
    path = path[1:].split('/')
    outd = ""
    resp = 200
    if data == "generate":
        g = game(auth0 = auth)
        outd = g.get_id()
        games[str(g.get_id())] = g
    elif path[0] in games.keys():
        outd = games[path[0]].process(data, auth0=auth)
    else:
        outd = "ERROR (game not found - maybe use 'generate' first)"
        resp = 404
    return (outd, resp)

class game():
    
    def __init__(self, data="", auth0=""):
        if not data:
            print auth0
            self.init_time = int(time())
            self.auth = auth0
            self.auth_op = ["Basic "+base64.b64encode("admin:admin")]
            self.solve_time = -1
            self.game_data, self.answer = self.generate_data(20)
            self.tries = []
            self.solved = False
            self.max_tries = 4
            self.timeout = 60*5 # in seconds
        else:
            self.load(data)
            
    def get_id(self):
        return self.init_time
    
    def generate_data(self, num):
        data = []
        from0 = range(1, num+1)
        to0 = range(1, num+1)
        thatone = random.randint(1,20)
        for i in from0:
            for a in to0:
                if a==thatone:
                    data += [[i, a]]
                else:
                    pass

    def process(self, data, auth0=""):
        if auth0 == self.auth or auth0 in self.auth_op:
            return self.process_auth(data)
        else:
            return self.process_nonauth(data)
    
    def process_auth(self, data):
        if data == "info":
            return "Init time: {}\nCount of asks: {}\nMax allowed asks: {}\nAsks data: {}\nSolved: {}\nClosed: {}".format(self.init_time,len(self.tries),self.max_tries,self.tries,
                                                                                                                          self.solved, self.solve_time>-1)
        if data == "timeout":
            return str(self.init_time+self.timeout-int(time()))
        if data == "solved":
            return str(self.solved)
        if data == "solve time":
            return str(self.solve_time)
        
        if data == "close":
            self.solve_time = time()
            return "CLOSED"

        if self.solve_time > -1:
            return "ERROR (game closed)"
        if self.init_time < int(time()) - self.timeout:
            return "ERROR (timed out)"
        if "answer:" in data:
            data = data.split()
            try:
                num = int(data[1])
                if num == self.answer:
                    self.solved = True
                    self.solve_time = time()
                    return "TRUE"
                else:
                    self.solve_time = time()
                    return "FALSE"
            except:
                return "ERROR (answer not recognized)"
        if len(self.tries) > self.max_tries:
            return "ERROR (max requests reached)"
        data = data.split('->')
        try:
            data_int = [int(data[0]), int(data[1])]
            self.tries += [data_int]
            return ("A" if (data_int in self.game_data) else "N")
        except:
            return "ERROR (invalid data)"

    def process_nonauth(self, data):
        if data == "info":
            return "Init time: {}\nCount of asks: {}\nMax allowed asks: {}\nClosed: {}".format(self.init_time,len(self.tries),self.max_tries, self.solve_time>-1)
        if data == "timeout":
            return str(self.init_time+self.timeout-int(time()))
        if data == "solved":
            return str(self.solved)
        if data == "solve time":
            return str(self.solve_time)

        return "ERROR (access restricted)"

    def save(self):
        saveStr = "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(self.init_time, self.auth, self.solve_time, int(self.solved), self.max_tries,
                                                   self.timeout, self.answer, self.list_to_string(self.game_data), self.list_to_string(self.tries),
                                                      self.list_to_string(self.auth_op))
        return saveStr

    def load(self, data):
        data = data.split('|')
        try:
            self.init_time = int(data[0])
            self.auth = data[1]
            self.solve_time = int(data[2])
            self.solved = bool(int(data[3]))
            self.max_tries = int(data[4])
            self.timeout = int(data[5])
            self.answer = int(data[6])
            self.game_data = self.string_to_list_int(data[7])
            self.tries = self.string_to_list_int(data[8])
            self.auth_op = self.string_to_list(data[9])
        except:
            print "error when loading data!", data
            self.init_time = 0
            self.auth = ""
            self.auth_op = ["Basic "+base64.b64encode("admin:admin")]
            self.solve_time = -1
            self.game_data, self.answer = ([], -1)
            self.tries = []
            self.solved = False
            self.max_tries = 0
            self.timeout = 0 # in seconds

    def string_to_list(self, string):
        lst = string.split(";")
        if not lst[0]:
            return []
        else:
            return lst
    def string_to_list_int(self, string):
        lst0 = string.split(";")
        if not lst0[0]:
            return []
        lst = []
        for i in lst0:
            tmp = i.split(",")
            tmp2 = []
            for a in tmp:
                tmp2 += [int(a)]
            lst += [tmp2]
        return lst
    def list_to_string(self, lst):
        """ [[1,5],[2,4]] -> 1,5;2,4
            ["ahoj", "cus"] -> ahoj"""
        handler = ""
        for i in lst:
            if type(i)==list:
                for a in i:
                    handler += str(a) + ","
                handler = handler[:-1] + ";"
            else:
                handler = str(i) + ";"
        return handler[:-1]
class my_handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        datain = ""
        try:
            datain = self.rfile.read(int(self.headers.getheader("Content-Length")))
        except:
            pass
        auth = self.headers.getheader("Authorization")
        if auth == None:
            auth = ""
        print datain, self.path, auth
        dataout, resp = process(datain, self.path, auth)
        self.send_response(resp)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(str(dataout))

def server_save():
    print "saving!"
    to_save = ""
    cnt = 1
    for i in games.keys():
        print "progress: {}/{}".format(cnt, len(games.keys()))
        to_save += games[i].save() + "\n"
        cnt += 1
    to_save = to_save[:-1]
    f = open("savefile.txt", "w")
    f.write(to_save)
    f.close()
    print "save done!"
def server_load():
    print "loading!"
    f = open("savefile.txt", "r")
    d = f.read()
    f.close()
    lst = d.split('\n')
    cnt = 1
    for i in lst:
        print "progress: {}/{}".format(cnt, len(lst))
        g = game(i)
        games[str(g.get_id())] = g
        cnt += 1
    print "load done!"

def start():
    if os.path.exists("savefile.txt"):
        f = open("savefile.txt", "r")
        d = f.read()
        f.close()
        if d:
            resp = raw_input("Savefile detected, do you want to load data?\n(data will be overwritten after next successful close of server)\nY/N: ").lower()
            if resp == "y":
                server_load()
            else:
                print "No data will be loaded!"
    addr = ('127.0.0.1', 1234)
    hserver = SimpleHTTPServer.BaseHTTPServer.HTTPServer(addr, my_handler)
    try:
        print "starting server...", addr
        hserver.serve_forever()
    except KeyboardInterrupt:
        hserver.socket.close()
        print "server closed!"
        server_save()


start()
