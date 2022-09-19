#!/usr/bin/env python3
import os,sys,time,math,socket;from textwrap import wrap;#from multiprocessing import*;from multiprocessing import shared_memory
Error = 0
try: import pygame
except: os.system("pip3 install pygame"); Error+=1
try: from colorama import *
except: os.system("pip3 install colorama"); Error+=1
if Error > 0: print("Please Restart TGR.py to continue!"); sys.exit()

global Messages,Exit,CPU_SD,MEM_SD,OSsplit, skip_search,PORT,OSsplit,OSexec,PWD,buffer,running,TGRsock,IP #debug,MEM_SD.buf,UInput,Exit,MenuTimer,screen,chars,font,SW,SH,display,RAMUsage,VRAMUsage,Boarder,MEMsizes

clk = pygame.time.Clock()
print("Loading TGR-PRTO v0.0.43b Alpha Build...")
skip_search,PORT,OSsplit,OSexec,PWD = False,1213,"","",os.path.dirname(os.path.realpath(__file__))
buffer,running,TGRsock,IP = bytearray(1024),True,socket.socket(socket.AF_INET, socket.SOCK_STREAM),("127.0.0.1",PORT)
if not TGRsock: print(end=f"\n Socket creation error [THIS SHOULD NOT BE POSSIBLE!!!]\n"); os.exit(-1);

if os.name=="nt": OSsplit,OSexec="\\","exe"
else: OSsplit,OSexec="/","o"

RAMUsage,VRAMUsage,Boarder = 0,0,[128,0,0]
SW,SH,font,display,screen,Messages = 480,360,[],[],[],[]
          #0 1 2 3 4 5 6 7 8 9 A B C D
          #A B C X Y Z L R S s U D L R
UInput = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
#Canvas = [[bytearray(4) for Y in range(720)] for X in range(1280)]
Resolutions = [[480,360,32],[800,600,32],[852,480,32],[1280,720,16]]
MEMsizes = {
 "ROM0":  0x0800000, #  ROMSIZ/BIOSIZ
 "ROM1":  0x0800000,
 "SAV":   0x0800000, #  SAVSIZ
 "WRAM":  0x7fbfe00, #  RAMSIZ
 "STACK": 0x0040000,
 "SRAM":  0x0000200,
 "VRAM":  0x4000000, # VRAMSIZ
 "TOTAL": 0xD800000}
ROMSIZ,RAMSIZ,VRAMSIZ = MEMsizes["ROM0"]+MEMsizes["ROM1"],MEMsizes["WRAM"]+MEMsizes["STACK"]+MEMsizes["SRAM"],MEMsizes["VRAM"]

def hex2(x,l=2,j=False):x=hex(x)[2:][-l:];return("0x"*j)+("0"*(l-len(x)))+x.upper()
def bin2(x,l=8,j=False):x=bin(x)[2:][-l:];return("0b"*j)+("0"*(l-len(x)))+x.upper()

def log(msg,delay=300): global Messages; Messages.append([str(msg),delay]);print(end=str(msg))

## FONT DATA ##
def backChar(Length,X,Y,R,G,B):
 for y in range(8):
  for x in range(Length*8):
   plot(X+x,Y+y,R,G,B)

def getChar(Letter, X, Y, R, G, B, A=0xFF, shadow=True,S=1):
 global chars,font,SW,SH
 # print("Drawing string: "+Letter)
 for i in range(len(Letter)):
  for j in range(len(chars)):
   if (Letter[i] == chars[j]): break
  if j==0: continue
  for ix in range(8):
   for iy in range(8):
    if (font[j][iy][ix] == '1' and ((i*8)+X+ix)*S >= 0 and ((i*8)+X+ix)*S < SW and (Y+iy)*S >= 0 and (Y+iy)*S < SH):
#     PixelAddr = getI((i*8)+X+ix+1,Y+iy+1) ### what was this for again???? ###
     if (shadow == True): plot((i*8)+X+ix+1,Y+iy+1,0,0,0,A,S)
     plot((i*8)+X+ix,Y+iy,R,G,B,A,S)
