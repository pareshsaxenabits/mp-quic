from time import sleep
import os
import yaml

from TestUtils import TestUtils
from protocol_selector import MPTCP, MPQUIC
from BwmParser import BwmParser
from settings import *
from mininet.net import CLI
from shutil import rmtree
import glob

EXPERIMENTS = range(1,5)

class Tests:

    def __init__(self, experiment_id):
        self.experiment_dir = os.path.join(
            EXPERIMENTS_BASE_DIR, experiment_id)
        self.experiment_id = experiment_id
        self.result_dir = TestUtils.generate_result_dir(experiment_id)
        with open(os.path.join(self.experiment_dir, 'exp.yaml')) as exp_conf:
            conf = yaml.safe_load(exp_conf)
            self.block_size = conf['BLOCK_SIZE']
            self.delay_time = conf['DELAY_TIME']
            self.iterations = conf['ITERATIONS']
        TESTS_OVER = Value('d',0)

    def test_all(self):
        self.mptcp_default()
        self.mptcp_redundant()
        # self.mptcp_roundrobin()
        self.tcp()
        self.quic()
        self.mpquic_lowest_rtt()
        self.mpquic_roundrobin()

        TESTS_OVER = Value('d',1)
        sleep(2)

    def mptcp_default(self):
        print('-'*25)
        print('\nMPTCP (Default scheduling)')
        MPTCP.enable()
        MPTCP.scheduler_default()

        net, client, server = TestUtils.start_network(self.experiment_dir)

        sleep(2) # If no sleep, multiple are not used
        bwmng_process = TestUtils.run_bwmng()
        TestUtils.run_tcp_server(server)
        time_taken = TestUtils.run_tcp_client(
            client, self.block_size, self.delay_time, self.iterations)
        print('Transfer complete')

        sleep(2)
        print('Stopping bwmng...',end='')
        bwmng_process.terminate()
        print('DONE!')

        print('Stopping mininet network...',end='')
        net.stop()
        print('DONE!')

        print('Test complete. Preparing result...')
        TestUtils.dump_result(
            self.result_dir,
            'mptcp_default',
            time_taken,
            self.block_size,
            self.iterations
        )

    def mptcp_redundant(self):
        print('-'*25)
        print('\nMPTCP (Redundant scheduling)')
        MPTCP.enable()
        MPTCP.scheduler_redundant()

        net, client, server = TestUtils.start_network(self.experiment_dir)

        sleep(2) # If no sleep, multiple are not used
        bwmng_process = TestUtils.run_bwmng()
        TestUtils.run_tcp_server(server)
        time_taken = TestUtils.run_tcp_client(
            client, self.block_size, self.delay_time, self.iterations)
        print('Transfer complete')

        sleep(2)
        print('Stopping bwmng...',end='')
        bwmng_process.terminate()
        print('DONE!')

        print('Stopping mininet network...',end='')
        net.stop()
        print('DONE!')

        print('Test complete. Preparing result...')
        TestUtils.dump_result(
            self.result_dir,
            'mptcp_redundant',
            time_taken,
            self.block_size,
            self.iterations
        )

    def mptcp_roundrobin(self):
        print('-'*25)
        print('\nMPTCP (Round robin scheduling)')
        MPTCP.enable()
        MPTCP.scheduler_roundrobin()

        net, client, server = TestUtils.start_network(self.experiment_dir)

        sleep(2) # If no sleep, multiple are not used
        bwmng_process = TestUtils.run_bwmng()
        TestUtils.run_tcp_server(server)
        time_taken = TestUtils.run_tcp_client(
            client, self.block_size, self.delay_time, self.iterations)
        print('Transfer complete')

        sleep(2)
        print('Stopping bwmng...',end='')
        bwmng_process.terminate()
        print('DONE!')

        print('Stopping mininet network...',end='')
        net.stop()
        print('DONE!')

        print('Test complete. Preparing result...')
        TestUtils.dump_result(
            self.result_dir,
            'mptcp_roundrobin',
            time_taken,
            self.block_size,
            self.iterations
        )

    def tcp(self):
        print('-'*25)
        print('\nTCP (Multipath off)')
        MPTCP.disable()

        net, client, server = TestUtils.start_network(self.experiment_dir)

        bwmng_process = TestUtils.run_bwmng()
        TestUtils.run_tcp_server(server)
        time_taken = TestUtils.run_tcp_client(
            client, self.block_size, self.delay_time, self.iterations)
        print('Transfer complete')

        sleep(2)
        print('Stopping bwmng...',end='')
        bwmng_process.terminate()
        print('DONE!')

        print('Stopping mininet network...',end='')
        net.stop()
        print('DONE!')

        print('Test complete. Preparing result...')
        TestUtils.dump_result(
            self.result_dir,
            'tcp',
            time_taken,
            self.block_size,
            self.iterations
        )


    def quic(self):
        print('-'*25)
        print("\nQUIC (Multipath off)")

        net, client, server = TestUtils.start_network(self.experiment_dir)

        bwmng_process = TestUtils.run_bwmng()
        TestUtils.run_mpquic_server(server)
        time_taken = TestUtils.run_quic_client(
            client, self.block_size, self.delay_time, self.iterations)
        print('Transfer complete')

        sleep(2)
        print('Stopping bwmng...',end='')
        bwmng_process.terminate()
        print('DONE!')

        print('Stopping mininet network...',end='')
        net.stop()
        print('DONE!')

        print('Test complete. Preparing results...')
        TestUtils.dump_result(
            self.result_dir,
            'quic', # Subtest name
            time_taken,
            self.block_size,
            self.iterations
        )

    def mpquic_roundrobin(self):
        print('-'*25)
        print("\nMPQUIC (round robin Scheduling)")
        MPQUIC.scheduler_round_robin()
        net, client, server = TestUtils.start_network(self.experiment_dir)

        bwmng_process = TestUtils.run_bwmng()
        TestUtils.run_mpquic_server(server)
        time_taken = TestUtils.run_mpquic_client(
            client, self.block_size, self.delay_time, self.iterations)
        print('Transfer complete')

        sleep(2)
        print('Stopping bwmng...',end='')
        bwmng_process.terminate()
        print('DONE!')

        print('Stopping mininet network...',end='')
        net.stop()
        print('DONE!')

        print('Test complete. Preparing results...')
        TestUtils.dump_result(
            self.result_dir,
            'mpquic_roundrobin', # Subtest name
            time_taken,
            self.block_size,
            self.iterations
        )

    def mpquic_lowest_rtt(self):
        print('-'*25)
        print("\nMPQUIC (Lowest RTT Scheduling)")
        MPQUIC.scheduler_lowest_rtt()
        net, client, server = TestUtils.start_network(self.experiment_dir)

        bwmng_process = TestUtils.run_bwmng()
        TestUtils.run_mpquic_server(server)
        time_taken = TestUtils.run_mpquic_client(
            client, self.block_size, self.delay_time, self.iterations)
        print('Transfer complete')

        sleep(2)
        print('Stopping bwmng...',end='')
        bwmng_process.terminate()
        print('DONE!')

        print('Stopping mininet network...',end='')
        net.stop()
        print('DONE!')

        print('Test complete. Preparing results...')
        TestUtils.dump_result(
            self.result_dir,
            'mpquic_lowestrtt', # Subtest name
            time_taken,
            self.block_size,
            self.iterations
        )

if __name__ == "__main__":
    print("START")
    fd_fail = open("failedtests", "w+")
    for i in EXPERIMENTS:
        try:
            print(
            '''
                #######################################################
                #######################################################
                #                                                     #
                #                 TEST {}                             #
                #                                                     #
                #######################################################
                #######################################################

            '''.format(str(i))
            )
            test = Tests(str(i))
            test.test_all() 
        except:
            print("Exception")
            files = glob.glob(RESULTS_BASE_DIR + '/' +str(i) + "-*")
            rmtree(files[0])
            fd_fail.write(str(i)+"\n")
            fd_fail.flush()
    
    fd_fail.close()
