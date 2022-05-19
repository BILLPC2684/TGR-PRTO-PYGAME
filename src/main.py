#############################
#############################
##      THE GAME RAZER     ##
##     MAIN SYSTEM FILE    ##
##     **DO NOT EDIT**     ##
#############################
#############################
#############################

#
import os
import CPU
import GPU
import Components

ascii     = "................................ !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~.................................¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ";
ascii_non = "................................ !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~.......................................................................................................................................................";
#def concat(s1,*s2):
# len1 = len(s1);
# len2 = len(s2);
# result = malloc(len1+len2+1);#+1 for the null-terminator
# #in real code you would check for errors in malloc here
# memcpy(result, s1, len1);
# memcpy(result+len1, s2, len2+1);#+1 to copy the null-terminator
# return result;

def bin_dump(u):
 int i = 63;
 while(i<=0):
  print((u&(2**64-1)) & pow(2, i))["0","1"],end=''); i-=1;
 print();

def dumpData(name, file, size, bool use_non, int start, int end) {
 use_non&=1
 bytes=bytearray(16);
 print(end="._______._______________________________________________.________________.\n|"+str(name));
 if   (len(name) < 2): print("      ");
 elif (len(name) < 3): print("     ");
 elif (len(name) < 4): print("    ");
 elif (len(name) < 5): print("   ");
 elif (len(name) < 6): print("  ");
 elif (len(name) < 7): print(" ");
 print(end="|00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F|0123456789ABCDEF|\n|-------|-----------------------------------------------|----------------|\n|0000000|");
 j,l=1,0;
 for i in range(start,end):
  if (i >= file.size): break
  if (j > 15):
   bytes[j-1] = file.data[i];
   if (file.data[i] < 0x10): printf("0");
   print(hex(file.data[i]).upper()[-2:],end="|");
   for k in range(0,16):
   if (use_non): printf(ascii_non[bytes[k]]);
   else:         printf(ascii[bytes[k]]);
   l=0;
   print(end="|\n|");
   if      (i+1 < 0x1):        print(end=f"0000000{i+1}|");
   else if (i+1 < 0x10):       print(end=f"000000{i+1}|");
   else if (i+1 < 0x100):      print(end=f"00000{i+1}|");
   else if (i+1 < 0x1000):     print(end=f"0000{i+1}|");
   else if (i+1 < 0x10000):    print(end=f"000{i+1}|");
   else if (i+1 < 0x100000):   print(end=f"00{i+1}|");
   else if (i+1 < 0x1000000):  print(end=f"0{i+1}|");
   else if (i+1 < 0x10000000): print(end=f"{i+1}|");
   j = 0;
  else:
   if (file.data[i] < 0x10): printf("0");
   print(hex(file.data[i]).upper()[-2:]); bytes[j-1] = file.data[i];
  j++; l++;

 if (j > 0):
  for i in range(j,16):
   print(end="-- "); bytes[j-1] = 0x00;
  print(end="--|");
  for i in range(0,l-1):
   if (use_non): print(ascii_non[bytes[i]]);
   else:         print(ascii[bytes[i]]);

  for i in range(j,16): printf(" ");
  print(end=" |\n");
 print(end="|_______|_______________________________________________|________________|\n\\Size: 0x%lx/%ld Bytes(",file.size,file.size);
 if (file.size < 1024*1024): print(file.size/1024/1024,end=" KB)");
 else: print(file.size/1024/1024,end=" MB)");
 print(end=f" of {hex(file.data[i]).upper()}/{size} bytes(");
 if      (size < 1024*1024): print((size+1)/1024,end=" KB)\n\n");
 else: print((size+1)/1024/1024,end=" MB)\n\n");


def crop(dst, src, mn, mx):
 leng = mx - mn; src += mn;
 for i in range(0,leng): dst[i] = src[i];
 dst[leng] = '\0';

def load(address, make=False):
 file={}; file["found"] = True;
 if (os.path.exists(address) == -1):
  if (make == 0):
   print(end=f"EMU ERROR: file(\"{address}\") was not found...\n");
   file["found"] = false;
   return file;
  else:
   printf("EMU WARNING: file \"%s\" was not found(your data could be lost if existsed), attempting to create local file...", address);
   FILE *SAV_file = fopen(address, "wb");
   fwrite(calloc(SAVSIZ, sizeof(*SAV)), SAVSIZ-1, 8, SAV_file);
   fclose(SAV_file);
#   file["fp"] = fopen(address, "wb+");
#   file["data"] = calloc(SAVSIZ, sizeof(*SAV));
#   fwrite(&file.data, SAVSIZ, 8, file.fp);
#   fclose(file.fp);
  }
 }
 file.fp = fopen(address, "rb");
 fseek(file.fp, 0, SEEK_END);
 file.size = ftell(file.fp);
 rewind(file.fp);
 file.data = malloc((file.size + 1) * sizeof(*file.data));
 fread(file.data, file.size, 1, file.fp);
 file.data[file.size] = '\0';
 fclose(file.fp);
 return file;
}
bool     showInfo = false;
int      slowdown = 0;
int      FPSLimmit = 1000;
int      delay = 0;
int      delay_skip = 62;
int      frames = 0;
bool     Exit = false;
int      argc;
char*    argv[10];
bool     UInput[14][2] = {false};
bool     gotUIn = false;
int      FPS = 0;
char     execLoc[1024];
char*    dropped_filedir = "";
bool*    restart;
char     chars[95];
char*    font[95][8];
bool     ShowFPS;
bool     crash;
uint8_t  overlay[SW][SH][4] = {{{0}}};
uint8_t  screen[SW][SH][3] = {{{0}}};
bool     enableOL = true;
bool     Title_lock = false;
int      MsgTimer = 0;
char     Message[255] = "";
bool     p = false;
bool     HUDinfo = false;
bool     ShowInput = false;
bool     Fullscreen = false;
int      zoom = 0;

#ZOOM INFO
#0 - normal
#1 - 2x
#2 - scanlines (2x)
#3 - pixelated (2x)
#4 - 3x
#5 - scanlines (3x)
#6 - pixelated (3x)

#int      info_scr[SW*2];
CPU_INIT CPU;
SDL_DisplayMode display;