# `ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-+_=[]{}\|;:'".,<>/?~abcdefghijklmnopqrstuvwxyz
chars = " `ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-+_=[]{}\\|;:'\".,<>/?~abcdefghijklmnopqrstuvwxyz";
font = [
 ["00000000","00000000","00000000","00000000","00000000","00000000","00000000","00000000"], #   00
 ["11111111","11111111","11111111","11111111","11111111","11111111","11111111","11111111"], # `█01
 ["00111100","01000010","01000010","01111110","01000010","01000010","01000010","00000000"], # A 02
 ["01111100","01000010","01000010","01111100","01000010","01000010","01111100","00000000"], # B 03
 ["00111100","01000010","01000000","01000000","01000000","01000010","00111100","00000000"], # C 04
 ["01111100","01000010","01000010","01000010","01000010","01000010","01111100","00000000"], # D 05
 ["01111110","01000000","01000000","01111100","01000000","01000000","01111110","00000000"], # E 06
 ["01111110","01000000","01000000","01111100","01000000","01000000","01000000","00000000"], # F 07
 ["00111100","01000010","01000000","01001110","01000010","01000010","00111100","00000000"], # G 08
 ["01000010","01000010","01000010","01111110","01000010","01000010","01000010","00000000"], # H 09
 ["01111110","00011000","00011000","00011000","00011000","00011000","01111110","00000000"], # I 10
 ["01111110","00000100","00000100","00000100","00000100","01000100","00111000","00000000"], # J 11
 ["01000100","01001000","01010000","01100000","01010000","01001000","01000100","00000000"], # K 12
 ["01000000","01000000","01000000","01000000","01000000","01000000","01111110","00000000"], # L 13
 ["01000010","01100110","01100110","01011010","01011010","01000010","01000010","00000000"], # M 14
 ["01000010","01100010","01010010","01001010","01000110","01000010","01000010","00000000"], # N 15
 ["00111100","01000010","01000010","01000010","01000010","01000010","00111100","00000000"], # O 16
 ["01111100","01000010","01000010","01111100","01000000","01000000","01000000","00000000"], # P 17
 ["00111100","01000010","01000010","01000010","01001010","01000110","00111110","00000000"], # Q 18
 ["01111100","01000010","01000010","01111100","01010000","01001000","01000100","00000000"], # R 19
 ["00111100","01000010","00100000","00011000","00000100","01000010","00111100","00000000"], # S 20
 ["01111110","00011000","00011000","00011000","00011000","00011000","00011000","00000000"], # T 21
 ["01000010","01000010","01000010","01000010","01000010","01000010","00111100","00000000"], # U 22
 ["01000010","01000010","01000010","01000010","00100100","00100100","00011000","00000000"], # V 23
 ["01010100","01010100","01010100","01010100","01010100","01010100","00101000","00000000"], # W 24
 ["01000010","01000010","00100100","00011000","00011000","00100100","01000010","00000000"], # X 25
 ["01000010","01000010","00100100","00011000","00011000","00011000","00011000","00000000"], # Y 26
 ["01111110","00000100","00001000","00010000","00100000","01000000","01111110","00000000"], # Z 27
 ["00111100","01000010","01100010","01011010","01000110","01000010","00111100","00000000"], # 0 28
 ["00001000","00011000","00001000","00001000","00001000","00001000","00001000","00000000"], # 1 29
 ["00111100","01000010","00000100","00001000","00010000","00100000","01111110","00000000"], # 2 30
 ["00111100","01000010","00000010","00001100","00000010","01000010","00111100","00000000"], # 3 31
 ["00000100","00001100","00010100","00100100","01111110","00000100","00000100","00000000"], # 4 32
 ["01111110","01000000","01000000","01111100","00000010","01000010","00111100","00000000"], # 5 33
 ["00111100","01000010","01000000","01111100","01000010","01000010","00111100","00000000"], # 6 34
 ["01111110","00000010","00000100","00000100","00001000","00001000","00010000","00000000"], # 7 35
 ["00111100","01000010","01000010","00111100","01000010","01000010","00111100","00000000"], # 8 36
 ["00111100","01000010","01000010","00111110","00000010","00000010","00111100","00000000"], # 9 37
 ["00001000","00001000","00001000","00001000","00001000","00000000","00001000","00000000"], # ! 38
 ["00111100","01000010","01110010","01101010","01110010","01011100","00111110","00000000"], # @ 39
 ["00000000","00100100","01111110","00100100","00100100","01111110","00100100","00000000"], # # 40
 ["00011000","00111100","01011010","00111000","00011100","01011010","00111100","00011000"], # $ 41
 ["01100001","10010010","10010100","01101000","00010110","00101001","01001001","10000110"], # % 42
 ["00011000","00100100","01000010","00000000","00000000","00000000","00000000","00000000"], # ^ 43
 ["00011000","00100100","00100100","00111010","01000100","01000100","00111010","00000000"], # & 44
 ["00101010","00011100","00111110","00011100","00101010","00000000","00000000","00000000"], # * 45
 ["00001100","00010000","00010000","00010000","00010000","00010000","00001100","00000000"], # ( 46
 ["00110000","00001000","00001000","00001000","00001000","00001000","00110000","00000000"], # ) 47
 ["00000000","00000000","00000000","01111110","01111110","00000000","00000000","00000000"], # - 48
 ["00000000","00011000","00011000","01111110","01111110","00011000","00011000","00000000"], # + 49
 ["00000000","00000000","00000000","00000000","00000000","00000000","00000000","11111111"], # _ 50
 ["00000000","00000000","01111110","00000000","00000000","01111110","00000000","00000000"], # = 51
 ["00011100","00010000","00010000","00010000","00010000","00010000","00011100","00000000"], # [ 52
 ["00111000","00001000","00001000","00001000","00001000","00001000","00111000","00000000"], # ] 53
 ["00011100","00010000","00010000","00100000","00010000","00010000","00011100","00000000"], # { 54
 ["00111000","00001000","00001000","00000100","00001000","00001000","00111000","00000000"], # } 55
 ["10000000","01000000","00100000","00010000","00001000","00000100","00000010","00000001"], # \ 56 /
 ["00011000","00011000","00011000","00011000","00011000","00011000","00011000","00011000"], # | 57
 ["00000000","00000000","00001000","00000000","00000000","00001000","00010000","00000000"], # ; 58
 ["00000000","00000000","00001000","00000000","00000000","00001000","00000000","00000000"], # : 59
 ["00001000","00001000","00000000","00000000","00000000","00000000","00000000","00000000"], # ' 60
 ["00100100","00100100","00000000","00000000","00000000","00000000","00000000","00000000"], # " 61
 ["00000000","00000000","00000000","00000000","00000000","00000000","00001000","00000000"], # . 62
 ["00000000","00000000","00000000","00000000","00000000","00000000","00001000","00010000"], # , 63
 ["00000000","00000110","00011000","01100000","00011000","00000110","00000000","00000000"], # < 64
 ["00000000","01100000","00011000","00000110","00011000","01100000","00000000","00000000"], # > 65
 ["00000001","00000010","00000100","00001000","00010000","00100000","01000000","10000000"], # / 66
 ["00111100","01000010","01000010","00001100","00001000","00000000","00001000","00000000"], # ? 67
 ["00000000","00000000","00000000","00110010","01001100","00000000","00000000","00000000"], # ~ 68
 ["00111100","01000010","01000010","01111110","01000010","01000010","01000010","00000000"], # A 69
 ["01111100","01000010","01000010","01111100","01000010","01000010","01111100","00000000"], # B 70
 ["00111100","01000010","01000000","01000000","01000000","01000010","00111100","00000000"], # C 71
 ["01111100","01000010","01000010","01000010","01000010","01000010","01111100","00000000"], # D 72
 ["01111110","01000000","01000000","01111100","01000000","01000000","01111110","00000000"], # E 73
 ["01111110","01000000","01000000","01111100","01000000","01000000","01000000","00000000"], # F 74
 ["00111100","01000010","01000000","01001110","01000010","01000010","00111100","00000000"], # G 75
 ["01000010","01000010","01000010","01111110","01000010","01000010","01000010","00000000"], # H 76
 ["01111110","00011000","00011000","00011000","00011000","00011000","01111110","00000000"], # I 77
 ["01111110","00000100","00000100","00000100","00000100","01000100","00111000","00000000"], # J 78
 ["01000100","01001000","01010000","01100000","01010000","01001000","01000100","00000000"], # K 79
 ["01000000","01000000","01000000","01000000","01000000","01000000","01111110","00000000"], # L 80
 ["01000010","01100110","01100110","01011010","01011010","01000010","01000010","00000000"], # M 81
 ["01000010","01100010","01010010","01001010","01000110","01000010","01000010","00000000"], # N 82
 ["00111100","01000010","01000010","01000010","01000010","01000010","00111100","00000000"], # O 83
 ["01111100","01000010","01000010","01111100","01000000","01000000","01000000","00000000"], # P 84
 ["00111100","01000010","01000010","01000010","01001010","01000110","00111110","00000000"], # Q 85
 ["01111100","01000010","01000010","01111100","01010000","01001000","01000100","00000000"], # R 86
 ["00111100","01000010","00100000","00011000","00000100","01000010","00111100","00000000"], # S 87
 ["01111110","00011000","00011000","00011000","00011000","00011000","00011000","00000000"], # T 88
 ["00000000","01000010","01000010","01000010","01000010","01000010","00111100","00000000"], # U 89
 ["00000000","01000010","01000010","01000010","00100100","00100100","00011000","00000000"], # V 90
 ["00000000","01010100","01010100","01010100","01010100","01010100","00101000","00000000"], # W 91
 ["00000000","01000010","00100100","00011000","00011000","00100100","01000010","00000000"], # X 92
 ["01000010","01000010","00100100","00011000","00011000","00011000","00011000","00000000"], # Y 93
 ["01111110","00000100","00001000","00010000","00100000","01000000","01111110","00000000"], # Z 94
];

