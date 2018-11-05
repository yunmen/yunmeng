from urllib.parse import parse_qs
from html import escape

def hello_world(environ, start_response):
    # 获取URL参数
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    print(environ.get('PATH_INFO', ''))
    # 获取URL参数中的name
    print(parameters)
    if 'name' in parameters:
        print(parameters['name'])
        name = parameters['name'][0]
    else:
        name = 'World'
    # 输出响应头
    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=utf-8')
    ])
    # escape 用来转义字符，防止脚本攻击
    return [
        '''Hello {name}'''.format(**{
            'name': escape(name)
            # 'name': '<script>alert("哈哈")</script>'
        }).encode('utf-8', 'ignore')
    ]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 9000, hello_world)
    srv.serve_forever()
