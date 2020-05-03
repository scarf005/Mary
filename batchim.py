from yaml_functions import LANG

def Batchim(word, with_Batchim, without_Batchim):
    if LANG == "ko\\":
        criteria = (ord(word[-1]) - 44032) % 28
        if criteria == 0: #No Batchim!
            return word+without_Batchim
        else:
            return word+with_Batchim
    else: return word