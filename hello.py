# coding=utf-8

import os
# 异步发送邮件模块
from threading import Thread
from flask import Flask, render_template, session, redirect, url_for
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail, Message


# 获取当前项目路径
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


# 定义smtp服务器
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
# 定义smtp服务器端口
app.config['MAIL_PORT'] = 587
# 使用加密连接
app.config['MAIL_USE_TLS'] = True
# 定义邮箱用户名，在环境保存用户名：export MAIL_USERNAME=phoenix_hu@outlook.com
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# 定义邮箱密码，在环境变量中保存密码：export MAIL_PASSWORD=XXXXXX
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# 定义邮件主题前缀
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
# 定义发件人地址
app.config['FLASKY_MAIL_SENDER'] = 'phoenix_hu@outlook.com'
# 定义收件人地址
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')


manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

# 异步发送邮件函数
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# 发送邮件函数
def send_email(to, subject, template, **kwargs):
    '''发送邮件函数，参数分别为：收件人地址，主题，渲染邮件正文的模板，关键字参数列表'''
    # 定义一封邮件，参数分别为主题，发件人，收件人
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    # 渲染纯文本正文
    msg.body = render_template(template + '.txt', **kwargs)
    # 渲染富文本正文
    msg.html = render_template(template + '.html', **kwargs)
    # 异步发送邮件
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


class NameForm(Form):
    name = StringField(u'你叫什么名字？', validators=[Required()])
    submit = SubmitField(u'提交')


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    # 定义表单实例化
    form = NameForm()
    # 如果数据能被验证函数接受（不为空），执行以下语句块
    if form.validate_on_submit():
        # 从数据库users表中查询表单中的数据，如果没有结果则返回None
        user = User.query.filter_by(username=form.name.data).first()
        # 如果没有查询到，执行以下语句快
        if user is None:
            # 将表单数据插入到表中
            user = User(username=form.name.data)
            # 添加到数据库会话管理
            db.session.add(user)
            # 将用户回话中的'known'键设为False
            session['known'] = False
            # 如果设置了收件人地址，执行发送邮件函数
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        # 如果从数据库查到表单中的数据，将用户回话中的'known'键设为True
        else:
            session['known'] = True
        # 将表单提交的数据保存到用户会话的‘name’键中
        session['name'] = form.name.data
        # http重定向到index函数
        return redirect(url_for('index'))
    # 渲染模板
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))


if __name__ == '__main__':
    manager.run()