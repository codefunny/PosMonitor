import inspect

def pytest(iline,ilength):
    print iline,ilength
    return

print inspect.getframeinfo(inspect.currentframe())[1]
filename, linenum, funcname = inspect.getframeinfo(inspect.currentframe())[:3] 

print filename,linenum,funcname

    
