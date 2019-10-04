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


def multipathNet():
    net = Mininet(build = False)
    # net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )
    # TODO Kaustubh : Study TCLink    
    
    c0 = net.addController("c0")
    
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

    c0.start()
    
    leftSwitch.start([c0])
    rightSwitch.start([c0])
    serverSwitch.start([c0])
    
    return net

if __name__ == "__main__":
    net = multipathNet()
    CLI(net)

