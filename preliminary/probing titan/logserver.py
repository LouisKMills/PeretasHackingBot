#
# logserver.py, by Seb
# Super unbeleivably basic HTTP server that logs the body of all post requests.
# Use through ngrok so we can log info regardless of the status of our script.
#

from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode()
        print("="*30)
        if len(body.split("\t")) == 3:
            _, filename, content_b64 = body.split("\t")
            content_bin = bytearray(base64.b64decode(content_b64))
            open(os.path.join("yoinked", filename), "wb").write(content_bin)
            print(">< Saved b64 binary content to file", filename, "><")
        elif content_length < 2048:
            print("### Received body:\n" + body)
        else:
            print("!! Content too long, see generated file !!")
            print("### Received body:\n" + body, file=open(str(content_length) + ".txt", "w+"))
        print("="*30)
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    if not os.path.exists("yoinked"): os.mkdir("yoinked")
    server = HTTPServer(("0.0.0.0", 8080), SimpleHandler)
    print("Listening on port 8080...")
    try: server.serve_forever()
    except KeyboardInterrupt: print("CTRL+C, bye bye :)")
