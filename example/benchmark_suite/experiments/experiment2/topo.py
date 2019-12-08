from mininet.topo import Topo

class MyTopo( Topo ):

    def build( self ):
        server = self.addHost('server')
        client = self.addHost('client')
        router = self.addHost('router')

        leftSwitch = self.addSwitch( 's1' )
        rightSwitch = self.addSwitch( 's2' )
        serverSwitch = self.addSwitch( 's3' )

        self.addLink(client, leftSwitch)
        self.addLink(client, rightSwitch)

        self.addLink(router,leftSwitch)
        self.addLink(router,rightSwitch)
        self.addLink(router,serverSwitch) 
        self.addLink(serverSwitch,server)
