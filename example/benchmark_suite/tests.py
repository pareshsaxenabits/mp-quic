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
        # self.mptcp_default()
        # self.mptcp_redundant()
        # self.mptcp_roundrobin()
        # self.tcp()
        self.quic()
        self.mpquic_lowest_rtt()
        self.mpquic_roundrobin()

    def mptcp_default(self):
        MPTCP.enable()
        MPTCP.scheduler_default()
        # TODO: Start a client-server code

    def mptcp_redundant(self):
        MPTCP.enable()
        MPTCP.scheduler_redundant()
        # TODO: Start a client-server code

    def mptcp_roundrobin(self):
        MPTCP.enable()
        MPTCP.scheduler_roundrobin()
        # TODO: Start a client-server code

    def tcp(self):
        MPTCP.disable()
        # TODO: Start a client-server code

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