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

# Ignore paramiko warnings
import warnings
warnings.filterwarnings("ignore")

import os
import paramiko


def getnodes(master, username, sshkey):
    ''' Returns node list from master node ip '''

    # Ssh key
    sshkeytmp = 'sshkey'

    with open(sshkeytmp,'w') as f:
        # We clear the trailing ^M
        f.write(sshkey.replace('\r\n', os.linesep))

    nodelscmd = 'sudo kubectl get nodes -o wide | grep -v EXTER| awk \'{print $7}\''

    # Build SSH Client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(str(master), username=username, key_filename=sshkeytmp)

    ssh.invoke_shell()

    # Execute fetch the list of Kubernetes nodes and copy to nodes array
    _, stdout, _ = ssh.exec_command(nodelscmd)
    nodes = []
    for node in stdout.readlines():
        nodes.append(node.rstrip())

    # Close SSH client for Master node
    ssh.close()

    return nodes


def inject(nodes, username, text, sshkey):
    for node in nodes:
        # Temp script name
        script = 'remotescript.sh'

        # Ssh key
        sshkeytmp = 'sshkey'

        with open(sshkeytmp,'w') as f:
            # We clear the trailing ^M
            f.write(sshkey.replace('\r\n', os.linesep))

        # Build SSH Client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(str(node), username=username,
                    key_filename=sshkeytmp)

        # Open the sftp client
        sftp_client = ssh.open_sftp()

        # Determine target home directory
        _, stdout, _ = ssh.exec_command('echo $HOME')
        target_home_directory = stdout.readline().split('\n')[0]
        
        
        with open(script,'w') as f:
            # We clear the trailing ^M
            f.write(text.replace('\r\n', os.linesep))
        
        sftp_client.put(script, '{}/{}'.format(target_home_directory, script))
        ssh.exec_command(
            'chmod +x {}/{}'.format(target_home_directory, script))
        ssh.exec_command(
            'sudo {}/{}'.format(target_home_directory, script))
        ssh.exec_command(
            'sudo rm {}/{}'.format(target_home_directory, script))

        # Close SSH clients
        sftp_client.close()
        ssh.close()

        # Remove Temp files
        os.remove(sshkeytmp)
        os.remove(script)

# Flask app

from flask import Flask, request, render_template, redirect
from flask_bootstrap import Bootstrap
from forms import injectForm

app = Flask(__name__)
Bootstrap(app)

# Secret Key
app.config['SECRET_KEY'] = b'\xdb\xe6\xb2x\xd4\x8a!\xaa\xc6Mu\xac\xfd(&P\x08\xc18\x8c\xb6\xc0\xcd|'

@app.route('/', methods=['GET', 'POST'])
def form():
    form = injectForm()
    if form.validate_on_submit(): 

        k8s_master = request.form['k8s_master']
        master_user = request.form['master_user']
        nodes_sshkey = request.form['nodes_sshkey']
        code = request.form['code']

        try:
            nodes = getnodes(k8s_master,master_user, nodes_sshkey)
            inject(nodes,master_user,code, nodes_sshkey)
            return render_template('done.html', nodes=nodes)
        except:
            return render_template('failure.html')
    return render_template('index.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def int_err(e):
    return render_template('500.html'), 500

# Run API server as long as the program is running
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
