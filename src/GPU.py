global MEM,UInput,Exit,MenuTimer,txt_font,screen,chars,font,SW,SH,display,RAMUsage,VRAMUsage,IPC,Boarder
GPU_x = 0x0000000
def reset():
 print("\\Initalizing GPU")
 
 print(" \\GPU Initalized!")

instuctions = []
def inst(Core,Arg): # 0x00:// |    NOP     |  -  |
 Arg=0x0
 return
instuctions.append(inst)

def inst(Core,Arg): # 0x01:// |   SET Y    |  +  |
 Arg%=0xFFFF
 
 if debug == True: print(f"GPU for CPU#{Core}: Setting GPU.X to 0x{hex2(Arg,4)}")
 if Arg >= 0:
  if (Arg < SW): GPU_x = Arg;
  else: GPU_x = SW;
 else:
  MEM[GPU_x] = -1;
 return
instuctions.append(inst)
"""
def inst(Core,Arg) # 0x01:// |   SET Y    |  +  |
   if (CPU.debug == True): printf("GPU: Setting GPU.y to 0x%x\n", Arg); }
   if (Arg >= 0):
    if (Arg < SH): GPU_y = Arg; }
    else: GPU_y = SH; }
   } else:
   : GPU_y = -1; }
   }
   break;
def inst(Core,Arg): # 0x02:// |   SET R    |  +  |
   if (CPU.debug == True): printf("GPU: Setting GPU.R to 0x%x\n", Arg); }
   GPU_r = Arg % 0x100;
   break;
def inst(Core,Arg): # 0x03:// |   SET G    |  +  |
   if (CPU.debug == True): printf("GPU: Setting GPU.G to 0x%x\n", Arg); }
   GPU_g = Arg % 0x100;
   break;
def inst(Core,Arg): # 0x04:// |   SET B    |  +  |
   if (CPU.debug == True): printf("GPU: Setting GPU.B to 0x%x\n", Arg); }
   GPU_b = Arg % 0x100;
   break;
def inst(Core,Arg): # 0x05:// | SET CPallet|  +  |
   lArg = Arg%0x10;
   if (lArg == 0x0):
    printf("GPU NOTTICE: You can't set CPU.CP[0x0]...\n");
    break;
   } if (CPU.debug == True): printf("GPU: Setting GPU.CP[0x%x\t] to [R:0x%x\t,G:0x%x\t,B:0x%x\t]\n",lArg,GPU_r,GPU_g,GPU_b); }
   GPU_cp[lArg-1][0] = GPU_r;
   GPU_cp[lArg-1][1] = GPU_g;
   GPU_cp[lArg-1][2] = GPU_b;
   break;
def inst(Core,Arg): # 0x06:// |   plot     |  +  |
   if (GPU_x == -1 || GPU_y == -1):
    if (CPU.debug == True): printf("GPU NOTTICE: Skipping pixel at [X:0x%x\t,Y:0x%x\t] due to being OutOfBounds...\n", GPU_x, GPU_y); }
    break;
   }
   if (GPU_x < SW && GPU_y < SW):
    lArg = Arg%0x20;
    if (lArg == 0x0):
     if (CPU.debug == True): printf("GPU: Skiping pixel plot at [X:0x%x\t,Y:0x%x\t]\n", GPU_x, GPU_y); }
     break;
    }
    if (Arg > 0xF):
     if (CPU.debug == True): printf("GPU: Plotting pixel at [X:0x%x\t,Y:0x%x\t] as GPU.REGs (R:0x%x\t,G:0x%x\t,B:0x%x\t)\n", GPU_x, GPU_y, GPU_r, GPU_g, GPU_b); }
     buffer[GPU_x][GPU_y][0] = GPU_r;
     buffer[GPU_x][GPU_y][1] = GPU_g;
     buffer[GPU_x][GPU_y][2] = GPU_b;
    } else:
     if (CPU.debug == True): printf("GPU: Plotting pixel at [X:0x%x\t,Y:0x%x\t] as GPU.CP[0x%x\t] (R:0x%x\t,G:0x%x\t,B:0x%x\t)\n",GPU_x, GPU_y, lArg, GPU_cp[lArg][0], GPU_cp[lArg][1], GPU_cp[lArg][2]); }
     buffer[GPU_x][GPU_y][0] = GPU_cp[lArg-1][0];
     buffer[GPU_x][GPU_y][1] = GPU_cp[lArg-1][1];
     buffer[GPU_x][GPU_y][2] = GPU_cp[lArg-1][2];
    }
   } else:
    if (CPU.debug == True): printf("GPU NOTTICE: skipping pixel at [X:0x%x\t,Y:0x%x\t] due to being OutOfBounds...\n", GPU_x, GPU_y); }
   }
   if (forceRender == True): GPU.run  = True; }
   break;
def inst(Core,Arg): # 0x07:// |   update   |  -  |
   GPU.run  = True;
   break;
  default:// nothing
   System_Error(0, inst, CPU.IP, 0, name0);
   break;
 }
}

int  GPU_recv(int inst):
 switch(inst):
def inst(Core,Arg): # 0x00:// |  GET W     |  +  |
   if (CPU.debug == True): printf("GPU: Returning Screen Width"); }
   return SW-1;
   break;
def inst(Core,Arg): # 0x01:// |  GET H     |  +  |
   if (CPU.debug == True): printf("GPU: Returning Screen Height"); }
   return SH-1;
   break;
def inst(Core,Arg): # 0x02:// |  GET GPU.R |  +  |
   return buffer[GPU_x][GPU_y][0];
   break;
def inst(Core,Arg): # 0x03:// |  GET GPU.G |  +  |
   return buffer[GPU_x][GPU_y][1];
   break;
def inst(Core,Arg): # 0x04:// |  GET GPU.B |  +  |
   return buffer[GPU_x][GPU_y][2];
   break;
def inst(Core,Arg): # 0x05:// |  GET GPU.X |  +  |
   return GPU_x;
   break;
def inst(Core,Arg): # 0x06:// |  GET GPU.Y |  +  |
   return GPU_y;
   break;
  default:// nothing
   System_Error(0, inst, CPU.IP, 0, name0);
   break;
 }
 return 0;
}








def inst(Core,Arg): //SetColorPalletRGB
 Arg=0xFFFFFF
 return
instuctions.append(inst)

00:
01:SetColorPalletRGB
02:plot
03:line
04:rectangle
05:circle
06:sprite plot
FE:copy
FF:render
"""
