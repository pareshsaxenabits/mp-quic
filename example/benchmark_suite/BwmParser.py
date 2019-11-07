import csv
import os
import matplotlib.pyplot as plt

class BwmParser:

    PLOT_IMAGE_QUALITY = 500 # DPI
    TP_INTERFACES = [
        's1-eth1',
        's2-eth1',
    ]
    TP_TYPES = [
        'in',
        'out',
        'total'
    ]

    def __init__(self, output_filename, plot=True):
        
        self.filename = output_filename
        self.data = []
        self.ifaces = set()

        self.gather_data()
        self.get_interfaces()
        self.byte_transfers()

        if plot:
            self.create_plots()

    def byte_transfers(self):
        self.total_bytes_transferred = {iface:0 for iface in self.ifaces}
        for row in self.data:
            iface = row[1]
            if iface in self.ifaces:
                self.total_bytes_transferred[iface] = max(
                    int(self.total_bytes_transferred[iface]), int(row[4]))
        
        total = 0
        for iface, bytes_sent in self.total_bytes_transferred.items():
            if iface in self.ifaces:
                total += bytes_sent
        self.total_bytes_transferred['total'] = total

    @staticmethod
    def plot_graph(data,label):
        x = []
        y = []
        for tup in data:
            x.append(tup[0])
            y.append(tup[1])
        
        plt.plot(x,y,label=label)

    def create_plots(self):
        self.plots = {}

        for iface in self.ifaces:
            self.plots[iface] = {}
            self.plots[iface]['out'] = []
            self.plots[iface]['in'] = []
            self.plots[iface]['total'] = []

        for row in self.data:
            timestamp = row[0]
            iface = row[1]
            if iface in self.ifaces:
                self.plots[iface]['out'].append((timestamp,int(row[2])/(1024*1024)))
                self.plots[iface]['in'].append((timestamp,int(row[3])/(1024*1024)))
                self.plots[iface]['total'].append((timestamp,int(row[4])/(1024*1024))) # MBytes

        for iface,dats in self.plots.items():
            for label,dat in dats.items():
                if label in BwmParser.TP_TYPES:
                    BwmParser.plot_graph(dat,'_'.join([iface,label]))

        plt.legend()

        image_filename = list(os.path.splitext(self.filename))
        image_filename[-1] = '.png'
        image_filename = ''.join(image_filename)
        plt.savefig(image_filename,dpi=BwmParser.PLOT_IMAGE_QUALITY)
        plt.clf()

    def gather_data(self):
        with open(self.filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.data.append(row)

    def get_interfaces(self):
        for row in self.data:
            iface = row[1]
            if iface in BwmParser.TP_INTERFACES:
                self.ifaces.add(iface)
