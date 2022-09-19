#!/usr/bin/env python3
#beginning code reused from old assembler!

###################################################
## TGR MEMORY MAP #################################
# ROM[0]  $0800000 [$0000000 - $07FFFFF]   8   MB #
# ROM[1]  $0800000 [$0800000 - $0FFFFFF]   8   MB #
# SAV     $0800000 [$1000000 - $17FFFFF]   8   MB #
# WRAM    $7fbfe00 [$1800000 - $97BFDFF] 127.9 MB #
# STACK   $0040000 [$97BFE00 - $97FFDFF] 256   KB #
# I/O     $0000200 [$97BFE00 - $97FFFFF] 512   BY #
# VRAM    $4000000 [$9800000 - D7FFFFF$]  64   MB #
## 216 MB [0xD800000] #############################
###################################################
#### ROM can be up to 16MB split into 2 Banks! ####
## exROM can be up to 128MB split into 16 Banks! ##
###################################################

import sys,os
global asm

def reg(x):
 try: return "abcdefgh".index(str(x).lower())
 except ValueError: return -1

def ctc(a,b): ##CombineToChar##
 if b < 0xf and a < 0xf: return b | a << 4
 else: raise ValueError("values too large to fit in char")

def include(FN,loc):
 global asm
 try:
  with open(FN,"r") as file:
   asm=asm[:loc]+["; "+("#"*(14+len(FN)))+"\n","; ## FILE: \""+FN+"\" ##\n","; "+("#"*(14+len(FN)))+"\n"]+file.readlines()+asm[loc:]
   len(file.readlines())
  print(FN,"loaded...")
 except IOError: print("ImportError: File \""+FN+"\" could not be found..."); exit(-1)

def replace(st,rp):
 loc = st.find(rp)
 if loc == -1: return st[:loc]+st[loc+len(rp):]
 else: return st

def check(number):
 if str(number)[:2] == "0x": return int(number[2:],16)
 else:
  try: return int(number)
  except ValueError: print("Invalid Value given: \""+str(number)+"\"... if this is hex, please provide 0x at the start of the value"); sys.exit()

def wram16(arg,addr,out,address):
 if arg == reg("A"): out+=[
  0x1C,0x00,0x00,0x00,0x00,0x00, #push A
  0x1C,0x10,0x00,0x00,0x00,0x00, #push B
  0x0C,0x10,0x10,0x00,0x00,0x00, #split B,A,B
  0x14,0x00,(check(addr  )&0xF000000)>>24,(check(addr  )&0x0FF0000)>>16,(check(addr  )&0x000FF00)>> 8, check(addr  )&0x00000FF, #wram A,[XX..]
  0x14,0x10,(check(addr+1)&0xF000000)>>24,(check(addr+1)&0x0FF0000)>>16,(check(addr+1)&0x000FF00)>> 8, check(addr+1)&0x00000FF, #wram B,[..XX]
  0x1B,0x10,0x00,0x00,0x00,0x00, #pop B
  0x1B,0x00,0x00,0x00,0x00,0x00] #pop A
 else: j=ctc(reg(arg),0); out+=[
  0x1C,  j ,0x00,0x00,0x00,0x00, #push ARG[2]
  0x1C,0x00,0x00,0x00,0x00,0x00, #push A
  0x0C,  j ,  j ,0x00,0x00,0x00, #split ARG[2],A,ARG[2]
  0x14,0x00,(check(addr  )&0xF000000)>>24,(check(addr  )&0x0FF0000)>>16,(check(addr  )&0x000FF00)>> 8, check(addr  )&0x00000FF, #wram   A   ,[XX..]
  0x14,  j ,(check(addr+1)&0xF000000)>>24,(check(addr+1)&0x0FF0000)>>16,(check(addr+1)&0x000FF00)>> 8, check(addr+1)&0x00000FF, #wram ARG[2],[..XX]
  0x1B,0x00,0x00,0x00,0x00,0x00, #pop A
  0x1B,  j ,0x00,0x00,0x00,0x00] #pop ARG[2]
 return out,address+(6*7)

