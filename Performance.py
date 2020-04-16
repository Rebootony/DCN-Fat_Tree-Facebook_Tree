class fatTree():
    "create fat tree topo with 4 core 8 aggregate 8 edge 16 hosts"
    def build(self):
        coreSet = {}
        aggSet = {}
        edgeSet = {}
        hostSet = {}
        K=4
        for i in range(K):
            coreSet[i] = addSwitch("cs"+str(i))
        for i in range(K*2):
            aggSet = addSwitch("as"+str(i))
            edgeSet = addSwitch("es"+str(i))
        for i in range(K*4):
            hostSet = addSwitch("hs"+str(i))
        
        

