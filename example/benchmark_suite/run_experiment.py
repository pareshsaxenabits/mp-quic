from importlib import import_module
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch
import os
import sys
import subprocess
import argparse

EXPERIMENT_BASE_DIR = 'experiment1'

def import_topo(base_dir, module_name=None, topo_class=None):
    sys.path.append(os.path.join(os.getcwd(), EXPERIMENT_BASE_DIR))
    topo_module = import_module(
        'topo' if module_name is None else module_name)
    return getattr(topo_module, topo_class if topo_class else 'MyTopo')

def start_network(experiment_dir):

    # net = Mininet(build=False, topo=import_topo(experiment_dir)())
    net = Mininet(build=False)

    c0 = net.addController('c0')

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

    switches = net.switches
    run_configs(experiment_dir, net)

    c0.start()
    for switch in switches:
        print(switch)
        switch.start([c0])

    return net

def start_network2(experiment_dir):

    net = Mininet(build=False, topo=import_topo(experiment_dir)())
    # net = Mininet(build=False)

    c0 = net.addController('c0')

    net.build()

    switches = net.switches

    run_configs(experiment_dir, net)

    c0.start()
    for switch in switches:
        print(switch)
        switch.start([c0])

    return net


def run_configs(experiment_dir, net):
    hosts = net.hosts
    for host in hosts:
        script_filename = os.path.join(
            experiment_dir, str(host),'config.sh')
        host.cmd(script_filename)

def run_qdiscs(experiment_dir, qdisc_filename=None):
    qdisc_config_file = os.path.join(
        experiment_dir, 
        qdisc_filename if qdisc_filename else 'qdisc.yaml')
    subprocess.call([
        'python3', 'qdisc.py', 'runconfigs', qdisc_config_file
    ])

def begin_experiment(experiment_base_dir):
    net = start_network2(EXPERIMENT_BASE_DIR)
    run_configs(experiment_base_dir, net)
    run_qdiscs(experiment_base_dir)
    CLI(net)

begin_experiment(EXPERIMENT_BASE_DIR)