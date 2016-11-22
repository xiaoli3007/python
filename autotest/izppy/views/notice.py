#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-*- coding: utf-8 -*-
"""
    notice.py
    ~~~~~~~~~

    notice views: it is hun of hudson server and db.

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""

from flask import Module, session, request, jsonify, g, abort
from izppy.models.task import Taskcount, Task
from izppy.models.cases import Case
from izppy.extensions import db
from izppy.permissions import auth
from izppy.extensions import mail
from flask_mail import Message
from izppy.config import defaultconfig
from izppy.helpers import async
from izppy.views.tool import clear_cache
import re
import time
pattern = re.compile(r'case=(\d+)&?')

notice = Module(__name__)


@notice.route("/case/", methods=("GET", "POST"))
@auth.require(401)
def case():
    if g.user and request.method == 'POST' and request.headers.get("Referer"):
        result = request.values.get("cases")
        if result:
            result = re.findall(pattern, result)
            try:
                session[g.user.username] = [int(item) for item in result if Case.query.get_by_id(int(item))]
                return "OK"
            except:
                return "Error"
    return "Error"


@notice.route('/start/', methods=("GET", "POST"))
def test():
    if request.method == 'POST':
        #print request.values.to_dict()
        test = Taskcount(**request.values.to_dict())
        db.session.add(test)
        db.session.commit()

        return 'OK'

    return jsonify(name='dan')


@async
def send_async_email(msg):
    mail.send(msg)


def mail_send(subject, body, sender):
    msg = Message(recipients=sender,
                  subject=subject,
                  body=body
                  )
    send_async_email(msg)


@notice.route("/<JOB_NAME>/<int:BUILD_ID>/<BUILD_NUMBER>/", methods=("GET", "POST"))
#@auth.require(401)
def hudson_to_task(JOB_NAME, BUILD_NUMBER, BUILD_ID):
    task = Task.query.get_by_name(JOB_NAME)
    if task:
        input = []
        output = []
        id = []
        caseall_id = []
        casefail_id = []
        other = []

        if request.method == 'POST' and request.headers.get("Referer") == 'izpautotest':
            #tmp1 = ['0','0','0']
            #tmp_timing = time.strftime('%H:%M:%S',time.gmtime(tmp2-float(task.timing)))
            #tmp2 = time.mktime(tuple(int(i) for i in str(BUILD_NUMBER).replace('_','-').split('-') + tmp1))
            try:
                tmp_timing = BUILD_NUMBER.replace('_', ' ')[0:10] + BUILD_NUMBER.replace('-', ':').replace('_', ' ')[10:]
                post_data = request.values.to_dict()
                taskcount = Taskcount()
                taskcount.task_id = task.id
                taskcount.case_all = len(task.case)
                if len(task.case) == len(eval(post_data.get('success'))):
                    taskcount.fail_case = str(caseall_id)
                else:
                    for name in task.case:
                        case = Case.query.get_by_title(name)
                        caseall_id.append(case.id)
                    for i in caseall_id:
                        if str(i) not in post_data.get('success'):
                            casefail_id.append(i)
                    taskcount.fail_case = str(casefail_id)
                taskcount.case_pass = post_data.get('case_pass')
                taskcount.case_fail = taskcount.case_all - eval(taskcount.case_pass)
                taskcount.result_path = post_data.get('result_path')
                taskcount.build_id = BUILD_ID
                taskcount.timing = tmp_timing
                task.timing = tmp_timing
                task.hudson = 4
                name = task.name
                fail_num = taskcount.case_fail
                db.session.add(taskcount)
                db.session.add(task)
                db.session.commit()
                db.session.remove()
                clear_cache()
                if fail_num:

                        subject = defaultconfig().MAIL_SUBJECT % (name, str(fail_num))
                        body = defaultconfig().MAIL_BODY % name
                        mail_send(subject, body, defaultconfig().MAIL_RECEIVER)

                return 'OK'
            except:
                return abort(401)
        for case_title in task.case:
            case = Case.query.get_by_title(case_title)
            if case:
                if case.usecase_input:
                    input.append(case.usecase_input)
                else:
                    input.append('')
                if case.usecase_output:
                    output.append(case.usecase_output)
                else:
                    output.append('')
                if case.other:
                    other.append(case.other)
                else:
                    other.append('')
                id.append(case.id)
        if len(input) == len(output) == len(id):
            return jsonify(input=input, output=output, id=id, other=other)
        else:
            input = []
            output = []
            id = []
            other = []
            return jsonify(input=input, output=output, id=id, other=other)
    return 'fail'


@notice.route('/hudson/', methods=("GET", "POST"))
def hudson():
    if request.method == 'POST':
        result = request.json
        if result.get("build").get("phase") == "FINISHED":
            task = Task.query.get_by_name(result.get("name"))
            if task and (task.hudson is not 4):
                task.hudson = 4
                db.session.add(task)
                db.session.commit()
                db.session.remove()
                clear_cache()
                return "ok"
    return "fail"
