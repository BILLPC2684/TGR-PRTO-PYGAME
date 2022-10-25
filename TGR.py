#!/usr/bin/env python3
print("Loading TGR-PRTO v0.0.45b Alpha Build..."); Error = 0
import os,sys,time,math,socket,traceback,logging;from textwrap import wrap;from threading import * #from multiprocessing import*;from multiprocessing import shared_memory
try: import pygame
except: os.system("pip3 install pygame"); Error+=1
try: from colorama import *
except: os.system("pip3 install colorama"); Error+=1
if Error > 0: print("Please Restart TGR.py to continue!"); sys.exit()
SendSilent,Error=False,0
clk = pygame.time.Clock()
skip_search,PORT,OSsplit,OSexec,PWD = False,1213,"","",os.path.dirname(os.path.realpath(__file__))
buffer,running,TGRsock,sockIP = bytearray(1024*9),True,socket.socket(socket.AF_INET, socket.SOCK_STREAM),"127.0.0.1"
if not TGRsock: print(end=f"\n Socket creation error [THIS SHOULD NOT BE POSSIBLE!!!]\n"); os.exit(-1);
TGRsock.settimeout(1)

if os.name=="nt": OSsplit,OSexec="\\","exe"
else: OSsplit,OSexec="/","o"
SystemPath = OSsplit.join(os.path.realpath(__file__).split(OSsplit)[:-1])

RAMUsage,VRAMUsage,Boarder,SelectRez,TargetRez = 0,0,[128,0,0],0,0

Pause,Debug,EasterEgg,Running,CPU_IP,CPU_IPS,CPU_TIPS = False,False,False,[False,False],[0,0],[0,0],[0,0]
SW,SH,font,display,screen,Messages = 480,360,[],[],[],[]
          #0 1 2 3 4 5 6 7 8 9 A B C D
          #A B C X Y Z L R S s U D L R
UInput = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
#Canvas = [[bytearray(4) for Y in range(720)] for X in range(1280)]
Resolutions = [[480,360,32],[800,600,32],[852,480,32],[1280,720,16]]

SIZ8MB,RAMSIZ,VRAMSIZ = 0x0800000,0x7FBFE00,0x4000000

def hex2(x,l=2,j=False):x=hex(x)[2:][-l:];return("0x"*j)+("0"*(l-len(x)))+x.upper()
def bin2(x,l=8,j=False):x=bin(x)[2:][-l:];return("0b"*j)+("0"*(l-len(x)))+x.upper()

def send(args): global TGRsock; print(end=f"Client Send: {args}\n"*(not SendSilent)); input("---[paused after send]---"); return TGRsock.send(args+b";\x00")
def log(msg,delay=300): global Messages; Messages.append([str(msg),delay]);print(end=str(msg))
def ping(DELAY=0.1):
 time.sleep(DELAY)
 TGRsock.send(b"ping")
 while True:
  try:
   if TGRsock.recv(1024) == b"pong": break
  except socket.timeout: pass

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
 ["01000010","01000010","01000010","01000010","01000010","01000010","00111100","00000000"], # U 89
 ["00000000","01000010","01000010","01000010","00100100","00100100","00011000","00000000"], # V 90
 ["01010100","01010100","01010100","01010100","01010100","01010100","00101000","00000000"], # W 91
 ["01000010","01000010","00100100","00011000","00011000","00100100","01000010","00000000"], # X 92
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

################

def ServiceProcess(): pass #os.system(f"{SystemPath}{OSsplit}bin{OSsplit}server.{OSexec} {PORT}")
def ReadMEM(Address,Length=1): send(f"rmem{hex2(Address,7)}{hex2(Length)}".encode())
def WriteMEM(Address,Data,Length=1,Override=False): send(f"wmem{Address.to_bytes(4,'big')}{Length.to_bytes(1,'big')}{int(''.join([hex2(i)for i in Data]),16).to_bytes(Length,'big')}{Override.to_bytes(1,'big')}".encode())

def readFile(Filename):
 try: file=open(Filename,"rb"); return file.read()
 except Exception as e: return [-1,e]
def writeFile(Filename):
 try: file=open(Filename,"wb"); return file.write()
 except Exception as e: return [-1,e]
def uploadROM(RAW_Data):
 [send(b"uplrom"+(i).to_bytes(1,'big')+RAW_Data[i*0x0800000:(i+1)*0x0800000]) for i in range(ceil(RAW_Data/0x0800000))]
 print(end="uploadROM\n"*(not SendSilent))
def uploadBIOS(RAW_Data):
 send(b"uplbios"+RAW_Data[:0x0800000])
 print(end="uploadBIOS\n"*(not SendSilent))
