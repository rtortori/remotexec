'''
Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''

from flask_wtf import FlaskForm
from wtforms.fields import TextField, TextAreaField
from wtforms.validators import InputRequired, IPAddress


class injectForm(FlaskForm):
    ''' A class that defines inject form '''

    k8s_master = TextField('Kubernetes Master IP', validators=[InputRequired(), IPAddress(message='This must be a valid IPv4 address')])
    master_user = TextField('SSH Username', validators=[InputRequired()])
    nodes_sshkey = TextAreaField('SSH private key', validators=[InputRequired()], render_kw={"rows": 10, "cols": 90})
    code = TextAreaField('Script to Inject', validators=[InputRequired()], render_kw={"rows": 10, "cols": 70})
