import re
from html import escape

def index(environ, start_response):
    """首页"""
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return ['''Python Web [首页]：
        <h3>读足下，好就业！</h3>
        '''.encode('utf-8', 'ignore')]

def hello(environ, start_response):
    """Hello页面"""
    # 获取url中的路径参数
    args = environ['app.url_args']
    if len(args) > 0:
        print(args)
        name = args[0]
    else:
        name = '无名氏'
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [
        '''Hello <strong>{name}</strong>'''.format(**{
            'name': escape(name)
        }).encode('utf-8', 'ignore')
    ]

def not_found(environ, start_response):
    """404错误"""
    start_response('404 NOT FOUND', [('Content-Type', 'text/html; charset=utf-8')])
    return [b'Page Not Found']

# 访问路径-页面输出函数 映射
urls = [
    (r'^$', index),
    (r'hello/?$', hello),
    (r'hello/([^\/]+)/?$', hello)
]

def application(environ, start_response):
    """WSGI应用程序"""
    global urls
    path = environ.get('PATH_INFO', '').lstrip('/')
    # 路径处理
    for regex, callback in urls:
        # 搜索路径
        match = re.search(regex, path)
        if match is not None:
            # 如果路径存在，则将正则分组作为路径参数，存入环境变量
            # 注意：由于正则处理时编码存在问题，路径参数中如果出现中文可能会导致乱码
            environ['app.url_args'] = match.groups()
            return callback(environ, start_response)
    # 如果没有匹配到路径，则返回404错误
    return not_found(environ, start_response)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 9000, application)
    srv.serve_forever()