def clearMEM(): send(f"clrmem".encode()); print("clearMEM \n"*(not SendSilent));
def CPU_INIT(): send(f"init\x01".encode());   print(end="CPU_INIT \n"*(not SendSilent));
def CPU_DEBUG(State): global Debug;Debug=State; send(b"debug"+(State*1).to_bytes(1,'big')); print(end=f"CPU_DEBUG {State}\n"*(not SendSilent));
def CPU_PAUSE(State): global Pause;Pause=State; send(b"pause"+(State*1).to_bytes(1,'big')); print(end=f"CPU_PAUSE {State}\n"*(not SendSilent));
def CPU_RUN(ID):  global Running;Running[ID]=True;  send(b"run" +(ID*1).to_bytes(1,'big')); print(end=f"CPU_RUN   {ID}\n"*(not SendSilent));
def CPU_STOP(ID): global Running;Running[ID]=False; send(b"stop"+(ID*1).to_bytes(1,'big')); print(end=f"CPU_STOP  {ID}\n"*(not SendSilent));

def EXIT(silent=False): print(end="IT IS NOW SAFE TO TURN OFF YOUR SYSTEM!!\n"*EasterEgg); (send(f"quit".encode()) if not silent else print(end=''))

def main():
 global TGRsock,sockIP,PORT,SystemPath,OSsplit,OSexec,SW,SH,UInput,Exit,MenuTimer,screen,display,RAMUsage,VRAMUsage,Pause,Debug,Running,CPU_IP,CPU_IPS,CPU_TIPS,EasterEgg,Resolutions,SelectRez,TargetRez
 #while True:
 # try: tmpsock=socket.socket(); tmpsock.bind((sockIP,PORT)); tmpsock.close(); break
 # except OSError: PORT+=1
 print(end=f"\\Initialize Memory...\n");
 ##SEND ARRAY
 #Uinput,   Running+Pause+Debug+Exit, |
 #4,        1 byte (5-bits),          |
 #0,1,2,3,  4                         |
 ##RECV ARRAY
 #IP,  Flags, Running+Pause+Debug+Exit, Error, MEMORY MAP, Display[720p], |
 #8,   1,     1 byte (5-bits),          1024,  0xD800000,  0x2A3000,      |
 #0,3, 7,     8,                        9,     0x409       0xD800409,     0xDAA3409|
 #MEM = bytearray(0xD800000) #Full MemoryMap: 216 MiB
 ROMPG = [bytearray(SIZ8MB)*33]
 print(end=f" \\0x{hex2(RAMSIZ,7)}\\{RAMSIZ}\tBytes({RAMSIZ/1024/1024} MB)\tof RAM were allocated...\n");
 print(end=f" \\0x{hex2(VRAMSIZ,7)}\\{VRAMSIZ}\tBytes({VRAMSIZ/1024/1024} MB)\tof VideoRAM was allocated...\n",);
 pygame.init(); pygame.display.set_icon(pygame.image.load(f"bin{OSsplit}TGR_logo.png"))
 pygame.display.set_caption('TheGameRazer - [NO-ROM]'); print(end=".")
 display = pygame.display.set_mode((Resolutions[SelectRez][0]+2, (Resolutions[SelectRez][1]*3)+2),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,Resolutions[0][2]); print(end=".")
 SW,SH=Resolutions[SelectRez][0],Resolutions[SelectRez][1]
# display = pygame.display.set_mode(HOSTdisplay.current_h, HOSTdisplay.current_w),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,Resolutions[SelectRez][2]); print(end=".")
 screen = pygame.Surface((SW,SH)).convert(); print(end=".\n")
 ROMPATH,HUDinfo,ShowInput,Frames,FPS,IPS,TIPS,MX,MY,PMX,PMY,MB = "",True,False,0,0,[0,0],[0,0],0,0,0,0,0
 SecTimer,SecTimer2=time.time(),time.time()
 
 EMU_Service = Thread(target=ServiceProcess, args=()).start()
 time.sleep(1); TGRsock.connect((sockIP,PORT)); ping();
 CPU_INIT(); init(); ping()
 
 import Settings as config
 CPU_DEBUG(config.emulation[0]); ping()
 if config.emulation[0]: print("Debug Mode: Enabled")
 else: print("Debug Mode: Disbaled")
 CPU_RUN(0); ping(); zoom,ShowInput=(0 if(config.video[0]==1)else(1+((config.video[2]*2)or(config.video[1]*1))if(config.video[0]==2)else(4+((config.video[2]*2)or(config.video[1]*1))if(config.video[0]==3)else print("Error: Zoom Setting is too high!!")==None))),config.video[4]
 fuzz = config.video[3]
 for i in range(len(sys.argv)):
  if (sys.argv[i]=="--slow"         or sys.argv[i]=="-s"   ): i+=1; slowdown = sys.argv[i]
  if (sys.argv[i]=="--debug"        or sys.argv[i]=="-d"   ): CPU_DEBUG(True)
