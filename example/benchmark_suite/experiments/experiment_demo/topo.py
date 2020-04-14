from mininet.topo import Topo

class MyTopo( Topo ):

    def build( self ):
        server = self.addHost('server')
        client = self.addHost('client')
        router = self.addHost('router')

        leftSwitch = self.addSwitch( 's1' )
        rightSwitch = self.addSwitch( 's2' )
        serverSwitch = self.addSwitch( 's3' )

        self.addLink(client, leftSwitch, max_queue_size=1000)
        self.addLink(client, rightSwitch, max_queue_size=1000)

        self.addLink(router,leftSwitch, max_queue_size=1000)
        self.addLink(router,rightSwitch, max_queue_size=1000)
        self.addLink(router,serverSwitch, max_queue_size=1000) 
        self.addLink(serverSwitch,server, max_queue_size=1000)
