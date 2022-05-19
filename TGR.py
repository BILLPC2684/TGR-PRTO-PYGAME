#!/bin/env python3
import pygame,os,sys,time
from threading import *
from colorama import *
global Exit,CPU_Thread,OSsplit #debug,MEM,UInput,Exit,MenuTimer,screen,chars,font,SW,SH,display,RAMUsage,VRAMUsage,Boarder,MEMsizes
if os.name=="nt": OSsplit="\\"
else: OSsplit="/"
clk = pygame.time.Clock()
print(end="Loading TGR-PRTO v0.0.42e Alpha Build...")

RAMUsage,VRAMUsage,Boarder = 0,0,[128,0,0]
SW,SH,MEM,font,display,screen = 480,360,[],[],[],[]
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
ROMPG = [bytearray(MEMsizes["ROM0"])*33]

def hex2(x,l): x=hex(x)[2:][-l:]; return ("0"*(l-len(x)))+x

## FONT DATA ##
def backChar(Length,X,Y,R,G,B):
 for y in range(8):
  for x in range(Length*8):
   plot(X+x,Y+y,R,G,B)

def getChar(Letter, X, Y, R, G, B, A=0xFF, shadow=True,S=1):
 global chars,font,SW,SH
 # print("Drawing string: "+Letter)
 for i in range(len(Letter)):
  for j in range(98):
   if (Letter[i] == chars[j]): break
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

