from wsgiref.simple_server import make_server

def wsgi_application(environ, start_response):
    '''WSGI应用程序'''
    status = '200 OK'
    headers = [
        ('Content-Type', 'text/html; charset=utf-8')
    ]
    # 应用中间件中添加的头（如果有的话）
    if 'middleware.headers' in environ:
        # 将中间件中传递头添加到响应头中
        headers.extend(environ['middleware.headers'].copy())
        environ.pop('middleware.headers', None) # 移除中间件添加的头
    start_response(status, headers)
    return [b'Hello World']

class Middleware(object):
    '''中间件'''
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        # 进入WSGI应用之前
        # 例如：添加自定义头
        from datetime import datetime
        environ['middleware.headers'] = [
            ('X-Time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        ]
        # 进入WSGI应用程序
        resp = self.app(environ, start_response)
        # 执行WSGI应用程序之后
        return resp

# 加载中间件
wrapped_app = Middleware(wsgi_application)
# 创建WSGI服务器
with make_server('', 8000, wrapped_app) as httpd:
    # 获取监听地址
    print('visit by [http://{0}:{1}]'.format(*httpd.server_address))
    # 运行服务器
    httpd.serve_forever()