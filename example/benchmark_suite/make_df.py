import pandas as pd
import yaml
import os
import re
import json
import pandas as pd

EXPERIMENTS = range(1,26)
EXPERIMENT_DIR_ROOT = './experiments/'
RESULTS_DIR = './results/'
PROTOCOLS = ['mpquic_lowestrtt', 'mpquic_roundrobin', 'mptcp_default', 'mptcp_redundant', 'quic', 'tcp']

def getExperimentSummary(exp_id):
    df_row = dict()

    exp_dir = EXPERIMENT_DIR_ROOT + str(exp_id) + "/"
    exp_yaml_file = exp_dir + 'exp.yaml'

    with open(exp_yaml_file, "r") as f:
        experiment_settings = yaml.load(f)
        for c in experiment_settings:
            if c != 'varying_qdisc':
                df_row[c] = experiment_settings[c]

    exp_qdisc_yaml = exp_dir + 'qdisc.yaml'
    with open(exp_qdisc_yaml) as f:
        config_data = yaml.load(f)
        for interface_data in config_data:
            interface = interface_data['interface'].split("-")[0]
            df_row[interface+'_delay'] = interface_data['netem']['delay']['delay_time']
            df_row[interface+'_loss'] = interface_data['netem']['packet_loss']['loss']
            df_row[interface+'_bandwidth'] = interface_data['tbf']['rate']
    
    regex = re.compile(str(exp_id)+'_.*')
    match_files = [o for o in os.listdir(RESULTS_DIR) if regex.match(o)]
    assert( len(match_files) == 1 )
    
    result_dir = RESULTS_DIR + match_files[0]
    for proto in PROTOCOLS:
        report_file = result_dir + '/' + proto + '/report.json'
        with open(report_file, 'r') as f:
            run_stats = json.load(f)
    
    df_row['Time'] = run_stats['Total time taken (s)']
    df_row['s1_total'] = run_stats['Transfers (Bytes)']['total']['s1-eth1']
    df_row['s2_total'] = run_stats['Transfers (Bytes)']['total']['s2-eth1']
    df_row['goodput'] = int(1024 * 1024 * run_stats['Goodput (MBytes/s)'] * run_stats['Total time taken (s)'])
    return df_row


if __name__ == "__main__":
    # df = pd.DataFrame(columns = [])
    data = []
    for i in range(1,27):
        data.append(getExperimentSummary(i))

    df = pd.DataFrame(data)
    df.to_csv('results/summary.csv')