def rram16(arg,addr,out,address):
 if arg == reg("A"): out+=[
  0x1C,0x00,0x00,0x00,0x00,0x00, #push A
  0x1C,0x10,0x00,0x00,0x00,0x00, #push B
  0x13,0x00,(check(addr  )&0xF000000)>>24,(check(addr  )&0x0FF0000)>>16,(check(addr  )&0x000FF00)>> 8, check(addr  )&0x00000FF, #wram A,[XX..]
  0x13,0x10,(check(addr+1)&0xF000000)>>24,(check(addr+1)&0x0FF0000)>>16,(check(addr+1)&0x000FF00)>> 8, check(addr+1)&0x00000FF, #wram B,[..XX]
  0x0D,0x01,0x10,0x00,0x00,0x00, #split A,B,B
  0x1B,0x10,0x00,0x00,0x00,0x00, #pop B
  0x1B,0x00,0x00,0x00,0x00,0x00] #pop A
 else: j=ctc(reg(arg),0); out+=[
  0x1C,  j ,0x00,0x00,0x00,0x00, #push ARG[2]
  0x1C,0x00,0x00,0x00,0x00,0x00, #push A
  0x13,0x00,(check(addr  )&0xF000000)>>24,(check(addr  )&0x0FF0000)>>16,(check(addr  )&0x000FF00)>> 8, check(addr  )&0x00000FF, #wram   A   ,[XX..]
  0x13,  j ,(check(addr+1)&0xF000000)>>24,(check(addr+1)&0x0FF0000)>>16,(check(addr+1)&0x000FF00)>> 8, check(addr+1)&0x00000FF, #wram ARG[2],[..XX]
  0x0D,ctc(0,reg(arg)),  j ,0x00,0x00,0x00, #combine A,ARG[2],ARG[2]
  0x1B,0x00,0x00,0x00,0x00,0x00, #pop A
  0x1B,  j ,0x00,0x00,0x00,0x00] #pop ARG[2]
 return out,address+(6*7)

ascii = "................................ !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~.................................¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ.............................."
def dumpData(name, data, use_non, start, end):
 bytes = []
 print("._______._______________________________________________.________________.\n|{}".format(name),end='')
 if   len(name) < 2:  print("      ",end='')
 elif len(name) < 3:  print("     ",end='')
 elif len(name) < 4:  print("    ",end='')
 elif len(name) < 5:  print("   ",end='')
 elif len(name) < 6:  print("  ",end='')
 elif len(name) < 7:  print(" ",end='')
 print("|00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F|0123456789ABCDEF|\n|-------|-----------------------------------------------|----------------|\n|0000000|",end='')
 j,l,m = 1,0,""
 for i in range(start,end):
  if i >= len(data): break
  if j > 15:
   bytes.append(data[i])
   if data[i] < 0x10: print("0",end='');
   print("{}|".format(hex(data[i])[2:]),end='')
   for k in range(16):
    if use_non: print(ascii[bytes[i-15+k]],end='')
    else:       print(ascii[bytes[i-15+k]],end='')
   l=i
   print("|\n|",end='')
   if   i+1 < 0x1:        print("0000000{}|".format(hex(i+1)[2:]),end='')
   elif i+1 < 0x10:       print("000000{}|".format(hex(i+1)[2:]),end='')
   elif i+1 < 0x100:      print("00000{}|".format(hex(i+1)[2:]),end='')
   elif i+1 < 0x1000:     print("0000{}|".format(hex(i+1)[2:]),end='')
   elif i+1 < 0x10000:    print("000{}|".format(hex(i+1)[2:]),end='')
   elif i+1 < 0x100000:   print("00{}|".format(hex(i+1)[2:]),end='')
   elif i+1 < 0x1000000:  print("0{}|".format(hex(i+1)[2:]),end='')
   elif i+1 < 0x10000000: print("{}|".format(hex(i+1)[2:]),end='')
   j = 0
  else:
   if data[i] < 0x10: print("0",end='')
   print(hex(data[i])[2:],end=' ')
   bytes.append(data[i])
  j+=1
 if j > 0:
  for i in range(j,16):
   print("-- ",end='')
   bytes.append(0x00)
  print("--|",end='')
  for i in range(0,j-1):
   if use_non: print(ascii[bytes[l+i+1]],end='')
   else:       print(ascii[bytes[l+i+1]],end='')
  for i in range(j,16):
   print(" ",end='')
  print(" |")
 print("|_______|_______________________________________________|________________|\n\\Size: {}/{} Bytes(".format(hex(len(data)),len(data)),end='')
 if len(data) < 1024: print("{} KB)".format(len(data)/1024))
 else: print("{} MB) of {}/{} bytes".format(len(data)/1024/1024,hex(len(data)),len(data)))

#################################

print("TGR Assembler v7.01b")
if len(sys.argv) < 2:
 print("please give an assembly file to compile"); exit(-1)
elif len(sys.argv) < 3:
 print("please give an output file"); exit(-1)
else:
 asm = []
 include(sys.argv[1],0)
 FNout = sys.argv[2]
 out=[]
 labels = []
 address = 0
 preaddr = 0
 devices = ["gpu","input","inp","sound","snd"]
 instructions = ["raw", "set", "get", "mov", "lmov", "add", "inc", "sub", "dec", "mul", "div", "rem", "and", "or", "xor", "bsl", "bsr", "not", "split", "combine", "jmp", "led", "cmpeq", "cmplt", "cmpgt", "rpos", "wram", "rram", "wvram", "rvram", "rsav", "wsav", "rrom", "hlt", "disp", "flags", "dsend", "drecv", "icout", "exec", "rbios", "push", "pop", "call", "ret", "swap", "gclk", "wait", "nop"]
 
 ncs = True
 title = False

 print("first scan checks for %<flags> and data")
 i=-1
 while i < len(asm)-1:
