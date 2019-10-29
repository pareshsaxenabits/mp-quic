from protocol_selector import MPTCP, MPQUIC
from setup_experiment import setup_experiment
import mininet
from mininet.cli import CLI
from threading import Thread
import subprocess
from time import sleep

def mptcp_default():
    MPTCP.enable()
    MPTCP.scheduler_default()
    # TODO: Start a client-server code

def mptcp_redundant():
    MPTCP.enable()
    MPTCP.scheduler_redundant()
    # TODO: Start a client-server code

def mptcp_roundrobin():
    MPTCP.enable()
    MPTCP.scheduler_roundrobin()
    # TODO: Start a client-server code

def tcp():
    MPTCP.disable()
    # TODO: Start a client-server code

def quic():
    # TODO: Start a client-server code
    pass

def mpquic_roundrobin():
    # TODO: Start a client-server code
    MPQUIC.scheduler_round_robin()
    

def mpquic_lowest_rtt(directory):
    net = setup_experiment('experiment1')    
    # MPQUIC.scheduler_lowest_rtt()
    MPQUIC.scheduler_round_robin()
    # print(net.hosts)
    # CLI(net) 

    client = net.getNodeByName('client')
    server = net.getNodeByName('server')

    # server_thread = Thread(target=server.cmd, args = ('go run ./{}/server/server.go'.format(directory),) )
    # server_thread.start()
    # print(directory)

    pid = subprocess.Popen(["./bwm-ng.sh"])

    server.popen('/usr/local/go/bin/go run ./{}/server/server.go'.format(directory) )
    sleep(2)
    print('Server started')
    print('/usr/local/go/bin/go run ./{}/client/client.go'.format(directory))
    time_taken = client.cmd('/usr/local/go/bin/go run ./{}/client/client.go'.format(directory))
    time_taken = int(time_taken)
    print("Time taken = {}".format(1.0*time_taken/1000000000) )
    print("Goodput = {} MBytes/second".format(1.0*1024*1024*100*1000000000/time_taken/1024/1024))

    sleep(10)
    pid.kill()

    net.stop()

    
if __name__ == "__main__":
    mpquic_lowest_rtt('experiment1')
    