import os
import sys
import subprocess
from importlib import import_module
from mininet.cli import CLI
from mininet.net import Mininet

from qdisc import get_config_data, run_qdisc_configs

EXPERIMENT_BASE_DIR = 'experiment1'

def import_topo(base_dir, module_name=None, topo_class=None):
    sys.path.append(os.path.join(os.getcwd(), EXPERIMENT_BASE_DIR))
    topo_module = import_module(
        'topo' if module_name is None else module_name)
    return getattr(topo_module, topo_class if topo_class else 'MyTopo')

def start_network(experiment_dir):
    print('Cleaning mininet...',end='')
    subprocess.run(
        ['mn', '-c'],
        stderr=subprocess.STDOUT,
        stdout=subprocess.DEVNULL
    )
    print('DONE!')
    print('Starting mininet network...',end='')
    net = Mininet(topo=import_topo(experiment_dir)())
    net.start()
    print('DONE!')
    return net

def run_configs(experiment_dir, net):
    hosts = net.hosts
    print('Setting routing configs...',end='')
    for host in hosts:
        script_filename = os.path.join(
            experiment_dir, str(host),'config.sh')
        host.cmd(script_filename)
    print('DONE!')

def run_qdiscs(experiment_dir, qdisc_filename=None):
    print('Setting queue discipline configs...',end='')
    qdisc_config_file = os.path.join(
        experiment_dir, 
        qdisc_filename if qdisc_filename else 'qdisc.yaml'
    )
    qdisc_configs = get_config_data(qdisc_config_file)
    run_qdisc_configs(qdisc_configs)
    print('DONE!')

def setup_experiment(experiment_base_dir):
    net = start_network(EXPERIMENT_BASE_DIR)
    run_configs(experiment_base_dir, net)
    run_qdiscs(experiment_base_dir)
    print('Experiment setup complete.')
    return net

if __name__ == '__main__':
    net = setup_experiment(EXPERIMENT_BASE_DIR)
    CLI(net)