def plot(X,Y,R,G,B,A,S=1):
 global SW,SH,display,screen
 pygame.draw.rect(screen, (R,G,B,A), (X*S,Y*S,S,S))

def fadd(memview,addr,leng,out=0):
 for i in range(addr,addr+leng): out=(out<<8)|memview.buf[i]
 return out

MenuTimer = 0
Exit = -1
tmp=[0,0,0,0,0,0,0,0,0,0]

def ReadMEM(Address,Length=1):
 send(bytes(["rmem",Address,Length]))
def WriteMEM(Address,Data,Length=1,Override=False):
 send(bytes(["wmem",Address,"\x00\x00\x00\x00"+chr(Data),Length,Override]))

def main():
 global Messages,CPU_SD,MEM_SD,SW,SH,UInput,Exit,MenuTimer,screen,display,RAMUsage,VRAMUsage,skip_search,PORT,OSsplit,OSexec,PWD,buffer,running,TGRsock,IP
 print(end=f"\\Initialize Memory...\n");
 ##SEND ARRAY
 #Uinput,   Running+Pause+Debug+Exit, |
 #4,        1 byte (5-bits),          |
 #0,1,2,3,  4                         |
 ##RECV ARRAY
 #IP,  Flags, Running+Pause+Debug+Exit, Error, MEMORY MAP, Display[720p], |
 #8,   1,     1 byte (5-bits),          1024,  0xD800000,  0x2A3000,      |
 #0,3, 7,     8,                        9,     0x409       0xD800409,     0xDAA3409|
