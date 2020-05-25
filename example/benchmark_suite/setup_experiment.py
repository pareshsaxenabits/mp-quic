import os
import sys
import subprocess
from importlib import import_module
from itertools import cycle
from mininet.cli import CLI
from mininet.net import Mininet
from multiprocessing import Process
from time import sleep
from yaml import safe_load

from qdisc import get_config_data, run_qdisc_configs, remove_all_qdisc
from settings import TESTS_OVER

def import_topo(base_dir, module_name='topo', topo_class='MyTopo'):
    module_path = os.path.join(base_dir, module_name) + '.py'
    if not os.path.exists(module_path):
        raise OSError('Topology file does not exist: ' + module_path)
    sys.path.append(base_dir)
    topo_module = import_module(module_name)
    return getattr(topo_module, topo_class)

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
    TESTS_OVER.value = 0
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

def run_qdiscs_background(qdisc_all_confs, TESTS_OVER):
    for config, duration in cycle(qdisc_all_confs):
        if TESTS_OVER.value == 1:
            exit(0)
        run_qdisc_configs(config)
        sleep(duration)


def run_multiple_qdiscs(experiment_dir, qdisc_confs):
    qdisc_all_confs = []
    for filename, duration in qdisc_confs.items():
        filepath = os.path.join(experiment_dir, filename)
        config = get_config_data(filepath)
        qdisc_all_confs.append((config,duration))
    processqdisc = Process(target=run_qdiscs_background, name='processqd',args=(qdisc_all_confs,TESTS_OVER))
    processqdisc.start()

def setup_experiment(experiment_dir):
    if not os.path.exists(experiment_dir):
        raise OSError('Experiment directory does not exist: ' + experiment_dir)
    net = start_network(experiment_dir)
    run_configs(experiment_dir, net)

    experiment_conf_file = os.path.join(experiment_dir, 'exp.yaml')
    with open(experiment_conf_file) as conf:
        exp_confs = safe_load(conf)
        varying_qdiscs = exp_confs['varying_qdisc']
        if not varying_qdiscs:
            run_qdiscs(experiment_dir)
        else:
            qdisc_confs = exp_confs['qdisc_confs']
            if len(qdisc_confs) == 1:
                run_qdiscs(experiment_dir,list(qdisc_confs.keys())[0])
            else:
                run_multiple_qdiscs(experiment_dir, qdisc_confs)

    print('Experiment setup complete.')
    return net

if __name__ == '__main__':
    EXPERIMENT_DIR = 'experiments/experiment1'
    net = setup_experiment(EXPERIMENT_DIR)
    CLI(net)
