from multiprocessing import Value

# Global settings (Prefer absolute links)
RESULTS_BASE_DIR = 'results'
EXPERIMENTS_BASE_DIR = 'experiments'
BWM_NG_SCRIPT = './bwm-ng.sh'
TCP_SERVER_FILE = 'utils/tcp_server.go'
TCP_CLIENT_FILE = 'utils/tcp_client.go'
MPQUIC_SERVER_FILE = 'utils/mpquic_server.go'
MPQUIC_CLIENT_FILE = 'utils/mpquic_client.go'
QUIC_CLIENT_FILE = 'utils/quic_client.go'
SAMPLES_DIRECTORY = 'results/temp' # Used in experiment-comparison.py

REPORT_FILENAME = 'report.json'             # Name of output file
BWM_NG_LOGS_FILENAME = 'bwmng_results.csv'  # Name of output file

PLOT_GRAPH = True           # Only if True, graphs will be created. 
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
EXPERIMENT_ID = 'experiment2'

# Flag for hacky fix
# TODO: Toggle value of flag before and after EACH sub-test
TESTS_OVER = Value('d',0)
