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
        for i in range(K*K):                        #customize
            hostSet = addHost("hs"+str(i))

        for i in range(0, K*2, 2):
            for j in range(0,K/2):
                self.addLink(self.coreSet[j], self.aggSet[i], bw=10) #bw is changable

        for i in range(1, K*2, 2):
            for j in range(K/2, K):
                self.addLink(self.coreSet[j], self.aggSet[i], bw=10) #bw is changable
        