#  print(end="Press [enter]"); input()
  i+=1;  asm[i] = asm[i].replace("\t"," ")
  line = asm[i].split("\n")[0].split(";")[0].split(" ")
  for j in range(len(line)):
   try: line.remove('')
   except ValueError: p=0
  print("[line: "+str(i+1)+"\t| "+str(preaddr)+"/"+hex(preaddr)+"\t]"+asm[i],end='')
  if len(line) < 1: continue
  if   line[0].lower() == "%nochecksum":
   ncs = False
   asm[i] = "\n";
  elif line[0].lower() == "%title":
   title = True
   asm[i] = "\n"
  elif line[0].lower() == "%include":
   print("Including File \""+line[1]+"\"...")
   asm[i] = "\n";
   include(line[1],i)
   i-=1
   #print(asm)
  elif ":" in line[0]:
   line = line[0].split(":")
   if line[0].lower() in devices:
    print("DEVICE",line)
   else:
    labels.append([line[0],preaddr])
    if "{" in line:
     print("ARRAY",[line[0],preaddr],end="\n>> [");j=i
     while j<len(asm):
      if i==j: pline = (asm[j].split("\n")[0].split(";")[0]+" ")[len(line[0])+2]
      else: pline = asm[j].split("\n")[0].split(";")[0]
      for k in pline.split(","):
       if "0x" in k and not "\n" in k: preaddr+=1; print(end = k+", ")
       if "}" in k: i,j=j,len(asm); break
       if k == asm[len(asm[i])]: print("DataError: Data from line "+str(i+1)+" was expecting \"}\" before reaching the end of the program...."); exit(-1)
      j=j+1
     print("]")
    else: print("LABEL",[line[0],preaddr])
  else:
   if line[0] in instructions:
    if line[0] == "lmov": preaddr+=6
    preaddr+=6
 
 if ncs == True:
  out = [0x00,0x54,0x47,0x52]
  address,preaddr = 4, 4
  for i in labels:
   i[1]+=4
 if title == True:
  if len(sys.argv) < 4:
   print("please give an 8 char. ROM name")
   exit()
  sys.argv[3]+=" "*(8-len(sys.argv[3]))
  out[0] = 0x01
  out+=[ord(sys.argv[3][i]) for i in range(8)]
  address+= 8
  preaddr+= 8
  for i in labels:
   i[1]+=8
 
 print("----------------------------------------------------\nsecond scan reads and compiles instructions")
 i,p,j=0,0,0
 while i<len(asm):
#  print("Press [enter]"); input()
  line = asm[i].split("\n")[0].split(";")[0].split(" ")
  for j in range(len(line)):
   try: line.remove('')
   except ValueError: p=p
  if len(line) < 1: print("[line: "+str(i+1)+"\t| "+str(address)+"/"+hex(address)+"\t] *LINE FLAGED AS UN-USABLE BY FIRST SCAN*"); i=i+1; continue
  elif line[0].lower() == "%define":
   if len(line)<3: print("DataError: Data from line "+str(i+1)+" was missing!"); exit(-1)
   labels.append([line[1],check(line[2])])
  
  elif ":" in line[0]:
   print(line)
   line = line[0].split(":")+line[1:]
   if line[0].lower() in devices:
    line=[i.lower() for i in line]; print("PUT DEVICE EXECUTE HERE",line)
    if   line[0] == "gpu":
     if   line[1] == "setx":
      out,address=wram16(line[2],0x97BFE02,out,address)
     elif line[1] == "sety":
      out,address=wram16(line[2],0x97BFE04,out,address)
     
    elif line[0] in ["input","inp"]:
     print("Notice: Device \"INP\" is not implimented yet",line)
    elif line[0] in ["sound","snd"]:
     print("Notice: Device \"SND\" is not implimented yet",line)
    elif line[0] in ["network","net"]:
     print("Notice: Device \"NET\" is not implimented yet",line)
    #
   else:
    if i!=j and j!=0: i=i+1; continue
    if "{" in line:
     print("ARRAY",[line[0],preaddr]);j=i
     while j<len(asm):
      if i==j: pline = (asm[j].split("\n")[0].split(";")[0]+" ")[len(line[0])+2]
      else: pline = asm[j].split("\n")[0].split(";")[0]
      #print("[line: "+str(j+1)+"\t| "+str(address)+"\t]"+asm[j],end='')
      for k in pline.split(","):
