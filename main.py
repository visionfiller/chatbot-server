import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")


# Load your API key from an environment variable or secret management service



# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
   
    def do_POST(self):
        
        """Handles POST requests to the server"""
        # client will send a conversation array from the client to the server, which then 
        # sends it to openai, which then sends the chat response back

        self._set_headers(201)

        if self.path == "/chat":
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)
            messages = json.loads(post_body)
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

# print the chat completion
        response = chat_completion.choices[0].message.content
        self.wfile.write(json.dumps(response).encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
