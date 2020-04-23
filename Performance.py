from mininet.log import setLogLevel, info
from mininet.node import Controller
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.node import RemoteController
from mininet.cli import CLI
import subprocess
import sys
import threading
from concurrent.futures import thread
class fatTree(Topo):
    "create fat tree topo with 4 core 8 aggregate 8 edge 16 hosts"
    def build(self, n=4):
        K=4
        coreSet = {}
        aggSet = {}
        edgeSet = {}
        hostSet = {}
        for i in range(pow(K/2,2)):
            coreSet[i] = self.addSwitch("cs"+str(i))
        for i in range(K*K/2):
            aggSet[i] = self.addSwitch("as"+str(i))
            edgeSet[i] = self.addSwitch("es"+str(i))
        for i in range(K*K):                                        #customize
            hostSet[i] = self.addHost("hs"+str(i))

        #core and agg
        for i in range(0, K*K/2, 2):
            for j in range(0,pow(K/2,2)/2):
                self.addLink(coreSet[j], aggSet[i], bw=10) #bw is changable
        for i in range(1, K*K/2, 2):
            for j in range(pow(K/2,2)/2, pow(K/2,2)):
                self.addLink(coreSet[j], aggSet[i], bw=10) #bw is changable
        
        #agg and edge
        for i in range(0,K*K/2,2):
            self.addLink(aggSet[i],edgeSet[i],bw=10)
            self.addLink(aggSet[i],edgeSet[i+1],bw=10)
        for i in range(1,K*K/2,2):
            self.addLink(aggSet[i],edgeSet[i],bw=10)
            self.addLink(aggSet[i],edgeSet[i-1],bw=10)

        #edge and host
        for i in range(0,K*K,1):
            self.addLink(edgeSet[i/2],hostSet[i],bw=10)

def iperf_thread(net, src, dst):#cited from "lebiednik/ICNmininet" 
    hostPair = [src, dst]
    bandwidth = net.iperf(hostPair, seconds = 10)

def perfTest():
    "test the fat tree"
    topo = fatTree(n=4)
    net = Mininet( topo=topo, controller=None)
    net.addController( 'ctr0', controller=RemoteController, ip='127.0.0.1', port=6633 ) 
    net.build()
    net.waitConnected()
    net.pingAll()
    host={}
    maxHost = 16
    for y in range(0, maxHost):
        hostName = 'h' +str(y)
        host[y] = net.get(hostName)

    for x in range(0, (maxHost/2)):
        src = host[x]
        dst = host[(maxHost-1)-x]
        thread.start_new_thread(iperf_thread(net, dst, src))
        thread.start_new_thread(iperf_thread(net, src, dst))
    out= {}

    for h in range(0, maxHost):
        out[ host[h] ] = '/tmp/%s.out' % host[h].name
        host[h].cmd( 'echo >', out[ host[h] ] )

    packetSize=[50,100,150,200,300,450,600,750,900,1200]
    for i in range (10):
        host[h].cmdPrint('ping', host[h+1].IP(), '-s', packetSize[i], '>', out[ host[h] ], '&' )
    
    CLI(net)
    net.stop()
    subprocess.call(['mn', '-c'])
    pass

if __name__ == '__main__':
    setLogLevel('info')
    perfTest()