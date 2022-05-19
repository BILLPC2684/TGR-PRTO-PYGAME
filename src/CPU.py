import pygame,colorama; REGN = "ABCDEFGH********"
global MEM,UInput,Exit,MenuTimer,txt_font,screen,chars,font,SW,SH,display,RAMUsage,VRAMUsage,IPC,Boarder
global IC,REGS,Cache,IP,FLAGS,Running,IPS,TIPS,Pause,Debug,EXIT,Running,Error
def hex2(x,l): x=hex(x)[2:][-l:]; return ("0"*(l-len(x)))+x

REGS  = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
Cache = [bytearray(1024),bytearray(1024)]
IP,FLAGS,Running = [0x0000000,0x0000000],[0x0,0x0],[False,False]
IPS,TIPS = [0,0],[0,0]
Pause,Debug,EXIT,Error = False,False,False,""

def reset():
 global REGS,Cache,IP,FLAGS,Running,IPS,TIPS,Pause,Error
 print("\\Initalizing CPU")
 REGS  = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
 Cache = [bytearray(1024),bytearray(1024)]
 IP,FLAGS,Running = [0x0000000,0x0000000],[0x0,0x0],[False,False]
 IPS,TIPS = [0,0],[0,0]
 Pause,Error = False,""
 print(" \\CPU Initalized!")

instructions = []
def inst(Core,A,B,C,IMM):
 A&=0xF; B=0; C=0; IMM&=0xFFFF
 print(end=f"LOAD 0x{hex2(IMM,4)} to REG[{REGN[A]}]\n"*Debug)
 REGS[Core][A] = IMM
instructions.append(inst)
def inst(Core,A,B,C,IMM):
 A&=0xF; B&=0xF; C&=0xF; IMM&=0x7FFFFFF
 if (IMM>>27)&0xF==0:
  print(end=f"ADD REG[{REGN[A]}] and REG[{REGN[B]}] to REG[{REGN[C]}]\n"*Debug)
  REGS[Core][C] = REGS[Core][A] + REGS[Core][B]
 else:
  print(end=f"ADD REG[{REGN[A]}] and 0x{hex2(IMM%0xFFFF,4)} to REG[{REGN[C]}]\n"*Debug)
  REGS[Core][C] = REGS[Core][A] + (IMM%0xFFFF)
instructions.append(inst)
def inst(Core,A,B,C,IMM):
 print(end=f"HALTED!\n")
 Running[Core]=False
instructions.append(inst)

def inst(Core,A,B,C,IMM):
 A=0; B=0; C=0; IMM=0; global Running,Error
 print(end=f"[CPU#{Core}] {'0'*(9-len(str(IP[Core])))}{IP[Core]}/0x{hex2(IP[Core],7)}: " * (not Debug) + f"UNKNOWN INSTRUCTION: 0x{hex2(CI,2)}\n")
 Running=[False,False];Error = f"[CPU#{Core}] {'0'*(9-len(str(IP[Core])))}{IP[Core]}/0x{hex2(IP[Core],7)}: UNKNOWN INSTRUCTION: 0x{hex2(CI,2)}"
for i in range(255-len(instructions)): instructions.append(inst)

def inst(Core,A,B,C,IMM):
 A=0; B=0; C=0; IMM=0
 print(end=f"NOP\n"*Debug)
instructions.append(inst)

def Thread(MEM):
 global CI,REGS,Cache,Running,IP,FLAGS,EXIT
 clk = pygame.time.Clock();i=0
 MEM[i:i+6]=[0x00,0x00,0x00,0x00,0x00,0x01];i+=6
 MEM[i:i+6]=[0x00,0x10,0x00,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x01,0x00,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x10,0x10,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x01,0x00,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x10,0x10,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x01,0x00,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x10,0x10,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x01,0x00,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x10,0x10,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x01,0x00,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x10,0x10,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x01,0x00,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x10,0x10,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x01,0x00,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x10,0x10,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x01,0x00,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x10,0x10,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x01,0x00,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x01,0x10,0x10,0x00,0x00,0x00];i+=6
 MEM[i:i+6]=[0x7F,0x00,0x00,0x00,0x00,0x00]
 while not EXIT:
  for Core in range(2):
   CI=MEM[IP[Core]];#print(end=f"Tick {Core}\n"*Debug)
   if Running[Core] and not Pause:
    print(end=f"\n[CPU#{Core}] {'0'*(9-len(str(IP[Core])))}{IP[Core]}/0x{hex2(IP[Core],7)}: "*Debug)
    instructions[MEM[IP[Core]]](Core,(MEM[IP[Core]+1]>>4)&0xF,MEM[IP[Core]+1]&0xF,(MEM[IP[Core]+2]>>4)&0xF,\
     (MEM[IP[Core]+2]&0xF)<<8|(MEM[IP[Core]+3]&0xFF)<<8|(MEM[IP[Core]+4]&0xFF)<<8|(MEM[IP[Core]+5]&0xFF))
    IP[Core]+=6;IPS[Core]+=1;TIPS[Core]+=1;print(end=f"\\A: 0x{hex2(REGS[Core][0],4)}, B: 0x{hex2(REGS[Core][1],4)}, C: 0x{hex2(REGS[Core][2],4)}, D: 0x{hex2(REGS[Core][3],4)}, E: 0x{hex2(REGS[Core][4],4)}, F: 0x{hex2(REGS[Core][5],4)}, G: 0x{hex2(REGS[Core][6],4)}, H: 0x{hex2(REGS[Core][7],4)}\n"*Debug)
  clk.tick(24000000) #24MHz

