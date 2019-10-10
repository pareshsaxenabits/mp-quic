import os
import sys
import subprocess
from importlib import import_module
from mininet.cli import CLI
from mininet.net import Mininet

EXPERIMENT_BASE_DIR = 'experiment1'

def import_topo(base_dir, module_name=None, topo_class=None):
    sys.path.append(os.path.join(os.getcwd(), EXPERIMENT_BASE_DIR))
    topo_module = import_module(
        'topo' if module_name is None else module_name)
    return getattr(topo_module, topo_class if topo_class else 'MyTopo')

def start_network(experiment_dir):
    net = Mininet(topo=import_topo(experiment_dir)())
    net.start()
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

def setup_experiment(experiment_base_dir):
    net = start_network(EXPERIMENT_BASE_DIR)
    run_configs(experiment_base_dir, net)
    run_qdiscs(experiment_base_dir)
    CLI(net)

setup_experiment(EXPERIMENT_BASE_DIR)