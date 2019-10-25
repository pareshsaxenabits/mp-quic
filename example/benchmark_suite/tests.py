from mptcp import MPTCP

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
    pass

def mpquic_lowest_rtt():
    # TODO: Start a client-server code
    pass