# MEM=0xD800000) #Full MemoryMap: 218 MiB
 #MEM_SD.buf = bytearray(0xD800000)
 ROMPG = [bytearray(MEMsizes["ROM0"])*33]
 print(end=f" \\0x{hex2(RAMSIZ,7)}\\{RAMSIZ}\tBytes({RAMSIZ/1024/1024} MB)\tof RAM were allocated...\n");
 print(end=f" \\0x{hex2(VRAMSIZ,7)}\\(VRAMSIZ)\tBytes({VRAMSIZ/1024/1024} MB)\tof VideoRAM was allocated...\n",);
 pygame.init(); pygame.display.set_icon(pygame.image.load(f"bin{OSsplit}TGR_logo.png"))
 pygame.display.set_caption('TheGameRazer - [NO-ROM]');
 display = pygame.display.set_mode((SW+4, SH+4));
 screen = pygame.Surface((SW,SH)).convert();
 ROMPATH,HUDinfo,ShowInput,Frames,FPS,IPS,TIPS,MX,MY,PMX,PMY,MB = "",True,True,0,0,[0,0],0,0,0,0,0,0
 SecTimer=time.time()
# CPU_Error,CPU_Thread = "",Process(target=CPU.Thread, args=(CPU_SD.name,MEM_SD.name,))
 init();i=0
 MEM_SD.buf[i:i+6]=bytes([0x00,0x00,0x00,0x00,0x00,0x01]);i+=6; MEM_SD.buf[i:i+6]=bytes([0x00,0x10,0x00,0x00,0x00,0x00]);i+=6
 while i<8*1024*1024: MEM_SD.buf[i:i+6]=bytes([0x01,0x01,0x00,0x00,0x00,0x00]);i+=6; MEM_SD.buf[i:i+6]=bytes([0x01,0x10,0x10,0x00,0x00,0x00]);i+=6
 MEM_SD.buf[i:i+6]=bytes([0x7F,0x00,0x00,0x00,0x00,0x00])
 #CPU_Thread.start()
 import Settings as config
 CPU_SD.buf[13]=(CPU_SD.buf[13]&0b111110111)|(config.emulation[0]%2*0b000001000);
# CPU_SD.buf[13]=(CPU_SD.buf[13]&0b111011100)|((int(bin2(CPU_SD.buf[13])[5],2)+1)%2*0b000100000);
 if config.emulation[0]: print("Debug Mode: Enabled")
 else: print("Debug Mode: Disabled")
# CPU.Running[0]=True
 sys.argv[0]=''
 if len(sys.argv)>1:
  for i in range(1,len(sys.argv)):
   if (sys.argv[i]=="--slow"         or sys.argv[i]=="-s"   ): i+=1; slowdown = sys.argv[i]
   if (sys.argv[i]=="--debug"        or sys.argv[i]=="-d"   ): CPU.Debug       = True
