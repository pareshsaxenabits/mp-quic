import os
import yaml
from multiprocessing import Value

# Global settings (Prefer absolute links)
RESULTS_BASE_DIR = 'results/temp'
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
EXPERIMENT_DIR = os.path.join(EXPERIMENTS_BASE_DIR, EXPERIMENT_ID)
conf = {}
with open(os.path.join(EXPERIMENT_DIR, 'exp.yaml')) as exp_conf:
    conf = yaml.safe_load(exp_conf)
BLOCK_SIZE = conf['BLOCK_SIZE']
DELAY_TIME = conf['DELAY_TIME']
ITERATIONS = conf['ITERATIONS']

# Flag for hacky fix
TESTS_OVER = Value('d',0)