locust-swarm
============

.. image:: https://travis-ci.org/ryankanno/locust-swarm.png?branch=master
   :target: https://travis-ci.org/ryankanno/locust-swarm

.. image:: https://coveralls.io/repos/ryankanno/locust-swarm/badge.png
   :target: https://coveralls.io/r/ryankanno/locust-swarm

Forget about [dragons](https://en.wikipedia.org/wiki/Here_be_dragons), here be locusts.

These scripts brings up a [locust](https://github.com/locustio/locust) 
master/slave cluster in EC2. 

&lt;disclaimer&gt;
As a note, you'll be charged **$$** using this. Since you can potentially bring up 
many EC2 nodes, if you don't understand what you're doing, don't run these scripts.
&lt;/disclaimer&gt;

Scripts perform the following using [boto](https://github.com/boto/boto) + 
[fabric](https://github.com/fabric/fabric):

 * Brings up an EC2 instance-store image
 * Assigns a role-based tag to the instance
 * Creates a security group to expose port 8089 for the locust master and
   authorizes the master/slave cluster to send/receive traffic from one
   another
 * Copies over the contents of a user-specified directory to bootstrap the 
   locust master/slave
 * Executes a script named bootstrap.sh
 * Executes locust in master/slave mode

requirements
------------

`pip install -r requirements.txt`

To run these commands, you'll need to have at least two files in the
user-specified directory:

 * bootstrap.sh
 * locustfile.py (your load test file)

The fabric scripts automatically will execute bootstrap.sh to run things like 
apt-get update, etc. Check out the included sample [bootstrap.sh](https://github.com/ryankanno/locust-swarm/blob/master/example/bootstrap-slave/bootstrap.sh)
The script will automatically start locust in a master or slave configuration
so it'll need your load test in a file called `locustfile.py`.

As a note, at some point, I'll refactor and wrap the locust install into the
actual scripts instead of in the sample bootstrap.sh.  For now, just take a
peek there to see what I mean.

supported commands
------------------

(All commands support -h flag)

create master
~~~~~~~~~~~~~

To create a locust master, run the following:

`python locust-swarm/swarm.py up master -c ./locust-swarm.cfg -d ./example/bootstrap-master/`

 * -c is a path to your configuration file ([sample](https://github.com/ryankanno/locust-swarm/blob/master/locust-swarm.example.cfg))
 * -d is a path to a directory containing your bootstrap.sh/locustfile ([sample](https://github.com/ryankanno/locust-swarm/tree/master/example/bootstrap-master))

create slave(s)
~~~~~~~~~~~~~~~

To create a locust slave, run the following:

`python locust-swarm/swarm.py up slaves -c ./locust-swarm.cfg -d ./example/bootstrap-slave/ -s 5`

 * -c is a path to your configuration file ([sample](https://github.com/ryankanno/locust-swarm/blob/master/locust-swarm.example.cfg))
 * -d is a path to a directory containing your bootstrap.sh/locustfile ([sample](https://github.com/ryankanno/locust-swarm/tree/master/example/bootstrap-slave))
 * -s is the number of slaves you want to create

go to master server to start load test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`http://<master_ip>:8089/`

* You should see your slaves connected to your master

shutting down the studio
~~~~~~~~~~~~~~~~~~~~~~~~

`python locust-swarm/swarm.py down master -c ./locust-swarm.cfg`<br/>
`python locust-swarm/swarm.py down slaves -c ./locust-swarm.cfg`

or 

`python locust-swarm/swarm.py down all -c ./locust-swarm.cfg`

notes
-----

If you're on a Mac and gevent can't build because it doesn't know where the 
libevent header files are, you either:

* Haven't installed them (sudo port install libevent / brew install libevent)
* Told pip (or whatever installer) where they are. Set CFLAGS environment
  variable and install gevent individually (vs through a pip dependency)

`sudo port install libevent`<br/>
`CFLAGS="-I /opt/local/include -L /opt/local/lib" pip install gevent`

* The locust-swarm.example.cfg uses ami_id=ami-ad3660c4 from alestic.com
  (ubuntu/images/ubuntu-precise-12.04-amd64-server-20131003). At some point,
  I'll probably have to figure out where an EC2 repository mirror is for
  bandwidth reasons.

* Sometimes, `sudo apt-get update -y` fails in the bootstrap.sh script. Need to
  investigate. I usually just bring down the swarm and bring everything back
  up.

todo
----

* Enable `swarm.py up all` command
* Encapsulate a bit more of the swarm logic into a CommandController. This
  was a tiny weekend project. :D