#   if (sys.argv[i]=="--pauseLoad"    or sys.argv[i]=="-pl"  ): stopatloadrom   = True
   if (sys.argv[i]=="--waitInput"    or sys.argv[i]=="-wi"  ): waitInput       = True
   if (sys.argv[i]=="--skip"         or sys.argv[i]=="-sk"  ): i+=1; skip = sys.argv[i]; skipBIOS = True
   if (sys.argv[i]=="--info"         or sys.argv[i]=="-i"   ): showInfo        = True
   if (sys.argv[i]=="--noUnicode"    or sys.argv[i]=="-nu"  ): noUnicode       = True
#   if (sys.argv[i]=="--noPrint"      or sys.argv[i]=="-np"  ): noPrint         = True
#   if (sys.argv[i]=="--devInfo"      or sys.argv[i]=="-di"  ): devInfo         = True
#   if (sys.argv[i]=="--forceRender"  or sys.argv[i]=="-fr"  ): GPU.forceRender = True
#   if (sys.argv[i]=="--debugBIOS"    or sys.argv[i]=="-db"  ): debugBIOS       = True
   if (sys.argv[i]=="--skipBIOS"     or sys.argv[i]=="-sb"  ): skipBIOS        = True
   if (sys.argv[i]=="--noDump"       or sys.argv[i]=="-nd"  ): noDump          = True
   if (sys.argv[i]=="--hudInfo"      or sys.argv[i]=="-hi"  ): HUDinfo         = True
   if (sys.argv[i]=="--render2x"     or sys.argv[i]=="-2x"  ): zoom            =    1 ## 2x Video
   if (sys.argv[i]=="--scanLines"    or sys.argv[i]=="-sl"  ): zoom            =    2
   if (sys.argv[i]=="--pixelate"     or sys.argv[i]=="-px"  ): zoom            =    3
   if (sys.argv[i]=="--render3x"     or sys.argv[i]=="-3x"  ): zoom            =    4 ## 3x Video
   if (sys.argv[i]=="--scanLines3x"  or sys.argv[i]=="-sl3" ): zoom            =    5
   if (sys.argv[i]=="--pixelate3x"   or sys.argv[i]=="-px3" ): zoom            =    6
   if (sys.argv[i]=="--showInput"    or sys.argv[i]=="-si"  ): ShowInput       = True
