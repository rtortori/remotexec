from flask_wtf import FlaskForm
from wtforms.fields import TextField, TextAreaField
from wtforms.validators import InputRequired, IPAddress


class injectForm(FlaskForm):
    ''' A class that defines inject form '''

    k8s_master = TextField('Kubernetes Master IP', validators=[InputRequired(), IPAddress(message='This must be a valid IPv4 address')])
    master_user = TextField('SSH Username', validators=[InputRequired()])
    nodes_sshkey = TextAreaField('SSH private key', validators=[InputRequired()], render_kw={"rows": 10, "cols": 90})
    code = TextAreaField('Script to Inject', validators=[InputRequired()], render_kw={"rows": 10, "cols": 70})