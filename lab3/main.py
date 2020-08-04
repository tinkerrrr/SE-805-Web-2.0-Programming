import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import signal
import logging
from tornado.options import options

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

# signal_handler
def signal_handler(signum, frame):
    global is_closing
    logging.info('exiting...')
    is_closing = True

    
# try_exit
def try_exit(): 
    global is_closing
    if is_closing:    
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('exit success')

class item:
    def __init__(self, name, filetype, size):
        self.name = name
        self.filetype = filetype;
        if size < 1024:
            self.size = "%d b" % size
        elif size < 1024 * 1024:
            self.size = "%d kb" % (size/1024)
        else:
            self.size = "%d mb" % (size/(1024*1024))

# getAllFiles
def getAllFiles():
    allFile = []
    mypath = "static/songs"
    dirlist = os.listdir(mypath)
    for filename in dirlist:
        allFile.append(item(filename, filename.split(".")[1], os.path.getsize(mypath + '/' + filename)))
        allFile.sort(key=lambda x:(x.filetype, x.name))


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        playlist = self.get_argument("playlist", "hehe")
        allFile = []
        mypath = "static/songs"        
        if playlist != 'hehe':
            txt = open(mypath + '/' + playlist)
            filenames = txt.read().splitlines()
            for filename in filenames:
                allFile.append(item(filename, filename.split(".")[1], os.path.getsize(mypath + '/' + filename)))
            allFile.sort(key=lambda x:(x.filetype, x.name))
        else:
            dirlist = os.listdir(mypath)
            for filename in dirlist:
                allFile.append(item(filename, filename.split(".")[1], os.path.getsize(mypath + '/' + filename)))
            allFile.sort(key=lambda x:(x.filetype, x.name))
        self.render('music.html', allFile=allFile)

if __name__ == "__main__":
    ## aa
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "template"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
