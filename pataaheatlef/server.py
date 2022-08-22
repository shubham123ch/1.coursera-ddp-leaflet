'''
import http.server
import socketserver
class RequestsHandler(http.server.SimpleHTTPRequestHandler):
  """
  Handles http requests
  """
  def do_GET(self):
    if self.path == '/':
      self.path = 'index.html'
    return http.server.SimpleHTTPRequestHandler.do_GET(self)
# Create object of above class
handler_object = RequestsHandler
PORT = 8000
my_server = socketserver.TCPServer(("", PORT), handler_object)
# Start the server
print("Server started at localhost:" + str(PORT))
my_server.serve_forever()

'''
from flask import Flask, render_template
app=Flask(__name__)
@app.route('/')
def root():
   markers=[
   {
   'lat':0,
   'lon':0,
   'popup':'This is the middle of the map.'
    }
   ]
   return render_template('index.html',markers=markers )
if __name__ == '__main__':
   app.run(host="localhost", port=8085, debug=True)