#  if (sys.argv[i]=="--pauseLoad"    or sys.argv[i]=="-pl"  ): stopatloadrom   = True
  if (sys.argv[i]=="--waitInput"    or sys.argv[i]=="-wi"  ): waitInput       = True
  if (sys.argv[i]=="--skip"         or sys.argv[i]=="-sk"  ): i+=1; skip = sys.argv[i]; skipBIOS = True
  if (sys.argv[i]=="--info"         or sys.argv[i]=="-i"   ): showInfo        = True
  if (sys.argv[i]=="--noUnicode"    or sys.argv[i]=="-nu"  ): noUnicode       = True
#  if (sys.argv[i]=="--noPrint"      or sys.argv[i]=="-np"  ): noPrint         = True
#  if (sys.argv[i]=="--devInfo"      or sys.argv[i]=="-di"  ): devInfo         = True
#  if (sys.argv[i]=="--forceRender"  or sys.argv[i]=="-fr"  ): GPU.forceRender = True
#  if (sys.argv[i]=="--debugBIOS"    or sys.argv[i]=="-db"  ): debugBIOS       = True
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
  if (sys.argv[i]=="--fuzz"         or sys.argv[i]=="-px"  ): fuzz            =    True
#  if (sys.argv[i]=="--extSAV"       or sys.argv[i]=="-sav" ): i+=1; extSAV = sys.argv[i]
 print(sys.argv[-1])
 if sys.argv[-1][0]=="-":
  ROMPATH=sys.argv[-1].split(OSsplit)
 print(f"ROMPATH: {ROMPATH}")
 inDialog,DialogButton,DialogScroll,DialogSelect,DialogFile,DialogContents,Messages,EasterEgg=-1,0,0,0,"",[],[],config.EasterEgg #DialogType: -1:None | 0:LoadROM | 1:LoadState | 2:SaveState | 3:DumpMemory | 4:MemoryEditor
 if ROMPATH!="": Messages.append([f"ROM \"{ROMPATH}\" Loaded!",600]); Title_lock = False;
 Messages.append(["Notice: TheGameRazer is Back-In-Action!!\n\nCurrent Build: TGR-PRTO v0.0.45b Alpha\nAgain Please be patent with slow progress,\nReminder of whats new:\n----------------------------------------------------------\n\n* Using New Method for Emulation, Using Pygame as SystemIO\n\\while using C for all emulation work\n* Working on a File Manager for Accessing Files\n* Refining some internal errors in the design\n\n\nJust finished:\n* Finished File Manager\n\n----------------------------------------------------------\nTo-Do List:\n* Finish the C Service\n\\ * Add the CPU Instuctions\n\\ * Setup Sockets for Online Play/Networking\n\\ * Finishing Up Communication between UI and Service\n\n* and last of all, do BUG FIXES!! {SPOOKY...}\n\\... well more AAAAAH!! in the wrong way... pounding your\n \\head agenst the desk kind... WHAT FUN!!\n  \\(not)",100000]);
# SystemPath = "/"
 Title_lock,TN,blitrt,zw,zh,ga,BitDepth=True,"",screen,0,0,0,32
 while True:
  HOSTdisplay = pygame.display.Info()
  try:
   if (~Running[0] and ~Running[1]): LED={0x00,0x00,0x00}
   if (zoom == 0):
    print(zoom,"|",zw,SW,"|",zh,SH)
    if (zw != SW) | (zh != SH):
#     pygame.display.set_mode((),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,BitDepth)
     screen = pygame.Surface((SW,SH)).convert();
     #pygame.display.set_mode((SW+2, SH+2),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,BitDepth)
#     SDL_SetWindowSize(window, SW+2, SH+2);
     zw,zh,ga=SW,SH,1;
   elif (zoom >= 1) & (zoom <= 3):
    print(zoom,"|",zw,SW*2,"|",zh,SH*2)
    if (zw != SW*2) | (zh != SH*2):
     screen = pygame.Surface((SW*2,SH*2)).convert();
#     pygame.display.set_mode(((SW*2)+2, (SH*2)+2),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,BitDepth)
#     SDL_SetWindowSize(window, (SW*2)+2, (SH*2)+2);
     zw,zh,ga=SW*2,SH*2,2;
   elif (zoom >= 4) & (zoom <= 7):
    print(zoom,"|",zw,W*3,"|",zh,SH*3)
    if (zw != SW*3) | (zh != SH*3):
     screen = pygame.Surface((SW*3,SH*3)).convert();