int main(int c, char *v[]) {
 char TN[1024] = "TheGameRazer - [NO ROM]"; for (int i=0;i<23;i++) { Title_Name[i] = TN[i]; } Title_lock = false;
 argc = c; for (int i=0; i<argc; i++) { argv[i] = v[i]; }  #printf(">>ARG[%d]: %s\n",i,argv[i]);
 
 printf("Loading TGR-PRTO v0.0.36 Alpha Build...\n");

 if        (sysOS == 0) {  printf("Detected WindowsOS\n");
 } else if (sysOS == 1) {  printf("Detected LinuxOS\n");
 } else {                  printf("Unkown OS Detected...\n"); exit(EXIT_FAILURE); }
 
 for(int i=0;i<SDL_GetNumVideoDisplays();++i){
  int should_be_zero = SDL_GetCurrentDisplayMode(i, &display);
  if(should_be_zero != 0) {
   SDL_Log("Could not get display mode for video display #%d: %s", i, SDL_GetError());
  } else {
   SDL_Log("Display #%d: display display mode is %dx%dpx @ %dhz.", i, display.w, display.h, display.refresh_rate);
  }
 }
 if (video_Zoom == 2 && video_ScanLines == false && video_Pixelate == false) {  zoom = 1; }
 if (video_Zoom == 2 && video_ScanLines == true  && video_Pixelate == false) {  zoom = 2; }
 if (video_Zoom == 2 && video_Pixelate  == true )                            {  zoom = 3; }
 if (video_Zoom == 3 && video_ScanLines == false && video_Pixelate == false) {  zoom = 4; }
 if (video_Zoom == 3 && video_ScanLines == true  && video_Pixelate == false) {  zoom = 5; }
 if (video_Zoom == 3 && video_Pixelate  == true)                             {  zoom = 6; }
 SDL_Init(SDL_INIT_VIDEO);
 SDL_CreateWindowAndRenderer(SW, SH, 2, &window, &GPU_SCREEN);
 SDL_SetRenderDrawColor(GPU_SCREEN, 0, 0, 0, 255);
 SDL_RenderClear(GPU_SCREEN);
''' SDL_CreateWindowAndRenderer(SW*2, SH/2, 2, &window2, &INFO_SCREEN);
 SDL_SetRenderDrawColor(INFO_SCREEN, 0, 0, 0, 255);
 SDL_RenderClear(INFO_SCREEN);'''
 printf("EMU Notice: Screen Opened...\n");
 pthread_t call_CPU;
 pthread_create(&call_CPU, NULL, CPU_EXEC, 0);
 pthread_t call_CLOCK;
 pthread_create(&call_CLOCK, NULL, CPU_CLOCK, NULL);
 pthread_t call_Tick;
 pthread_create(&call_Tick, NULL, CPU_tick, NULL);
# clock_t EMU_clock = time(0);
 int gx = 0, gy = 0, ga = 1, zw = SW,zh = SH;
 crash = true; #when the EMU crashes it'll know if it was a crash or a exit
 while (Exit == false) {
  #SDL_GetCurrentDisplayMode();
  #printf("ga: %d\n",ga);
  if (zoom >= 1 && zoom <= 3) {
   if (zw != SW*2 || zh != SH*2) {
    SDL_SetWindowSize(window, SW*2, SH*2);
    zw = SW*2,zh = SH*2;
    ga = 2;
   }
  } else if (zoom >= 4 && zoom <= 6) {
   if (zw != SW*3 || zh != SH*3) {
    SDL_SetWindowSize(window, SW*3, SH*3);
    zw = SW*3,zh = SH*3;
    ga = 3;
   }
  } else if (zoom >= 7 && zoom <= 9) {
   if (zw != SW*4 || zh != SH*4) {
    SDL_SetWindowSize(window, SW*4, SH*4);
    zw = SW*4,zh = SH*4;
    ga = 4;
   }
  }
  ''' ############# GPU ############# '''
  #printf("p == %d\n",p);
  if (p == false) {
   GPU.run = true;
   getChar("Please drop a file or provide a", SW/2-15*8, SH/2-4, 255,255,255,true,true);
   getChar("file in the terminal command...", SW/2-15*8, SH/2+4, 255,255,255,true,true);
  } else {
   if (CPU.running == true && CPU.pause == false) {
    getChar("```````````````````````````````", SW/2-15*8, SH/2-8,   0,  0,  0,false,true);
    getChar("```````````````````````````````", SW/2-15*8, SH/2  ,   0,  0,  0,false,true);
    getChar("```````````````````````````````", SW/2-15*8, SH/2+8,   0,  0,  0,false,true);
    getChar("```````````````````````````````", SW/2-15*8, SH/2-4,   0,  0,  0,false,true);
   }
  }
  if (Title_lock == false) {
   #printf("ROM Title: %s\n",Title_Name);
   SDL_SetWindowTitle(window,Title_Name);
   Title_lock = true;
  }
  SDL_SetRenderDrawColor(GPU_SCREEN, 0, 0, 0, 255);
  SDL_RenderClear(GPU_SCREEN);
  gx = 0; gy = 0;
  #printf("%d\n",zoom);
  #ZOOM INFO
  #0 - normal
  #1 - 2x
  #2 - scanlines (2x)
  #3 - pixelated (2x)
  #4 - 3x
  #5 - scanlines (3x)
  #6 - pixelated (3x)
  SDL_SetRenderDrawColor(GPU_SCREEN,0x7F,0x7F,0x7F,0xFF);
  for (int y=0;y<zh;y++) {
   for (int x=0;x<zw;x++) {
    SDL_RenderDrawPoint(GPU_SCREEN, x, y);
   }
  }
  for (int y=0;y<SH*ga;y=y+ga) {
   for (int x=0;x<SW*ga;x=x+ga) {
    SDL_SetRenderDrawColor(GPU_SCREEN,   screen[gx][gy][0],    screen[gx][gy][1],    screen[gx][gy][2],   255);
    SDL_RenderDrawPoint(GPU_SCREEN, x, y);
    if (zoom == 1) { #2x video
     SDL_RenderDrawPoint(GPU_SCREEN, x+1, y  );
     SDL_RenderDrawPoint(GPU_SCREEN, x,   y+1);
     SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+1);
    }
    if (zoom == 2) {
     SDL_RenderDrawPoint(GPU_SCREEN, x+1, y  );
     SDL_SetRenderDrawColor(GPU_SCREEN,  (screen[gx][gy][0]/4)|0x08,  (screen[gx][gy][1]/4)|0x08,  (screen[gx][gy][2]/4)|0x08, 255);
     SDL_RenderDrawPoint(GPU_SCREEN, x,   y+1);
     SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+1);
    }
    if (zoom == 3) {
     SDL_SetRenderDrawColor(GPU_SCREEN,  (screen[gx][gy][0]/4)|0x08,  (screen[gx][gy][1]/4)|0x08,  (screen[gx][gy][2]/4)|0x08, 255);
     SDL_RenderDrawPoint(GPU_SCREEN, x+1, y  );
     SDL_RenderDrawPoint(GPU_SCREEN, x,   y+1);
     SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+1);
    }
    if (zoom == 4) { #3x video
     SDL_RenderDrawPoint(GPU_SCREEN, x+1, y  );
     SDL_RenderDrawPoint(GPU_SCREEN, x+2, y  );
     SDL_RenderDrawPoint(GPU_SCREEN, x,   y+1);
     SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+1);
     SDL_RenderDrawPoint(GPU_SCREEN, x+2, y+1);
     SDL_RenderDrawPoint(GPU_SCREEN, x,   y+2);
     SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+2);
     SDL_RenderDrawPoint(GPU_SCREEN, x+2, y+2);
    }
    if (zoom == 5) {
     SDL_RenderDrawPoint(GPU_SCREEN, x+1, y  );
     SDL_RenderDrawPoint(GPU_SCREEN, x+2, y  );
     SDL_RenderDrawPoint(GPU_SCREEN, x,   y+1);
     SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+1);
     SDL_RenderDrawPoint(GPU_SCREEN, x+2, y+1);
     SDL_SetRenderDrawColor(GPU_SCREEN,  (screen[gx][gy][0]/4)|0x08,  (screen[gx][gy][1]/4)|0x08,  (screen[gx][gy][2]/4)|0x08, 255);
     SDL_RenderDrawPoint(GPU_SCREEN, x,   y+2);
     SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+2);
     SDL_RenderDrawPoint(GPU_SCREEN, x+2, y+2);
    }
    if (zoom == 6) {
     SDL_RenderDrawPoint(GPU_SCREEN, x+1, y  );
     SDL_RenderDrawPoint(GPU_SCREEN, x,   y+1);
     SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+1);
     SDL_SetRenderDrawColor(GPU_SCREEN,  (screen[gx][gy][0]/4)|0x08,  (screen[gx][gy][1]/4)|0x08,  (screen[gx][gy][2]/4)|0x08, 255);
     SDL_RenderDrawPoint(GPU_SCREEN, x+2, y+1);
     SDL_RenderDrawPoint(GPU_SCREEN, x+2, y  );
     SDL_RenderDrawPoint(GPU_SCREEN, x,   y+2);
     SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+2);
     SDL_RenderDrawPoint(GPU_SCREEN, x+2, y+2);
    }
    SDL_SetRenderDrawColor(GPU_SCREEN,   screen[gx][gy][0],    screen[gx][gy][1],    screen[gx][gy][2],   255);
    if (enableOL == true && overlay[gx][gy][3] == 1) {
     SDL_SetRenderDrawColor(GPU_SCREEN,  overlay[gx][gy][0],   overlay[gx][gy][1],   overlay[gx][gy][2],   255);
     SDL_RenderDrawPoint(GPU_SCREEN, x, y);
     if (zoom == 1) { #2x video
      SDL_RenderDrawPoint(GPU_SCREEN, x+1, y  );
      SDL_RenderDrawPoint(GPU_SCREEN, x,   y+1);
      SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+1);
     }
     if (zoom == 2) {
      SDL_RenderDrawPoint(GPU_SCREEN, x+1, y  );
      SDL_SetRenderDrawColor(GPU_SCREEN,  (overlay[gx][gy][0]/4)|0x08,  (overlay[gx][gy][1]/4)|0x08,  (overlay[gx][gy][2]/4)|0x08, 255);
      SDL_RenderDrawPoint(GPU_SCREEN, x,   y+1);
      SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+1);
     }
     if (zoom == 3) {
      SDL_SetRenderDrawColor(GPU_SCREEN,  (overlay[gx][gy][0]/4)|0x08,  (overlay[gx][gy][1]/4)|0x08,  (overlay[gx][gy][2]/4)|0x08, 255);
      SDL_RenderDrawPoint(GPU_SCREEN, x+1, y  );
      SDL_RenderDrawPoint(GPU_SCREEN, x,   y+1);
      SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+1);
     }
     if (zoom == 4) { #3x video
      SDL_RenderDrawPoint(GPU_SCREEN, x+1, y  );
      SDL_RenderDrawPoint(GPU_SCREEN, x+2, y  );
      SDL_RenderDrawPoint(GPU_SCREEN, x,   y+1);
      SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+1);
      SDL_RenderDrawPoint(GPU_SCREEN, x+2, y+1);
      SDL_RenderDrawPoint(GPU_SCREEN, x,   y+2);
      SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+2);
      SDL_RenderDrawPoint(GPU_SCREEN, x+2, y+2);
     }
     if (zoom == 5) {
      SDL_RenderDrawPoint(GPU_SCREEN, x+1, y  );
      SDL_RenderDrawPoint(GPU_SCREEN, x+2, y  );
      SDL_RenderDrawPoint(GPU_SCREEN, x,   y+1);
      SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+1);
      SDL_RenderDrawPoint(GPU_SCREEN, x+2, y+1);
      SDL_SetRenderDrawColor(GPU_SCREEN,  (overlay[gx][gy][0]/4)|0x08,  (overlay[gx][gy][1]/4)|0x08,  (overlay[gx][gy][2]/4)|0x08, 255);
      SDL_RenderDrawPoint(GPU_SCREEN, x,   y+2);
      SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+2);
      SDL_RenderDrawPoint(GPU_SCREEN, x+2, y+2);
     }
     if (zoom == 6) {
      SDL_RenderDrawPoint(GPU_SCREEN, x+1, y  );
      SDL_RenderDrawPoint(GPU_SCREEN, x,   y+1);
      SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+1);
      SDL_SetRenderDrawColor(GPU_SCREEN,  (overlay[gx][gy][0]/4)|0x08,  (overlay[gx][gy][1]/4)|0x08,  (overlay[gx][gy][2]/4)|0x08, 255);
      SDL_RenderDrawPoint(GPU_SCREEN, x+2, y+1);
      SDL_RenderDrawPoint(GPU_SCREEN, x+2, y  );
      SDL_RenderDrawPoint(GPU_SCREEN, x,   y+2);
      SDL_RenderDrawPoint(GPU_SCREEN, x+1, y+2);
      SDL_RenderDrawPoint(GPU_SCREEN, x+2, y+2);
     }
     SDL_SetRenderDrawColor(GPU_SCREEN,   overlay[gx][gy][0],   overlay[gx][gy][1],   overlay[gx][gy][2],   255);
    } gx++;
    SDL_RenderDrawPoint(GPU_SCREEN, x, y);
   }gy++; gx = 0;
  }
  if (GPU.run == true) {
   if (frames < FPSLimmit) {
    if (CPU.debug == true && CPU.running == true && CPU.pause == false && p == true) { printf("GPU: update"); }
    for (int y=0;y<SH;y++) {
     for (int x=0;x<SW;x++) {
      screen[x][y][0] = buffer[x][y][0];
      screen[x][y][1] = buffer[x][y][1];
      screen[x][y][2] = buffer[x][y][2];
     }
    }
    frames++;
   } else if (CPU.debug == true) { printf("GPU: update skip'd\n"); }
   GPU.run = false;
  }
  SDL_RenderPresent(GPU_SCREEN);
  #if (ShowFPS == true) {
