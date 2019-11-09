from time import sleep

from TestUtils import TestUtils
from protocol_selector import MPTCP, MPQUIC
from BwmParser import BwmParser

EXPERIMENT_ID = 'experiment1'

class Tests:

    def __init__(self, experiment_id):
        self.experiment_id = experiment_id
        self.results_base_dir = TestUtils.generate_results_dir(experiment_id)

    def test_all(self):
        self.mptcp_default()
        self.mptcp_redundant()
        self.mptcp_roundrobin()
        self.tcp()
        self.quic()
        self.mpquic_lowest_rtt()
        self.mpquic_roundrobin()

    def mptcp_default(self):
        print('-'*25)
        print('\nMPTCP (Default scheduling)')
        MPTCP.enable()
        MPTCP.scheduler_default()

        net, client, server = TestUtils.start_network(self.experiment_id)

        bwmng_process = TestUtils.run_bwmng()
        TestUtils.run_tcp_server(server)
        time_taken = TestUtils.run_tcp_client(client)
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
            self.results_base_dir,
            'mptcp_default',
            time_taken,
            1024,
            10
        )

    def mptcp_redundant(self):
        print('-'*25)
        print('\nMPTCP (Redundant scheduling)')
        MPTCP.enable()
        MPTCP.scheduler_redundant()

        net, client, server = TestUtils.start_network(self.experiment_id)

        bwmng_process = TestUtils.run_bwmng()
        TestUtils.run_tcp_server(server)
        time_taken = TestUtils.run_tcp_client(client)
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
            self.results_base_dir,
            'mptcp_redundant',
            time_taken,
            1024,
            10
        )

    def mptcp_roundrobin(self):
        print('-'*25)
        print('\nMPTCP (Round robin scheduling)')
        MPTCP.enable()
        MPTCP.scheduler_roundrobin()

        net, client, server = TestUtils.start_network(self.experiment_id)

        bwmng_process = TestUtils.run_bwmng()
        TestUtils.run_tcp_server(server)
        time_taken = TestUtils.run_tcp_client(client)
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
            self.results_base_dir,
            'mptcp_roundrobin',
            time_taken,
            1024,
            10
        )

    def tcp(self):
        print('-'*25)
        print('\nTCP (Multipath off)')
        MPTCP.disable()

        net, client, server = TestUtils.start_network(self.experiment_id)

        bwmng_process = TestUtils.run_bwmng()
        TestUtils.run_tcp_server(server)
        time_taken = TestUtils.run_tcp_client(client)
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
            self.results_base_dir,
            'tcp',
            time_taken,
            1024,
            10
        )


    def quic(self):
        print('-'*25)
        print("\nQUIC (Multipath off)")

        net, client, server = TestUtils.start_network(self.experiment_id)

        bwmng_process = TestUtils.run_bwmng()
        TestUtils.run_mpquic_server(server)
        time_taken = TestUtils.run_quic_client(client)
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
            self.results_base_dir,
            'quic', # Subtest name
            time_taken,
            1024 * 1024, # Data sent = 1024 * 1024
            100 # Number of iterations
        )

    def mpquic_roundrobin(self):
        print('-'*25)
        print("\nMPQUIC (round robin Scheduling)")
        MPQUIC.scheduler_round_robin()
        net, client, server = TestUtils.start_network(self.experiment_id)

        bwmng_process = TestUtils.run_bwmng()
        TestUtils.run_mpquic_server(server)
        time_taken = TestUtils.run_mpquic_client(client)
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
            self.results_base_dir,
            'mpquic_roundrobin', # Subtest name
            time_taken,
            1024 * 1024, # Data sent = 1024 * 1024
            100 # Number of iterations
        )

    def mpquic_lowest_rtt(self):
        print('-'*25)
        print("\nMPQUIC (Lowest RTT Scheduling)")
        MPQUIC.scheduler_lowest_rtt()
        net, client, server = TestUtils.start_network(self.experiment_id)

        bwmng_process = TestUtils.run_bwmng()
        TestUtils.run_mpquic_server(server)
        time_taken = TestUtils.run_mpquic_client(client)
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
            self.results_base_dir,
            'mpquic_lowestrtt', # Subtest name
            time_taken,
            1024 * 1024, # Data sent = 1024 * 1024
            100 # Number of iterations
        )

if __name__ == "__main__":
    tests = Tests(EXPERIMENT_ID)
    tests.test_all()