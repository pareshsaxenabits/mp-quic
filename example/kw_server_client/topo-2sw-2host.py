"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        leftSwitch = self.addSwitch( 's1' )
        # rightSwitch = self.addSwitch( 's2' )
        # extraSwitch = self.addSwitch( 's3' )

        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftHost, leftSwitch ) 
        self.addLink( leftHost, leftSwitch ) 

        self.addLink( rightHost, leftSwitch )
        self.addLink( rightHost, leftSwitch )
        self.addLink( rightHost, leftSwitch )


        # leftHost.setIP("10.0.0.1", intf='h1-eth0')    
        # leftHost.setIP("10.0.1.1", intf='h1-eth1')
        # rightHost.setIP("10.0.0.2", intf='h2-eth0')
        # rightHost.setIP("10.0.1.2", intf='h2-eth1') 

topos = { 'mytopo': ( lambda: MyTopo() ) }