#   bool* ShowFPS;
   #getChar("TEST", 25, SH-26, 256,128,132,true,true);
   #getChar("TEST", 26, SH-25, 8,8,8,true,true);
  #}
  ''' ############ INPUT ############ '''
  const Uint8 *keystates = SDL_GetKeyboardState(NULL);
  gotUIn = false;
  while(SDL_PollEvent(&event)) {
   #Player 1#
   if (keystates[input0_A])      { UInput[ 0][0] = true; } else { UInput[ 0][0] = false; }
   if (keystates[input0_B])      { UInput[ 1][0] = true; } else { UInput[ 1][0] = false; }
   if (keystates[input0_C])      { UInput[ 2][0] = true; } else { UInput[ 2][0] = false; }
   if (keystates[input0_X])      { UInput[ 3][0] = true; } else { UInput[ 3][0] = false; }
   if (keystates[input0_Y])      { UInput[ 4][0] = true; } else { UInput[ 4][0] = false; }
   if (keystates[input0_Z])      { UInput[ 5][0] = true; } else { UInput[ 5][0] = false; }
   if (keystates[input0_L])      { UInput[ 6][0] = true; } else { UInput[ 6][0] = false; }
   if (keystates[input0_R])      { UInput[ 7][0] = true; } else { UInput[ 7][0] = false; }
   if (keystates[input0_Start])  { UInput[ 8][0] = true; } else { UInput[ 8][0] = false; }
   if (keystates[input0_Select]) { UInput[ 9][0] = true; } else { UInput[ 9][0] = false; }
   if (keystates[input0_Up])     { UInput[10][0] = true; } else { UInput[10][0] = false; }
   if (keystates[input0_Down])   { UInput[11][0] = true; } else { UInput[11][0] = false; }
   if (keystates[input0_Left])   { UInput[12][0] = true; } else { UInput[12][0] = false; }
   if (keystates[input0_Right])  { UInput[13][0] = true; } else { UInput[13][0] = false; }
   #Player 2#
   if (keystates[input1_A])      { UInput[ 0][1] = true; } else { UInput[ 0][1] = false; }
   if (keystates[input1_B])      { UInput[ 1][1] = true; } else { UInput[ 1][1] = false; }
   if (keystates[input1_C])      { UInput[ 2][1] = true; } else { UInput[ 2][1] = false; }
   if (keystates[input1_X])      { UInput[ 3][1] = true; } else { UInput[ 3][1] = false; }
   if (keystates[input1_Y])      { UInput[ 4][1] = true; } else { UInput[ 4][1] = false; }
   if (keystates[input1_Z])      { UInput[ 5][1] = true; } else { UInput[ 5][1] = false; }
   if (keystates[input1_L])      { UInput[ 6][1] = true; } else { UInput[ 6][1] = false; }
   if (keystates[input1_R])      { UInput[ 7][1] = true; } else { UInput[ 7][1] = false; }
   if (keystates[input1_Start])  { UInput[ 8][1] = true; } else { UInput[ 8][1] = false; }
   if (keystates[input1_Select]) { UInput[ 9][1] = true; } else { UInput[ 9][1] = false; }
   if (keystates[input1_Up])     { UInput[10][1] = true; } else { UInput[10][1] = false; }
   if (keystates[input1_Down])   { UInput[11][1] = true; } else { UInput[11][1] = false; }
   if (keystates[input1_Left])   { UInput[12][1] = true; } else { UInput[12][1] = false; }
   if (keystates[input1_Right])  { UInput[13][1] = true; } else { UInput[13][1] = false; }
   if (keystates[SDL_SCANCODE_ESCAPE]) {
    if (enableOL == true) {
     enableOL = false;
     printf("[EMU] enableOL: false\n");
    } else {
     enableOL = true;
     printf("[EMU] enableOL: true\n");
    } SDL_Delay(100);
   }
   if (keystates[SDL_SCANCODE_F4]) {
    if (Fullscreen == true) {
     Fullscreen = false;
     printf("[EMU] Fullscreen: False\n");
    } else {
     Fullscreen = true;
     printf("[EMU] Fullscreen: True\n"); 
    } SDL_SetWindowFullscreen(window, Fullscreen); SDL_Delay(100);
    SDL_RenderSetScale(window, display.w/SW,display.h/SH);
   }
   if (keystates[SDL_SCANCODE_LCTRL] && keystates[SDL_SCANCODE_D]) {
    if (CPU.debug == true) {
     CPU.debug = false;
     printf("\n\n[EMU] CPU.debug: False\n");
    } else {
     CPU.debug = true;
     printf(    "[EMU] CPU.debug: True\n"); 
    } SDL_Delay(100);
   }
   if ((keystates[SDL_SCANCODE_LCTRL] && keystates[SDL_SCANCODE_P] || keystates[SDL_SCANCODE_PAUSE]) && CPU.running == true) {
    if (CPU.pause == true) {
     CPU.pause = false;
     printf("[EMU] CPU.pause: False\n"); 
     getChar("```````````````", SW/2-7*8, SH/2-8,   0,   0,   0, false,false);
     getChar("```````````````", SW/2-7*8, SH/2,     0,   0,   0, false,false);
     getChar("```````````````", SW/2-7*8, SH/2+8,   0,   0,   0, false,false);
    } else {
     CPU.pause = true;
     printf("[EMU] CPU.pause: True\n"); 
     getChar("```````````````", SW/2-7*8, SH/2-8,  16,  16, 255, true, false);
     getChar("```````````````", SW/2-7*8, SH/2,    16,  16, 255, true, false);
     getChar("```````````````", SW/2-7*8, SH/2+8,  16,  16, 255, true, false);
     getChar("+----[EMU]----+", SW/2-7*8, SH/2-8, 128, 128, 255, true,  true);
     getChar("|CPU PAUSED...|", SW/2-7*8, SH/2,   128, 128, 255, true,  true);
     getChar("+-------------+", SW/2-7*8, SH/2+8, 128, 128, 255, true,  true);
    } SDL_Delay(500);
   }
   if (keystates[SDL_SCANCODE_LCTRL] && keystates[SDL_SCANCODE_I]) {
    if (HUDinfo == true) {
     HUDinfo = false;
     printf("EMU: [HUD Info: False]\n");
     getChar("``````````````````````````````````````````````````````````",  2*8,      2*8, 128, 255, 128, false, false);
     getChar("``````````````````````````````````````````````````````````",  2*8, SH-(4*8),   0,   0,   0, false, false);
     getChar("``````````````````````````````````````````````````````````",  1*8, SH-(5*8),   0,   0,   0, false, false);
     getChar("````````````````````````````````````````````````````",        2*8, SH-(3*8),   0,   0,   0, false, false);
     getChar("````````````````````````````````````````````````````",        2*8, SH-(2*8),   0,   0,   0, false,  true);
    } else {
     HUDinfo = true;
     printf("EMU: [HUD Info: True]\n");
    } SDL_Delay(100);
   }
   if (keystates[SDL_SCANCODE_LCTRL] && keystates[SDL_SCANCODE_C]) {
    if (ShowInput == true) {
     ShowInput = false;
     printf("[EMU] Show Controller Input: False\n");
     getChar("````````````````````````````````````````````````````",        2*8, SH-(3*8),   0,   0,   0, false, false);
     getChar("````````````````````````````````````````````````````",        2*8, SH-(2*8),   0,   0,   0, false,  true);
    } else {
     ShowInput = true;
     printf("[EMU] Show Controller Input: True\n");
    } SDL_Delay(100);
   }
   if (keystates[SDL_SCANCODE_LCTRL] && keystates[SDL_SCANCODE_R]) {
    char TN[1024] = "TheGameRazer - [NO ROM]"; for (int i=0;i<23;i++) { Title_Name[i] = TN[i]; } Title_lock = false;
    getChar("```````````````````````````````", SW/2-15*8, SH/2-8,   0,  0,  0,false,true);
    getChar("```````````````````````````````", SW/2-15*8, SH/2,     0,  0,  0,false,true);
    getChar("```````````````````````````````", SW/2-15*8, SH/2+8,   0,  0,  0,false,true);
    p = true;
    CPU.IP = 0;
    CPU.IPC = 0;
    CPU.pause = false;
    FPS = 0;
    for (int i=0;i<8;i++) { CPU.REGs[i] = 0; }
#    CPU.IPC = 12000000; #### THIS IS HERE TO FIX A PROBBLEM WITH THE TOTALRAN COUNT ###
    CPU.reset = false;
    if (keystates[SDL_SCANCODE_LSHIFT] || CPU.running == false) {
     CPU.TI = 0;
     CPU.running = false;
     printf("--------[[EMU-HARD-RESTART]]--------\n");
     GPU_reset();
     CPU.running = true;
     pthread_create(&call_CPU, NULL, CPU_EXEC, NULL);
    } else {
     printf("--------[[EMU-SOFT-RESTART]]--------\n");
     CPU.reset = true;
    } SDL_Delay(100);
   }
   if (keystates[SDL_SCANCODE_LCTRL] && keystates[SDL_SCANCODE_Q]) { crash = false; Exit = true; }
   switch(event.type) {
#    case SDL_KEYDOWN:
#     printf("Oh! Key press: %d\n",event.type);
#     break;
    case SDL_QUIT:
     crash = false;
     Exit = true;
     break;
    
    case (SDL_DROPFILE):
     dropped_filedir = event.drop.file;
     CPU.running = false;
     printf("EMU Notice: Switching ROM to: %s\n",dropped_filedir);
     char TN[1024] = "TheGameRazer - [NO ROM]"; for (int i=0;i<23;i++) { Title_Name[i] = TN[i]; } Title_lock = false;
     getChar("```````````````````````````````", SW/2-15*8, SH/2-4,   0,  0,  0,false,true);
     getChar("```````````````````````````````", SW/2-15*8, SH/2+4,   0,  0,  0,false,true);
     p = true;
     GPU_reset();
     CPU.pause = false;
     CPU.IP = 0;
     CPU.TI = 0;
     CPU.IPC = 0;
     CPU.SP = NULL;
     CPU.BP = NULL;
     FPS = 0;
     for (int i=0;i<8;i++) { CPU.REGs[i] = 0; }
     CPU.IPC = 12000000; #### THIS IS HERE TO FIX A PROBBLEM WITH THE TOTALRAN COUNT ###
     CPU.reset = false;
     printf("--------[[EMU-HARD-RESTART]]--------\n");
     GPU_reset();
     CPU.running = true;
     pthread_create(&call_CPU, NULL, CPU_EXEC, 0);
     MsgTimer = 100;
     memset(Message,0,strlen(Message));
     strcat(Message,"LOADED ROM: ");
     strcat(Message,dropped_filedir);
     break;
   }
   if (keystates[SDL_SCANCODE_LCTRL] && keystates[SDL_SCANCODE_O]) {
    #0: Load ROM
    dropped_filedir = openGUI(0);
    printf("%s\n",dropped_filedir);
    if (dropped_filedir != NULL) {
     CPU.running = false;
     printf("EMU Notice: Switching ROM to: %s\n",dropped_filedir);
     char TN[1024] = "TheGameRazer - [NO ROM]"; for (int i=0;i<23;i++) { Title_Name[i] = TN[i]; } Title_lock = false;
     getChar("```````````````````````````````", SW/2-15*8, SH/2-4,   0,  0,  0,false,true);
     getChar("```````````````````````````````", SW/2-15*8, SH/2+4,   0,  0,  0,false,true);
     p = true;
     GPU_reset();
     CPU.pause = false;
     CPU.IP = 0;
     CPU.TI = 0;
     CPU.IPC = 0;
     CPU.SP = NULL;
     CPU.BP = NULL;
     FPS = 0;
     for (int i=0;i<8;i++) { CPU.REGs[i] = 0; }
     CPU.IPC = 12000000; #### THIS IS HERE TO FIX A PROBBLEM WITH THE TOTALRAN COUNT ###
     CPU.reset = false;
     printf("--------[[EMU-HARD-RESTART]]--------\n");
     GPU_reset();
     CPU.running = true;
     pthread_create(&call_CPU, NULL, CPU_EXEC, 0);
     MsgTimer = 100;
     memset(Message,0,strlen(Message));
     strcat(Message,"LOADED ROM: ");
     strcat(Message,dropped_filedir);
    } SDL_Delay(100); dropped_filedir = "";
   }
'''   if (keystates[SDL_SCANCODE_LCTRL] && keystates[SDL_SCANCODE_L]) {
    #1: Load SaveState as ..
    FileStruct ROM = load(openGUI(1),0);
    #2: Save SaveState as ..
    #3: export V/RAM dump as HEX in ASCII(will cause lag)
    CPU.running = false;
    printf("EMU Notice: Switching ROM to: %s\n",dropped_filedir);
    char TN[1024] = "TheGameRazer - [NO ROM]"; for (int i=0;i<23;i++) { Title_Name[i] = TN[i]; } Title_lock = false;
    getChar("```````````````````````````````", SW/2-15*8, SH/2-4,   0,  0,  0,false,true);
    getChar("```````````````````````````````", SW/2-15*8, SH/2+4,   0,  0,  0,false,true);
    p = true;
    GPU_reset();
    int StateLoc = 0;
    CPU.pause = State.data[StateLoc++];
    #       8        16       24       32
    CPU.IP = State.data[StateLoc++]>>8)|State.data[StateLoc++] State.data[StateLoc++] State.data[StateLoc++];
    CPU.TI = 0;
    CPU.IPC = 0;
    CPU.SP = ;
    CPU.BP = NULL;
    FPS = 0;
    
    for (int i=0;i<8;i++) { CPU.REGs[i] = 0; }
    for (int i=0;i<8;i++) { CPU.REGs[i] = 0; }
    for (int i=0;i<8;i++) { CPU.REGs[i] = 0; }
    CPU.IPC = 12000000; #### THIS IS HERE TO FIX A PROBBLEM WITH THE TOTALRAN COUNT ###
    CPU.reset = false;
    printf("--------[[EMU-HARD-RESTART]]--------\n");
    GPU_reset();
    CPU.running = true;
    pthread_create(&call_CPU, NULL, CPU_EXEC, 0);
    MsgTimer = 100;
    memset(Message,0,strlen(Message));
    strcat(Message,"LOADED ROM: ");
    strcat(Message,dropped_filedir);
   } SDL_Delay(100);'''
  }
  gotUIn = true;
  if (p == true) {
   if (MsgTimer > 0) {
    if (MsgTimer == 1) {
     getChar("``````````````````````````````````````````````````````````", 2*8, 2*8, 128,255,128, false,true);
     memset(Message,0,strlen(Message));
     #for (int i=0;i<256;i++) { Message[i] = ""; } free(*Message);
    }
    #printf("%d, \"%s\"\n",MsgTimer,Message);
    if (Message != "") {
     getChar(Message, 2*8, 2*8, 128, 255, 128, true,true);
    } MsgTimer--;
   }
   #if (FPS > 0) { SDL_Delay(FPS/12000000); }
   getChar("``````````````````````````````````````````````````````````",  2*8, SH-(7*8),   0,   0,   0, false, false);
   getChar("``````````````````````````````````````````````````````````",  2*8, SH-(4*8),   0,   0,   0, false, false);
   getChar("``````````````````````````````````````````````````````````",  1*8, SH-(6*8),   0,   0,   0, false, false);
   getChar("``````````````````````````````````````````````````````````",  1*8, SH-(5*8),   0,   0,   0, false, false);
   #FPS,128,"RAM POINTER: 0x%x/%d | STACK POINTER: 0x%x/%d | STACK BASE: 0x%x/%d",CPU.RP,CPU.RP,CPU.SP,CPU.SP,CPU.BP,CPU.BP);
   if (HUDinfo == false) {
    char TFPS[255]; snprintf(TFPS,128,"FPS: %d",FPS);
    getChar(TFPS,          2*8, SH-(4*8), 255, 128, 128,  true,  true);
   } else {
    char TFPS[255]; snprintf(TFPS,128,"FPS: %d | IPS: %d(%.2lf%%) | TotalRan: %ld",FPS,IPS,RunQuality,TIPS);
    getChar(TFPS,          2*8, SH-(4*8), 255, 128, 128,  true,  true);
       
    #                " RAM Usage: 134217727 bytes/134217727 (100.00% full) | VRAM Usage: 67108863 bytes/67108863 (100.00% full)"
    snprintf(TFPS,128, "RAMPOS: 0x%x/%d",CPU.RP,CPU.RP);
    getChar(TFPS,                2*8, SH-(7*8), 255, 128, 128,  true,  true);
    snprintf(TFPS,128, " RAM Usage: %.0lf/%d bytes(%.2lf%% full)", RAMUsage, RAMSIZ+1,( RAMUsage/ RAMSIZ)*100);
    getChar(TFPS,                1*8, SH-(6*8), 255, 128, 128,  true,  true);
    if (VRAMUsage > 9) {
     snprintf(TFPS,128,"VRAM Usage:  %.0lf/%d bytes(%.2lf%% full)",VRAMUsage,VRAMSIZ+1,(VRAMUsage/VRAMSIZ)*100);
    } else {
     snprintf(TFPS,128,"VRAM Usage: %.0lf/ %d bytes(%.2lf%% full)",VRAMUsage,VRAMSIZ+1,(VRAMUsage/VRAMSIZ)*100);
    }
    getChar(TFPS,                1*8, SH-(5*8), 255, 128, 128,  true,  true);
   }
   if (ShowInput == true) {
    getChar("````````````````````````````````````````````````````", 2*8, SH-(3*8),   0,   0,   0, false, false);
#  getChar("P1: A B C X Y Z L R Start Select Up Down Left Right", 2*8, SH-(3*8), 0, 0, 0, 0);
    getChar("P1:[                                               ]", 2*8, SH-(3*8),  64,  64, 255,  true,  true);
    if (UInput[ 0][0] == true) { getChar("A",       6*8, SH-(3*8),  64,  64, 255, 1,true); }
    if (UInput[ 1][0] == true) { getChar("B",       8*8, SH-(3*8),  64,  64, 255, 1,true); }
    if (UInput[ 2][0] == true) { getChar("C",      10*8, SH-(3*8),  64,  64, 255, 1,true); }
    if (UInput[ 3][0] == true) { getChar("X",      12*8, SH-(3*8),  64,  64, 255, 1,true); }
    if (UInput[ 4][0] == true) { getChar("Y",      14*8, SH-(3*8),  64,  64, 255, 1,true); }
    if (UInput[ 5][0] == true) { getChar("Z",      16*8, SH-(3*8),  64,  64, 255, 1,true); }
    if (UInput[ 6][0] == true) { getChar("L",      18*8, SH-(3*8),  64,  64, 255, 1,true); }
    if (UInput[ 7][0] == true) { getChar("R",      20*8, SH-(3*8),  64,  64, 255, 1,true); }
    if (UInput[ 8][0] == true) { getChar("START",  22*8, SH-(3*8),  64,  64, 255, 1,true); }
    if (UInput[ 9][0] == true) { getChar("SELECT", 28*8, SH-(3*8),  64,  64, 255, 1,true); }
    if (UInput[10][0] == true) { getChar("UP",     35*8, SH-(3*8),  64,  64, 255, 1,true); }
    if (UInput[11][0] == true) { getChar("DOWN",   38*8, SH-(3*8),  64,  64, 255, 1,true); }
    if (UInput[12][0] == true) { getChar("LEFT",   43*8, SH-(3*8),  64,  64, 255, 1,true); }
    if (UInput[13][0] == true) { getChar("RIGHT",  48*8, SH-(3*8),  64,  64, 255, 1,true); }
    getChar("````````````````````````````````````````````````````", 2*8, SH-(2*8), 0, 0, 0, 0,true);
#  getChar("P2: A B C X Y Z L R Start Select Up Down Left Right", 2*8, SH-(3*8), 0, 0, 0, 0);
    getChar("P2:[                                               ]", 2*8, SH-(2*8),  64,  64, 255, 1,true);
    if (UInput[ 0][1] == true) { getChar("A",       6*8, SH-(2*8),  64,  64, 255, 1,true); }
    if (UInput[ 1][1] == true) { getChar("B",       8*8, SH-(2*8),  64,  64, 255, 1,true); }
    if (UInput[ 2][1] == true) { getChar("C",      10*8, SH-(2*8),  64,  64, 255, 1,true); }
    if (UInput[ 3][1] == true) { getChar("X",      12*8, SH-(2*8),  64,  64, 255, 1,true); }
    if (UInput[ 4][1] == true) { getChar("Y",      14*8, SH-(2*8),  64,  64, 255, 1,true); }
    if (UInput[ 5][1] == true) { getChar("Z",      16*8, SH-(2*8),  64,  64, 255, 1,true); }
    if (UInput[ 6][1] == true) { getChar("L",      18*8, SH-(2*8),  64,  64, 255, 1,true); }
    if (UInput[ 7][1] == true) { getChar("R",      20*8, SH-(2*8),  64,  64, 255, 1,true); }
    if (UInput[ 8][1] == true) { getChar("START",  22*8, SH-(2*8),  64,  64, 255, 1,true); }
    if (UInput[ 9][1] == true) { getChar("SELECT", 28*8, SH-(2*8),  64,  64, 255, 1,true); }
    if (UInput[10][1] == true) { getChar("UP",     35*8, SH-(2*8),  64,  64, 255, 1,true); }
    if (UInput[11][1] == true) { getChar("DOWN",   38*8, SH-(2*8),  64,  64, 255, 1,true); }
    if (UInput[12][1] == true) { getChar("LEFT",   43*8, SH-(2*8),  64,  64, 255, 1,true); }
    if (UInput[13][1] == true) { getChar("RIGHT",  48*8, SH-(2*8),  64,  64, 255, 1,true); }
    #if (CPU.running == false && dropped_filedir != "") { Exit = true; printf("-1\n"); }
   }
  }
  #SDL_Delay(((FPS/60)/100));
