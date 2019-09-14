from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        server = self.addHost( 'server' )
        client = self.addHost( 'client' )

        router = self.addHost( 'router' )
        
        leftSwitch = self.addSwitch( 's1' )
        rightSwitch = self.addSwitch( 's2' )
        serverSwitch = self.addSwitch( 's3' )

        # Add links
        self.addLink( client, leftSwitch )
        self.addLink( client, rightSwitch ) 

        self.addLink(router,leftSwitch)
        self.addLink(router,rightSwitch)
        self.addLink(router,serverSwitch) 

        self.addLink(serverSwitch,server)

        # router_obj = self.get('router')
        # router_obj.cmd("./router/config.sh")
        # server.cmd("./server/config.sh")
        # client.cmd("./client/config.sh")

        # leftHost.setIP("10.0.0.1", intf='h1-eth0')    
        # leftHost.setIP("10.0.1.1", intf='h1-eth1')
        # rightHost.setIP("10.0.0.2", intf='h2-eth0')
        # rightHost.setIP("10.0.1.2", intf='h2-eth1') 

topos = { 'mytopo': ( lambda: MyTopo() ) }
