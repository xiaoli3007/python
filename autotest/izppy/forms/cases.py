#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
    case.py
    ~~~~~~~~~~~

    case form

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""

from flask.ext.wtf import Form, RadioField, SubmitField,\
    TextField, required, ValidationError, SelectField, TextAreaField, HiddenField
from flask.ext.babel import gettext, lazy_gettext as _
from izppy.extensions import db
from izppy.models.cases import Case
from .validators import is_legal_name


class AddCaseForm(Form):
    '''It is used for adding cases, defines add cases form.'''

    next = HiddenField()
    title = TextField(_(u"用例名:"), validators=[
        required(message=_(u"请输入用例名")), is_legal_name])

    description = TextAreaField(_(u"描述:"))
    access = RadioField(_(u"状态:"), default=Case.PUBLIC, coerce=int, choices=(
                        (Case.PUBLIC, _(u"公开")), (Case.PRIVATE,
                                                  _(u"私有"))))
    pre = TextAreaField(_(u"用例数据准备:"))
    usecase_input = TextAreaField(_(u"用例输入:"))
    usecase_output = TextAreaField(_(u"用例输出:"))
    other = TextAreaField(_(u"其它:"))

    module_type = SelectField(_(u"所属模块:"), coerce=int)
    submit = SubmitField(_(u"提交"))

    def validate_title(self, field):
        case = Case.query.filter(Case.title.like(field.data)).first()
        if case:
            raise ValidationError(gettext(u"用例名已经存在"))


class EditCaseForm(Form):
    '''It is used for editing cases, defines edit cases form.'''

    next = HiddenField()
    title = TextField(_(u"用例名:"), validators=[
        required(message=_(u"请输入用例名")), is_legal_name])

    description = TextAreaField(_(u"描述:"))
    access = RadioField(_(u"状态:"), default=Case.PUBLIC, coerce=int, choices=(
                        (Case.PUBLIC, _(u"公开")), (Case.PRIVATE,
                                                  _(u"私有"))))
    pre = TextAreaField(_(u"用例数据准备:"))
    usecase_input = TextAreaField(_(u"用例输入:"))
    usecase_output = TextAreaField(_(u"用例输出:"))
    other = TextAreaField(_(u"其它:"))

    module_type = SelectField(_(u"所属模块:"), coerce=int)
    submit = SubmitField(_(u"保存"))

    def __init__(self, case, *args, **kwargs):
        self.case = case
        kwargs['obj'] = self.case
        super(EditCaseForm, self).__init__(*args, **kwargs)

    def validate_title(self, field):
        case = Case.query.filter(db.and_(
                                 Case.title.like(field.data),
                                 db.not_(Case.id == self.case.id))).first()

        if case:
            raise ValidationError(gettext(u"用例名已经存在"))
