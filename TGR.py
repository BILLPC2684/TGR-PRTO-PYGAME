#!/usr/bin/env python3
#####################################################################################
# THE GAME RAZER © 2022 BILLPC2684 ## https://github.com/BILLPC2684/TGR-PRTO-PYGAME #
#   Main Interface(Client) File    ##################################################
#####################################################################################
####################################
__version__ = "v0.0.46c"
print(f"Loading TGR-PRTO {__version__} Alpha Build..."); Error = 0
import os,sys,time,math,socket,traceback,logging;from textwrap import wrap;from threading import * #from multiprocessing import*;from multiprocessing import shared_memory
try:
 import pygame
 if pygame.version.ver < '2.1.3': raise ImportError;
except: os.system("pip3 install pygame>=2.1.3 --upgrade --pre"); Error+=1
try: from colorama import *
except: os.system("pip3 install colorama"); Error+=1
if Error > 0: print("Please Restart TGR.py to continue!"); sys.exit()
SendSilent,Error=False,0
clk = pygame.time.Clock()
skip_search,PORT,OSsplit,OSexec,PWD = False,1213,"","",os.path.dirname(os.path.realpath(__file__))
buffer,running,TGRsock,sockIP = bytearray(1024*9),True,socket.socket(socket.AF_INET, socket.SOCK_STREAM),"127.0.0.1"
if not TGRsock: print(end=f"\n Socket creation error [THIS SHOULD NOT BE POSSIBLE!!!]\n"); os.exit(-1);
TGRsock.settimeout(0.0001)

IGNORESERVER = True

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
Resolutions = [[480,360,32],[800,600,32],[852,480,32],[1280,720,24]]

SIZ8MB,RAMSIZ,VRAMSIZ = 0x0800000,0x7FBFE00,0x4000000

def hex2(x,l=2,j=False):x=hex(x)[2:][-l:];return("0x"*j)+("0"*(l-len(x)))+x.upper()
def bin2(x,l=8,j=False):x=bin(x)[2:][-l:];return("0b"*j)+("0"*(l-len(x)))+x.upper()

def send(args):
 if IGNORESERVER == True: return -1
 global TGRsock; print(end=f"Client Send: {args}\n"*(not SendSilent));
 try: return TGRsock.send(args+b";\x00"); input("---[paused after send]---");
 except BrokenPipeError: print("ERROR: Lost Connection to Service!!"); return -1
def log(msg,delay=300): global Messages; Messages.append([str(msg),delay]);print(end=str(msg))
def ping(DELAY=0.1):
 time.sleep(DELAY)
 if IGNORESERVER == False:
  TGRsock.send(b"ping")
  while True:
   try:
    if TGRsock.recv(1024) == b"pong": break
   except socket.timeout: pass
   except BrokenPipeError: print("ERROR: Lost Connection to Service!!"); return -1
## FONT DATA ##
def backChar(X,Y,W,H,R,G,B,A=0xFF,shadow=False,S=1):
 for h in range(H): getChar("`"*W, X, Y+(h*8*S), R, G, B, A,shadow,S)

def getChar(Letter, X, Y, R, G, B, A=0xFF, shadow=True,S=1):
 global chars,font,SW,SH
 # print("Drawing string: "+Letter)
 for i in range(len(Letter)):
  for j in range(len(chars)):
   if (Letter[i] == chars[j]): break
  if j==0: continue
  for k in range(shadow*1+1):
   surf = pygame.transform.scale(font[j], (8*S,8*S))
   with pygame.PixelArray(surf) as char: char.replace((0xFF,0xFF,0xFF),(R if k else 0,G if k else 0,B if k else 0))
   surf.set_alpha(A) #adding back alpha
   screen.blit(surf, ((i*(8*S))+X+(1-k), Y+(1-k)))
  
#  copy = pygame.Surface((8*S,8*S))
#  char = pygame.transform.scale(font[j], (8*S,8*S))
#  if (shadow == True):
#   copy.fill((0, 0, 0, 0xFF))
#   char.blit(copy, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
#   char.set_alpha(0xFF-A)
#   screen.blit(char, ((i*(8*S))+X+1, (8*S)+Y-7))
#   copy = pygame.Surface((8*S,8*S))
#   char = pygame.transform.scale(font[j], (8*S,8*S))
#  copy.fill((R, G, B, 0xFF))
#  char.blit(copy, (0,0), special_flags=pygame.BLEND_RGB_MULT)
#  char.set_alpha(0xFF-A)
#  screen.blit(char, ((i*(8*S))+X, (8*S)+Y-8))

def compile_font():
 for i in range(len(fontraw)):
  char=b''
  for iy in range(8):
   for ix in range(8):
    if fontraw[i][iy][ix] == '1': char+=b'\xFF'*4
    else: char+=b'\x00'*4
  font.append(pygame.image.frombytes(char,(8,8),"RGBA"))
  #
 #