'''
############# NEEDS FIXED #############
  SDL_SetRenderDrawColor(INFO_SCREEN,   0,   0,   0, 255);
  SDL_RenderClear(INFO_SCREEN);
  SDL_SetRenderDrawColor(INFO_SCREEN,   0, 255,   0, 255);
  for(int x=0; x<SW*2;x++) {
   SDL_RenderDrawPoint(INFO_SCREEN, x, ((float)info_scr[x]/12000000)/SH);
   if (x > 0 && x < (SW*2)-1) { info_scr[x-1] = info_scr[x]; }
   if (x == (SW*2)-1) { info_scr[x] = (CPU.IPC/12000000)*(SH/2); }
  }
  printf("%d, %d, %d, %f\n", info_scr[SW*2-1], info_scr[SW*2-1]/12000000, CPU.IPC, CPU.IPC/12000000);
  SDL_RenderPresent(INFO_SCREEN);'''
 }
 if (argc < 2 && crash == true) { SDL_ShowSimpleMessageBox(SDL_MESSAGEBOX_INFORMATION,"TheGameRazer [[HALT DETECTED]]","\nEMU: We have detected the main loop has stopped due to a halt...\n\nThis halt is due to the program has ended or due to a Emulation Error.\nIf there is a Emulation Error check in the terminal for what the problem is in the ROM.\n/!\\Reminder: check the ROM before reporting EMU probblems/!\\",window); }
 SDL_DestroyRenderer(GPU_SCREEN);
 SDL_DestroyWindow(window);
 SDL_Quit();
 printf("EMU Notice: Screen Closed...\n");
 if (crash == true) {
  printf("\nEMU: We have detected the main loop has stopped due to a halt...\n\nThis halt is due to the program has ended or due to a Emulation Error.\nIf there is a Emulation Error check above for what the problem is in the ROM.\n/!\\Reminder: check the ROM before reporting EMU probblems/!\\\n");
 }
 #printf("The screen isn't active but is can still be viewed, to reset the emulator you need to goto your\n terminal and press [CTRL] + [C] and relaunch.");
 #printf("TIP: pressing [CTRL] + [M] will list RAM from RenderRAMPOS + 0x0000 to RenderRAMPOS + 0x02FF\n same with VideoRAM by pressing [CTRL] + [V]...\n and pressing [CTRL] + [KeyPad+] or [CTRL] + [KeyPad-] will adjust RenderRAMPOS by 0x10");
 printf("\nTotal ran instructions: %ld\n\n",CPU.TI);
 return 0;
}