#      print(end=str(k));input()
       if k in [" ","","\n"]: continue
       elif "0x" in k: out.append(int(k,16)); address+=1
       else:
        try: out.append(int(k)); address+=1
        except ValueError:
         if str(k)== "}": print("ARRAY Finished at line: "+str(j+1)+"!");
         else: print("Error: \""+str(k)+"\"");
       if "}" in k: i,j,p=j,len(asm),j; break
       if k == asm[len(asm[i])]: print("DataError: Data from line "+str(i+1)+" was expecting \"}\" before reaching the end of the program...."); exit(-1)
      if p==j: p=0; break
      j=j+1
    else: print("LABEL",[line[0],preaddr])
  else:
   if i>p: print("[line: "+str(i+1)+"\t| "+str(address)+"/"+hex(address)+"\t]"+asm[i],end='')
  if 
  if line[0] in instructions:
   if len(line) < 2: args = []
   else: args = line[1].split(",")
   print("found instruction: "+line[0]+" at ["+str(i+1)+"|"+str(address)+"]")
   
   if line[0] == "raw":
    if len(args) != 6: print("ERROR at line "+str(i+1)+": the instruction \"RAW\" requres 6 arguments, got "+str(len(args))); exit(-1)
    j=0
    try:
     while j<7:
      print(j,args[j],args[j][:2] == "0x")
      out+=check(args[j])&0xFF
      j=j+1
    except TypeError:
     print("ERROR at line "+str(i+1)+"[0]: Value at index["+str(j)+"] for \"RAW\" is invalid (got \""+args[j]+"\")"); exit(-1)
   
   if line[0] == "mov":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if "[" in args[1]:
     if "]" in args[1]:
      k = False
      for j in labels:
       if args[1][1:-1] == j[0]: out+=[0x00,ctc(reg(args[0]),0),0x00,0x00,(j[1]&0x000FF00)>> 8,j[1]&0x00000FF]; k = True; break
      if k == False: print("ERROR at line "+str(i+1)+"[1]: Label \""+args[1][1:-1]+"\" was not found or is invalid\n",labels); print("\""+str(args[1][1:-1])+"\"\n\""+str(j[0])+"\""); exit(-1)
     else: print("ERROR at line "+str(i+1)+"[1]: Expected \"]\" near label"); exit(-1)
    else:
     print(reg(args[0]),args[0],"|",reg(args[1]),args[1])
     if reg(args[1]) < 0:
      out+=[0x00,ctc(reg(args[0]),0),0x00,0x00,(check(args[1])&0x000FF00)>> 8,check(args[1])&0x00000FF]
     else:
      out+=[0x1B,ctc(reg(args[0]),reg(args[1])),0x00,0x00,0x00,0x00]
