"""Hosted coursework demonstration; original local application stays unchanged.

Run behind Render's HTTPS proxy. Use fictional data only. Free hosting uses
temporary SQLite storage: records can reset after sleep, restart or redeploy.
"""
import os
from urllib.parse import urlparse
from http.server import ThreadingHTTPServer
import app

PUBLIC_ORIGIN = os.environ.get('CLEANING_PUBLIC_ORIGIN', os.environ.get('RENDER_EXTERNAL_URL', '')).rstrip('/')
NOTICE = ('<aside role="note" style="padding:16px;background:#fff4ce;border:1px solid #876800;line-height:1.5">'
          '<strong>Shared coursework demonstration.</strong> Use fictional names and addresses only. '
          'Demo accounts are public; other visitors can see or change demo records. '
          'Bookings are stored in SQLite while the demo is running, but may reset after sleep, restart or deployment. '
          'This is not a real cleaning business.</aside>')

class HostedHandler(app.Handler):
    def setup(self):
        super().setup()
        self.connection.settimeout(15)

    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'same-origin')
        self.send_header('X-Robots-Tag', 'noindex, nofollow')
        super().end_headers()

    def csrf(self):
        # TLS terminates at Render, so the public origin is HTTPS even though
        # the proxy-to-Python request is HTTP. Never trust a client-supplied
        # X-Forwarded-Proto value to select the accepted origin.
        expected = PUBLIC_ORIGIN or ('http://' + self.headers.get('Host', ''))
        origin = self.headers.get('Origin')
        if origin and origin != expected:
            raise app.Error(403, 'Origin rejected')

    def send_json(self, status, obj, extra=None):
        extra = dict(extra or {})
        if PUBLIC_ORIGIN.startswith('https://') and 'Set-Cookie' in extra:
            extra['Set-Cookie'] += '; Secure'
        return super().send_json(status, obj, extra)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/healthz':
            try:
                with app.connection() as c:
                    c.execute('SELECT 1 FROM Services LIMIT 1').fetchone()
                return self.send_json(200, {'status': 'ok', 'mode': 'coursework-demo'})
            except app.sqlite3.Error:
                return self.send_json(503, {'status': 'unavailable'})
        if path == '/robots.txt':
            body = b'User-agent: *\nDisallow: /\n'
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(body)
            return
        if path == '/':
            html = (app.ROOT / 'index.html').read_text(encoding='utf-8')
            html = html.replace('<main>', '<main>' + NOTICE, 1)
            html = html.replace('Local coursework demonstration', 'Hosted coursework demonstration')
            body = html.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)
            return
        return super().do_GET()

if __name__ == '__main__':
    app.init()
    port = int(os.environ.get('PORT', os.environ.get('CLEANING_PORT', '10000')))
    host = os.environ.get('CLEANING_HOST', '0.0.0.0')
    print(f'Coursework demo listening on {host}:{port}', flush=True)
    ThreadingHTTPServer((host, port), HostedHandler).serve_forever()
