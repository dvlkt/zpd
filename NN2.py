from random import *
from math import *
Max_Button_Count=10
#creates a class for a network
class network:
    #data tiek strukturēts šādi:
    # 0. Max neironu skaits
    # 1. Max dažādu pikseļu skaits Bildē-1
    # 2. Bildes Platums
    # 3. Bildes Augstums
    # 4. cik % neironu izmainīt
    def __init__(self,neironi=[],data=[1,0,16,32,10]):
        self.knowledge=[[0 for i in range(32)] for i in range(16)]
        if neironi!=[]:
            self.neironi=neironi #paņem neironus no iepriekšējā tīkla
            #for i in range(len(self.neironi)):
                #if randint(1,100)>=data[3]: #izmaina daļu neironu
                    #which=randint()
        else:
            self.neironi=[] #izveido jaunus neironus
            for i in range(randint(1,data[0])): #paņem nejaušu skaitli jaunus neironus
                receptori=[]
                for i in range(randint(1,5)):
                    if randint(1,data[3]*data[2]+len(self.neironi))<=len(self.neironi): #izvēlas ko ņemt, neironu, vai pikseli no bildes
                        receptori.append(randint(0,len(self.neironi)-1)) #paņem neironu
                    else:
                        receptori.append([randint(0,data[2]-1),randint(0,data[3]-1),randint(0,data[1])]) #paņem pikseli no bildes
                self.neironi.append([receptori,0,1==randint(1,2)]) #ieliek receptorus un šībrīža vērtību neironam, un vai neironam jābūt ieslēgtam
        self.reqs=[]#requirements for each of the 10 output buttons
        for i in range(10):
            req=[]
            for i in range(randint(1,min(10,len(self.neironi)))):#nejaušu skaitu neironu izvēlas starp 1 un pieci
                req.append([randint(0,len(self.neironi)-1),1==randint(1,2)]) #izvēlas neironu, vai tam jābūt ieslēgtam
            self.reqs.append([req,0])#saglabā neironu un pašreizējo vērtību
    def aknowledge(self,Double_Array=[]):# recieves a 2d array, and saves it as its knowledge
        self.knowledge=Double_Array
    def think(self):
        for i in range(len(self.neironi)):
            self.neironi[i][1]=1
            for i1 in range(len(self.neironi[i][0])):
                if type(self.neironi[i][0][i1])==int: #paskatās vai i1 tais inputs ir neirons
                    if (self.neironi[self.neironi[i][0][i1]][1]==1)!=self.neironi[i][2]:#paskatās vai neironam būtu jābūt ieslēgtam lai šis aktivizētos un vai tas ir ieslēgts, un izslēdz ja kāds nestrādā
                        self.neironi[i][1]=0
                else: #ja i1 tais inputs ir pikselis bildē
                    if self.knowledge[self.neironi[i][0][i1][0]][self.neironi[i][0][i1][1]]!=self.neironi[i][0][i1][2]: #ja pikselis bildē neatbilst pikselim, ko meklē neirons, tas izslēdzas
                        self.neironi[i][1]=0
        self.outputs=[0 for i in range(10)]
        for i in range(len(self.reqs)):
            self.reqs[i][1]=1 #ieslēdz reqs
            for i1 in range(len(self.reqs[i][0])):
                if self.neironi[self.reqs[i][0][i1][0]][1]!=self.reqs[i][0][i1][1]: #paskatās vai i1 tajā req neitrona stāvoklis atbilst stāvoklim, ko req sagaida, un ja nē, tad req tiek izslēgts                
                    self.reqs[i][1]=0
            if self.reqs[i][1]==1:
                self.outputs[i]=1
    def generate(self):
        #self.aknowledge()
        self.think()
        return self.outputs

N=network([],[2,0,16,32,10])
print(N.generate())
                        
                       #vēlāk sarakstīšu komentārus kur vajag
                    
        
        
        
    
