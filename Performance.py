class fatTree():
    "create fat tree topo with 4 core 8 aggregate 8 edge 16 hosts"
    coreSet = {}
    aggSet = {}
    edgeSet = {}
    hostSet = {}
    def build(self):
        K=4
        for i in range(pow(K/2,2)):
            coreSet[i] = addSwitch("cs"+str(i))
        for i in range(K*K/2):
            aggSet = addSwitch("as"+str(i))
            edgeSet = addSwitch("es"+str(i))
        for i in range(K*K):                                        #customize
            hostSet = addHost("hs"+str(i))

        #core and agg
        for i in range(0, K*K/2, 2):
            for j in range(0,pow(K/2,2)/2):
                self.addLink(self.coreSet[j], self.aggSet[i], bw=10) #bw is changable
        for i in range(1, K*K/2, 2):
            for j in range(pow(K/2,2)/2, pow(K/2,2)):
                self.addLink(self.coreSet[j], self.aggSet[i], bw=10) #bw is changable
        
        #agg and edge
        for i in range(0,K*K/2,2):
            self.addLink(self.aggSet[i],self.edgeSet[i],bw=10)
            self.addLink(self.aggSet[i],self.edgeSet[i+1],bw=10)
        for i in range(1,K*K/2,2):
            self.addLink(self.aggSet[i],self.edgeSet[i],bw=10)
            self.addLink(self.aggSet[i],self.edgeSet[i-1],bw=10)

        #edge and host
        for i in range(0,K*K,1):
            self.addLink(self.edgeSet[i/2],self.hostSet[i],bw=10)

        