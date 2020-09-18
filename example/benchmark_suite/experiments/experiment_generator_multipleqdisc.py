import os
from shutil import copystat, copyfile

qdisc_start = "---\n"
qdisc_terminate = "...\n"

qdisc_interface_1 = '''
  - 
    interface: "{}"
    
    netem:
      netem_on: yes
      
      packet_corruption_on: no
      packet_corruption: 1%

      delay_on: yes
      delay: 
        delay_time: {}ms
        error: {}ms
        correlation: 0%

      packet_loss_on: yes
      packet_loss: 
        loss: {}%
        correlation: 0%
   
    tbf: 
      tbf_on: yes
      rate: {}kbit
      latency: '3000'
      burst: 32kbit
#---------------------------#
  
'''

qdisc_interface_2 = '''
  - 
    interface: "{}"
    
    netem:
      netem_on: yes
      
      packet_corruption_on: no
      packet_corruption: 1%

      delay_on: yes
      delay: 
        delay_time: {}ms
        error: {}ms
        correlation: 0%

      packet_loss_on: yes
      packet_loss: 
        loss: {}%
        correlation: 0%
   
    tbf: 
      tbf_on: yes
      rate: {}kbit
      latency: '3000'
      burst: 32kbit
#---------------------------#
  
'''

exp = '''
# Blocks of size BLOCK_SIZE bytes will be requested 
# DELAY_TIME milliseconds pause after each block
# ITERATIONS number of times, with 

BLOCK_SIZE: {}
DELAY_TIME: {}
ITERATIONS: {}

varying_qdisc: yes

# List of qdisc files and their duration
qdisc_confs: {
    'qdisc.yaml': 5,
    'qdisc_2.yaml': 5
}
---------------------------
'''



#time_1 = 5
#time_2 = 5

BLOCK_SIZES = [100000000] # 100 MB
TIME_REQ = [0]#in ms
ITERATIONS = [1]

# s1_delays = [50]
# s1_losses = [1]
# s1_bandwidths = [2000] #2Mbps

# s2_delays = [500]
# s2_losses = [0.001]
# s2_bandwidths = [250] #250kbps

# Satellite connection
s1_delays_1 = [250]
s1_losses_1 = [0]
s1_bandwidths_1 = [150] # in Kbps

s2_delays_1 = [150]
s2_losses_1 = [0]
s2_bandwidths_1 = [1000] # in Kbps

# Cellular connection
s1_delays_2 = [250]
s1_losses_2 = [0]
s1_bandwidths_2 = [150] # in Kbps

s2_delays_2 = [150]
s2_losses_2 = [0]
s2_bandwidths_2 = [1] # in Kbps

filename_begin = "{}"

exp_num = 0

for s1_delay_1 in s1_delays_1:
    for s1_loss_1 in s1_losses_1:
        for s1_bandwidth_1 in s1_bandwidths_1:
            for s2_delay_1 in s2_delays_1:
                for s2_loss_1 in s2_losses_1:
                    for s2_bandwidth_1 in s2_bandwidths_1:
                        for s1_delay_2 in s1_delays_2:
                            for s1_loss_2 in s1_losses_2:
                                for s1_bandwidth_2 in s1_bandwidths_2:
                                    for s2_delay_2 in s2_delays_2:
                                        for s2_loss_2 in s2_losses_2:
                                            for s2_bandwidth_2 in s2_bandwidths_2:
                                                for block_size in BLOCK_SIZES:
                                                    for time_req in TIME_REQ:
                                                        for iterations in ITERATIONS:
                                                            exp_num += 1
                                                            exp_dir = filename_begin.format(str(exp_num)) 
                                                            os.mkdir( exp_dir )
                                                            os.mkdir( exp_dir + '/client')
                                                            os.mkdir( exp_dir + '/router')
                                                            os.mkdir( exp_dir + '/server')

                                                            copyfile('experiment_demo/topo.py', exp_dir+'/topo.py')
                                                            copystat('experiment_demo/topo.py', exp_dir+'/topo.py')
                                                            copyfile('experiment_demo/client/config.sh', exp_dir+'/client/config.sh')
                                                            copystat('experiment_demo/client/config.sh', exp_dir+'/client/config.sh')
                                                            copyfile('experiment_demo/server/config.sh', exp_dir+'/server/config.sh')
                                                            copystat('experiment_demo/server/config.sh', exp_dir+'/server/config.sh')
                                                            copyfile('experiment_demo/router/config.sh', exp_dir+'/router/config.sh')
                                                            copystat('experiment_demo/router/config.sh', exp_dir+'/router/config.sh')

                                                            qdisc_file = open(exp_dir+"/qdisc.yaml", "w+")
                                                            qdisc_file.write(qdisc_start)
                                    
                                                            qdisc_file.write( qdisc_interface_1.format("s1-eth1", str(s1_delay_1), str(s1_delay_1//10), str(s1_loss_1), str(s1_bandwidth_1)) )
                                                            qdisc_file.write( qdisc_interface_1.format("s1-eth2", str(s1_delay_1), str(s1_delay_1//10), str(s1_loss_1), str(s1_bandwidth_1)) )
                                                            qdisc_file.write( qdisc_interface_1.format("s2-eth1", str(s2_delay_1), str(s2_delay_1//10), str(s2_loss_1), str(s2_bandwidth_1)) )
                                                            qdisc_file.write( qdisc_interface_1.format("s2-eth2", str(s2_delay_1), str(s2_delay_1//10), str(s2_loss_1), str(s2_bandwidth_1)) )

                                                            qdisc_file.write(qdisc_terminate)
                                                            qdisc_file.close()


                                                            qdisc_file = open(exp_dir+"/qdisc_2.yaml", "w+")
                                                            qdisc_file.write(qdisc_start)
                                    
                                                            qdisc_file.write( qdisc_interface_2.format("s1-eth1", str(s1_delay_2), str(s1_delay_2//10), str(s1_loss_2), str(s1_bandwidth_2)) )
                                                            qdisc_file.write( qdisc_interface_2.format("s1-eth2", str(s1_delay_2), str(s1_delay_2//10), str(s1_loss_2), str(s1_bandwidth_2)) )
                                                            qdisc_file.write( qdisc_interface_2.format("s2-eth1", str(s2_delay_2), str(s2_delay_2//10), str(s2_loss_2), str(s2_bandwidth_2)) )
                                                            qdisc_file.write( qdisc_interface_2.format("s2-eth2", str(s2_delay_2), str(s2_delay_2//10), str(s2_loss_2), str(s2_bandwidth_2)) )

                                                            qdisc_file.write(qdisc_terminate)
                                                            qdisc_file.close()

                                                            copyfile('experiment_multiple_qdisk_demo/exp.yaml', exp_dir+'/exp.yaml')
                                                            copystat('experiment_multiple_qdisk_demo/exp.yaml', exp_dir+'/exp.yaml')

                                                            #exp_file = open(exp_dir+"/exp.yaml", "w+")
                                                            #exp_file.write(exp.format(str(block_size),str(time_req), str(iterations)))
                                                            #exp_file.close()
