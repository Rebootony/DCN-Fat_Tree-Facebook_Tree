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

def perfTest():
    "test the fat tree"
    topo = fatTree(n=4)
    net = Mininet( topo=topo, controller=None)
    net.addController( 'ctr0', controller=RemoteController, ip='127.0.0.1', port=6633 ) 
    net.build()
    CLI(net)
    net.stop()
    pass

if __name__ == "__main__":
    perfTest()