#locust-swarm

Swarm of locusts in the clouds. Forget about dragons, here be locusts.

# notes

If you're on a Mac and gevent can't build because it doesn't know where the 
libevent header files are, you either:

* Haven't installed them (sudo port install libevent / brew install libevent)
* Told pip (or whatever installer) where they are. Set CFLAGS environment
  variable and install gevent individually (vs through a pip dependency)

`sudo port install libevent` 
`CFLAGS="-I /opt/local/include -L /opt/local/lib" pip install gevent`