MenuTimer = 0
Exit = -1
def main():
 global CPU_Thread,SW,SH,MEM,UInput,Exit,MenuTimer,screen,display,RAMUsage,VRAMUsage
 print(end=f"\\Initialize Memory...\n");
 MEM = bytearray(0xD800000) #Full MemoryMap: 218 MiB
 print(end=f" \\0x{hex2(RAMSIZ,7)}\\{RAMSIZ}\tBytes({RAMSIZ/1024/1024} MB)\tof RAM were allocated...\n");
 print(end=f" \\0x{hex2(VRAMSIZ,7)}\\(VRAMSIZ)\tBytes({VRAMSIZ/1024/1024} MB)\tof VideoRAM was allocated...\n",);
 pygame.init(); pygame.display.set_icon(pygame.image.load(f"bin{OSsplit}TGR_logo.png"))
 pygame.display.set_caption('TheGameRazer - [NO-ROM]'); print(end=".")
 display = pygame.display.set_mode((SW+4, SH+4));       print(end=".")
 screen = pygame.Surface((SW,SH)).convert(); print(end=".\n")
 ROMPATH,HUDinfo,ShowInput,Frames,FPS,IPS,TIPS,MX,MY,PMX,PMY,MB = "",True,True,0,0,0,0,0,0,0,0,0
 SecTimer=time.time()
 CPU_Thread = Thread(target=CPU.Thread, args=[MEM])
 init()
 CPU_Thread.start()
 import Settings as config
 CPU.Debug = config.emulation[0]
 if config.emulation[0]: print("Debug Mode: Enabled")
 else: print("Debug Mode: Disbaled")
 CPU.Running[0]=True
 for i in range(len(sys.argv)):
  if (sys.argv[i]=="--slow"         or sys.argv[i]=="-s"   ): i+=1; slowdown = sys.argv[i]
  if (sys.argv[i]=="--debug"        or sys.argv[i]=="-d"   ): CPU.Debug       = True
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
#  if (sys.argv[i]=="--extSAV"       or sys.argv[i]=="-sav" ): i+=1; extSAV = sys.argv[i]
 print(sys.argv[-1])
 if sys.argv[-1][0]=="-":
  ROMPATH=sys.argv[-1].split(OSsplit)
 print(f"ROMPATH: {ROMPATH}")
 Messages=[]
 if ROMPATH!="": Messages.append([f"ROM \"{ROMPATH}\" Loaded!",600])
 while True:
  Title_lock,TN=True,""
  if not Title_lock:
   print(end=f"\n\\ROM Header info:\n \\Type: {MEM[0]}\n  \\System: {chr(MEM[1])+chr(MEM[2])+chr(MEM[3])}\n");
   if MEM[0]==1:
    print(end=f"   \\Title: {chr(MEM[4])+chr(MEM[5])+chr(MEM[6])+chr(MEM[7])+chr(MEM[8])+chr(MEM[9])+chr(MEM[10])+chr(MEM[11])}\n");
    TN="TheGameRazer - "+[MEM[i+4] for i in range(8)].join() ## Title_Name[i+16] = MEM[i+4]; }
   else:
    TN="TheGameRazer - NO TITLE";
   pygame.display.set_caption(TN); Title_lock = True
 
  SW,SH=display.get_size()
  for event in pygame.event.get():
   if event.type == pygame.QUIT: Exit+=1
   for i in range(2):
    for j in range(14):
     if pygame.key.get_pressed()[config.controllers[i][j]]: UInput[i][j]=1
     else: UInput[i][j]=0
   if pygame.key.get_mods()==4160 and pygame.key.get_pressed()[pygame.K_d]:
    if Exit==-1 and MenuTimer==0: CPU.Debug,MenuTimer=not CPU.Debug,20; print(end=f"[EMU] CPU.debug: {CPU.Debug}\n");
   if pygame.key.get_mods()==4160 and pygame.key.get_pressed()[pygame.K_p]:
    if Exit==-1 and MenuTimer==0: CPU.Pause,MenuTimer=not CPU.Pause,20; print(end=f"[EMU] CPU.pause: {CPU.Pause}\n");
   if pygame.key.get_pressed()[pygame.K_ESCAPE]: CPU.Paused,HUDinfo,MenuTimer=True,not HUDinfo,20
   #elif event.type == MOUSEMOTION: MX,MY = event.pos
   #elif event.type == MOUSEBUTTONDOWN: MB = event.key
  print(end='')
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
    else: CPU.Paused,Exit = False,-1
  elif CPU.Pause==True:
   getChar("```````````````", SW/4-7*8, SH/4-8,  16,  16, 255, True, False,2);
   getChar("```````````````", SW/4-7*8, SH/4,    16,  16, 255, True, False,2);
   getChar("```````````````", SW/4-7*8, SH/4+8,  16,  16, 255, True, False,2);
   getChar("+----[EMU]----+", SW/4-7*8, SH/4-8, 128, 128, 255, True,  True,2);
   getChar("|CPU PAUSED...|", SW/4-7*8, SH/4,   128, 128, 255, True,  True,2);
   getChar("+-------------+", SW/4-7*8, SH/4+8, 128, 128, 255, True,  True,2);

  if HUDinfo == False:
   getChar(f"FPS: {FPS}", 2*8, SH-(4*8), 255, 128, 128,  True,  True);
  else:
   getChar(f"Instruction Pointer: [0x{hex2(CPU.IP[0],7)}, 0x{hex2(CPU.IP[1],7)}]", 2*8, SH-(7*8), 128, 128, 255,  True,  True);
   getChar(f"FPS: {FPS} | IPS: {IPS[0]+IPS[1]}({round((IPS[0]+IPS[1]/24000000)*100)/100}) | TotalRan: {CPU.TIPS[0]+CPU.TIPS[1]}", 2*8, SH-(4*8), 255, 128, 128,  True,  True);
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
  display.blit(screen, (2, 2))
  pygame.draw.rect(display, Boarder, (0,0,2,SH))
  pygame.draw.rect(display, Boarder, (0,0,SW,2))
  pygame.draw.rect(display, Boarder, (SW-2,0,SW,SH))
  pygame.draw.rect(display, Boarder, (0,SH-2,SW,SH))
  if SecTimer+1 < time.time():TIPS=CPU.TIPS;FPS=Frames;Frames=0;SecTimer=time.time();IPS=CPU.IPS;CPU.IPS=[0,0]
#  getChar("FPS: "+str(FPS), 10, SH-26, 128, 255, 128, 0xFF, True,1)
  #if (time.time()*1000)%((1/60)*1000):
  pygame.display.update();Frames+=1;MenuTimer-=(MenuTimer>0)*1;clk.tick(60)
##################################################

from src.Components import *
try: main()
except KeyboardInterrupt: pass
print("\nShutting down...");CPU.Running,CPU.EXIT=[False,False],True; CPU_Thread.join();pygame.quit()
