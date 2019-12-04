# Global settings (Prefer absolute links)

RESULTS_BASE_DIR = '/home/basu/go/src/github.com/lucas-clemente/quic-go/example/benchmark_suite/results'
EXPERIMENTS_BASE_DIR = '/home/basu/go/src/github.com/lucas-clemente/quic-go/example/benchmark_suite/experiments'
BWM_NG_SCRIPT = '/home/basu/go/src/github.com/lucas-clemente/quic-go/example/benchmark_suite/bwm-ng.sh'

TCP_SERVER_FILE = '/home/basu/go/src/github.com/lucas-clemente/quic-go/example/benchmark_suite/utils/tcp_server.py'
TCP_CLIENT_FILE = '/home/basu/go/src/github.com/lucas-clemente/quic-go/example/benchmark_suite/utils/tcp_client.py'
MPQUIC_SERVER_FILE = '/home/basu/go/src/github.com/lucas-clemente/quic-go/example/benchmark_suite/utils/mpquic_server.go'
MPQUIC_CLIENT_FILE = '/home/basu/go/src/github.com/lucas-clemente/quic-go/example/benchmark_suite/utils/mpquic_client.go'
QUIC_CLIENT_FILE = '/home/basu/go/src/github.com/lucas-clemente/quic-go/example/benchmark_suite/utils/quic_client.go'

REPORT_FILENAME = 'report.json'             # Name of output file
BWM_NG_LOGS_FILENAME = 'bwmng_results.csv'  # Name of output file

PLOT_GRAPH = True          # Only if True, graphs will be created. 
PLOT_IMAGE_QUALITY = 500    # DPI
TP_INTERFACES = [           # List of interfaces to plot
    's1-eth1',
    's2-eth1'
]
TP_TYPES = [                
    # 'in',                 # Incoming traffic to interfaces will be plotted
    # 'out',                # Outgoing traffic to interfaces will be plotted
    'total'                 # Total traffic through the interfaces will be plotted
]

# Experiment settings
EXPERIMENT_ID = 'experiment1'