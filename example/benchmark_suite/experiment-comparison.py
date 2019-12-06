import os
import json
from pprint import pprint
from time import sleep
import matplotlib.pyplot as plt
from numpy import nan

from BwmParser import BwmParser
from settings import *

reports = {}

class ExperimentsComparison:

    ERROR_VAL = nan

    def __init__(self, samples_directory):
        self.directory = samples_directory
        self.experiments = sorted(os.listdir(self.directory))
        self.experiments = list(
            filter(lambda x: os.path.isdir(os.path.join(self.directory,x)), self.experiments))
        self.schemes = set()
        self.reports = {}

        self.gather_reports()

    def gather_reports(self):
        for experiment in self.experiments:
            experiment_dir = os.path.join(self.directory,experiment)
            schemes = os.listdir(experiment_dir)
            self.schemes = self.schemes.union(schemes)

            self.reports[experiment] = {}

            for scheme in schemes:
                report_file = os.path.join(experiment_dir, scheme, 'report.json')
                with open(report_file, 'r') as fp:
                    self.reports[experiment][scheme] = json.load(fp)

    def prepare_plots(self, param):
        y_vals = {}
        for scheme in self.schemes:
            y_vals[scheme] = []

        for experiment in self.experiments:
            reports_ = self.reports[experiment]
            for scheme in self.schemes:
                report = reports_.get(scheme)
                val = ExperimentsComparison.ERROR_VAL
                if report is not None:
                    try:
                        if param == 'goodput':
                            val = report['Goodput (MBytes/s)']
                        elif param == 'throughtput_total':
                            val = report['Throughputs: (MBytes/s)']['total']['all_ifaces']
                        elif param == 'throughput_out':
                            val = report['Throughputs: (MBytes/s)']['out']['all_ifaces']
                        elif param == 'throughput_in':
                            val = report['Throughputs: (MBytes/s)']['in']['all_ifaces']
                        elif param == 'time_taken':
                            val = report['Total time taken (s)']
                    except KeyError:
                        val = 0
                y_vals[scheme].append(val)
        
        plots = {}

        for scheme in self.schemes:
            plots[scheme] = list(zip(self.experiments, y_vals[scheme]))
            BwmParser.plot_graph(plots[scheme], scheme, 'o-')

        plt.ylabel(param)
        plt.legend()
        image_filename = os.path.join(self.directory, param + '.png')
        plt.savefig(image_filename,dpi=PLOT_IMAGE_QUALITY)
        plt.clf()

if __name__ == "__main__":
    exp_comp = ExperimentsComparison(SAMPLES_DIRECTORY)
    exp_comp.prepare_plots('goodput')
    exp_comp.prepare_plots('throughtput_total')
    exp_comp.prepare_plots('time_taken')