#right val nibble = byte & 0xF;
#left  val nibble = byte >> 4;

void getChar(char* Letter, int x, int y, int R, int G, int B, bool A, bool shadow) {
 for (int i=0;i<strlen(Letter);i++) {
  int j = 0;
  for (j=0;j<98;j++) {
   #if (j == 70) { j = 0; break; }
   if (Letter[i] == chars[j]) { break; }
  }
  for (int ix=0;ix<8;ix++) {
   for (int iy=0;iy<8;iy++) {
    if (font[j][iy][ix] == '1' && (i*8)+x+ix >= 0 && (i*8)+x+ix < SW && y+iy >= 0 && y+iy < SH) {
     if (shadow == true) {
      overlay[(i*8)+x+ix+1][y+iy+1][0] = 0;
      overlay[(i*8)+x+ix+1][y+iy+1][1] = 0;
      overlay[(i*8)+x+ix+1][y+iy+1][2] = 0;
      overlay[(i*8)+x+ix+1][y+iy+1][3] = (int)A;
     }
     overlay[(i*8)+x+ix][y+iy][0] = R;
     overlay[(i*8)+x+ix][y+iy][1] = G;
     overlay[(i*8)+x+ix][y+iy][2] = B;
     overlay[(i*8)+x+ix][y+iy][3] = (int)A;
    }
   }
  }
 }
}
# `ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-+_=[]{}\|;:'".,<>/?~abcdefghijklmnopqrstuvwxyz
char chars[95] = " `ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-+_=[]{}\\|;:'\".,<>/?~abcdefghijklmnopqrstuvwxyz";
char *font[95][8] = {
 {"00000000","00000000","00000000","00000000","00000000","00000000","00000000","00000000"},#   00
 {"11111111","11111111","11111111","11111111","11111111","11111111","11111111","11111111"},# `█01
 {"00111100","01000010","01000010","01111110","01000010","01000010","01000010","00000000"},# A 02
 {"01111100","01000010","01000010","01111100","01000010","01000010","01111100","00000000"},# B 03
 {"00111100","01000010","01000000","01000000","01000000","01000010","00111100","00000000"},# C 04
 {"01111100","01000010","01000010","01000010","01000010","01000010","01111100","00000000"},# D 05
 {"01111110","01000000","01000000","01111100","01000000","01000000","01111110","00000000"},# E 06
 {"01111110","01000000","01000000","01111100","01000000","01000000","01000000","00000000"},# F 07
 {"00111100","01000010","01000000","01001110","01000010","01000010","00111100","00000000"},# G 08
 {"01000010","01000010","01000010","01111110","01000010","01000010","01000010","00000000"},# H 09
 {"01111110","00011000","00011000","00011000","00011000","00011000","01111110","00000000"},# I 10
 {"01111110","00000100","00000100","00000100","00000100","01000100","00111000","00000000"},# J 11
 {"01000100","01001000","01010000","01100000","01010000","01001000","01000100","00000000"},# K 12
 {"01000000","01000000","01000000","01000000","01000000","01000000","01111110","00000000"},# L 13
 {"01000010","01100110","01100110","01011010","01011010","01000010","01000010","00000000"},# M 14
 {"01000010","01100010","01010010","01001010","01000110","01000010","01000010","00000000"},# N 15
 {"00111100","01000010","01000010","01000010","01000010","01000010","00111100","00000000"},# O 16
 {"01111100","01000010","01000010","01111100","01000000","01000000","01000000","00000000"},# P 17
 {"00111100","01000010","01000010","01000010","01001010","01000110","00111110","00000000"},# Q 18
 {"01111100","01000010","01000010","01111100","01010000","01001000","01000100","00000000"},# R 19
 {"00111100","01000010","00100000","00011000","00000100","01000010","00111100","00000000"},# S 20
 {"01111110","00011000","00011000","00011000","00011000","00011000","00011000","00000000"},# T 21
 {"01000010","01000010","01000010","01000010","01000010","01000010","00111100","00000000"},# U 22
 {"01000010","01000010","01000010","01000010","00100100","00100100","00011000","00000000"},# V 23
 {"01010100","01010100","01010100","01010100","01010100","01010100","00101000","00000000"},# W 24
 {"01000010","01000010","00100100","00011000","00011000","00100100","01000010","00000000"},# X 25
 {"01000010","01000010","00100100","00011000","00011000","00011000","00011000","00000000"},# Y 26
 {"01111110","00000100","00001000","00010000","00100000","01000000","01111110","00000000"},# Z 27
 {"00111100","01000010","01100010","01011010","01000110","01000010","00111100","00000000"},# 0 28
 {"00001000","00011000","00001000","00001000","00001000","00001000","00001000","00000000"},# 1 29
 {"00111100","01000010","00000100","00001000","00010000","00100000","01111110","00000000"},# 2 30
 {"00111100","01000010","00000010","00001100","00000010","01000010","00111100","00000000"},# 3 31
 {"00000100","00001100","00010100","00100100","01111110","00000100","00000100","00000000"},# 4 32
 {"01111110","01000000","01000000","01111100","00000010","01000010","00111100","00000000"},# 5 33
 {"00111100","01000010","01000000","01111100","01000010","01000010","00111100","00000000"},# 6 34
 {"01111110","00000010","00000100","00000100","00001000","00001000","00010000","00000000"},# 7 35
 {"00111100","01000010","01000010","00111100","01000010","01000010","00111100","00000000"},# 8 36
 {"00111100","01000010","01000010","00111110","00000010","00000010","00111100","00000000"},# 9 37
 {"00001000","00001000","00001000","00001000","00001000","00000000","00001000","00000000"},# ! 38
 {"00111100","01000010","01110010","01101010","01110010","01011100","00111110","00000000"},# @ 39
 {"00000000","00100100","01111110","00100100","00100100","01111110","00100100","00000000"},# # 40
 {"00011000","00111100","01011010","00111000","00011100","01011010","00111100","00011000"},# $ 41
 {"01100001","10010010","10010100","01101000","00010110","00101001","01001001","10000110"},# % 42
 {"00011000","00100100","01000010","00000000","00000000","00000000","00000000","00000000"},# ^ 43
 {"00011000","00100100","00100100","00111010","01000100","01000100","00111010","00000000"},# & 44
 {"00101010","00011100","00111110","00011100","00101010","00000000","00000000","00000000"},# * 45
 {"00001100","00010000","00010000","00010000","00010000","00010000","00001100","00000000"},# ( 46
 {"00110000","00001000","00001000","00001000","00001000","00001000","00110000","00000000"},# ) 47
 {"00000000","00000000","00000000","01111110","01111110","00000000","00000000","00000000"},# - 48
 {"00000000","00011000","00011000","01111110","01111110","00011000","00011000","00000000"},# + 49
 {"00000000","00000000","00000000","00000000","00000000","00000000","00000000","11111111"},# _ 50
 {"00000000","00000000","01111110","00000000","00000000","01111110","00000000","00000000"},# = 51
 {"00011100","00010000","00010000","00010000","00010000","00010000","00011100","00000000"},# [ 52
 {"00111000","00001000","00001000","00001000","00001000","00001000","00111000","00000000"},# ] 53
 {"00011100","00010000","00010000","00100000","00010000","00010000","00011100","00000000"},# { 54
 {"00111000","00001000","00001000","00000100","00001000","00001000","00111000","00000000"},# } 55
 {"10000000","01000000","00100000","00010000","00001000","00000100","00000010","00000001"},# \ 56 /
 {"00011000","00011000","00011000","00011000","00011000","00011000","00011000","00011000"},# | 57
 {"00000000","00000000","00001000","00000000","00000000","00001000","00010000","00000000"},# ; 58
 {"00000000","00000000","00001000","00000000","00000000","00001000","00000000","00000000"},# : 59
 {"00001000","00001000","00000000","00000000","00000000","00000000","00000000","00000000"},# ' 60
 {"00100100","00100100","00000000","00000000","00000000","00000000","00000000","00000000"},# " 61
 {"00000000","00000000","00000000","00000000","00000000","00000000","00001000","00000000"},# . 62
 {"00000000","00000000","00000000","00000000","00000000","00000000","00001000","00010000"},# , 63
 {"00000000","00000110","00011000","01100000","00011000","00000110","00000000","00000000"},# < 64
 {"00000000","01100000","00011000","00000110","00011000","01100000","00000000","00000000"},# > 65
 {"00000001","00000010","00000100","00001000","00010000","00100000","01000000","10000000"},# / 66
 {"00111100","01000010","01000010","00001100","00001000","00000000","00001000","00000000"},# ? 67
 {"00000000","00000000","00000000","00110010","01001100","00000000","00000000","00000000"},# ~ 68
 {"00111100","01000010","01000010","01111110","01000010","01000010","01000010","00000000"},# A 69
 {"01111100","01000010","01000010","01111100","01000010","01000010","01111100","00000000"},# B 70
 {"00111100","01000010","01000000","01000000","01000000","01000010","00111100","00000000"},# C 71
 {"01111100","01000010","01000010","01000010","01000010","01000010","01111100","00000000"},# D 72
 {"01111110","01000000","01000000","01111100","01000000","01000000","01111110","00000000"},# E 73
 {"01111110","01000000","01000000","01111100","01000000","01000000","01000000","00000000"},# F 74
 {"00111100","01000010","01000000","01001110","01000010","01000010","00111100","00000000"},# G 75
 {"01000010","01000010","01000010","01111110","01000010","01000010","01000010","00000000"},# H 76
 {"01111110","00011000","00011000","00011000","00011000","00011000","01111110","00000000"},# I 77
 {"01111110","00000100","00000100","00000100","00000100","01000100","00111000","00000000"},# J 78
 {"01000100","01001000","01010000","01100000","01010000","01001000","01000100","00000000"},# K 79
 {"01000000","01000000","01000000","01000000","01000000","01000000","01111110","00000000"},# L 80
 {"01000010","01100110","01100110","01011010","01011010","01000010","01000010","00000000"},# M 81
 {"01000010","01100010","01010010","01001010","01000110","01000010","01000010","00000000"},# N 82
 {"00111100","01000010","01000010","01000010","01000010","01000010","00111100","00000000"},# O 83
 {"01111100","01000010","01000010","01111100","01000000","01000000","01000000","00000000"},# P 84
 {"00111100","01000010","01000010","01000010","01001010","01000110","00111110","00000000"},# Q 85
 {"01111100","01000010","01000010","01111100","01010000","01001000","01000100","00000000"},# R 86
 {"00111100","01000010","00100000","00011000","00000100","01000010","00111100","00000000"},# S 87
 {"01111110","00011000","00011000","00011000","00011000","00011000","00011000","00000000"},# T 88
 {"00000000","01000010","01000010","01000010","01000010","01000010","00111100","00000000"},# U 89
 {"01000010","01000010","01000010","00100100","00100100","00100100","00011000","00000000"},# V 90
 {"00000000","01010100","01010100","01010100","01010100","01010100","00101000","00000000"},# W 91
 {"00000000","01000010","00100100","00011000","00011000","00100100","01000010","00000000"},# X 92
 {"01000010","01000010","00100100","00011000","00011000","00011000","00011000","00000000"},# Y 93
 {"01111110","00000100","00001000","00010000","00100000","01000000","01111110","00000000"},# Z 94
};

