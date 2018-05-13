import random

#la = [1,2,3,4,5,6,7,8,9,0,A,B,C,D,E,F]
#re = random.sample(la,32)
def getWorkKey(count):
    listNum = ['1','2','3','4','5','6','7','8','9','0','A','B','C','D','E','F']
    key = ""
    for i in xrange(count):
        index = random.randint(0,15)
        #print index
        key += listNum[index]
    print key

    return
def getWorkKey1(count):
    listNum = "1234567890ABCDEF1234567890ABCDEF"
    key = ""
    for i in xrange(count):
        index = random.randint(0,31)
        #print index
        key += listNum[index]
    print key

    return

getWorkKey1(32)
getWorkKey1(16)

