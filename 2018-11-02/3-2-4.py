from flask import Flask, abort
app = Flask(__name__)

@app.route('/')
def index():
    '''首页'''
    return '足下：<h3>培养五百万行业精英</h3>'

@app.route('/hello')
def hello():
    '''hello页面，不带参数'''
    return '<strong>读足下，好就业</strong>'

@app.route('/hello/<name>')
def hello_name(name=None):
    '''hello页面，需要参数'''
    if name is None:
        # 如果没有携带参数，将会抛出错误
        return abort(404)
    return 'Hello <strong>{0}</strong>！'.format(name)

if __name__ == '__main__':
    app.run(port=9000)