#   if (sys.argv[i]=="--extSAV"       or sys.argv[i]=="-sav" ): i+=1; extSAV = sys.argv[i]
  print(sys.argv[-1])
  if sys.argv[-1][0]!="-":
   ROMPATH=sys.argv[-1].split(OSsplit)
 log(f"ROMPATH: {ROMPATH}"+"{PATH NOT PROVIDED}"*(ROMPATH==''))
 inDialog,DialogSelect,DialogPath,DialogFile=-1,0,[],0 #DialogType: -1:None | 0:LoadROM | 1:LoadState | 2:SaveState | 3:DumpMemory | 4:MemoryEditor
 if ROMPATH!="": Messages.append([f"ROM \"{ROMPATH}\" Loaded!",600]); Title_lock = False
 while True:
  msg,Title_lock,TN=0,True,""
  if not Title_lock:
   MEM = ReadMEM(0x0000000,12)
   print(end=f"\n\\ROM Header info:\n \\Type: {MEM[0]}\n  \\System: {chr(MEM[1])+chr(MEM[2])+chr(MEM[3])}\n");
   if MEM[0]==1:
    print(end=f"   \\Title: {chr(MEM[4])+chr(MEM[5])+chr(MEM[6])+chr(MEM[7])+chr(MEM[8])+chr(MEM[9])+chr(MEM[10])+chr(MEM[11])}\n");
    TN="TheGameRazer - "+[chr(MEM[i+4]) for i in range(8)].join() ## Title_Name[i+16] = MEM_SD.buf[i+4]; }
   else:
    TN="TheGameRazer - NO TITLE";
   pygame.display.set_caption(TN); Title_lock = True
 
  SW,SH=display.get_size()
  for event in pygame.event.get():
   if event.type == pygame.QUIT:
    if inDialog!=-1: CPU_SD.buf[13]|=0b100*tmp[0]
    else: tmp[0]=int(bin2(CPU_SD.buf[13])[2],2); CPU_SD.buf[13]|=0b100 #CPU_SD.buf[13]|=0b100*
    Exit+=1; inDialog=-1
   CPU_SD.buf.obj.seek(0);CPU_SD.buf.obj.write(bytes(4))
   for i in range(2):
    for j in range(14):
     if pygame.key.get_pressed()[config.controllers[i][j]]: UInput[i][j]=1; CPU_SD.buf[((i*14)+j)//8]+=(2**((i*14)+j))%0xFF
     else: UInput[i][j]=0
#   print(pygame.key.get_mods())
   if pygame.key.get_mods() in [4160,4224] and pygame.key.get_pressed()[pygame.K_o]:
    if Exit==-1 and inDialog==-1: Exit,tmp[0]=-2,int(bin2(CPU_SD.buf[13])[2],2); print(tmp[0]); CPU_SD.buf[13]|=0b100;inDialog=0;log(f"[EMU] Opening File Menu for ROM\n")
   if pygame.key.get_mods() in [4160,4224] and pygame.key.get_pressed()[pygame.K_r]:
    if Exit==-1 and MenuTimer==0: CPU_SD.buf[13]&=0b11111000;MenuTimer=20;init();log(f"[EMU] Emulation Soft-Reset\n");CPU_SD.buf[13]=(CPU_SD.buf[13]&0b11111000)|0b01000001
   if pygame.key.get_mods() in [4161,4226] and pygame.key.get_pressed()[pygame.K_r]:
    if Exit==-1 and MenuTimer==0: CPU_SD.buf[13]&=0b11111000;MenuTimer=20;MEM_SD.buf.obj.seek(0);MEM_SD.buf.obj.write(bytes(0xD800000));log(f"[EMU] Emulation Hard-Reset\n");CPU_SD.buf[13]=(CPU_SD.buf[13]&0b11111000)|0b01000001
   if pygame.key.get_mods() in [4160,4224] and pygame.key.get_pressed()[pygame.K_d]:
    if Exit==-1 and MenuTimer==0: CPU_SD.buf[13]=(CPU_SD.buf[13]&0b11110111)|((int(bin2(CPU_SD.buf[13])[-4],2)+1)%2*0b1000);MenuTimer=20; log(f"[EMU] Debug Mode: "+("Enabled"*(int(bin2(CPU_SD.buf[13])[-4],2)==True))+("Disabled"*(int(bin2(CPU_SD.buf[13])[-4],2)==False))+"\n")
   if pygame.key.get_mods() in [4160,4224] and pygame.key.get_pressed()[pygame.K_p]:
    if Exit==-1 and MenuTimer==0: CPU_SD.buf[13]=(CPU_SD.buf[13]&0b11111011)|((int(bin2(CPU_SD.buf[13])[-3],2)+1)%2*0b0100);MenuTimer=20; log(f"[EMU] Emulation "+("Paused..."*(int(bin2(CPU_SD.buf[13])[-3],2)==True))+("Resumed..."*(int(bin2(CPU_SD.buf[13])[-3],2)==False))+"\n")
   if pygame.key.get_pressed()[pygame.K_ESCAPE]: CPU.Paused,HUDinfo,MenuTimer=True,not HUDinfo,20
   #elif event.type == MOUSEMOTION: MX,MY = event.pos
   #elif event.type == MOUSEBUTTONDOWN: MB = event.key
#  if Exit==-2 and : Exit=-1; print(tmp[0]); CPU.Pause=tmp[0]
#  print(Exit,inDialog)
  ### RENDERING ###
  screen.fill((16, 16, 16))
  
  
  
  
  
  if Exit == 2: return
  if Exit != -1:
   exitx,exity=(SW/4)-88,(SH/4)-16
   getChar("#####[EMU=PAUSED]#####",exitx,exity,255, 128, 128,  True,  True, 2);exity+=8
   getChar("#       EXIT?        #",exitx,exity,255, 128, 128,  True,  True, 2);exity+=8
   getChar(((Exit==0)*"#  {[NO]}    [YES]   #")+((Exit==1)*"#   [NO]    {[YES]}  #"),exitx,exity,255, 128, 128,  True,  True, 2);exity+=8
   getChar("#Unsaved will be lost#",exitx,exity,255, 128, 128,  True,  True, 2);exity+=8
   getChar("######################",exitx,exity,255, 128, 128,  True,  True, 2);exity+=8
   if (UInput[0][0xC] or UInput[0][0xD]) and not MenuTimer: Exit,MenuTimer = not Exit,20
   if (UInput[0][0x8] or UInput[0][0x0]):
    if Exit == 1: break
    else: CPU_SD.buf[13]|=0b100*tmp[0];Exit =-1
  elif int(bin2(CPU_SD.buf[13])[-3],2):
   pygame.draw.rect(screen, (16,  16, 255, 255), (SW/4-7*8, SH/4-8, SW/4-(7+15)*8, SH/4+16))
#   getChar("+----[EMU]----+", SW/4-7*8, SH/4-8, 128, 128, 255, True,  True,2);
#   getChar("|CPU PAUSED...|", SW/4-7*8, SH/4,   128, 128, 255, True,  True,2);
#   getChar("+-------------+", SW/4-7*8, SH/4+8, 128, 128, 255, True,  True,2);

  if HUDinfo == False:
   getChar(f"FPS: {FPS}\\{IPS[0]+IPS[1]}", 2*8, SH-(4*8), 255, 128, 128,  True,  True);
  else:
   getChar(f"Instruction Pointer: [0x{hex2(fadd(CPU_SD,4,7),7)}, 0x{hex2(fadd(CPU_SD,8,11),7)}]", 2*8, SH-(7*8), 128, 128, 255,  True,  True);
   getChar(f"FPS: {FPS} | IPS: {IPS[0]+IPS[1]}({round((IPS[0]+IPS[1])/2/24000000*100)/100}) | TotalRan: {TIPS}", 2*8, SH-(4*8), 255, 128, 128,  True,  True);
  ##                " RAM Usage: 134217727 bytes/134217727 (100.00% full) | VRAM Usage: 67108863 bytes/67108863 (100.00% full)"
   #getChar(f"RAMPOS: 0x{hex(CPU.RP)[2:]}/{CPU.RP}", 2*8, SH-(7*8), 255, 128, 128,  True,  True);
   #nprintf(TFPS,128, " RAM Usage: %.0lf/%d bytes(%.2lf%% full)", RAMUsage, RAMSIZ+1,( RAMUsage/ RAMSIZ)*100);
   getChar(f" RAM Usage: {RAMUsage}/{RAMSIZ+1} bytes( {(RAMUsage//RAMSIZ)*100}% full)", 1*8, SH-(6*8), 255, 128, 128,  True,  True);
   if (VRAMUsage > 9):
    getChar(f"VRAM Usage:  {VRAMUsage}/{VRAMSIZ+1} bytes( {(VRAMUsage//VRAMSIZ)*100}% full)",1*8, SH-(5*8), 255, 128, 128,  True,  True);
   else:
    getChar(f"VRAM Usage: {VRAMUsage}/ {VRAMSIZ+1} bytes( {(VRAMUsage//VRAMSIZ)*100}% full)",1*8, SH-(5*8), 255, 128, 128,  True,  True);

   if (ShowInput == True):
    getChar("P1:[                                               ]", 2*8, SH-(3*8),  64, 255,  64,  True,  True);
    if UInput[0][ 0]:getChar("A",       6*8, SH-(3*8),  64, 255,  64, 1,True);
    if UInput[0][ 1]:getChar("B",       8*8, SH-(3*8),  64, 255,  64, 1,True);
    if UInput[0][ 2]:getChar("C",      10*8, SH-(3*8),  64, 255,  64, 1,True);
    if UInput[0][ 3]:getChar("X",      12*8, SH-(3*8),  64, 255,  64, 1,True);
    if UInput[0][ 4]:getChar("Y",      14*8, SH-(3*8),  64, 255,  64, 1,True);
    if UInput[0][ 5]:getChar("Z",      16*8, SH-(3*8),  64, 255,  64, 1,True);
    if UInput[0][ 6]:getChar("L",      18*8, SH-(3*8),  64, 255,  64, 1,True);
    if UInput[0][ 7]:getChar("R",      20*8, SH-(3*8),  64, 255,  64, 1,True);
    if UInput[0][ 8]:getChar("START",  22*8, SH-(3*8),  64, 255,  64, 1,True);
    if UInput[0][ 9]:getChar("SELECT", 28*8, SH-(3*8),  64, 255,  64, 1,True);
    if UInput[0][10]:getChar("UP",     35*8, SH-(3*8),  64, 255,  64, 1,True);
    if UInput[0][11]:getChar("DOWN",   38*8, SH-(3*8),  64, 255,  64, 1,True);
    if UInput[0][12]:getChar("LEFT",   43*8, SH-(3*8),  64, 255,  64, 1,True);
    if UInput[0][13]:getChar("RIGHT",  48*8, SH-(3*8),  64, 255,  64, 1,True);
    getChar("P2:[                                               ]", 2*8, SH-(2*8), 255, 165,  0, 1,True);
    if UInput[1][ 0]:getChar("A",       6*8, SH-(2*8), 255, 165,   0, 1,True);
    if UInput[1][ 1]:getChar("B",       8*8, SH-(2*8), 255, 165,   0, 1,True);
    if UInput[1][ 2]:getChar("C",      10*8, SH-(2*8), 255, 165,   0, 1,True);
    if UInput[1][ 3]:getChar("X",      12*8, SH-(2*8), 255, 165,   0, 1,True);
    if UInput[1][ 4]:getChar("Y",      14*8, SH-(2*8), 255, 165,   0, 1,True);
    if UInput[1][ 5]:getChar("Z",      16*8, SH-(2*8), 255, 165,   0, 1,True);
    if UInput[1][ 6]:getChar("L",      18*8, SH-(2*8), 255, 165,   0, 1,True);
    if UInput[1][ 7]:getChar("R",      20*8, SH-(2*8), 255, 165,   0, 1,True);
    if UInput[1][ 8]:getChar("START",  22*8, SH-(2*8), 255, 165,   0, 1,True);
    if UInput[1][ 9]:getChar("SELECT", 28*8, SH-(2*8), 255, 165,   0, 1,True);
    if UInput[1][10]:getChar("UP",     35*8, SH-(2*8), 255, 165,   0, 1,True);
    if UInput[1][11]:getChar("DOWN",   38*8, SH-(2*8), 255, 165,   0, 1,True);
    if UInput[1][12]:getChar("LEFT",   43*8, SH-(2*8), 255, 165,   0, 1,True);
    if UInput[1][13]:getChar("RIGHT",  48*8, SH-(2*8), 255, 165,   0, 1,True);
  CPU_Error=CPU_SD.buf[18:].tobytes().decode().strip("\x00")
  if CPU_Error!="": Messages,CPU_Error=[[i,1200]for i in CPU_Error.split("\n")],""
  while msg<len(Messages): 
   try:
    msgi=wrap(Messages[msg][0],SW//8-2);[Messages.insert(msg+i+1,[msgi[i],Messages[msg][1]])for i in range(len(msgi))];Messages.pop(msg)
    getChar(Messages[msg][0],8, 8+(msg*8), 255, 128, 128,  True,  True); Messages[msg][1]-=1
    if Messages[msg][1]<0: Messages.pop(msg)
   except IndexError: pass
   msg+=1
  if inDialog > -1 and inDialog < 4: #File Dialog
   pygame.draw.rect(screen, (64,  64, 64, 255), (8,8,58*8,(SH//8-8)*8))
   #inDialog=3
   tmp[1]=(inDialog==0)*"[Load ROM]"+(inDialog==1)*"[Load State]"+(inDialog==2)*"[Save State]"+(inDialog==3)*"[Dump Memory]"
   getChar("/"+"-"*round((56-len(tmp[1]))/2)+tmp[1]+"-"*math.floor((56-len(tmp[1]))/2)+"\\", 8, 1*8,  255,  64, 64, 1,True)
   tmp[1]="C:"*(os.name=="nt")+OSsplit.join(DialogPath)+"/"
   getChar("|["+tmp[1]+" "*(54-len(tmp[1]))+"]|", 8, 2*8,  255,  64, 64, 1,True)
   getChar("|"+"-"*(56)+"|", 8, 3*8,  255,  64, 64, 1,True)
   for i in range(4,(SH//8)-10): getChar("|"+" "*(54)+"| |", 8, i*8,  255,  64, 64, 1,True)
   getChar("|"+"-"*(56)+"|", 8, (SH//8-10)*8,  255,  64, 64, 1,True)
   getChar("|"+" "*(12)+"{[___OK___]}         [_CANCEL_] "*(DialogSelect==0)+" [___OK___]         {[_CANCEL_]}"*(DialogSelect==1)+" "*(12)+"|", 8, (SH//8-9)*8,  255,  64, 64, 1,True)
   getChar("\\"+"-"*(56)+"/", 8, (SH//8-8)*8,  255,  64, 64, 1,True)
   getChar("|", (60/2)*8, 0*8,  255,  64, 64, 1,True)
   
   
   
   #
  #
  
  
  display.blit(screen, (2, 2))
  pygame.draw.rect(display, Boarder, (0,0,2,SH))
  pygame.draw.rect(display, Boarder, (0,0,SW,2))
  pygame.draw.rect(display, Boarder, (SW-2,0,SW,SH))
  pygame.draw.rect(display, Boarder, (0,SH-2,SW,SH))
  if SecTimer+1 < time.time(): FPS,Frames,SecTimer,IPS,TIPS,CPU_SD.buf[14:18]=Frames,0,time.time(),[fadd(CPU_SD,14,2),fadd(CPU_SD,16,2)],TIPS+(IPS[0]+IPS[1]),bytes(4)
#  getChar("FPS: "+str(FPS), 10, SH-26, 128, 255, 128, 0xFF, True,1)
  #if (time.time()*1000)%((1/60)*1000):
  pygame.display.update();Frames+=1;MenuTimer-=(MenuTimer>0)*1;clk.tick(60)
##################################################

def send(args): global TGRsock; print(f"Client Send: {args}"); TGRsock.send(args)

#from src.Components import *
try: main()
except KeyboardInterrupt: pass
print("\nShutting down...");CPU_SD.buf[13]=(CPU_SD.buf[13]&0b111011100)|0b000010000;pygame.quit();print(bin2(CPU_SD.buf[13]));CPU_SD.unlink();MEM_SD.unlink()
