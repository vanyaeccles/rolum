
class PRNG():

    # global values
    u = [0] * 97
    c = 0 
    cd = 0 
    cm = 0
    I97 = 0
    J97 = 0
    test = False

    def __init__(self):
        seed1 = 12344
        seed2 = 20256
        self.InitialiseRandomSeq(seed1, seed2)
        
    
    def InitialiseRandomSeq(self, ij, kl):
        s = 0.0
        t = 0.0
        i = 0 
        j = 0
        k = 0
        l = 0 
        m = 0
       
        if (ij < 0) or (ij > 31328) or (kl < 0) or (kl > 30081): 
            ij = 1802
            kl = 9373
        
        i = (ij / 177) % 177 + 2
        j = (ij % 177)       + 2
        k = (kl / 169) % 178 + 1
        l = (kl % 169)
        
        for ii in range (0, 97): 
            s = 0.0
            t = 0.5
      
            for jj in range (0, 24):
                m = (((i * j) % 179) * k) % 179
                i = j
                j = k
                k = m
                l = (53 * l + 1) % 169
                if (((l * m % 64)) >= 32):
                    s += t;
                t *= 0.5;
                
            self.u[ii] = s;

        self.c = 362436.0/16777216.0
        self.cd = 7654321.0/16777216.0
        self.cm = 16777213.0/16777216.0
        self.i97 = 97
        self.j97 = 33
        self.test = True
        
    def GetRandomUniform(self):
        uni = 0.0
        i97 = self.I97
        j97 = self.J97
        #if not self.test:
        #   self.InitialiseRandomSeq(1802,9373)
        uni = self.u[i97-1] - self.u[j97-1]
        if uni <= 0.0:
            uni += 1
        self.u[i97-1] = uni
        i97 -= 1
        if (i97 == 0):
            i97 = 97
        j97 -= 1
        if (j97 == 0):
            j97 = 97
        self.c -= self.cd
        if (self.c < 0.0):
            self.c += self.cm
        uni -= self.c
        if (uni < 0.0):
            uni += 1
            
        self.J97 = j97
        self.I97 = i97
        return uni
        
    def GetRandomInt(self, dType):
            
        '''rolled_number = self.GetRandomUniform()# * (dType + 1)
        rolled_number = str(int(rolled_number))
        return dType, rolled_number'''
        rolled_number = self.GetRandomUniform() * (int(dType) + 1)
        return dType, rolled_number
        