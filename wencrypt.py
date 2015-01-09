#coding=gbk
import struct
internalCypher = (159,129,152,205,212,146,150,224,223,193,176,124,85,150,1,45,204,180,142,244,82,146,141,81,10,
                  226,249,251,103,85,119,194,11,238,123,31,38,46,187,38,160,246,80,104,30,2,7,19,97,153,126,3,52,
                  163,230,12,244,70,194,241,152,154,121,138,74,238,113,102,27,225,6,158,249,104,83,92,66,36,50,8,219,229,
                  154,205,214,116,141,103,7,111,43,223,108,201,141,6,125,198,29,47,145,160,248,127,147,224,9,203,80,138,202,207,19,
                  186,22,178,255,171,179,213,96,9,95,172,182,38,49,47,219,76,222,123,6,3,119,59,237,26,58,245,106,194,22,
                  125,164,91,203,178,179,218,6,209,18,72,207,135,65,75,201,108,174,218,240,3,171,78,200,16,66,218,197,228,
                  113,190,106,158,242,226,7,90,91,127,123,1,70,13,105,190,51,239,249,161,81,205,70,144,210,19,209,86,146,186,
                  111,216,21,33,95,83,221,49,149,95,68,111,17,47,94,239,189,158,228,10,221,83,225,35,147,164,119,218,204,223,16,
                  176,199,160,16,162,235,36,173,21,225,2,90,154,93,226,188,23,50,226,85,50,114)

def GetCurCypher(sKey):
    '''
    '''
    curCypher = [c for c in internalCypher]
    l_sKey = len(sKey)
    l_Cypher = len(curCypher)
    for i in range(l_sKey):
        for j in range(l_Cypher):
            switchIndex = ((ord(sKey[i])+i)* curCypher[j]) % 255
            if(switchIndex != j):
                curCypher[j],curCypher[switchIndex] = curCypher[switchIndex],curCypher[j]
    return curCypher



def BytestoHexString(barr):
    s = ''
    if barr is None or len(barr)==0:
        return s
    l = [GetSingleHex(b) for b in barr]
    return reduce(lambda x,y:x+y,l)

def GetSingleHex(b):
    iCur = b & 0xFF
    sCur = hex(b)
    sCur = sCur.replace("0x","")
    if(len(sCur)==1):
        sCur="0" + sCur
    return sCur


def WEncode(sPassword,sKey):
    myCypher = GetCurCypher(sKey)
    iIndex = 0
    byPwd = sPassword.encode('utf-8')
    barrPwd = bytearray(byPwd)
    barrLen = len(barrPwd)
    while iIndex<barrLen:        
        barrPwd[iIndex] = barrPwd[iIndex] ^ myCypher[iIndex % 255]
        iIndex += 1
    encryptedPwd = BytestoHexString(barrPwd)    
    return encryptedPwd

def ChartoByte(c):
    s = "0123456789ABCDEF"
    return (s.find(c))

def HexStringtoBytes(sHex):
    if sHex is None or sHex=="":
        return None
    sHex = sHex.upper()
    length = len(sHex)   
    barr = []
    for i in range(0,length,2):
        pos = i
        by = (ChartoByte(sHex[pos]) << 4 | ChartoByte(sHex[pos+1]))
        barr.append(by)
    return barr

def WDecode(encryptedPassword,sKey):
    myCypher = GetCurCypher(sKey)
    barrPwd = HexStringtoBytes(encryptedPassword)
    strPwd = ""
    iIndex = 0
    barrLen = len(barrPwd)
    while iIndex<barrLen:
        barrPwd[iIndex] = barrPwd[iIndex] ^ myCypher[iIndex % 255]
        strPwd = strPwd + chr(barrPwd[iIndex])
        iIndex += 1    
    return strPwd;


while(True):
    q = raw_input("input password and skey(password,skey)\n>>>")
    if(q=="q"):
        break
    else:
        oPwd = q
        sKey = ""
        if(q.find(",")>=0):
            pwd_skey = q.split(",")
            oPwd = pwd_skey[0]
            sKey = pwd_skey[1]
        enPwd = WEncode(oPwd,sKey)
        print "加密结果:" + enPwd+ "\n"
        oPwd1= WDecode(enPwd,sKey)
        print "原字符:" + oPwd1

#1234567890abcdefghijklmnopqrstuvwxyz

#def BytestoHexString(barr):
#    s = ''
#    if barr is None or len(barr)==0:
#        return s    
#    for i in range(len(barr)):
#        iCur = barr[i] & 0xFF
#        sCur = hex(iCur)        
#        sCur = sCur.replace("0x","")
#        if(len(sCur)==1):
#            sCur = "0" + sCur
#        s = s + sCur
#    return s