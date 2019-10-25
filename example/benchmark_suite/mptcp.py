from subprocess import run

class MPTCP:
    """ Utility class to toggle MPTCP specific kernel parameters """

    @staticmethod
    def __set_option(attribute, value):
        cmd = [
            'sysctl', '-w', 
            'net.mptcp.{}={}'.format(attribute, value),
        ]
        print(cmd)
        run(cmd)

    @staticmethod
    def enable():
        MPTCP.__set_option('mptcp_enabled', 1)

    @staticmethod
    def disable():
        MPTCP.__set_option('mptcp_enabled', 0)

    @staticmethod
    def scheduler_default():
        MPTCP.__set_option('mptcp_scheduler','default')

    @staticmethod
    def scheduler_roundrobin():
        MPTCP.__set_option('mptcp_scheduler','roundrobin')

    @staticmethod
    def scheduler_redundant():
        MPTCP.__set_option('mptcp_scheduler','redundant')