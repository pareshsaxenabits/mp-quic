import argparse
import os
import subprocess
import yaml

def get_config_data(config_file):
    """ Parse config file to return config dict """

    if not os.path.exists(config_file):
        raise FileNotFoundError('No config file found: ' + config_file)
    else:
        with open(config_file) as cf:
            return yaml.safe_load(cf)

def remove_all_qdisc(interface):
    """ Remove all existing queue disciplines in the interface """
    subprocess.run(
        ['tc', 'qdisc', 'delete', 'dev', interface, 'root'],
        stderr=subprocess.STDOUT,
        stdout=subprocess.DEVNULL,
    )

def get_tbf_command(tbf_config):
    cmd = [
        'tbf', 
        'rate', tbf_config['rate'],
        'latency', tbf_config['latency'],
        'burst', tbf_config['burst'],
    ]
    return(cmd)

def get_netem_command(netem_config):
    cmd = ['netem']

    if  not netem_config['delay_on'] and \
        not netem_config['packet_loss_on'] and \
        not netem_config['packet_corruption_on']:
        raise IOError('No NetEm options are on.')

    if netem_config['delay_on']:
        delay_info = netem_config['delay']
        cmd.extend([
            'delay', 
            delay_info['delay_time'],
            delay_info['error'],
            delay_info['correlation']
        ])

    if netem_config['packet_loss_on']:
        pl_info = netem_config['packet_loss']
        cmd.extend(['loss', pl_info['loss'], pl_info['correlation']])

    if netem_config['packet_corruption_on']:
        cmd.extend(['corrupt', netem_config['packet_corruption']])
    
    return(cmd)

def run_config(config):
    """ Run configurations for one interface """

    interface = config['interface']
    netem_config = config['netem']
    tbf_config = config['tbf']

    remove_all_qdisc(interface)

    if not netem_config['netem_on'] and not tbf_config['tbf_on']:
        return

    cmd = [
        'tc', 'qdisc', 'add', 'dev', interface, 'root', 'handle', '1:'
    ]

    if netem_config['netem_on']:
        cmd.extend(get_netem_command(netem_config))
        subprocess.run(cmd)
        cmd = [
            'tc', 'qdisc', 'add', 'dev', interface,
            'parent', '1:', 'handle', '2:'
        ]
    
    if tbf_config['tbf_on']:
        cmd.extend(get_tbf_command(tbf_config))
        subprocess.run(cmd)

def run_qdisc_configs(configs):
    for config in configs:
        run_config(config)

def show_current_qdisc(configs):
    for config in configs:
        interface = config['interface']
        print(interface)
        subprocess.run(['tc', 'qdisc', 'show', 'dev', interface])
        print()


choices = {'runconfigs': run_qdisc_configs, 'show': show_current_qdisc}

parser = argparse.ArgumentParser()
parser.add_argument('function', choices=choices, 
                    help='apply queue disciplines or show current ones')
parser.add_argument('filepath', help='path of config file')

args = parser.parse_args()
configs = get_config_data(args.filepath)
function = choices[args.function]
function(configs)
