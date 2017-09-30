
import http.server
import requests
import os
from PRNG import PRNG
import threading
from socketserver import ThreadingMixIn
from urllib.parse import unquote, parse_qs

drolls = []

form = '''<!DOCTYPE html>
  
  <title>Rol Um</title> 
  <br /> 
  <strong>Rol Um Dice</strong>
  <br />  <br /> 
  <form method="POST">
    <textarea name="seed1">Enter an integer between 0 and 30,000</textarea>  
    <textarea name="seed2">Enter an integer between 0 and 30,000</textarea>  
    <button type="submit" name="dtype" value="0">Generate!</button>
  </form>
  <br /> 
  <form method="POST">
    <button type="submit" name="dtype" value="4">Roll a d4!</button>
  </form>
  <form method="POST">
    <button type="submit" name="dtype" value="6">Roll a d6!</button>
  </form>
  <form method="POST">
    <button type="submit" name="dtype" value="8">Roll a d8!</button>
  </form>
  <form method="POST">
    <button type="submit" name="dtype" value="10">Roll a d10!</button>
  </form>
  <form method="POST">
    <button type="submit" name="dtype" value="20">Roll a d20!</button>
  </form>
  <pre>
{}
  </pre>

'''

class ThreadHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    "This is an HTTPServer that supports thread-based concurrency."
    

class Roller(http.server.BaseHTTPRequestHandler):
    
    # for number generation
    prng = PRNG()
        
    def do_POST(self):
       
        
        # How long was the message?
        length = int(self.headers.get('Content-length', 0))
        # Read the correct amount of data from the request.
        data = self.rfile.read(length).decode()
        # Extract the "dtype" field from the request data.
        if parse_qs(data)["dtype"][0]:
            dtype = parse_qs(data)["dtype"][0]
        
        if int(dtype) == 0:
            if parse_qs(data)["seed1"][0] and parse_qs(data)["seed2"][0]:
                seed1 = parse_qs(data)["seed1"][0] 
                seed2 = parse_qs(data)["seed2"][0]
                self.prng.InitialiseRandomSeq(int(seed1), int(seed2))
            # @TODO - figure out how to handle case when user doesn't enter seeds
            #else:
                #seed1 = (self.random.random() * 30000)
                #seed2 = (self.random.random() * 30000)
                #self.prng.InitialiseRandomSeq(int(1234), int(3545))
                #pass
            #clear roll history
            drolls.clear()
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            return
        
        
        # process for type
        d, value = self.prng.GetRandomInt(dtype)
        
        # Store it in memory.
        entry = "Rolled a d" + str(d) + ", got a " + str(int(value))
        drolls.insert(0, entry)

        # 1. Send a 303 redirect back to the root page.
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()
		
		
    def do_GET(self):
        # First, send a 200 OK response.
        self.send_response(200)
        # Then send headers.
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # 2. Put the response together out of the form and the stored rolls
        mesg = form.format("\n".join(drolls))
        # 3. write the rolls
        self.wfile.write(mesg.encode())
        
    
        
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))   # Use PORT if it's there.
    server_address = ('', port)
    httpd = ThreadHTTPServer(server_address, Roller)
    httpd.serve_forever()
