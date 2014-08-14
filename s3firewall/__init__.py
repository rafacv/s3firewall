import os
from boto.s3.connection import S3Connection

__all__ = [
    'app',
]


BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME', '')
BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD', '')
ALLOWED_ADDR = os.environ.get('ALLOWED_ADDR', '').split(',')

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')


def authenticated(environ):
    if BASIC_AUTH_USERNAME or BASIC_AUTH_PASSWORD:
        auth_method, auth = environ.get('HTTP_AUTHORIZATION', ' Og==').split(' ', 1)
        username, password = auth.decode('base64').split(':', 1)
        basic_auth = auth_method.lower() == 'basic' and \
                     username == BASIC_AUTH_USERNAME and \
                     password == BASIC_AUTH_PASSWORD
    else:
        basic_auth = True

    if any(ALLOWED_ADDR):
        if environ.get('HTTP_X_FORWARDED_FOR'):
            addr = environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
        else:
            addr = environ.get('REMOTE_ADDR')
        allowed_addr = addr in ALLOWED_ADDR
    else:
        allowed_addr = True

    return basic_auth and allowed_addr

def get_file(path):
    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(AWS_BUCKET_NAME)

    return bucket.get_key(path)

def app(environ, start_response):
    headers = []
    
    content_encoding = None

    if authenticated(environ):
        if not os.path.splitext(environ['PATH_INFO'])[1]:
            path = os.path.join(environ['PATH_INFO'], 'index.html')
        else:
            path = environ['PATH_INFO']

        file_ = get_file(path)
        if file_:
            content_type = file_.content_type
            content_encoding = file_.content_encoding
            content_length = file_.size
            status = '200 OK'
            content = file_.get_contents_as_string()
        else:
            content_type = 'text/html'
            content_length = '0'
            status = '404 Not Found'
            content = ''
    else:
        headers.append(('WWW-Authenticate', 'Basic realm="Static Website"'))
        content_type = 'text/html'
        content_length = '0'
        status = '401 Unauthorized'
        content = ''

    headers.append(('Content-Type', content_type))
    headers.append(('Content-Length', content_length))
    if content_encoding:
        headers.append(('Content-Encoding', content_encoding))

    start_response(status, headers)
    return [content]
