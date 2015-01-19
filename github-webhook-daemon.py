#!/usr/bin/env python3

import json, sys
import http.server, socketserver
from subprocess import call

CONFIG_PATH = sys.argv[1] if len(sys.argv) > 1 else './config.json'

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # reopen without buffering

class GWD(http.server.SimpleHTTPRequestHandler):
    config = None

    @classmethod
    def get_config(cls, attr):
        if cls.config == None:
            try:
                txt = open(CONFIG_PATH).read()
            except:
                sys.exit('Could not load config from ' + CONFIG_PATH)

            try:
                cls.config = json.loads(txt)
            except:
                sys.exit('File ' + CONFIG_PATH + ' is not valid JSON.')
        
        return cls.config[attr]

    def respond(self, code, headers={}):
        self.send_response(code)
        for h in headers:
            self.send_header(h, headers[h])
        self.end_headers()

    def do_GET(self):
        self.respond(405, { 'Allow': 'POST' })

    def do_POST(self):
        event = self.headers.get('x-github-event')
        if event == 'push':
            self.respond(204)
            repo, ref = self.parse_req()
            self.maybe_deploy(repo, ref)
        else:
            print('Received event is not a push (event: {})'.format(event))
            self.respond(304)

    def parse_req(self):
        body = self.rfile.read().decode('utf-8')
        content = json.loads(body)
        return content['repository']['url'], content['ref']

    def get_repo_config(self, url):
        conf = None
        for repo in self.get_config('repositories'):
            if repo['url'] == url:
                conf = repo
        if conf == None:
            raise KeyError(url)
        return conf

    def maybe_deploy(self, repo, ref):
        try:
            conf = self.get_repo_config(repo)
            if conf.get('ref') == None or ref == conf['ref']:
                print('deploying for {} (push to {}): {}'
                          .format(repo, ref, conf['command']))
                call(conf['command'], shell=True)
            else:
                print('repo {}: push to {} -- not interested'.format(repo, ref))
        except KeyError: 
            print('No such repository: ' + repo)

def main():
    server = None
    try:
        port = GWD.get_config('port')
        server = socketserver.TCPServer(('', port), GWD)
        print('Listening on port ' + str(port))
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit) as e:
        sys.stderr.write(str(e) + '\n')
        if server != None:
            server.socket.close()
        print('Goodbye')

if __name__ == '__main__':
    main()
