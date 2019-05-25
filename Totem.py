class Totem:
    def __init__(self,n):
        self.id = ["0" for _ in range(n)]
        self.index = [0 for _ in range(2)]
        self.uniqueid = -1

    def __repr__(self):
        ret = "["
        for i in range(len(self.id)):
            ret = ret + self.id[i]
        ret = ret + "]"
        return ret

    def setIDInt(self,val,n):
        bin = "{0:b}".format(val)
        bin = bin.zfill(n)
        l = list(bin)
        for i in range(len(l)):
            self.id[i] = l[i]
        self.uniqueid = val

    def match(self,other): # one element equal
        if(self is None or other is None):
            return False
        if(self == other):
            return False
        for i in range(len(self.id)):
            if(self.id[i] == other.id[i]):
                return True
        return False

    def __eq__(self,other): # all elements equal
        if(self is None or other is None):
            return False
        if(self.uniqueid == other.uniqueid):
            return True
        return False
        # for i in range(len(self.id)):
        #     if(self.id[i] != other.id[i]):
        #         return False
        # return True

    def setIndex(self,x,y):
        self.index[0] = x;
        self.index[1] = y;
