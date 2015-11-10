from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        newPath = self.path.partition('?')
        # main page
        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1>Restarant Manager</h1>"
            restaurants =  session.query(Restaurant).all()
            for restaurant in restaurants:
                message += "<h2>%s</h2>\n" % restaurant.name
                message += "<a href='/restaurants/edit?r=%s'>Edit</a>\n" % restaurant.id
                message += "<a href='/restaurants/delete?r=%s'>Delete</a>\n" % restaurant.id
                # message += restaurant.name[0:-2]
            message += "<hr><a href='/restaurants/new'>Create a new restaurant</a>"
            message += "</body></html>\n\n"
            self.wfile.write(message)
            print message
            return

        # create new
        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += " <html><body>\n"
            output += " <h1>Add a new restaurant</h1>\n"
            output += " <form method='POST' enctype='multipart/form-data' action='/restaurants/new'> \n\
                        <h2> Name of restarant to add: </h2> \n\
                        <input name='action' type='hidden' value='create'> \n\
                        <input name='message' type='text'><input type='submit' value='submit'> \n\
                        </form>\n"
            output += " </body></html>\n"
            self.wfile.write(output)
            print output
            return

        # edit
        if newPath[0] == ("/restaurants/edit") or self.path == ("/restaurants/edit"):
            editWhich = newPath[2].partition('=') # get the part after the ?, ie, the restarant id
            editId = editWhich[2]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # print editId
            editName = session.query(Restaurant.name).filter_by(id = editId).one()
            # print editName

            output = ""
            output += " <html><body>\n"
            output += " <h1>edit %s</h1>\n" % editName.name
            output += " <form method='POST' enctype='multipart/form-data' action='/restaurants/edit'> \n\
                        <input name='action' type='hidden' value='edit'> \n\
                        <input name='restaurantid' type='hidden' value='%s'>\n\
                        <input name='message' type='text'> \n\
                        <input type='submit' value='edit it!'> \n\
                        </form>\n" % editId
            output += " </body></html>\n"
            self.wfile.write(output)
            print output
            return

            
        # delete
        if newPath[0] == ("/restaurants/delete") or self.path == ("/restaurants/delete"):
            deleteWhich = newPath[2].partition('=') # get the part after the ?, ie, the restarant id
            deleteId = deleteWhich[2]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            print deleteId
            thisName = session.query(Restaurant.name).filter_by(id = deleteId).one()
            print thisName

            output = ""
            output += " <html><body>\n"
            output += " <h1>Delete %s</h1>\n" % thisName.name
            output += " <form method='POST' enctype='multipart/form-data' action='/restaurants/delete'> \n\
                        <input name='action' type='hidden' value='delete'> \n\
                        <input name='restaurantid' type='hidden' value='%s'><input type='submit' value='Delete it!'> \n\
                        </form>\n" % deleteId
            output += " </body></html>\n"
            self.wfile.write(output)
            print output
            return

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields=cgi.parse_multipart(self.rfile, pdict)
                action = fields.get('action')[0]
                if fields.get('message') != None:                    
                    message = fields.get('message')[0]
                if fields.get('restaurantid') != None:                    
                    restaurantid = fields.get('restaurantid')[0]

            print fields
            '''
            print "action: ", action            
            print "message: ", message
            print "restaurantid: ", restaurantid
            '''

            # create
            if action == 'create':
                addRestaurant = Restaurant(name = message)
                session.add(addRestaurant)
                session.commit()

                '''
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += " <html><body>\n"
                output += " <h2> Restaurant added: </h2>\n"
                output += " <h1> %s </h1>\n" % message

                output += " <form method='POST' enctype='multipart/form-data' action='/restaurants/new'> \n\
                            <h2> Add another one? </h2> \n\
                            <input name='message' type='text'><input type='submit' value='submit'> \n\
                            </form>\n"
                output += " <hr /><a href='/restaurants'>Return to restarant list</a>\n"
                output += " </body></html>\n"

                self.wfile.write(output)
                print output
                '''

            # edit
            if action == 'edit':
                
                edit = session.query(Restaurant).filter_by(id = restaurantid).one()
                edit.name = message
                session.add(edit)
                session.commit()
                
                '''
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""                
                output += "Attempting to edit a restaurant"

                self.wfile.write(output)
                print output
                '''
                
            # delete
            if action == 'delete':
                
                delete = session.query(Restaurant).filter_by(id = restaurantid).one()
                session.delete(delete)
                session.commit()
                
                '''
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""                
                output += "Attempting to delete a restaurant"

                self.wfile.write(output)
                print output
                '''
                
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/restaurants')
            self.end_headers()

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
