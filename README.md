# s3firewall
Simple WSGI application to interface your S3 bucket. Basic auth and IP address check are possible measures to restrict access.
Your AWS credentials must be supplied as env vars:

* AWS_ACCESS_KEY_ID (required)
* AWS_SECRET_ACCESS_KEY (required)
* AWS_BUCKET_NAME (required)

Optional access control are enforced if the following variables are set:

* BASIC_AUTH_USERNAME
* BASIC_AUTH_PASSWORD
* ALLOWED_ADDR - comma separated IP addresses values, e.g. '204.232.175.90' or '204.232.175.90,64.59.144.92'


## Example
You can import s3firewall into your code:

```python
from gevent import wsgi
from s3firewall import app

wsgi.WSGIServer(('', 8080), app).serve_forever()
```

Or invoke it directly from the command line with a capable webserver:

```bash
$ export AWS_ACCESS_KEY_ID='abcd1234' AWS_SECRET_ACCESS_KEY='1234abcd' AWS_BUCKET_NAME='mywebsite'
$ export BASIC_AUTH_USERNAME='username' BASIC_AUTH_PASSWORD='mypassword'
$ gunicorn s3firewall:app -w 3
```

## Copyright
The MIT License (MIT)

Copyright (c) 2013 Rafael Valverde

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
