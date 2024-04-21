from .mapper import mlist

def mapping(name:str)-> str:
    if name in mlist:
        name = mlist[name]
    return name