#     pygame.display.set_mode(((SW*3)+2, (SH*3)+2),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,BitDepth)
#     SDL_SetWindowSize(window, (SW*3)+2, (SH*3)+2);
     zw,zh,ga=SW*3,SH*3,3;
   if ROMPATH!=DialogFile:
    readROM();
   if not Title_lock:
    print(end=f"\n\\ROM Header info:\n \\Type: {MEM[0]}\n  \\System: {chr(MEM[1])+chr(MEM[2])+chr(MEM[3])}\n");
    if MEM[0]==1:
     print(end=f"   \\Title: {chr(MEM[4])+chr(MEM[5])+chr(MEM[6])+chr(MEM[7])+chr(MEM[8])+chr(MEM[9])+chr(MEM[10])+chr(MEM[11])}\n");
     TN="TheGameRazer - "+[MEM[i+4] for i in range(8)].join() ## Title_Name[i+16] = MEM[i+4]; }
    else:
     TN="TheGameRazer - NO TITLE";
    pygame.display.set_caption(TN); Title_lock = True
  
   #SW,SH=display.get_size()
   for event in pygame.event.get():
    if event.type == pygame.QUIT:
     if inDialog!=-1: inDialog=-1
     else: Exit+=1; inDialog=-1
    if event.type == pygame.DROPFILE: LoadROM(event.file)
#    if event.type == pygame.VIDEORESIZE and MenuTimer==0:
#    if event.type == pygame.VIDEOEXPOSE and MenuTimer==0:
    UInput=[[(1 if pygame.key.get_pressed()[config.controllers[i][j+1]]else 0)for j in range(14)]for i in range(2)]
#    print(pygame.key.get_mods())
    if Exit==-1 and MenuTimer==0 and inDialog==-1:
     if pygame.key.get_mods() in [4160,4224,64,128] and pygame.key.get_pressed()[pygame.K_o]:
      SecTimer2,inDialog,DialogButton,DialogScroll,DialogSelect=SecTimer2-10,0,0,0,0; print(end=f"[EMU] Opening File Menu for ROM\n")
     if pygame.key.get_mods() in [4160,4224,64,128] and pygame.key.get_pressed()[pygame.K_r]:
      CPU_PAUSE(False);CPU_STOP(0);CPU_STOP(1);MenuTimer=20;init();print(end=f"[EMU] Emulation Soft-Reset\n");Messages.append([f"Emulation Soft-Reset",300]);CPU_RUN(0)
     if pygame.key.get_mods() in [4161,4226,64,128] and pygame.key.get_pressed()[pygame.K_r]:
      CPU_PAUSE(False);CPU_STOP(0);CPU_STOP(1);MenuTimer=20;clearMEM();init();print(end=f"[EMU] Emulation Hard-Reset\n");Messages.append([f"Emulation Hard-Reset",300]);CPU_RUN(0)
     if pygame.key.get_mods() in [4160,4224,64,128] and pygame.key.get_pressed()[pygame.K_d]:
      MenuTimer=20; print(end=f"[EMU] CPU.debug: {Debug}\n"); Messages.append([f"Debug Mode "+("Enabled"*(Debug==True))+("Disbaled"*(Debug==False)),150])
     if pygame.key.get_mods() in [4160,4224,64,128] and pygame.key.get_pressed()[pygame.K_p]:
      CPU_PAUSE(not Pause);MenuTimer=20; print(end=f"[EMU] CPU.pause: {Pause}\n"); Messages.append([f"Emulation "+("Paused..."*(Pause==True))+("Resumed..."*(Pause==False)),150])
     if pygame.key.get_mods() in [4160,4224,64,128] and pygame.key.get_pressed()[pygame.K_i]:
      MenuTimer=20; print(end=f"[EMU] Show UserInput: {Pause}\n"); Messages.append([f"UserInput "+("Shown..."*(Pause==True))+("Hidden..."*(Pause==False)),100])
     if pygame.key.get_pressed()[pygame.K_ESCAPE] and Exit==-1 and MenuTimer==0: HUDinfo,MenuTimer=not HUDinfo,20
    #elif event.type == MOUSEMOTION: MX,MY = event.pos
    #elif event.type == MOUSEBUTTONDOWN: MB = event.key
