#coding=utf-8
# 定义的表单

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name = StringField(u'你叫什么名字？', validators=[Required()])
    submit = SubmitField(u'提交')