import inspect
import string

def debugstring(inbuf,iline,ilength):
    s = "\nDebug Information from Line:[%s],string length:[%s]\n"%(iline,ilength)
    print s

    k = int(ilength/0xFFFF)
    for l in range(0,k+1):
        s = '-'*84
        tmp = "[%02d BEGIN]"%(k+1)
        s = s[:35] + tmp + s[45:]
        print s

        if l == k:
            rlength = ilength%0xFFFF
        else:
            rlength = 0xFFFF

        j = 0
        for i in range(0,rlength):
            if j == 0:
                s = ' '*84
                tmp = "%04X:"%i
                s = tmp + s[6:]
                tmp = "%04X:"%(i+15)
                s = s[:74] + tmp
            tmp = "%02X "%ord(inbuf[i])
            offset = j*3 + 7 + (j>7)
            s = s[:offset] + tmp + s[offset+3:]
            if (inbuf[i] in string.printable) and ord(inbuf[i]) != 9 and ord(inbuf[i]) != 10:
                offset = j+56+(j>7)
                s = s[:offset] + inbuf[i] + s[offset+1:]
            else:
                offset = j+56+(j>7)
                s = s[:offset] + '.' + s[offset+1:]
            j+= 1
            if j == 16:
                print s
                j = 0
            
        if j and rlength:
            print s
        s = '-'*84
        tmp = "[%02d END]"%(k+1)
        s = s[:36] + tmp + s[44:]
        print s

if __name__ == '__main__':
    linenum = inspect.getframeinfo(inspect.currentframe())[1]
    sr = "4340617200411561d140710100000919000000"
    print string.printable
    for i in string.printable:
        print "%02X,%s"%(ord(i),i)
    