#   if Exit==-2 and : Exit=-1; print(tmp[0]); CPU_PAUSE(tmp[0])
#   print(Exit,inDialog)
   ### RENDERING ###
   screen.fill((16, 16, 16))
   
   
   if Exit == 2: break
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
     else: Exit=-1
   elif Pause==True:
    getChar("```````````````", SW/4-7*8, SH/4-8,  16,  16, 255, True, False,2);
    getChar("```````````````", SW/4-7*8, SH/4,    16,  16, 255, True, False,2);
    getChar("```````````````", SW/4-7*8, SH/4+8,  16,  16, 255, True, False,2);
    getChar("+----[EMU]----+", SW/4-7*8, SH/4-8, 128, 128, 255, True,  True,2);
    getChar("|CPU PAUSED...|", SW/4-7*8, SH/4,   128, 128, 255, True,  True,2);
    getChar("+-------------+", SW/4-7*8, SH/4+8, 128, 128, 255, True,  True,2);
   
   if HUDinfo == False:
    getChar(f"FPS: {FPS}", 2*8, SH-(4*8), 255, 128, 128,  True,  True);
   else:
    getChar(f"Instruction Pointer: [0x{hex2(CPU_IP[0],7)}, 0x{hex2(CPU_IP[1],7)}]", 2*8, SH-(7*8), 128, 128, 255,  True,  True);
    getChar(f"FPS: {FPS} | IPS: {IPS[0]+IPS[1]}({round((IPS[0]+IPS[1]/24000000)*100)/100}) | TotalRan: {CPU_TIPS[0]+CPU_TIPS[1]}", 2*8, SH-(4*8), 255, 128, 128,  True,  True);
   ##                " RAM Usage: 134217727 bytes/134217727 (100.00% full) | VRAM Usage: 67108863 bytes/67108863 (100.00% full)"
    #getChar(f"RAMPOS: 0x{hex(CPU.RP)[2:]}/{CPU.RP}", 2*8, SH-(7*8), 255, 128, 128,  True,  True);
    #nprintf(TFPS,128, " RAM Usage: %.0lf/%d bytes(%.2lf%% full)", RAMUsage, RAMSIZ+1,( RAMUsage/ RAMSIZ)*100);
    getChar(f" RAM Usage: {RAMUsage}/{RAMSIZ+1} bytes({(RAMUsage/RAMSIZ)*100}) full)", 1*8, SH-(6*8), 255, 128, 128,  True,  True);
    if (VRAMUsage > 9):
     getChar(f"VRAM Usage:  {VRAMUsage}/{VRAMSIZ+1} bytes({(VRAMUsage/VRAMSIZ)*100}) full)",1*8, SH-(5*8), 255, 128, 128,  True,  True);
    else:
     getChar(f"VRAM Usage: {VRAMUsage}/ {VRAMSIZ+1} bytes({(VRAMUsage/VRAMSIZ)*100}) full)",1*8, SH-(5*8), 255, 128, 128,  True,  True);
   
   if (ShowInput == True):
    getChar("P1:[                                               ]", 2*8, SH-(3*8),  64,  64, 255,  True,  True);
    if UInput[0][ 0]:getChar("A",       6*8, SH-(3*8),  64,  64, 255, 1,True);
    if UInput[0][ 1]:getChar("B",       8*8, SH-(3*8),  64,  64, 255, 1,True);
    if UInput[0][ 2]:getChar("C",      10*8, SH-(3*8),  64,  64, 255, 1,True);
    if UInput[0][ 3]:getChar("X",      12*8, SH-(3*8),  64,  64, 255, 1,True);
    if UInput[0][ 4]:getChar("Y",      14*8, SH-(3*8),  64,  64, 255, 1,True);
    if UInput[0][ 5]:getChar("Z",      16*8, SH-(3*8),  64,  64, 255, 1,True);
    if UInput[0][ 6]:getChar("L",      18*8, SH-(3*8),  64,  64, 255, 1,True);
    if UInput[0][ 7]:getChar("R",      20*8, SH-(3*8),  64,  64, 255, 1,True);
    if UInput[0][ 8]:getChar("START",  22*8, SH-(3*8),  64,  64, 255, 1,True);
    if UInput[0][ 9]:getChar("SELECT", 28*8, SH-(3*8),  64,  64, 255, 1,True);
    if UInput[0][10]:getChar("UP",     35*8, SH-(3*8),  64,  64, 255, 1,True);
    if UInput[0][11]:getChar("DOWN",   38*8, SH-(3*8),  64,  64, 255, 1,True);
    if UInput[0][12]:getChar("LEFT",   43*8, SH-(3*8),  64,  64, 255, 1,True);
    if UInput[0][13]:getChar("RIGHT",  48*8, SH-(3*8),  64,  64, 255, 1,True);
    getChar("P2:[                                               ]", 2*8, SH-(2*8),  64,  64, 255, 1,True);
    if UInput[1][ 0]:getChar("A",       6*8, SH-(2*8),  64,  64, 255, 1,True);
    if UInput[1][ 1]:getChar("B",       8*8, SH-(2*8),  64,  64, 255, 1,True);
    if UInput[1][ 2]:getChar("C",      10*8, SH-(2*8),  64,  64, 255, 1,True);
    if UInput[1][ 3]:getChar("X",      12*8, SH-(2*8),  64,  64, 255, 1,True);
    if UInput[1][ 4]:getChar("Y",      14*8, SH-(2*8),  64,  64, 255, 1,True);
    if UInput[1][ 5]:getChar("Z",      16*8, SH-(2*8),  64,  64, 255, 1,True);
    if UInput[1][ 6]:getChar("L",      18*8, SH-(2*8),  64,  64, 255, 1,True);
    if UInput[1][ 7]:getChar("R",      20*8, SH-(2*8),  64,  64, 255, 1,True);
    if UInput[1][ 8]:getChar("START",  22*8, SH-(2*8),  64,  64, 255, 1,True);
    if UInput[1][ 9]:getChar("SELECT", 28*8, SH-(2*8),  64,  64, 255, 1,True);
    if UInput[1][10]:getChar("UP",     35*8, SH-(2*8),  64,  64, 255, 1,True);
    if UInput[1][11]:getChar("DOWN",   38*8, SH-(2*8),  64,  64, 255, 1,True);
    if UInput[1][12]:getChar("LEFT",   43*8, SH-(2*8),  64,  64, 255, 1,True);
    if UInput[1][13]:getChar("RIGHT",  48*8, SH-(2*8),  64,  64, 255, 1,True);
   [[[Messages.append([msg,Messages[msgi][1]])for msg in(Messages[msgi][0].split("\n"))], Messages.pop(msgi)]for msgi in range(len(Messages))if"\n"in Messages[msgi][0]]
   for msg in range(len(Messages)):
    try:
     getChar(Messages[msg][0],8, 8+(msg*8), 255, 128, 128,  True,  True); Messages[msg][1]-=1
     if Messages[msg][1]<0: Messages.pop(msg)
    except IndexError: pass
   if inDialog > -1 and inDialog < 4: #File Dialog
    if SystemPath=="": SystemPath=("C:\\"if(os.name=="nt")else"/")
    pygame.draw.rect(screen, (64,  64,  64, 255), (8,8,58*8,(SH//8-8)*8))
    try:
     if SecTimer2+10 < time.time():SecTimer2=time.time();DialogContents=[[i.encode('ascii', 'ignore').decode()[:(SW//8)-15],-1] for i in [".."]+sorted(os.listdir(SystemPath)) if not os.path.isfile(SystemPath+OSsplit+i)]+[[i.encode('ascii', 'ignore').decode()[:(SW//8)-15],[round(os.path.getsize(SystemPath+OSsplit+i)/1024/1024/1024/1024/1024/1024/1024),"YiB"]if os.path.getsize(SystemPath+OSsplit+i)+1>1024*1024*1024*1024*1024*1024*1024 else[round(os.path.getsize(SystemPath+OSsplit+i)/1024/1024/1024/1024/1024/1024),"ZiB"]if os.path.getsize(SystemPath+OSsplit+i)+1>1024*1024*1024*1024*1024*1024 else[round(os.path.getsize(SystemPath+OSsplit+i)/1024/1024/1024/1024/1024),"EiB"]if os.path.getsize(SystemPath+OSsplit+i)+1>1024*1024*1024*1024*1024 else[round(os.path.getsize(SystemPath+OSsplit+i)/1024/1024/1024/1024),"PiB"]if os.path.getsize(SystemPath+OSsplit+i)+1>1024*1024*1024*1024 else[round(os.path.getsize(SystemPath+OSsplit+i)/1024/1024/1024),"GiB"]if os.path.getsize(SystemPath+OSsplit+i)+1>1024*1024*1024 else[round(os.path.getsize(SystemPath+OSsplit+i)/1024/1024),"MiB"]if os.path.getsize(SystemPath+OSsplit+i)+1>1024*1024 else[round(os.path.getsize(SystemPath+OSsplit+i)/1024),"KiB"]if os.path.getsize(SystemPath+OSsplit+i)+1>1024 else[os.path.getsize(SystemPath+OSsplit+i),"BYT"]] for i in [".."]+sorted(os.listdir(SystemPath)) if os.path.isfile(SystemPath+OSsplit+i)];
    except FileNotFoundError: print(f"FS Error: Cannot open \"{SystemPath}\""); SystemPath=OSsplit.join(SystemPath.split(OSsplit)[:-1]);
    except PermissionError:   print(f"FS Error: Cannot open \"{SystemPath}\""); SystemPath=OSsplit.join(SystemPath.split(OSsplit)[:-1]);
    tmp[1]=(inDialog==0)*"[Load ROM]"+(inDialog==1)*"[Load State]"+(inDialog==2)*"[Save State]"+(inDialog==3)*"[Dump Memory]"
    getChar("/"+"-"*round((56-len(tmp[1]))/2)+" "*len(tmp[1])+"-"*math.floor((56-len(tmp[1]))/2)+"\\", 8, 1*8, 255,  64,  64, 1,True)
    getChar(tmp[1],(round((56-len(tmp[1]))/2)+2)*8, 1*8, 255,  64, 255, 1,True)
    getChar("|[",    8, 2*8, 255,  64,  64, 1,True)
    getChar((SystemPath[-53:]if SystemPath.split(OSsplit)[1]=='' else SystemPath[-53:]+"/"),3*8, 2*8, 255, 255,  64, 1,True)
    getChar("]|", 57*8, 2*8, 255,  64,  64, 1,True)
    getChar("|"+"-"*(56)+"|", 8, 3*8, 255,  64,  64, 1,True);j=0;
    pygame.draw.rect(screen, (255,  95,  31, 255), (16,(DialogSelect+4)*8,54*8,8))
    for i in range(4,35): getChar("|",  1*8,i*8, 255,  64,  64, 1, True); getChar("|", 47*8,i*8, 255,  64,  64, 1, True); getChar(f"|{DialogScroll+j}",56*8, i*8, 255,  64,  64, 1, True); ((([getChar(DialogContents[DialogScroll+j][0], 2*8,i*8, 255, 255,  64, 1, True),getChar("PARENT", 49*8,i*8, 255, 255,  64, 1, True)]if DialogContents[DialogScroll+j][0]==".."else[getChar(DialogContents[DialogScroll+j][0], 2*8,i*8, 128, 128, 255, 1, True),getChar("FOLDER", 49*8,i*8, 128, 128, 255, 1, True)])if DialogContents[DialogScroll+j][1]==-1 else[getChar(DialogContents[DialogScroll+j][0],  2*8,i*8,  64, 255,  64, 1, True),getChar(str(DialogContents[DialogScroll+j][1][0]), (52-len(str(DialogContents[DialogScroll+j][1][0])))*8,i*8,  64, 255,  64, 1, True),getChar(DialogContents[DialogScroll+j][1][1],  53*8,i*8,  64, 255,  64, 1, True)])if DialogScroll+j<len(DialogContents)else""); j+=1
    getChar("|"+"-"*(56)+"|", 8, (SH//8-10)*8, 255,  64,  64, 1,True)
    getChar(f"|{DialogContents[DialogScroll+DialogSelect][0]}={DialogScroll+DialogSelect}"if(DialogScroll+DialogSelect<len(DialogContents))else"|", 8, (SH//8-9)*8, 255,  64,  64, 1,True)
    getChar("{[___OK___]}"*(DialogButton==0)+" [___OK___] "*(DialogButton==1), 12*8, (SH//8-9)*8, 255,  64,  64, 1,True)
    getChar(" [_CANCEL_] "*(DialogButton==0)+"{[_CANCEL_]}"*(DialogButton==1), 32*8, (SH//8-9)*8, 255,  64,  64, 1,True)
    getChar("|", 58*8, (SH//8-9)*8, 255,  64,  64, 1,True)
    getChar("\\"+"-"*(56)+"/", 8, (SH//8-8)*8, 255,  64,  64, 1,True)
    getChar("|", (60/2)*8, 0*8, 255,  64,  64, 1,True)
    
    if DialogScroll+DialogSelect >= len(DialogContents) and not MenuTimer: DialogScroll,DialogSelect,MenuTimer = (DialogScroll-1 if (DialogScroll>0 and DialogSelect==0) else DialogScroll),(DialogSelect-1 if DialogSelect>0 else DialogSelect),1
    if (UInput[0][0xC] or UInput[0][0xD]) and not MenuTimer: DialogButton,MenuTimer = not DialogButton,20
    if UInput[0][0xA] and not MenuTimer:
     DialogScroll,DialogSelect,MenuTimer = (DialogScroll-1 if (DialogScroll>0 and DialogSelect==0) else DialogScroll),(DialogSelect-1 if DialogSelect>0 else DialogSelect), 2
    if UInput[0][0xB] and not MenuTimer:
     DialogScroll,DialogSelect,MenuTimer = (DialogScroll+1 if (DialogScroll<len(DialogContents) and DialogSelect==30) else DialogScroll),(DialogSelect+1 if (DialogSelect<30 and DialogScroll+DialogSelect<len(DialogContents)-1) else DialogSelect),2
    if (UInput[0][0x8] or UInput[0][0x0]) and not MenuTimer:
     MenuTimer = 10
     if DialogButton == 1: inDialog = -1
     else:
      if DialogContents[DialogScroll+DialogSelect][1]==-1:
       SystemPath,SecTimer2=((OSsplit.join(SystemPath.split(OSsplit)[:-1])if len(SystemPath.split(OSsplit))>1 else SystemPath)if DialogContents[DialogScroll+DialogSelect][0]==".."else os.path.realpath(SystemPath+OSsplit+DialogContents[DialogScroll+DialogSelect][0])),SecTimer2-10
      else: DialogFile = DialogContents[DialogScroll+DialogSelect][0]; inDialog = -1; ROMPATH=DialogFile; Messages.append([f"File Selected: \"{DialogFile}\"",500])
    #
   #
   
   display.blit(blitrt, (2, 2))
   pygame.draw.rect(display, Boarder, (0,0,2,HOSTdisplay.current_h))
   pygame.draw.rect(display, Boarder, (0,0,HOSTdisplay.current_w,2))
   pygame.draw.rect(display, Boarder, (HOSTdisplay.current_w-2,0,SW,HOSTdisplay.current_h))
   pygame.draw.rect(display, Boarder, (0,HOSTdisplay.current_h-2,SW,HOSTdisplay.current_h))
   if SecTimer+1 < time.time():TIPS=CPU_TIPS;FPS=Frames;Frames=0;SecTimer=time.time();IPS=CPU_IPS;CPU_IPS=[0,0]
#   getChar("FPS: "+str(FPS), 10, SH-26, 128, 255, 128, 0xFF, True,1)
   #if (time.time()*1000)%((1/60)*1000):
   pygame.display.update();Frames+=1;MenuTimer-=(MenuTimer>0)*1;clk.tick(60)
   if inDialog == -1 and Exit==-1: send(b"tick"+b''.join([int("".join(str(i)for i in UInput[j]),2).to_bytes(2,"little") for j in range(2)])+((Running[0])+(Running[1]<<1)+(Pause<<2)+(Debug<<3)).to_bytes(1,"little"))
   else: send(b"tick\x00\x00\x00\x00"+ ((Running[0])+(Running[1]<<1)+(Pause<<2)+(Debug<<3)).to_bytes(1,"little"))
   buffer = TGRsock.recv(1024)
   if buffer!='':
    print(f"Client GOT: {buffer}")
    if buffer.startswith("rezch"):
     SelectRez = int(buffer[5]); display = pygame.display.set_mode(((Resolutions[SelectRez][0]*3)+2, (Resolutions[SelectRez][1]*3)+2),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,Resolutions[SelectRez][2])
     SW,SH=Resolutions[SelectRez][0],Resolutions[SelectRez][1]
    if buffer.startswith("quit"): print("EXIT"); raise KeyboardInterrupt
 #Uinput,   Running+Pause+Debug, |
 #4,        1 byte (4-bits),     |
 #0,1,      2                    |

  except BrokenPipeError: print("ERROR: Lost Connection to Service!!"); break
  except socket.error: print(end="\n[EMU] We have detected the main loop has stopped responding...\n\nThis halt is most likely due to a Emulation Error.\nIf there is a Error, check above for what the problem is. [If it's the ROM make sure Debug Mode is Active]\n/!\\Reminder: check the ROM before reporting EMU probblems/!\\\n"); break
 send(f"quit".encode());
##################################################

#CPU_DEBUG

#from src.Components import *
try: main()
except KeyboardInterrupt: Error=0
except BrokenPipeError: pass
except Exception as e: print(end="\n/!\\ FATAL ERROR!! /!\\\n"); logging.error(traceback.format_exc()); print(end="[EMU] /!\\ A FATAL ERROR HAS OCCORED!!! /!\\\nOh boy, we seem to have detected a Fatal issue with the main loop ( Reason can be seen above ^^ )\n\\and all Emulation has been Halted, and Eny UNSAVED DATA will be LOST.\n\nIf this is not the first time you've recived this message for this error:\n\\Please Contact US via Support Ticket in the TGR Forums: https://koranva-forest.com/forums/TGR\n \\Or Contact US via Discord: https://discord.gg/PWAf8ek\n"); Error+=1;
print("\nShutting down...");
if EasterEgg:
 pygame.draw.rect(screen, (  0,   0,   0, 255), (0,0,SW,SH)); SecTimer=time.time();
 while SecTimer+2>time.time(): display.blit(screen, (2, 2)); pygame.draw.rect(display, (0,0,0,255), (0,0,2,SH)); pygame.draw.rect(display, (0,0,0,255), (0,0,SW,2)); pygame.draw.rect(display, (0,0,0,255), (SW-2,0,SW,SH)); pygame.draw.rect(display, (0,0,0,255), (0,SH-2,SW,SH)); pygame.display.update(); clk.tick(60)
 getChar("IT IS NOW SAFE TO TURN", SW/4-11*8, SH/4-8, 0xED, 0x7B, 0x34, True,  True,2);getChar("  OFF YOUR COMPUTER!  ", SW/4-11*8, SH/4,   0xED, 0x7B, 0x34, True,  True,2);SecTimer=time.time()
 while SecTimer+10>time.time(): display.blit(screen, (2, 2)); pygame.draw.rect(display, (0,0,0,255), (0,0,2,SH)); pygame.draw.rect(display, (0,0,0,255), (0,0,SW,2)); pygame.draw.rect(display, (0,0,0,255), (SW-2,0,SW,SH)); pygame.draw.rect(display, (0,0,0,255), (0,SH-2,SW,SH)); pygame.display.update(); clk.tick(60)
EXIT(1*(Error==0)); pygame.quit()
