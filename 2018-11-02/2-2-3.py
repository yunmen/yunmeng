'''
https://docs.python.org/3/library/wsgiref.html#wsgiref.simple_server.make_server
https://docs.python.org/3/library/socketserver.html#socketserver.TCPServer
https://docs.python.org/3/library/socketserver.html#socketserver.BaseServer.serve_forever
'''
from wsgiref.simple_server import make_server

def hello_world_app(environ, start_response):
    status = '200 OK'
    # 输出响应头
    headers = [
        ('Content-Type', 'text/html; charset=utf-8')
    ]
    start_response(status, headers)
    
    return [b'Hello World']

with make_server('', 8000, hello_world_app) as httpd:
    print(httpd)
    # 获取监听地址
    print('visit by [http://{0}:{1}]'.format(*httpd.server_address))
    # 一直运行
    # httpd.serve_forever()
    # 响应一次就自动结束
    httpd.handle_request()