#    else:
#     print("ERROR at line "+str(i+1)+": was expecting REG or Value for IMM but is invalid (got \""+args[1]+"\")"); exit(-1)
   
   if line[0] == "lmov":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0: print("ERROR at line "+str(i+1)+"[1]: REG value for B is invalid (got \""+args[1]+"\")"); exit(-1)
    if "[" in args[2]:
     if "]" in args[2]:
      k = False
      for j in labels:
       if args[2][1:-1] == j[0]:
        out+=[0x00,ctc(reg(args[0]),0),0x00,0x00,(j[1]&0x000FF00)>> 8, j[1]&0x00000FF]
        out+=[0x00,ctc(reg(args[1]),0),0x00,0x00,(j[1]&0x00F0000)>>24,(j[1]&0x0FF0000)>>16]
        k = True; break
      if k == False: print("ERROR at line "+str(i+1)+"[2]: Label \""+args[1][1:-1]+"\" was not found or is invalid\n",labels); print("\""+str(args[1][1:-1])+"\"\n\""+str(j[0])+"\""); exit(-1)
     else: print("ERROR at line "+str(i+1)+"[2]: Expected \"]\" near label"); exit(-1)
    else:
     out+=[0x00,ctc(reg(args[0]),0),0x00,0x00,(check(args[2])&0x000FF00)>> 8, check(args[2])&0x00000FF]
     out+=[0x00,ctc(reg(args[1]),0),0x00,0x00,(check(args[2])&0xF000000)>>24,(check(args[2])&0x0FF0000)>>16]
    address+=6 # takes up 2 instuctions(12 bytes)
   ######
   if line[0] == "add":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0:
     out+=[0x01,ctc(reg(args[0]),0),ctc(reg(args[2]),0),0x00,(check(args[1])&0x0000FF00)>>8,check(args[1])&0x000000FF]
    else:
     out+=[0x01,ctc(reg(args[0]),reg(args[1])),ctc(reg(args[2]),0),0x00,0x00,0x00]
   
   if line[0] == "inc":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    out+=[0x01,ctc(reg(args[0]),0),ctc(reg(args[0]),0),0x00,0x00,0x01]
   
   if line[0] == "sub":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0:
     out+=[0x02,ctc(reg(args[0]),0),ctc(reg(args[2]),0),0x00,(check(args[1])&0x0000FF00)>>8,check(args[1])&0x000000FF]
    else:
     out+=[0x02,ctc(reg(args[0]),reg(args[1])),ctc(reg(args[2]),0),0x00,0x00,0x00]
   
   if line[0] == "dec":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    out+=[0x02,ctc(reg(args[0]),0),ctc(reg(args[0]),0),0x00,0x00,0x01]
   
   if line[0] == "mul":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0:
     out+=[0x03,ctc(reg(args[0]),0),ctc(reg(args[2]),0),0x00,(check(args[1])&0x0000FF00)>>8,check(args[1])&0x000000FF]
    else:
     out+=[0x03,ctc(reg(args[0]),reg(args[1])),ctc(reg(args[2]),0),0x00,0x00,0x00]
   
   if line[0] == "div":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0:
     out+=[0x04,ctc(reg(args[0]),0),ctc(reg(args[2]),0),0x00,(check(args[1])&0x0000FF00)>>8,check(args[1])&0x000000FF]
    else:
     out+=[0x04,ctc(reg(args[0]),reg(args[1])),ctc(reg(args[2]),0),0x00,0x00,0x00]

   if line[0] == "rem":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0:
     out+=[0x05,ctc(reg(args[0]),0),ctc(reg(args[2]),0),0x00,(check(args[1])&0x0000FF00)>>8,check(args[1])&0x000000FF]
    else:
     out+=[0x05,ctc(reg(args[0]),reg(args[1])),ctc(reg(args[2]),0),0x00,0x00,0x00]

   if line[0] == "mod":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0:
     out+=[0x06,ctc(reg(args[0]),0),ctc(reg(args[2]),0),0x00,(check(args[1])&0x0000FF00)>>8,check(args[1])&0x000000FF]
    else:
     out+=[0x06,ctc(reg(args[0]),reg(args[1])),ctc(reg(args[2]),0),0x00,0x00,0x00]
   
   if line[0] == "and" or line[0] == "band":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0:
     out+=[0x07,ctc(reg(args[0]),0),ctc(reg(args[2]),0),0x00,(check(args[1])&0x0000FF00)>>8,check(args[1])&0x000000FF]
    else:
     out+=[0x07,ctc(reg(args[0]),reg(args[1])),ctc(reg(args[2]),0),0x00,0x00,0x00]
   
   if line[0] == "or" or line[0] == "bor":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0:
     out+=[0x08,ctc(reg(args[0]),0),ctc(reg(args[2]),0),0x00,(check(args[1])&0x0000FF00)>>8,check(args[1])&0x000000FF]
    else:
     out+=[0x08,ctc(reg(args[0]),reg(args[1])),ctc(reg(args[2]),0),0x00,0x00,0x00]
   
   if line[0] == "xor" or line[0] == "bxor":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0:
     out+=[0x09,ctc(reg(args[0]),0),ctc(reg(args[2]),0),0x00,(check(args[1])&0x0000FF00)>>8,check(args[1])&0x000000FF]
    else:
     out+=[0x09,ctc(reg(args[0]),reg(args[1])),ctc(reg(args[2]),0),0x00,0x00,0x00]

   if line[0] == "bsl":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[2]) > 0: print("ERROR at line "+str(i+1)+"[2]: Value for IMM is invalid (got \""+args[2]+"\")"); exit(-1)
    out+=[0x0A,ctc(reg(args[0]),0),ctc(reg(args[2]),0),0x00,(check(args[1])&0x0000FF00)>>8,check(args[1])&0x000000FF]
   
   if line[0] == "bsr":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[2]) > 0: print("ERROR at line "+str(i+1)+"[2]: Value for IMM is invalid (got \""+args[2]+"\")"); exit(-1)
    out+=[0x0B,ctc(reg(args[0]),0),ctc(reg(args[2]),0),0x00,(check(args[1])&0x0000FF00)>>8,check(args[1])&0x000000FF]
   
   if line[0] == "not" or line[0] == "bnot":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    out+=[0x0C,ctc(reg(args[0]),0),ctc(reg(args[0]),0),0x00,0x00,0x01]
   
   if line[0] == "split":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0: print("ERROR at line "+str(i+1)+"[1]: REG value for B is invalid (got \""+args[1]+"\")"); exit(-1)
    if reg(args[2]) < 0: print("ERROR at line "+str(i+1)+"[2]: REG value for B is invalid (got \""+args[2]+"\")"); exit(-1)
    if reg(args[3]) > 0: print("ERROR at line "+str(i+1)+"[3]: Value for IMM is invalid (got \""+args[3]+"\")"); exit(-1)
    out+=[0x0D,ctc(reg(args[0]),reg(args[1])),ctc(reg(args[2]),0),0x00,0x00,check(args[3])]
    
   if line[0] == "combine":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0: print("ERROR at line "+str(i+1)+"[1]: REG value for B is invalid (got \""+args[1]+"\")"); exit(-1)
    if reg(args[2]) < 0: print("ERROR at line "+str(i+1)+"[2]: REG value for B is invalid (got \""+args[2]+"\")"); exit(-1)
    if reg(args[3]) > 0: print("ERROR at line "+str(i+1)+"[3]: Value for IMM is invalid (got \""+args[3]+"\")"); exit(-1)
    out+=[0x0E,ctc(reg(args[0]),reg(args[1])),ctc(reg(args[2]),0),0x00,0x00,check(args[3])]
    
   if line[0] == "jmp":
    if "[" in args[0]:
     if "]" in args[0]:
      k = False
      for j in labels:
       if args[0][1:-1] == j[0]: out+=[0x0F,0x00,ctc(1,(j[1]&0xF000000)>>24),(j[1]&0x0FF0000)>>16,(j[1]&0x000FF00)>> 8,j[1]&0x00000FF]; k = True; print(str(j)+" | "+hex(j[1])); print(args[0][1:-1]); break
      if k == False: print("ERROR at line "+str(i+1)+"[0]: Label \""+args[0][1:-1]+"\" was not found or is invalid\n",labels); exit(-1)
     else: print("ERROR at line "+str(i+1)+"[0]: Expected \"]\" near label"); exit(-1)
    else:
     if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A[Address] is invalid (got \""+args[0]+"\")"); exit(-1)
     if reg(args[1]) < 0: print("ERROR at line "+str(i+1)+"[1]: REG value for B[Address] is invalid (got \""+args[1]+"\")"); exit(-1)
     out+=[0x0F,ctc(reg(args[0]),reg(args[1])),0x00,0x00,0x00,0x00]
   
   if line[0] == "led":
    out+=[0x10,ctc(reg(args[0]),0),0x00,0x00,(reg(args[1])   &0x000FF00)>>8,reg(args[1])   &0x00000FF]
    
   if line[0] == "cmpeq":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0:
     out+=[0x11,ctc(reg(args[0]),0),0x10,0x00,(check(args[1])   &0x000FF00)>>8,check(args[1])   &0x00000FF]
    else:
     out+=[0x11,ctc(reg(args[0]),reg(args[1])),0x00,0x00,0x00,0x00]

   if line[0] == "cmplt":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0:
     out+=[0x12,ctc(reg(args[0]),0),0x10,0x00,(check(args[1])&0x000FF00)>>8,check(args[1])&0x00000FF]
    else:
     out+=[0x12,ctc(reg(args[0]),reg(args[1])),0x00,0x00,0x00,0x00]
   
   if line[0] == "cmpgt":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0:
     out+=[0x13,ctc(reg(args[0]),0),0x10,0x00,(check(args[1])&0x000FF00)>>8,check(args[1])&0x00000FF]
    else:
     out+=[0x13,ctc(reg(args[0]),reg(args[1])),0x00,0x00,0x00,0x00]
   
   if line[0] == "rpos": print("ERROR at line "+str(i+1)+"[0]: instuction \"rpos\" is departed!\n\\You must fix this inorder to continue!"); exit(-1)
   
   if line[0] == "wmem":
    if len(args) == 1: print("ERROR at line "+str(i+1)+"[0]: ILLEGAL INSTUCTION \"wmem\" was giving without a Address!!\n\\You must fix this inorder to continue!"); exit(-1)
    if len(args) == 2:
     if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
     if reg(args[1]) >-1: print("ERROR at line "+str(i+1)+"[1]: value for IMM is invalid (got \""+args[1]+"\")"); exit(-1)
     out+=[0x15,ctc(reg(args[0]),0),ctc(1,(check(args[1])&0xF000000)>>24),(check(args[1])&0x0FF0000)>>16,(check(args[1])&0x000FF00)>>8,check(args[1])&0x00000FF]
    elif len(args) == 3:
     if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
     if reg(args[1]) < 0: print("ERROR at line "+str(i+1)+"[1]: REG value for B is invalid (got \""+args[1]+"\")"); exit(-1)
     out+=[0x15,ctc(reg(args[0]),0),0x00,0x00,0x00,0x00]
    else:
     print("ERROR at line "+str(i+1)+": the instruction \"WRAM\" requres 1 or 2 arguments, got "+str(len(args)))
   
   if line[0] == "rmem":
    if len(args) == 1: print("ERROR at line "+str(i+1)+"[0]: ILLEGAL INSTUCTION \"rmem\" was giving without a Address!!\n\\You must fix this inorder to continue!"); exit(-1)
    if len(args) == 2:
     if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
     if reg(args[1]) >-1: print("ERROR at line "+str(i+1)+"[1]: value for IMM is invalid (got \""+args[1]+"\")"); exit(-1)
     out+=[0x14,ctc(reg(args[0]),0),ctc(1,(check(args[1])&0xF000000)>>24),(check(args[1])&0x0FF0000)>>16,(check(args[1])&0x000FF00>>8),check(args[1])&0x00000FF]
    elif len(args) == 1:
     if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
     if reg(args[1]) < 0: print("ERROR at line "+str(i+1)+"[1]: REG value for B is invalid (got \""+args[1]+"\")"); exit(-1)
     if reg(args[2]) < 0: print("ERROR at line "+str(i+1)+"[2]: REG value for C is invalid (got \""+args[2]+"\")"); exit(-1)
     out+=[0x14,ctc(reg(args[0]),reg(args[1])),ctc(reg(args[2]),0),0x00,0x00,0x00]
    else:
     print("ERROR at line "+str(i+1)+": the instruction \"RRAM\" requres 1 or 2 arguments, got "+str(len(args)))
   
   
   if line[0] == "hlt":
    if len(args) > 0:
     if reg(args[0]) >-1: print("ERROR at line "+str(i+1)+"[0]: Value for IMM is invalid (got \""+args[0]+"\")"); exit(-1)
     out+=[0x16,0x00,0x00,0x00,0x00,ctc(0x0,reg(args[0]))]
    else:
     out+=[0x16,0x00,0x00,0x00,0x00,0x01]
   
   if line[0] == "disp":
    if len(args) == 1:
     if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
     out+=[0x17,ctc(reg(args[0]),0),0x00,0x00,0x00,0x00]
    elif len(args) == 2:
     if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
     if reg(args[1]) < 0: print("ERROR at line "+str(i+1)+"[1]: REG value for B is invalid (got \""+args[1]+"\")"); exit(-1)
     out+=[0x17,ctc(reg(args[0]),reg(args[1])),0x00,0x00,0x00,0x01]
    elif len(args) == 3:
     if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
     if reg(args[1]) < 0: print("ERROR at line "+str(i+1)+"[1]: REG value for B is invalid (got \""+args[1]+"\")"); exit(-1)
     if reg(args[2]) < 0: print("ERROR at line "+str(i+1)+"[2]: REG value for C is invalid (got \""+args[2]+"\")"); exit(-1)
     out+=[0x17,ctc(reg(args[0]),reg(args[1])),ctc(reg(args[2]),0x0),0x00,0x00,0x02]
    else:
     print("ERROR at line "+str(i+1)+": the instruction \"DISP\" requres 1 to 3 arguments, got "+str(len(args)))
   
   if line[0] == "flags":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) >-1: print("ERROR at line "+str(i+1)+"[1]: Value for IMM is invalid (got \""+args[0]+"\")"); exit(-1)
    out+=[0x18,0x00,0x00,0x00,0x00,ctc(0x0,reg(args[0]))]
   
   if line[0] == "dsend":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) >-1: print("ERROR at line "+str(i+1)+"[1]: Device Value for IMM is invalid (got \""  +args[1]+"\")"); exit(-1)
    if reg(args[2]) >-1: print("ERROR at line "+str(i+1)+"[2]: Instuction Value for IMM is invalid (got \""  +args[2]+"\")"); exit(-1)
    if args[1] == "GPU":     tmp = 0x00
    if args[1] == "INPUT":   tmp = 0x01
    if args[1] == "SOUND":   tmp = 0x02
    if args[1] == "NETWORK": tmp = 0x03
    else:                    tmp = ctc(0x0,check(args[1]))
    out+=[0x19,ctc(reg(args[0]),0),0x00,0x00,tmp,check(args[2])%0x100]
   
   if line[0] == "drecv":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) >-1: print("ERROR at line "+str(i+1)+"[1]: Value for IMM is invalid (got \""  +args[1]+"\")"); exit(-1)
    if reg(args[2]) >-1: print("ERROR at line "+str(i+1)+"[2]: Value for IMM is invalid (got \""  +args[2]+"\")"); exit(-1)
    if args[1] == "GPU":     tmp = 0x00
    if args[1] == "INPUT":   tmp = 0x01
    if args[1] == "SOUND":   tmp = 0x02
    if args[1] == "NETWORK": tmp = 0x03
    else:                    tmp = ctc(0x0,check(args[1]))
    out+=[0x1A,ctc(reg(args[0]),0),0x00,0x00,tmp,check(args[2])%0x100]
   #0x1B is MOV-REG
   if line[0] == "icout":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if reg(args[1]) < 0: print("ERROR at line "+str(i+1)+"[1]: REG value for B is invalid (got \""+args[1]+"\")"); exit(-1)
    out+=[0x1C,0x00,0x00,0x00,0x00,ctc(0x0,reg(args[0]))]
   
   if line[0] == "page":
    if reg(args[1]):
     if reg(args[0]) >-1: print("ERROR at line "+str(i+1)+"[0]: ROM BANK ID for A is invalid (got \""   +args[1]+"\")"); exit(-1)
     if reg(args[1]) >-1: print("ERROR at line "+str(i+1)+"[1]: REG BANK Index for B is invalid (got \""+args[0]+"\")"); exit(-1)
     out+=[0x1D,ctc(args[0],args[1]),ctc(1,0),0x00,0x00,0x00]
    else:
     if reg(args[0]) >-1: print("ERROR at line "+str(i+1)+"[0]: ROM BANK ID for A is invalid (got \""     +args[1]+"\")"); exit(-1)
     if reg(args[1]) >-1: print("ERROR at line "+str(i+1)+"[1]: ROM Bank Index for IMM is invalid (got \""+args[0]+"\")"); exit(-1)
    out+=[0x1D,ctc(args[0],0),0x00,0x00,0x00,check(args[1])&0x00000FF]
   
   if line[0] == "push":
    if reg(args[0]) >-1: out+=[0x1F,ctc(reg(args[0]),0x00),0x00,0x00,0x00,0x00]
    else:                out+=[0x1F,0x01,ctc(0,(check(args[0])&0xF000000)>>24),(check(args[0])&0x0FF0000)>>16,(check(args[0])&0x000FF00)>>8,check(args[0])&0x00000FF]
   
   if line[0] == "pop":
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    out+=[0x1E,ctc(reg(args[0]),0x0),0x00,0x00,0x00,0x00]
   
   if line[0] == "call":
    if len(args) == 1:
     if "[" in args[0]:
      if "]" in args[0]:
       k = False
       for j in labels:
        if args[0][1:-1] == j[0]: out+=[0x20,0x00,ctc(0,(j[1]&0xF000000)>>24),(j[1]&0x0FF0000)>>16,(j[1]&0x000FF00)>>8,j[1]&0x00000FF]; k = True; print(j); print(args[0][1:-1]); break
       if k == False: print("ERROR at line "+str(i+1)+"[0]: Label \""+args[0][1:-1]+"\" was not found or is invalid\n",labels); exit(-1)
      else: print("ERROR at line "+str(i+1)+"[0]: Expected \"]\" near label"); exit(-1)
     else:
      print("ERROR at line "+str(i+1)+"[0]: Expected [label] (got \""+args[2]+"\")"); exit(-1)
    elif len(args) == 2:
     out+=[0x20,ctc(reg(args[0]),reg(args[1])),0x10,0x00,0x00,0x00]
    else:
      print("ERROR at line "+str(i+1)+": the instruction \"CALL\" requres 1 or 2 arguments, got "+str(len(args)))
   
   if line[0] == "ret":
    out+=[0x21,0x00,0x00,0x00,0x00,0x00]
   
   if line[0] == "swap":
    out+=[0x22,0x00,0x00,0x00,0x00,0x00]
   
   if line[0] == "gclk":
    print(args[0],reg(args[0]))
    print(args[1],reg(args[1]))
    if reg(args[0]) < 0: print("ERROR at line "+str(i+1)+"[0]: REG value for A is invalid (got \""+args[0]+"\")"); exit(-1)
    if args[1] == "1" or args[1] == "reset": out+=[0x22,ctc(reg(args[0]),0x1),0x00,0x00,0x00,0x00]
    else:                                    out+=[0x22,ctc(reg(args[0]),0x0),0x00,0x00,0x00,0x00]
   
   if line[0] == "wait":
    out+=[0x23,0x00,ctc(0x0,(check(args[0])&0xF000000)>>24),(check(args[0])&0x0FF0000)>>16,(check(args[0])&0x000FF00)>>8,check(args[0])&0x00000FF]
    
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   if line[0] == "nop":
    out+=[0xff,0x00,0x00,0x00,0x00,0x00]
    print("What? you want me to do something? NOPe sorry, not today!")
   address+=6
  for o in range(len(out)):
   if out[o] < 0: print(o,[out[o] for o in range(o-6,o)]); #exit(-1)
#  print("[",end='')
#  for i in out[-6:]:
#   if i < 0x10: print("0x0"+hex(i)[2:],end=", ")
#   else:        print("0x" +hex(i)[2:],end=", ")
#  print("]")
  for o in range(len(out)):
   if out[o] < 0 or out[o] > 0xFF: input()
  #
  i+=1
   
print("ASM:{")
for i in range(len(asm)): print(i+1,"\t#",asm[i],end='')
print("}\nLABELS:{")
for i in range(len(labels)): print(" #",labels[i])
print("}\nADDRESS:",address)
print("PREADDR:",preaddr)
dumpData("OUT", out, False, 0, len(out))