char *openGUI(int type) {
 #0: Load ROM
 #1: Load SaveState as ..
 #2: Save SaveState as ..
 #3: export V/RAM dump as HEX in ASCII(will cause lag)
 char cmd[128];
 if        (type == 0) {
  if        (sysOS == 0) { #Windows
   strcpy(cmd, ".\\bin\\winOpen.bat ROM");
  } else if (sysOS == 1) { #Linux
   strcpy(cmd, "zenity --file-selection --file-filter=\"GameRazerROM(*.tgr)|*.tgr\" --title=\"\"");
  } else {
   return "error";
  }
 } else if (type == 1) {
  if        (sysOS == 0) { #Windows
   strcpy(cmd, ".\\bin\\winOpen.bat LTGRS");
  } else if (sysOS == 1) { #Linux
   strcpy(cmd, "zenity --file-selection --file-filter=\"GameRazerState(*.tgrs)|*.tgrs\" --title=\"Load TGRState\"");
  } else {
   return "error";
  }
 } else if (type == 2) {
  if        (sysOS == 0) { #Windows
   strcpy(cmd, ".\\bin\\winSave.bat STGRS");
  } else if (sysOS == 1) { #Linux
   strcpy(cmd, "zenity --file-selection --save --file-filter=\"GameRazerState(*.tgrs)|*.tgrs\" --title=\"Save TGRState\"");
  } else {
   return "error";
  }
 } else if (type == 3) {
  if        (sysOS == 0) { #Windows
   strcpy(cmd, ".\\bin\\winSave.bat V-RAM");
  } else if (sysOS == 1) { #Linux
   strcpy(cmd, "zenity --file-selection --save --file-filter=\"Text file(*.txt)|*.txt\" --title=\"Export V/RAM\"");
  } else {
   return "error";
  }
 } #"error" -> "EMU Error: Uknown OS Detected"
 char *file = malloc(1024 * sizeof(char)); free(file);
 FILE *f = popen(cmd, "r");
 fgets(file, 1024, f);
 printf("0: %s\n",file);
 for (int i=0; i<strlen(file)-1; i++) {
  if (file[i]+file[i+1] == "\n") {
   file[i]   = "\0";
   file[i+1] = "\0";
  }
 }
 return file;
}
