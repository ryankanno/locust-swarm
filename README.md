# locust-swarm

Swarm of locusts in the clouds. Forget about dragons, here be locusts.

This system brings up a master/slave cluster in EC2 to run a load test using
the [locust](https://github.com/locustio/locust) load-testing framework.

Performs the following:

 * Brings up an EC2 instance-store image
 * Assigns a custom, role-based tag to the instance
 * Creates a security group to expose port 8089 for the locust master and
   authorizes the master/slave cluster to send / receive traffic 
 * Copies over the contents of a directory to bootstrap running the locust
   master/slave

# requirements

To run these commands, you'll need to have at least two files in the directory:

 * bootstrap.sh
 * locustfile.py

The fabric scripts will execute bootstrap.sh to run things like apt-get update.
Last step will be to run locust --locustfile=<path_to_yourlocustfile.py>

At some point, I will probably wrap the locust install into the deploy as well.
Currently, it's sitting in the bootstrap.sh file.

# installation

## create master

`python locust-swarm/swarm.py up master -c ./locust-swarm.cfg -d ./example/bootstrap-master/`

## create slave(s)

`python locust-swarm/swarm.py up slaves -c ./locust-swarm.cfg -d ./example/bootstrap-slave/ -s 5`


## go to master server to start load test

`http://<master_ip>:8089/`

* You should see your slaves connected to your master

## shutting down the house

`python locust-swarm/swarm.py down master -c ./locust-swarm.cfg`
`python locust-swarm/swarm.py down slaves -c ./locust-swarm.cfg`

or 

`python locust-swarm/swarm.py down all -c ./locust-swarm.cfg`

# notes

If you're on a Mac and gevent can't build because it doesn't know where the 
libevent header files are, you either:

* Haven't installed them (sudo port install libevent / brew install libevent)
* Told pip (or whatever installer) where they are. Set CFLAGS environment
  variable and install gevent individually (vs through a pip dependency)

`sudo port install libevent` 
`CFLAGS="-I /opt/local/include -L /opt/local/lib" pip install gevent`

* locust-swarm.example.cfg uses ami_id=ami-ad3660c4 from alestic.com (ubuntu/images/ubuntu-precise-12.04-amd64-server-20131003)

* Can probably extract this to be a more generic bootstrapper for machines

* Sometimes, `sudo apt-get update -y` fails in the bootstrap.sh script. Need to
  investigate. I usually just bring down the swarm and bring everything back
  up.

# todo

* enable `swarm.py up all` command
