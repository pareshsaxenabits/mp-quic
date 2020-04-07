from datetime import datetime
import os
import subprocess
from shutil import move as mv
from pprint import pprint
import json
from copy import deepcopy
from time import sleep

from setup_experiment import setup_experiment
from BwmParser import BwmParser
from settings import *

class TestUtils:

    BWMNG_OUTPUT_FILE = '/tmp/bwmng_result.csv' # Temporary file

    @staticmethod
    def start_network(experiment_dir):
        net = setup_experiment(experiment_dir)
        client = net.getNodeByName('client')
        server = net.getNodeByName('server')
        return (net, client, server)

    @staticmethod
    def run_tcp_server(host):
        print('Starting TCP server...',end='')
        host.popen('go run ' + TCP_SERVER_FILE)
        print('DONE!')

    @staticmethod
    def run_tcp_client(host, block_size, delay_time, iterations):
        sleep(5)
        print('Now running TCP client...')
        command = 'go run {} -blocksize {} -delayMilli {} -numBlocks {}'.format(
            TCP_CLIENT_FILE, block_size, delay_time, iterations
        )
        return int(host.cmd(command))

    @staticmethod
    def run_mpquic_server(host):
        print('Starting MPQUIC server...',end='')
        host.popen('go run ' + MPQUIC_SERVER_FILE)
        print('DONE!')

    @staticmethod
    def run_mpquic_client(host, block_size, delay_time, iterations):
        print('Now running MPQUIC client...')
        sleep(1)
        command = 'go run {} -blocksize {} -delayMilli {} -numBlocks {}'.format(
            MPQUIC_CLIENT_FILE, block_size, delay_time, iterations
        )
        return int(host.cmd(command))

    @staticmethod
    def run_quic_client(host, block_size, delay_time, iterations):
        print('Now running QUIC client...')
        sleep(1)
        command = 'go run {} -blocksize {} -delayMilli {} -numBlocks {}'.format(
            QUIC_CLIENT_FILE, block_size, delay_time, iterations
        )
        return int(host.cmd(command))

    @staticmethod
    def generate_result_dir(experiment_id):
        #test_id = '_'.join([
        #    experiment_id, str(int(datetime.now().timestamp()))]) #(PS) - '_' giving issues
        test_id = '-'.join([
            experiment_id, str(int(datetime.now().timestamp()))])    
        results_dir = os.path.join(RESULTS_BASE_DIR, test_id)
        if os.path.exists(results_dir):
            raise FileExistsError('Test already exists')
        else:
            os.makedirs(results_dir)
        return results_dir

    @staticmethod
    def run_bwmng():
        print('Starting bwm-ng...',end='')
        process = subprocess.Popen(
            ['exec {} {}'.format(BWM_NG_SCRIPT,TestUtils.BWMNG_OUTPUT_FILE)],shell=True)
        print('DONE!')
        return process

    @staticmethod
    def generate_report(time_taken, goodput, throughtputs, iterations, data_sent, subtest_dir, transfers):
        report = {
            'Data block size (in bits)': 8*data_sent,
            'Number of iterations': iterations,
            'Total data transferred (Mbits)': 8*data_sent * iterations / (1000 * 1000),
            'Total time taken (s)': time_taken,
            'Goodput (Mbits/s)': goodput,
            'Transfers (Bytes)': transfers,
            'Throughputs: (Mbits/s)': throughtputs,
        }

        print('\nREPORT:')
        print(json.dumps(report,indent=4))

        report_file = os.path.join(subtest_dir, REPORT_FILENAME)
        with open(report_file, 'w+') as f:
            json.dump(report, f, indent=4)
            f.close()

    @staticmethod
    def dump_result(
        results_base_dir,
        subtest_name,
        time_taken,
        data_sent,
        iterations,
        ):
        subtest_dir = os.path.join(results_base_dir, subtest_name)
        os.makedirs(subtest_dir)
        bwmng_results_file = os.path.join(subtest_dir,BWM_NG_LOGS_FILENAME)
        mv(TestUtils.BWMNG_OUTPUT_FILE, bwmng_results_file)
        time_taken = time_taken / 1000000000 # Seconds
        goodput = 8.0*(data_sent)*(iterations) / time_taken/1000/1000 # Mbits/s
        bwm_parser = BwmParser(bwmng_results_file, PLOT_GRAPH)
        throughputs = deepcopy(bwm_parser.transfers)

        for direction, thruput in throughputs.items():
            for iface, val in thruput.items():
                throughputs[direction][iface] = 8*val / time_taken / (1024 * 1024)
        TestUtils.generate_report(
            time_taken, goodput, throughputs, 
            iterations, data_sent, subtest_dir,
            bwm_parser.transfers
        )