# `ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-+_=[]{}\|;:'".,<>/?~abcdefghijklmnopqrstuvwxyz─│═║┌┬┐╔╦╗╓╥╖╒╤╕├┼┤╠╬╣╟╫╢╞╪╡└┴┘╚╩╝╙╨╜╘╧╛
chars = " `ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-+_=[]{}\\|;:'\".,<>/?~abcdefghijklmnopqrstuvwxyz─│═║┌┬┐╔╦╗╓╥╖╒╤╕├┼┤╠╬╣╟╫╢╞╪╡└┴┘╚╩╝╙╨╜╘╧╛";
font = []
fontraw = [
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
 ["00000000","00000000","00000000","00000000","11111111","00000000","00000000","00000000"], # ─ 95
 ["00001000","00001000","00001000","00001000","00001000","00001000","00001000","00001000"], # │ 96
 ["00000000","00000000","00000000","11111111","11111111","00000000","00000000","00000000"], # ═ 97
 ["00011000","00011000","00011000","00011000","00011000","00011000","00011000","00011000"], # ║ 98
 ["00000000","00000000","00000000","00000000","00000111","00001100","00001000","00001000"], # ┌ 99
 ["00000000","00000000","00000000","00000000","11111111","00011100","00001000","00001000"], # ┬ 100
 ["00000000","00000000","00000000","00000000","11110000","00011000","00001000","00001000"], # ┐ 101
 ["00000000","00000000","00000000","00001111","00011111","00011100","00011000","00011000"], # ╔ 102
 ["00000000","00000000","00000000","11111111","11111111","00111100","00011000","00011000"], # ╦ 103
 ["00000000","00000000","00000000","11110000","11111000","00111000","00011000","00011000"], # ╗ 104
 ["00000000","00000000","00000000","00000000","00001111","00011100","00011000","00011000"], # ╓ 105
 ["00000000","00000000","00000000","00000000","11111111","00111100","00011000","00011000"], # ╥ 106
 ["00000000","00000000","00000000","00000000","11110000","00111000","00011000","00011000"], # ╖ 107
 ["00000000","00000000","00000000","00000111","00001111","00001100","00001000","00001000"], # ╒ 108
 ["00000000","00000000","00000000","11111111","11111111","00011100","00001000","00001000"], # ╤ 109
 ["00000000","00000000","00000000","11110000","11111000","00011000","00001000","00001000"], # ╕ 110
 ["00001000","00001000","00001000","00001100","00001111","00001100","00001000","00001000"], # ├ 111
 ["00001000","00001000","00001000","00011100","11111111","00011100","00001000","00001000"], # ┼ 112
 ["00001000","00001000","00001000","00011000","11111000","00011000","00001000","00001000"], # ┤ 113
 ["00011000","00011000","00011100","00011111","00011111","00011100","00011000","00011000"], # ╠ 114
 ["00011000","00011000","00111100","11111111","11111111","00111100","00011000","00011000"], # ╬ 115
 ["00011000","00011000","00111000","11111000","11111000","00111000","00011000","00011000"], # ╣ 116
 ["00011000","00011000","00011000","00011100","00011111","00011100","00011000","00011000"], # ╟ 117
 ["00011000","00011000","00011000","00111100","11111111","00111100","00011000","00011000"], # ╫ 118
 ["00011000","00011000","00011000","00111000","11111000","00111000","00011000","00011000"], # ╢ 119
 ["00001000","00001000","00001100","00001111","00001111","00001100","00001000","00001000"], # ╞ 120
 ["00001000","00001000","00011100","11111111","11111111","00011100","00001000","00001000"], # ╪ 121
 ["00001000","00001000","00011000","11111000","11111000","00011000","00001000","00001000"], # ╡ 122
 ["00001000","00001000","00001000","00001100","00000111","00000000","00000000","00000000"], # └ 123
 ["00001000","00001000","00001000","00011100","11111111","00000000","00000000","00000000"], # ┴ 124
 ["00001000","00001000","00001000","00011000","11110000","00000000","00000000","00000000"], # ┘ 125
 ["00011000","00011000","00011100","00011111","00001111","00000000","00000000","00000000"], # ╚ 126
 ["00011000","00011000","00111100","11111111","11111111","00000000","00000000","00000000"], # ╩ 127
 ["00011000","00011000","00111000","11111000","11110000","00000000","00000000","00000000"], # ╝ 128
 ["00011000","00011000","00011000","00011100","00001111","00000000","00000000","00000000"], # ╙ 129
 ["00011000","00011000","00011000","00111100","11111111","00000000","00000000","00000000"], # ╨ 130
 ["00011000","00011000","00011000","00111000","11110000","00000000","00000000","00000000"], # ╜ 131
 ["00001000","00001000","00001100","00001111","00000111","00000000","00000000","00000000"], # ╘ 132
 ["00001000","00001000","00011100","11111111","11111111","00000000","00000000","00000000"], # ╧ 133
 ["00001000","00001000","00011000","11111000","11110000","00000000","00000000","00000000"], # ╛ 134
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

def ServiceProcess(): os.system(f"{SystemPath}{OSsplit}bin{OSsplit}server.{OSexec} {PORT}")
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
def GPU_FORCE_RENDER(State): send(b"forcerender"+(State*1).to_bytes(1,'big')); print(end=f"GPU_FORCE_RENDER {State}\n"*(not SendSilent));

def EXIT(silent=False): print(end="IT IS NOW SAFE TO TURN OFF YOUR SYSTEM!!\n"*EasterEgg); (send(f"quit".encode()) if not silent else print(end=''))

def main():
 global TGRsock,sockIP,PORT,SystemPath,OSsplit,OSexec,SW,SH,UInput,Exit,MenuTimer,screen,display,RAMUsage,VRAMUsage,Pause,Debug,Running,CPU_IP,CPU_IPS,CPU_TIPS,EasterEgg,Resolutions,SelectRez,TargetRez,buffer
 import Settings as config
 if not config.service[0]: sockIP,PORT = config.service[1],config.service[2]
 if IGNORESERVER == False:
  while config.service[0]:
   try: tmpsock=socket.socket(); tmpsock.bind((sockIP,PORT)); tmpsock.close(); break
   except OSError: PORT+=1
 print(end=f"\\Initialize Memory...\n");
 compile_font(); #//THIS IS NEEDED TO BE RAN FIRST//#
 print(pygame.image.tobytes(font[2],"RGBA"))
 ## TICK ############################################################################
 ##SEND ARRAY
 #Uinput,   Running+Pause+Debug+Exit, |
 #4,        1 byte (5-bits),          |
 #0,1,2,3,  4                         |
 ##RECV ARRAY 
 #IP,  Flags, Running+Pause+Debug+Exit, Error, MEMORY MAP, Display[720p], N/A|
 #8,   1,     1 byte (5-bits),          1024,  0xD800000,  0x2A3000,      N/A|
 #0,3, 7,     8,                        9,     0x409       0xD800409,     0xDAA3409|
 #MEM = bytearray(0xD800000) #Full MemoryMap: 216 MiB
 ROMPG = [] #bytearray(SIZ8MB)*33]
 print(end=f" \\0x{hex2(RAMSIZ,7)}\\{RAMSIZ}\tBytes({round(RAMSIZ/1024/1024*100)/100} MB)\tof RAM were allocated...\n");
 print(end=f" \\0x{hex2(VRAMSIZ,7)}\\ {VRAMSIZ}\tBytes( {VRAMSIZ/1024/1024}0 MB)\tof VideoRAM was allocated...\n",);
 pygame.init(); pygame.display.set_icon(pygame.image.load(f"bin{OSsplit}TGR_logo.png"))
 pygame.display.set_caption('TheGameRazer - [NO-ROM]'); print(end=".")
 display = pygame.display.set_mode((Resolutions[SelectRez][0]+4, Resolutions[SelectRez][1]+4),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,Resolutions[0][2]); print(end=".")
 SW,SH=Resolutions[SelectRez][0],Resolutions[SelectRez][1]
# display = pygame.display.set_mode(HOSTdisplay.current_h, HOSTdisplay.current_w),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,Resolutions[SelectRez][2]); print(end=".")
 screen = pygame.Surface((SW,SH)).convert(); print(end=".\n")
 ROMPATH,HUDinfo,ShowInput,Frames,FPS,IPS,TIPS,MX,MY,PMX,PMY,MB = "",True,False,0,0,[0,0],[0,0],0,0,0,0,0
 SecTimer,SecTimer2=time.time(),time.time()
 print(0)
 if IGNORESERVER == False:
  (Thread(target=ServiceProcess, args=()).start() if config.service[0] else "")
  socket_threadrt = Thread(target=socket_thread, args=()); socket_threadrt.start()
  time.sleep(1); TGRsock.connect((sockIP,PORT)); #ping();
  #CPU_INIT(); init(); ping()
 print(1)
 
 CPU_DEBUG(config.emulation[0]);# ping()
 if config.emulation[0]: print("Debug Mode: Enabled")
 else: print("Debug Mode: Disabled")
 #CPU_RUN(0); ping();
 zoom,ShowInput,fuzz,keepAspect=(0 if(config.video[0]==1)else(1+((config.video[2]*2)or(config.video[1]*1))if(config.video[0]==2)else(4+((config.video[2]*2)or(config.video[1]*1))if(config.video[0]==3)else error("Error: Zoom Setting is too high!!")==None))),config.video[6],config.video[3], config.video[4]
 slowdown,PauseAtLoad,waitInput,skip,skipBIOS,showInfo,noUnicode,noPrint,devInfo,GPU_forceRender,debugBIOS,skipBIOS,noDump,zoom,ShowInput,fuzz,extSAV = 0, False, False, 0, False, False, False, False, False, False, False, False, False, 0, False, False, ""
 print(2)
 for i in range(len(sys.argv)):
  if (sys.argv[i]=="--slow"         or sys.argv[i]=="-s"   ): i+=1; slowdown = sys.argv[i]
  if (sys.argv[i]=="--debug"        or sys.argv[i]=="-d"   ): CPU_DEBUG(True)
  if (sys.argv[i]=="--pauseLoad"    or sys.argv[i]=="-pl"  ): PauseAtLoad     = True
  if (sys.argv[i]=="--waitInput"    or sys.argv[i]=="-wi"  ): waitInput       = True
  if (sys.argv[i]=="--skip"         or sys.argv[i]=="-sk"  ): i+=1; skip = sys.argv[i]; skipBIOS = True
  if (sys.argv[i]=="--info"         or sys.argv[i]=="-i"   ): showInfo        = True
  if (sys.argv[i]=="--noUnicode"    or sys.argv[i]=="-nu"  ): noUnicode       = True
  if (sys.argv[i]=="--noPrint"      or sys.argv[i]=="-np"  ): noPrint         = True
  if (sys.argv[i]=="--devInfo"      or sys.argv[i]=="-di"  ): devInfo         = True
  if (sys.argv[i]=="--forceRender"  or sys.argv[i]=="-fr"  ): GPU_FORCE_RENDER(True)
  if (sys.argv[i]=="--debugBIOS"    or sys.argv[i]=="-db"  ): debugBIOS       = True
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
 if sys.argv[-1][0]!="-":
  ROMPATH=sys.argv[-1].split(OSsplit)
 print(f"ROMPATH: {ROMPATH}")
 inDialog,DialogButton,DialogScroll,DialogSelect,DialogFile,DialogContents,Messages,EasterEgg=-1,0,0,0,"",[],[],config.EasterEgg #DialogType: -1:None | 0:LoadROM | 1:LoadState | 2:SaveState | 3:DumpMemory | 4:MemoryEditor
 if ROMPATH!="": Messages.append([f"ROM \"{ROMPATH}\" Loaded!",600]); Title_lock = False;
 #Messages.append(["Notice: TheGameRazer is Back-In-Action!!\n\nCurrent Build: TGR-PRTO v0.0.45b Alpha\nAgain Please be patent with slow progress,\nReminder of whats new:\n----------------------------------------------------------\n\n* Using New Method for Emulation, Using Pygame as SystemIO\n\\while using C for all emulation work\n* Working on a File Manager for Accessing Files\n* Refining some internal errors in the design\n\n\nJust finished:\n* Finished File Manager\n\n----------------------------------------------------------\nTo-Do List:\n* Finish the C Service\n\\ * Add the CPU Instuctions\n\\ * Setup Sockets for Online Play/Networking\n\\ * Finishing Up Communication between UI and Service\n\n* and last of all, do BUG FIXES!! {SPOOKY...}\n\\... well more AAAAAH!! in the wrong way... pounding your\n \\head agenst the desk kind... WHAT FUN!!\n  \\(not)",100000]);
# SystemPath = "/"
 Title_lock,TN,blitrt,zw,zh,ga,BitDepth,dialogx,dialogy,SystemHUD,SystemMenu,MouseMenu=True,"",screen,0,0,0,32,0,0,True,[-1,-1,-1],-1
 print(4,"ENTERING LOOP!!!")
 while True:
  HOSTdisplay,SW,SH=pygame.display.Info(),Resolutions[SelectRez][0],Resolutions[SelectRez][1]
  pygame.draw.rect(display, (0,0,0), (0,0,HOSTdisplay.current_w,HOSTdisplay.current_h))
  try:
   if (~Running[0] and ~Running[1]): LED={0x00,0x00,0x00}
#   if (zoom == 0):
#    print(zoom,"|",zw,SW,"|",zh,SH)
#    if (zw != SW) | (zh != SH):
##     pygame.display.set_mode((),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,BitDepth)
#     screen = pygame.Surface((SW,SH)).convert();
#     #pygame.display.set_mode((SW+2, SH+2),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,BitDepth)
##     SDL_SetWindowSize(window, SW+2, SH+2);
#     zw,zh,ga=SW,SH,1;
#   elif (zoom >= 1) & (zoom <= 3):
#    print(zoom,"|",zw,SW*2,"|",zh,SH*2)
#    if (zw != SW*2) | (zh != SH*2):
#     screen = pygame.Surface((SW*2,SH*2)).convert();
##     pygame.display.set_mode(((SW*2)+2, (SH*2)+2),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,BitDepth)
##     SDL_SetWindowSize(window, (SW*2)+2, (SH*2)+2);
#     zw,zh,ga=SW*2,SH*2,2;
#   elif (zoom >= 4) & (zoom <= 7):
#    print(zoom,"|",zw,W*3,"|",zh,SH*3)
#    if (zw != SW*3) | (zh != SH*3):
#     screen = pygame.Surface((SW*3,SH*3)).convert();
##     pygame.display.set_mode(((SW*3)+2, (SH*3)+2),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,BitDepth)
##     SDL_SetWindowSize(window, (SW*3)+2, (SH*3)+2);
#     zw,zh,ga=SW*3,SH*3,3;
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
#    if event.type == pygame.VIDEORESIZE:
#     if event.size[0]<SW+2 or event.size[1]<SH+2: display = pygame.display.set_mode((event.size[0]if(event.size[0]>SW+4)else SW+4, event.size[1]if(event.size[1]>SH+4)else SH+4),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,Resolutions[0][2])
#    if event.type == pygame.VIDEORESIZE and MenuTimer==0:
#    if event.type == pygame.VIDEOEXPOSE and MenuTimer==0:
    UInput=[[(1 if pygame.key.get_pressed()[config.controllers[i][j+1]]else 0)for j in range(14)]for i in range(2)]
#    print(pygame.key.get_mods())
    if Exit==-1 and MenuTimer==0 and inDialog==-1:
     if not SystemHUD and pygame.key.get_mods() in [4160,4224,64,128] and pygame.key.get_pressed()[pygame.K_o]:
      SecTimer2,inDialog,DialogButton,DialogScroll,DialogSelect=SecTimer2-10,0,0,0,0; print(end=f"[EMU] Opening File Menu for ROM\n")
     if not SystemHUD and pygame.key.get_mods() in [4160,4224,64,128] and pygame.key.get_pressed()[pygame.K_r]:
      CPU_PAUSE(False);CPU_STOP(0);CPU_STOP(1);MenuTimer=20;init();print(end=f"[EMU] Emulation Soft-Reset\n");Messages.append([f"Emulation Soft-Reset",300]);CPU_RUN(0)
     if not SystemHUD and pygame.key.get_mods() in [4161,4226,64,128] and pygame.key.get_pressed()[pygame.K_r]:
      CPU_PAUSE(False);CPU_STOP(0);CPU_STOP(1);MenuTimer=20;clearMEM();init();print(end=f"[EMU] Emulation Hard-Reset\n");Messages.append([f"Emulation Hard-Reset",300]);CPU_RUN(0)
     if not SystemHUD and pygame.key.get_mods() in [4160,4224,64,128] and pygame.key.get_pressed()[pygame.K_d]:
      MenuTimer=20; print(end=f"[EMU] CPU.debug: {Debug}\n"); Messages.append([f"Debug Mode "+("Enabled"if(Debug==True)else"Disbaled"),150])
     if not SystemHUD and pygame.key.get_mods() in [4160,4224,64,128] and pygame.key.get_pressed()[pygame.K_p]:
      CPU_PAUSE(not Pause);MenuTimer=20; print(end=f"[EMU] CPU.pause: {Pause}\n"); Messages.append([f"Emulation "+("Paused..."if(Pause==True)else"Resumed..."),150])
     if not SystemHUD and pygame.key.get_mods() in [4160,4224,64,128] and pygame.key.get_pressed()[pygame.K_i]:
       HUDinfo,MenuTimer=not HUDinfo,20; print(end=f"[EMU] HUD Information: {HUDinfo}\n"); Messages.append([f"HUD Information "+("Shown..."if(HUDinfo==True)else"Hidden..."),100])
     if pygame.key.get_pressed()[pygame.K_ESCAPE] and Exit==-1 and MenuTimer==0:
      if (not SystemHUD and SystemMenu!=[-1,-1,-1]): CPU_PAUSE(SystemHUD); SystemHUD,MenuTimer=not SystemHUD,20; print(end=f"[EMU] Showing System HUD: {SystemHUD}\n"); Messages.append([("Showing SystemHUD..."if(SystemHUD==True)else"SystemHUD Hidden..."),100])
    elif event.type == pygame.MOUSEMOTION: MX,MY = event.pos; print(f"\aBEEP! {event.pos}")
    elif event.type == pygame.MOUSEBUTTONDOWN: MB = event.button
#   if Exit==-2 and : Exit=-1; print(tmp[0]); CPU_PAUSE(tmp[0])
#   print(Exit,inDialog)
   ### RENDERING ###
   screen.fill((16, 16, 16)); dialogy=2
   getChar(f"Current version: {__version__} Alpha Build",16,dialogy,255, 128, 128,  255,  True, 1);dialogy+=14
   for i in range(2):
    getChar("─ │ ┌ ┬ ┐ ╔ ╦ ╗ ╓ ╥ ╖ ╒ ╤ ╕",16,dialogy,255, 128, 128,  255,  True, i+1);dialogy+=32 if i else 16
    getChar("═ ║ ├ ┼ ┤ ╠ ╬ ╣ ╟ ╫ ╢ ╞ ╪ ╡",16,dialogy,255, 128, 128,  255,  True, i+1);dialogy+=32 if i else 16
    getChar("    └ ┴ ┘ ╚ ╩ ╝ ╙ ╨ ╜ ╘ ╧ ╛",16,dialogy,255, 128, 128,  255,  True, i+1);dialogy+=32 if i else 16
   dialogy-=16
   getChar("┌═─═─═─═─═─═─═─═─═─═─═─═─═─═─═─═─═─═─╗",16,dialogy,255, 128, 128,  255,  True, 1);dialogy+=8
   getChar("║ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789│",16,dialogy,255, 128, 128,  255,  True, 1);dialogy+=8
   getChar("│ `!@#$%^&*()-+_=[]{}\\|;:'\".,<>/?~╓─═╜",16,dialogy,255, 128, 128,  255,  True, 1);dialogy+=8
   getChar("╚─═─═─═─═─═─═─═─═─═─═─═─═─═─═─═─═─╛"  ,16,dialogy,255, 128, 128,  255,  True, 1);dialogy+=8
   
   if HUDinfo == False:
    getChar(f"FPS: {FPS}", 2*8, SH-(4*8), 255, 128, 128,224,  True);
#   getChar(Letter,          X,        Y,   R,   G,   B,  A,  True):
   else:
    getChar(f"Instruction Pointer: [0x{hex2(CPU_IP[0],7)}, 0x{hex2(CPU_IP[1],7)}]", 2*8, SH-(7*8), 128, 128, 255,  224,  True);
    getChar(f"FPS: {FPS} | IPS: {IPS[0]+IPS[1]}({round((IPS[0]+IPS[1]/24000000)*100)/100}) | TotalRan: {CPU_TIPS[0]+CPU_TIPS[1]}", 2*8, SH-(4*8), 255, 128, 128,  224,  True);
   ##                " RAM Usage: 134217727 bytes/134217727 (100.00% full) | VRAM Usage: 67108863 bytes/67108863 (100.00% full)"
    #getChar(f"RAMPOS: 0x{hex(CPU.RP)[2:]}/{CPU.RP}", 2*8, SH-(7*8), 255, 128, 128,  224,  True);
    #nprintf(TFPS,128, " RAM Usage: %.0lf/%d bytes(%.2lf%% full)", RAMUsage, RAMSIZ+1,( RAMUsage/ RAMSIZ)*100);
    getChar(f" RAM Usage: {RAMUsage}/{RAMSIZ+1} bytes({(RAMUsage/RAMSIZ)*100}) full)", 1*8, SH-(6*8), 255, 128, 128,  224,  True);
    if (VRAMUsage > 9):
     getChar(f"VRAM Usage:  {VRAMUsage}/{VRAMSIZ+1} bytes({(VRAMUsage/VRAMSIZ)*100}) full)",1*8, SH-(5*8), 255, 128, 128,  224,  True);
    else:
     getChar(f"VRAM Usage: {VRAMUsage}/ {VRAMSIZ+1} bytes({(VRAMUsage/VRAMSIZ)*100}) full)",1*8, SH-(5*8), 255, 128, 128,  224,  True);
   
   if (ShowInput == True):
    getChar("P1:[                                               ]", 2*8, SH-(3*8),64,64,255,224, True);
    if UInput[0][ 0]:getChar("A",       6*8, SH-(3*8),  64, 64,255,224, True,);
    if UInput[0][ 1]:getChar("B",       8*8, SH-(3*8),  64, 64,255,224, True,);
    if UInput[0][ 2]:getChar("C",      10*8, SH-(3*8),  64, 64,255,224, True,);
    if UInput[0][ 3]:getChar("X",      12*8, SH-(3*8),  64, 64,255,224, True,);
    if UInput[0][ 4]:getChar("Y",      14*8, SH-(3*8),  64, 64,255,224, True,);
    if UInput[0][ 5]:getChar("Z",      16*8, SH-(3*8),  64, 64,255,224, True,);
    if UInput[0][ 6]:getChar("L",      18*8, SH-(3*8),  64, 64,255,224, True,);
    if UInput[0][ 7]:getChar("R",      20*8, SH-(3*8),  64, 64,255,224, True,);
    if UInput[0][ 8]:getChar("START",  22*8, SH-(3*8),  64, 64,255,224, True,);
    if UInput[0][ 9]:getChar("SELECT", 28*8, SH-(3*8),  64, 64,255,224, True,);
    if UInput[0][10]:getChar("UP",     35*8, SH-(3*8),  64, 64,255,224, True,);
    if UInput[0][11]:getChar("DOWN",   38*8, SH-(3*8),  64, 64,255,224, True,);
    if UInput[0][12]:getChar("LEFT",   43*8, SH-(3*8),  64, 64,255,224, True,);
    if UInput[0][13]:getChar("RIGHT",  48*8, SH-(3*8),  64, 64,255,224, True,);
    getChar("P2:[                                               ]", 2*8, SH-(2*8), 64, 64,255,224, True,);
    if UInput[1][ 0]:getChar("A",       6*8, SH-(2*8),  64, 64,255,224, True,);
    if UInput[1][ 1]:getChar("B",       8*8, SH-(2*8),  64, 64,255,224, True,);
    if UInput[1][ 2]:getChar("C",      10*8, SH-(2*8),  64, 64,255,224, True,);
    if UInput[1][ 3]:getChar("X",      12*8, SH-(2*8),  64, 64,255,224, True,);
    if UInput[1][ 4]:getChar("Y",      14*8, SH-(2*8),  64, 64,255,224, True,);
    if UInput[1][ 5]:getChar("Z",      16*8, SH-(2*8),  64, 64,255,224, True,);
    if UInput[1][ 6]:getChar("L",      18*8, SH-(2*8),  64, 64,255,224, True,);
    if UInput[1][ 7]:getChar("R",      20*8, SH-(2*8),  64, 64,255,224, True,);
    if UInput[1][ 8]:getChar("START",  22*8, SH-(2*8),  64, 64,255,224, True,);
    if UInput[1][ 9]:getChar("SELECT", 28*8, SH-(2*8),  64, 64,255,224, True,);
    if UInput[1][10]:getChar("UP",     35*8, SH-(2*8),  64, 64,255,224, True,);
    if UInput[1][11]:getChar("DOWN",   38*8, SH-(2*8),  64, 64,255,224, True,);
    if UInput[1][12]:getChar("LEFT",   43*8, SH-(2*8),  64, 64,255,224, True,);
    if UInput[1][13]:getChar("RIGHT",  48*8, SH-(2*8),  64, 64,255,224, True,);
   [[[Messages.append([msg,Messages[msgi][1]])for msg in(Messages[msgi][0].split("\n"))], Messages.pop(msgi)]for msgi in range(len(Messages))if"\n"in Messages[msgi][0]]
   for msg in range(len(Messages)):
    try:
     getChar(Messages[msg][0],8, 8+(msg*8), 255, 128, 128,  255,  True); Messages[msg][1]-=1
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
    getChar("/"+"-"*round((56-len(tmp[1]))/2)+" "*len(tmp[1])+"-"*math.floor((56-len(tmp[1]))/2)+"\\", 8, 1*8, 255,  64,  64,224,True,)
    getChar(tmp[1],(round((56-len(tmp[1]))/2)+2)*8, 1*8, 255,  64, 255,224,True,)
    getChar("|[",    8, 2*8, 255,  64,  64,224,True,)
    getChar((SystemPath[-53:]if SystemPath.split(OSsplit)[1]=='' else SystemPath[-53:]+"/"),3*8, 2*8, 255, 255,  64,224,True,)
    getChar("]|", 57*8, 2*8, 255,  64,  64,224,True,)
    getChar("|"+"-"*(56)+"|", 8, 3*8, 255,  64,  64,224,True,);j=0;
    pygame.draw.rect(screen, (255,  95,  31, 255), (16,(DialogSelect+4)*8,54*8,8))
    for i in range(4,35): getChar("|",  1*8,i*8, 255,  64,  64, 1, True); getChar("|", 47*8,i*8, 255,  64,  64, 1, True); getChar(f"|{DialogScroll+j}",56*8, i*8, 255,  64,  64, 1, True); ((([getChar(DialogContents[DialogScroll+j][0], 2*8,i*8, 255, 255,  64, 1, True),getChar("PARENT", 49*8,i*8, 255, 255,  64, 1, True)]if DialogContents[DialogScroll+j][0]==".."else[getChar(DialogContents[DialogScroll+j][0], 2*8,i*8, 128, 128, 255, 1, True),getChar("FOLDER", 49*8,i*8, 128, 128, 255, 1, True)])if DialogContents[DialogScroll+j][1]==-1 else[getChar(DialogContents[DialogScroll+j][0],  2*8,i*8,  64, 255,  64, 1, True),getChar(str(DialogContents[DialogScroll+j][1][0]), (52-len(str(DialogContents[DialogScroll+j][1][0])))*8,i*8,  64, 255,  64, 1, True),getChar(DialogContents[DialogScroll+j][1][1],  53*8,i*8,  64, 255,  64, 1, True)])if DialogScroll+j<len(DialogContents)else""); j+=1
    getChar("|"+"-"*(56)+"|", 8, (SH//8-10)*8, 255,  64,  64,224,True,)
    getChar(f"|{DialogContents[DialogScroll+DialogSelect][0]}={DialogScroll+DialogSelect}"if(DialogScroll+DialogSelect<len(DialogContents))else"|", 8, (SH//8-9)*8, 255,  64,  64,224,True,)
    getChar("{[___OK___]}"*(DialogButton==0)+" [___OK___] "*(DialogButton==1), 12*8, (SH//8-9)*8, 255,  64,  64,224,True,)
    getChar(" [_CANCEL_] "*(DialogButton==0)+"{[_CANCEL_]}"*(DialogButton==1), 32*8, (SH//8-9)*8, 255,  64,  64,224,True,)
    getChar("|", 58*8, (SH//8-9)*8, 255,  64,  64,224,True,)
    getChar("\\"+"-"*(56)+"/", 8, (SH//8-8)*8, 255,  64,  64,224,True,)
    getChar("|", (60/2)*8, 0*8, 255,  64,  64,224,True,)
    
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
   
   if Pause==True:
    dialogx,dialogy=(SW/2)-(15*16/2),(SH/2)-(3*16/2)
    backChar(dialogx,dialogy, 15,3,  16, 16,255,0x7F, True, 2)
    getChar("╓────[EMU]────╖", dialogx,dialogy, 128, 128, 255, 127,  True,2);dialogy+=16
    getChar("║CPU PAUSED...║", dialogx,dialogy, 128, 128, 255, 127,  True,2);dialogy+=16
    getChar("╚═════════════╝", dialogx,dialogy, 128, 128, 255, 127,  True,2);dialogy+=16
   if SystemHUD:# ¶
    if pygame.mouse.get_visible(): pygame.mouse.set_visible(False)
    dialogx,dialogy=0,0 #HUD Menu Bar
    pygame.draw.rect(screen, (0x65, 0x2d, 0x51, 0x7F), (0,0,SW,SH))
    pygame.draw.rect(screen, (0x56, 0x52, 0x52, 0xE0), (0,dialogy,SW-12,2));dialogy+=2
    pygame.draw.rect(screen, (0x5e, 0x5d, 0x5d, 0xEF), (0,dialogy,SW-12,2));dialogy+=2
    pygame.draw.rect(screen, (0x6b, 0x68, 0x68, 0xFF), (0,dialogy,SW-12,2));dialogy+=2
    pygame.draw.rect(screen, (0x75, 0x75, 0x75, 0xFF), (0,dialogy,SW-12,2));dialogy+=2
    pygame.draw.rect(screen, (0x91, 0x8d, 0x8d, 0xFF), (0,dialogy,SW-12,4));dialogy+=4
    pygame.draw.rect(screen, (0x75, 0x75, 0x75, 0xFF), (0,dialogy,SW-12,2));dialogy+=2
    pygame.draw.rect(screen, (0x6b, 0x68, 0x68, 0xFF), (0,dialogy,SW-12,2));dialogy+=2
    pygame.draw.rect(screen, (0x5e, 0x5d, 0x5d, 0xEF), (0,dialogy,SW-12,2));dialogy+=2
    pygame.draw.rect(screen, (0x56, 0x52, 0x52, 0xE0), (0,dialogy,SW-12,2));dialogy+=2
    pygame.draw.rect(screen, (0x70, 0x2d, 0x2d, 0x7F), (SW-12,0,8,dialogy))
    pygame.draw.rect(screen, (0x70, 0x2d, 0x2d, 0x7F), (0,dialogy,SW-4,12));dialogy+=4
    #Menu Buttons
    if UInput[0][0xA]: MY-=(1 if(MY>-1)else 0)
    if UInput[0][0xB]: MY+=(1 if(MY<SH)else 0)
    if UInput[0][0xC]: MX-=(1 if(MX>-1)else 0)
    if UInput[0][0xD]: MX+=(1 if(MX<SW)else 0)

    dialogx,dialogy=5,5
    pygame.draw.rect(screen, (0,0,0,0xFF), (dialogx,dialogy,32,16))
    if MX>dialogx+0 and MX<dialogx+32 and MX>dialogy+0 and MX<dialogy+16:
     if MenuTimer>0: MenuTimer=20
     MouseMenu=0
    dialogx+=5+32
    pygame.draw.rect(screen, (0,0,0,0xFF), (dialogx,dialogy,32,16))
    if MX>dialogx+0 and MX<dialogx+32 and MX>dialogy+0 and MX<dialogy+16:
     if MenuTimer>0: MenuTimer=20
     MouseMenu=1
    dialogx+=5+32
    pygame.draw.rect(screen, (0,0,0,0xFF), (dialogx,dialogy,32,16))
    if MX>dialogx+0 and MX<dialogx+32 and MX>dialogy+0 and MX<dialogy+16:
     if MenuTimer>0: MenuTimer=20
     MouseMenu=2
    dialogx+=5+32
    pygame.draw.rect(screen, (0,0,0,0xFF), (dialogx,dialogy,32,16))
    if MX>dialogx+0 and MX<dialogx+32 and MX>dialogy+0 and MX<dialogy+16:
     if MenuTimer>0: MenuTimer=20
     MouseMenu=3
    dialogx+=5+32
    pygame.draw.rect(screen, (0,0,0,0xFF), (dialogx,dialogy,32,16))
    if MX>dialogx+0 and MX<dialogx+32 and MX>dialogy+0 and MX<dialogy+16:
     if MenuTimer>0: MenuTimer=20
     MouseMenu=4
    dialogx+=5+32
    if MenuTimer==0: SystemMenu = [-1,-1,-1]; MouseMenu=-1
    if (UInput[0][0x0] or MB==1):
     MenuTimer=20
     if MouseMenu!=-1: SystemMenu[0]=MouseMenu
    if SystemMenu[0]!=-1:
     #RenderMenu
     #MX,MY,MB
     pygame.draw.rect(screen, (0,0,0,0xFF), (5,5,10,5))
   else: pygame.mouse.set_visible(True)
   getChar(f"SystemHUD: {SystemHUD} | SystemMenu:{SystemMenu}", 16,SH-24, 128, 128, 255, 127,  True,1)
   getChar(f"Mouse: [{MX}, {MY}, {(UInput[0][0x0] or MB==1)}]", 16,SH-16, 128, 128, 255, 127,  True,1)
##HUD Color
# 565252
# 5e5d5d
# 6b6868
# 757575
# 918d8d
##Shadow
# 702d2d
##Display
# 652d51

   if Exit == 2: break
   if Exit != -1:
    dialogx,dialogy=(SW/2)-(22*16/2),(SH/2)-(5*16/2)
    backChar(dialogx,dialogy, 22,5, 255, 16, 16,0x7F, True, 2)
    #pygame.draw.rect(screen, (255,  16,  16, 0), (dialogx,dialogy,22*16,5*16));
    getChar("╓────[EMU=PAUSED]────╖",dialogx,dialogy,255, 128, 128,  127,  True, 2);dialogy+=16
    getChar("║      └EXIT?┘       ║",dialogx,dialogy,255, 128, 128,  127,  True, 2);dialogy+=16
    getChar(((Exit==0)*"╠══{[NO]}    [YES]───╢")+((Exit==1)*"╟───[NO]    {[YES]}══╣"),dialogx,dialogy,255, 128, 128,  127,  True, 2);dialogy+=16
    getChar("║Unsaved will be lost║",dialogx,dialogy,255, 128, 128,  127,  True, 2);dialogy+=16
    getChar("╚════════════════════╝",dialogx,dialogy,255, 128, 128,  127,  True, 2);dialogy+=24
     
    if (UInput[0][0xC] or UInput[0][0xD]) and not MenuTimer: Exit,MenuTimer = not Exit,10
    if (UInput[0][0x8] or UInput[0][0x0]):
     if Exit == 1: break
     else: Exit=-1

   if keepAspect == True:
    if SW > SH:
     scale_factor = (HOSTdisplay.current_w-4)/SW;
     sy = scale_factor*SH
     if sy > HOSTdisplay.current_h-4:
      scale_factor = (HOSTdisplay.current_h-4)/SH;
      sx,sy = scale_factor*SW,HOSTdisplay.current_h-4
     else: sx = HOSTdisplay.current_w-4
    else:
     scale_factor = (HOSTdisplay.current_h-4)/SH;
     sx = scale_factor*SW
     if sx > HOSTdisplay.current_w-4:
      scale_factor = (HOSTdisplay.current_w-4)/SW;
      sx,sy = HOSTdisplay.current_w-4, scale_factor*SH
     else: sy = HOSTdisplay.current_h-4
    centX = (HOSTdisplay.current_w/2)-(sx/2)
    centY = (HOSTdisplay.current_h/2)-(sy/2)
    display.blit(pygame.transform.scale(blitrt, (sx,sy) ), (centX, centY))
    pygame.draw.rect(display, Boarder, (centX-2 ,centY   ,   2,sy))
    pygame.draw.rect(display, Boarder, (centX-2 ,centY   ,sx+4, 2))
    pygame.draw.rect(display, Boarder, (centX+sx,centY   ,   2,sy))
    pygame.draw.rect(display, Boarder, (centX-2 ,centY+sy,sx+4, 2))
   else:
    display.blit(pygame.transform.scale(blitrt, (SW*(((HOSTdisplay.current_w>>1<<1)-2)*128//SW)/128,SH*(((HOSTdisplay.current_h>>1<<1)-2)*128//SH)/128)), (2, 2))
    pygame.draw.rect(display, Boarder, (0,0,2,HOSTdisplay.current_h))
    pygame.draw.rect(display, Boarder, (0,0,HOSTdisplay.current_w,2))
    pygame.draw.rect(display, Boarder, (HOSTdisplay.current_w-2,0,2,HOSTdisplay.current_h))
    pygame.draw.rect(display, Boarder, (0,HOSTdisplay.current_h-2,HOSTdisplay.current_w,2))
   if SecTimer+1 < time.time():TIPS=CPU_TIPS;FPS=Frames;Frames=0;SecTimer=time.time();IPS=CPU_IPS;CPU_IPS=[0,0]
#   getChar("FPS: "+str(FPS), 10, SH-26, 128, 255, 128, 0xFF, True,1)
   #if (time.time()*1000)%((1/60)*1000):
   pygame.display.update();Frames+=1;MenuTimer-=(MenuTimer>0)*0.5;clk.tick(60)
   if inDialog == -1 and Exit==-1: send(b"tick"+b''.join([int("".join(str(i)for i in UInput[j]),2).to_bytes(2,"little") for j in range(2)])+((Running[0])+(Running[1]<<1)+(Pause<<2)+(Debug<<3)).to_bytes(1,"little"))
   else: send(b"tick\x00\x00\x00\x00"+ ((Running[0])+(Running[1]<<1)+(Pause<<2)+(Debug<<3)).to_bytes(1,"little"))
 ## TICK #########################
 #Uinput,   Running+Pause+Debug, |
 #4,        1 byte (4-bits),     |
 #0,1,      2                    |
   if IGNORESERVER == False:
    if not socket_threadrt.is_alive(): raise socket.error
  except BrokenPipeError: print("ERROR: Lost Connection to Service!!"); break
  except socket.error as err: print(end=f"\nerr:{err}\n[EMU] We have detected the main loop has stopped responding...\n\nThis halt is most likely due to a Emulation Error.\nIf there is a Error, check above for what the problem is. [If it's the ROM make sure Debug Mode is Active]\n/!\\Reminder: check the ROM before reporting EMU probblems/!\\\n"); break
 send(f"quit".encode());
  
###
def socket_thread():
 global TGRsock,sockIP,PORT,SystemPath,OSsplit,OSexec,SW,SH,UInput,Exit,MenuTimer,screen,display,RAMUsage,VRAMUsage,Pause,Debug,Running,CPU_IP,CPU_IPS,CPU_TIPS,EasterEgg,Resolutions,SelectRez,TargetRez,buffer
 if IGNORESERVER == False:
  while True:
   try:
    try: buffer = TGRsock.recv(1024) #; print("GOT DATA: {buffer}")
    except socket.error: buffer=b''; #print("Socket Error, no data in request (timeout responce)")
    if buffer!=b'':
     print(f"Client GOT: \"{buffer}\"")
     if buffer.startswith(b"rezch"): SelectRez = int(buffer[5]); SW,SH=Resolutions[SelectRez][0],Resolutions[SelectRez][1]; screen = pygame.Surface((SW,SH)).convert()
     if buffer.startswith(b"quit"): print("EXIT"); raise KeyboardInterrupt
   except BrokenPipeError: print("ERROR: Lost Connection to Service!!"); break
   except socket.error as err: break
 return -1
##################################################

#CPU_DEBUG

#from src.Components import *
try: main()
except KeyboardInterrupt: Error=0
except BrokenPipeError: pass
except Exception as e: print(end="\n/!\\ FATAL ERROR!! /!\\\n"); logging.error(traceback.format_exc()); print(end="[EMU] /!\\ A FATAL ERROR HAS OCCORED!!! /!\\\nOh boy, we seem to have detected a Fatal issue with the main loop ( Reason can be seen above ^^ )\n\\and all Emulation has been Halted, and Eny UNSAVED DATA will be LOST.\n\nIf this is not the first time you've recived this message for this error:\n\\Please Contact US via Support Ticket in the TGR Forums: https://koranva-forest.com/forums/TGR\n \\Or Contact US via Discord: https://discord.gg/PWAf8ek\n"); Error+=1;
print("\nShutting down...");
print(0)
if EasterEgg:
 print(-1)
 pygame.draw.rect(screen, (  0,   0,   0, 255), (0,0,SW,SH)); SecTimer=time.time();
 print(-2)
 while SecTimer+2>time.time(): display.blit(screen, (2, 2)); pygame.draw.rect(display, (0,0,0,255), (0,0,2,SH)); pygame.draw.rect(display, (0,0,0,255), (0,0,SW,2)); pygame.draw.rect(display, (0,0,0,255), (SW-2,0,SW,SH)); pygame.draw.rect(display, (0,0,0,255), (0,SH-2,SW,SH)); pygame.display.update(); clk.tick(60)
 print(-3)
 getChar("IT IS NOW SAFE TO TURN", SW/4-11*8, SH/4-8, 0xED, 0x7B, 0x34, 255,  True,2);getChar("  OFF YOUR COMPUTER!  ", SW/4-11*8, SH/4,   0xED, 0x7B, 0x34, 255,  True,2);SecTimer=time.time()
 print(-4)
 while SecTimer+10>time.time(): display.blit(screen, (2, 2)); pygame.draw.rect(display, (0,0,0,255), (0,0,2,SH)); pygame.draw.rect(display, (0,0,0,255), (0,0,SW,2)); pygame.draw.rect(display, (0,0,0,255), (SW-2,0,SW,SH)); pygame.draw.rect(display, (0,0,0,255), (0,SH-2,SW,SH)); pygame.display.update(); clk.tick(60)
 print(-5)
print(1)
EXIT(1*(Error==0)); print(2); pygame.quit(); sys.exit()
