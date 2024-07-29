#!/usr/bin/python3

import sys

from http import server

ANSWER_HTML = bytes('''<!DOCTYPE html>
<head>
<title>You seem to have lost your way...</title>
</head>
<body>
    <h2>This could have been an attack...</h2>
    <p>Your system seems to be have a strange domain search list. This is an
    insecure/attackable configuration, please fix it as soon as
    possible</a>.</p>
    <hr>
    <address>This PSA brought to you by your friendly BOFH team.</address>
</body>
</html>
''', 'utf-8')

class Handler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.answer()

    def do_HEAD(self):
        self.answer()

    def do_POST(self):
        self.answer(500)

    def do_CONNECT(self):
        self.answer(418)

    def answer(self, code=200):
        # Custom log
        self.log_message('"%s" %d %d', self.requestline, code, len(ANSWER_HTML))
        self.send_response_only(code)
        self.send_header('Date', self.date_time_string())
        if code == 407:
            self.send_header("Proxy-Authenticate", 'Basic realm="You fell into a honeypot. Visit http://honeypot.invalid for details."')
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(ANSWER_HTML))
        self.end_headers()
        self.wfile.write(ANSWER_HTML)

    def log_message(self, format, *args):
        """Log auth header if it exists."""

        auth = self.headers.get('Authorization', self.headers.get('Proxy-Authorization' ,'-')).translate(self._control_char_table).replace(' ', '_')
        message = format % args
        sys.stderr.write('%s - %s [%s] %s "%s" "%s"\n' % (
            self.address_string(),
            auth,
            self.log_date_time_string(),
            message.translate(self._control_char_table),
            self.headers.get('referer', '-').translate(self._control_char_table),
            self.headers.get('user-agent', '-').translate(self._control_char_table),
        ))

if __name__ == '__main__':
    server.ThreadingHTTPServer(('', 3128), Handler).serve_forever()
