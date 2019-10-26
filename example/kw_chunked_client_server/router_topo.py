from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from time import sleep


def multipathTopo():
    net = Mininet(build = False)
    # net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )
    
    c0 = net.addController("c0")
    
    # server = net.addHost('server', ip='100.0.0.1/8')
    # client = net.addHost('client', ip='10.0.0.1/8')
    # router = net.addHost('router', ip='10.0.0.2/8')
    server = net.addHost('server')
    client = net.addHost('client')
    router = net.addHost('router')

    leftSwitch = net.addSwitch( 's1' )
    rightSwitch = net.addSwitch( 's2' )
    serverSwitch = net.addSwitch( 's3' )
        
    net.addLink(client, leftSwitch)
    net.addLink(client, rightSwitch)

    net.addLink(router,leftSwitch)
    net.addLink(router,rightSwitch)
    net.addLink(router,serverSwitch) 
    net.addLink(serverSwitch,server)

    net.build()

    server.cmd('./server/config.sh')
    client.cmd('./client/config.sh')
    router.cmd('./router/config.sh')

    controller = net.controllers[0]
    controller.start()
    
    leftSwitch.start([controller])
    rightSwitch.start([controller])
    serverSwitch.start([controller])

    return net

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

if __name__ == "__main__":
    net = multipathTopo()
    CLI(net)

