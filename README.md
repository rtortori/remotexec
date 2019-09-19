# remotexec
### Starting from a Kubernetes master node, it will execute a shell script on all Kubernetes nodes

#### Disclaimer
This is NOT an official Cisco application and comes with absolute NO WARRANTY!
Please check LICENSE-CISCO.md for further information

#### What is this?
remotexec will connect to a Kubernetes master node using SSH and will fetch the node list using kubectl.<br>
Once the node list has been created, it will execute a script on each node.<br>

#### Usage
To use this application, there are a number of prerequisites:<br>
* All Kubernetes nodes MUST support SSH key authentication with the same user <br>
* The SSH user MUST be able to run the command 'kubectl get nodes' <br>


Run the application:<br>

```
docker run -it -p 5000:5000 rtortori/remotexec
```

or daemonized, if you want:<br>

```
docker run -itd -p 5000:5000 rtortori/remotexec

```

That's it. Connect with your browser to: [http://127.0.0.1:5000][1]

[1]: http://127.0.0.1:5000/ "remotexec"

#### Frequently used scripts
In the sample_scripts folder, you will find a collection of scripts that can be run on all Kubernetes nodes.<br>
A frequent use case is to configure the docker daemon to use an HTTP proxy, without altering the Cisco Container Platform tenant image.

#### Screeshots
Script Injection<br>
![alt text](https://gitlab-sjc.cisco.com/rtortori/remotexec/raw/master/screenshots/remotexec1.png "Script Injection")
<br>
Success<br>
![alt text](https://gitlab-sjc.cisco.com/rtortori/remotexec/raw/master/screenshots/remotexec2.png "Success")
<br>
Fail<br>
![alt text](https://gitlab-sjc.cisco.com/rtortori/remotexec/raw/master/screenshots/remotexec3.png "Fail")