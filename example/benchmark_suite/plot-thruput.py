import matplotlib
import csv
from pprint import pprint
import matplotlib.pyplot as plt
from time import sleep

FILENAME = 'results.csv'

def plot_graph(data,label):
    x = []
    y = []
    for tup in data:
        x.append(tup[0])
        y.append(tup[1])
    
    plt.plot(x,y,label=label)

data = []
ifaces = set()
plots = {}

with open(FILENAME) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        data.append(row)

for row in data:
    iface = row[1]
    ifaces.add(iface)
    
for iface in ifaces:
    plots[iface] = {}
    # plots[iface]['in'] = []
    # plots[iface]['out'] = []
    plots[iface]['total'] = []

pprint(plots)

for row in data:
    timestamp = row[0]
    iface = row[1]
    bytes_out = row[2]
    bytes_in = row[3]
    bytes_total = row[4]

    # plots[iface]['in'].append((timestamp,int(bytes_in)/1024))
    # plots[iface]['out'].append((timestamp,int(bytes_out)/1024))
    plots[iface]['total'].append((timestamp,int(bytes_total)/(1024*1024)))

for iface,dats in plots.items():
    for lab,dat in dats.items():
        plot_graph(dat,'_'.join([iface,lab]))

plt.legend()
plt.savefig('result.png',dpi=500)