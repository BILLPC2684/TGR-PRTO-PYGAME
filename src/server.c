//#include "include.h"
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <stdbool.h>

#include <pthread.h>
#include <math.h>
#include <time.h>

char *ascii     = "................................ !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~.................................¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ";
char *ascii_non = "................................ !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~.......................................................................................................................................................";

char* concat(const char *s1, const char *s2) {
 const size_t len[2] = {strlen(s1), strlen(s2)};
 char *result = malloc(len[0]+len[1]+1);//+1 for the null-terminator
 //in real code you would check for errors in malloc here
 memcpy(result, s1, len[0]);
 memcpy(result+len[0], s2, len[1]+1);//+1 to copy the null-terminator
 return result;
}

void bin_dump(uint64_t u) { int i=63; while (i --> 0) { printf("%hhu",(u&(uint64_t)pow(2,i))?1:0); } printf("\n"); }

void dumpData(char *name, FileStruct file, int size, bool use_non, int start, int end) {
 uint8_t bytes[16];
 printf("._______._______________________________________________.________________.\n|%s",name);
 if       (strlen(name) < 2) {  printf("      "); }
  else if (strlen(name) < 3) {  printf("     "); }
  else if (strlen(name) < 4) {  printf("    "); }
  else if (strlen(name) < 5) {  printf("   "); }
  else if (strlen(name) < 6) {  printf("  "); }
  else if (strlen(name) < 7) {  printf(" "); }
 printf("|00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F|0123456789ABCDEF|\n|-------|-----------------------------------------------|----------------|\n|0000000|");
 int j = 1,l=0;
 for (int i=start; i < end; i++) {
  if (i >= file.size) { break; }
  if (j > 15) {
   bytes[j-1] = file.data[i];
   if (file.data[i] < 0x10) { printf("0"); }
   printf("%x|",file.data[i]);
   for (int k=0; k < 16; k++) {
   if (use_non) { printf("%c",ascii_non[bytes[k]]); }
    else        { printf("%c",ascii[bytes[k]]); }
   } l=0;
   printf("|\n|");
   if      (i+1 < 0x1) {        printf("0000000%x|",i+1); }
   else if (i+1 < 0x10) {       printf("000000%x|",i+1); }
   else if (i+1 < 0x100) {      printf("00000%x|",i+1); }
   else if (i+1 < 0x1000) {     printf("0000%x|",i+1); }
   else if (i+1 < 0x10000) {    printf("000%x|",i+1); }
   else if (i+1 < 0x100000) {   printf("00%x|",i+1); }
   else if (i+1 < 0x1000000) {  printf("0%x|",i+1); }
   else if (i+1 < 0x10000000) { printf("%x|",i+1); }
   j = 0;
  } else {
   if (file.data[i] < 0x10) { printf("0"); } printf("%x ",file.data[i]);
   bytes[j-1] = file.data[i];
  } j++; l++;
 }
 if (j > 0) {
  for (int i=j; i < 16; i++) {
   printf("-- ");
   bytes[j-1] = 0x00;
  } printf("--|");
  for (int i=0; i < l-1; i++) {
   if (use_non) { printf("%c",ascii_non[bytes[i]]); }
    else        { printf("%c",ascii[bytes[i]]); }
  }
  for (int i=j; i < 16; i++) {
   printf(" ");
  } printf(" |\n");
 } printf("|_______|_______________________________________________|________________|\n\\Size: 0x%lx/%ld Bytes(",file.size,file.size);
 if (file.size < 1024) { printf("%ld KB)",file.size/1024); } else { printf("%ld MB)",file.size/1024/1024); }
 printf(" of 0x%x/%d bytes(",size,size);
 if (size < 1024) { printf("%d KB)\n\n",(size/1024)+1); } else { printf("%d MB)\n\n",(size/1024/1024)+1); }
}

void crop(char *dst, char *src, size_t mn, size_t mx) {
 const int len = mx - mn;
 src += mn;
 for (int i = 0; i < len; i++){
  dst[i] = src[i];
 }
 dst[len] = '\0';
}

FileStruct load(char *address, int make) {
 FileStruct file;
 file.found = true;
 if (access(address, F_OK) == -1) {
  if (make == 0) {
   printf("EMU ERROR: file(\"%s\") was not found...\n", address);
   file.found = false;
   return file;
  } else {
   printf("EMU WARNING: file \"%s\" was not found(your data could be lost if existsed), attempting to create local file...", address);
   FILE *SAV_file = fopen(address, "wb");
   fwrite(calloc(SAVSIZ, sizeof(SAV)), SAVSIZ-1, 8, SAV_file);
   fclose(SAV_file);
//   file.fp = fopen(address, "wb+");
//   file.data = calloc(SAVSIZ, sizeof(*SAV));
//   fwrite(&file.data, SAVSIZ, 8, file.fp);
//   fclose(file.fp);
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


void *CPU_CLOCK(void *null) {
 double dummy;
 while (true) {
  if (reset == true) { CPU.time = 0; }
  SDL_Delay(1); //0.1 secs
  CPU.time++;
  //if (CPU.time% 100 == 0) { printf("CPU.time: %d\n",CPU.time); }
  if (CPU.time%(1000/8) == 0) { CPU.ticked = true; }
  if (CPU.time%1000 == 0) {
   if (p == true) {
    dummy = 0.0; for (int i=0;i<0x7FFFFFF+1;i++) { dummy+= RAM[i]/255; }  RAMUsage = dummy;
    dummy = 0.0; for (int i=0;i<0x3FFFFFF+1;i++) { dummy+=VRAM[i]/255; } VRAMUsage = dummy;
   }
   IPS = CPU.IPC;
   FPS = frames;
   TIPS = CPU.TI;
   RunQuality = (double)(CPU.IPC/12000000)*100;
   if (showInfo == true) {
    printf("P1:[A:%d,B:%d,C:%d,X:%d,Y:%d,Z:%d,L:%d,R:%d,Start:%d,Select:%d,Up:%d,Down:%d,Left:%d,Right:%d]\nP2:[A:%d,B:%d,C:%d,X:%d,Y:%d,Z:%d,L:%d,R:%d,Start:%d,Select:%d,Up:%d,Down:%d,Left:%d,Right:%d]\n",UInput[0][0],UInput[1][0],UInput[2][0],UInput[3][0],UInput[4][0],UInput[5][0],UInput[6][0],UInput[7][0],UInput[8][0],UInput[9][0],UInput[10][0],UInput[11][0],UInput[12][0],UInput[13][0],UInput[0][1],UInput[1][1],UInput[2][1],UInput[3][1],UInput[4][1],UInput[5][1],UInput[6][1],UInput[7][1],UInput[8][1],UInput[9][1],UInput[10][1],UInput[11][1],UInput[12][1],UInput[13][1]);
    printf("FPS: %d\t | IPS: %d\t | TotalRan: %d\t| CPU Run Quality: %.2lf%%\n",FPS,(double)IPS,TIPS,RunQuality);
    if (p == true) {
     printf("RAM Usage: %.0lf bytes/%d (%.2lf%% full)\t| VRAM Usage: %.0lf bytes/%d (%.2lf%% full)\n",RAMUsage*100,0x7FFFFFF,(RAMUsage/0x7FFFFFF)*100,VRAMUsage*100,0x3FFFFFF,(VRAMUsage/0x3FFFFFF)*100);
    }
//    printf(">>>> %d\n",CPU.IPC/12000000);
   }
  }if (CPU.time%1100 == 0) {
   CPU.IPC = 0;
   frames = 0;
  }
 }
}

void *CPU_EXEC(void *null) {
 
}

int main(int argc, char const* argv[]) {
 if (argc < 2) { printf("EMU Error: No Emulation Service Port Was Given!\nUsage: ./server.o <PORT>\n"); return -1; }
 printf("EMU Service: Initalizing Emulation...\n"); struct sockaddr_in address; char buffer[1024*9] = {0};
 int TGRsock, client, valread, opt = 1, addrlen = sizeof(address);
 if ((TGRsock = socket(AF_INET, SOCK_STREAM, 0)) == 0) { perror("socket failed"); exit(EXIT_FAILURE); }
 if (setsockopt(TGRsock, SOL_SOCKET, SO_REUSEADDR|SO_REUSEPORT, &opt, sizeof(opt))) { perror("setsockopt"); exit(EXIT_FAILURE); }
 address.sin_family = AF_INET; address.sin_addr.s_addr = INADDR_ANY; address.sin_port = htons((int)strtol(argv[1],(char**)NULL,10));
 if (bind(TGRsock, (struct sockaddr*)&address, sizeof(address)) < 0) { perror("EMU Service: bind failed"); exit(EXIT_FAILURE); }
 if (listen(TGRsock, 3) < 0) { perror("listen"); exit(EXIT_FAILURE); } printf("EMU Service: Initalized, waiting for Emulation Client\n");
 if ((client = accept(TGRsock, (struct sockaddr*)&address, (socklen_t*)&addrlen)) < 0) { perror("accept"); exit(EXIT_FAILURE); }
 printf("EMU Service: Connected! Starting main loop...\n\n");
 
 //       Full MemoryMap: 216 MiB | 32 8MB ROM Pages + BIOS Page
// uint8_t  *SAV = malloc(0x0800000), *RAM = malloc(0xC000000), **MEM = malloc(0xD800000), *ROMPG[33] = {malloc(0x0800000)}, Page[2]={0};
 bool     Pause=false, Running[2]={0}, Debug=false;
 uint8_t  *MEM=malloc(0xD800000), *ROMPG[33]={[0 ... 32]=malloc(0x0800000)}, Page[2]={0}, RGB[3]={0}, id=0,id2=0;
 uint32_t IP[2]={0},SP[2]={0x97FFDFF,0x97DFDFF},SPMIN[2]={0x97DFE00,0x97BFE00},SPMAX[2]={SP[0],SP[1]},IPS=0,i,j,k;
 uint16_t REG[2][8]; //A,B,C,D,E,F,G,H
 char command[10];
 for(j=0;j<33;j++){for(i=0;i<0x0800000;i++){ROMPG[j][i]=0;}}
// for(i=0;i<0x0800000;i++) { MEM[IP] = &ROMPG[0][i];IP++; } printf("%x\n",IP);
// for(i=0;i<0x0800000;i++) { MEM[IP] = &ROMPG[1][i];IP++; } printf("%x\n",IP);
// for(i=0;i<0x0800000;i++) { MEM[IP] = &SAV     [i];IP++; } printf("%x\n",IP);
// for(i=0;i<0xC000000;i++) { if(IP>0x3400000){printf("%x,%x\n",i,IP);} MEM[IP] = &RAM     [i];IP++; } printf("%x\n",IP);
 void updateROM() { int j,i; for(j=0;j<2;j++) { for(i=0;i<0x0800000;i++) { /*printf("ROMPG[%d:%7x][%7x]\n",j,i,i+(0x0800000*j));*/ MEM[i+(0x0800000*j)] = ROMPG[Page[j]][i]; } } }
 
 pthread_t call_CPU;
 pthread_create(&call_CPU, NULL, CPU_EXEC, NULL);
 pthread_t call_CLOCK;
 pthread_create(&call_CLOCK, NULL, CPU_CLOCK, NULL);

//testing
/* MEM[0] = 0xFF;
 ROMPG[1][0] = 15;
 MEM[0x0800000] = 0x7F;
 printf("EMU Service: Before:\nROMPG[0]: %d\nMEM[0]:   %d\n",ROMPG[1][0],MEM[0x0800000]);
 updateROM();
 printf(">>>> 1\n");memset(MEM, 0, sizeof(MEM));printf(">>>> 2\n"); Page[0]=0;Page[1]=1;printf(">>>> 2\n"); Running[0]=0;Running[1]=0;printf(">>>> 3\n"); Pause=false; for(j=0;j<33;j++){for(i=0;i<0x0800000;i++){ROMPG[j][i]=0;}} printf(">>>> 4\n");
 IP=0x0000000; SP=0x97FFDFF; SPMAX=SP; IPS=0; printf(">>>> 5\n"); for(j=0;j<2;j++){for(i=0;i<8;i++){REG[j][i]=0;}}; printf(">>>> 6\n");
 updateROM();
 printf("[A: %4x, B: %4x, C: %4x, D: %4x, E: %4x, F: %4x, G: %4x, H: %4x]\n",REG[i][0],REG[i][1],REG[i][2],REG[i][3],REG[i][4],REG[i][5],REG[i][6],REG[i][7]);
 printf("EMU Service: After:\nROMPG[0]: %d\nMEM[0]:   %d\n",ROMPG[1][0],MEM[0x0800000]);
 updateROM();
 */
 while(1) {
  memset(buffer, 0, sizeof(buffer));
  valread = read(client,buffer,sizeof(buffer));
  memcpy(command,&buffer,10);
  
  if (valread > 0) {
   printf("EMU Service: \""); for(i=0;i<sizeof(buffer);i++) { printf("%c", buffer[i]); } printf("\" | \"%s\"\n",buffer);
   //for(int i=0;i<sizeof(buffer);i++) { printf("%c", (buffer[i]<32)?'.':buffer[i]); } printf("\n%s\n",buffer);
   if        (strstr(command, "init")!=NULL) {
    printf("EMU Service: Starting CPU initalization...\n");
    memset(MEM,0,sizeof(MEM));Page[0]=0;Page[1]=1;Running[0]=0;Running[1]=0;Pause=false;for(j=0;j<33;j++){for(i=0;i<0x0800000;i++){ROMPG[j][i]=0;}}
    IP[0]=0;IP[1]=0;SP[0]=0x97FFDFF;SP[1]=0x97DFDFF;IPS=0;for(j=0;j<2;j++){for(i=0;i<8;i++){REG[j][i]=0;}};updateROM();
   } else if (strstr(command, "pause")!=NULL) {
    printf("EMU Service: Emulation Paused!!\n");
   } else if (strstr(command, "ping" )!=NULL) { send(client, "pong", 4, 0);
   } else if (strstr(command, "debug")!=NULL) { Debug=buffer[5]; printf("EMU Service: Debug mode %s\n",(Debug==1)?"activated":"deactivated");
   } else if (strstr(command, "run"  )!=NULL) { Running[buffer[3]]=true; printf("EMU Service: Running CPU Core #%d", buffer[3]);
   } else if (strstr(command, "stop" )!=NULL) { Running[buffer[4]]=false;printf("EMU Service: Stopping CPU Core #%d",buffer[4]);
   } else if (strstr(command, "quit" )!=NULL) { send(client, "quit", 4, 0); break; }
   //send(client, buffer, strlen(buffer), 0); //Echoing
  } for(id=0;id<2;id++) {
   switch(MEM[IP[id]]) {
    case 0x00:
    
   }
  }
 } printf("EMU Service: Shutting down..."); close(client); shutdown(TGRsock, SHUT_RDWR); return 0;
}

//##SERVER VERSION
//#RECV ARRAY
//Uinput,   Running+Pause+Debug+Exit, |
//4,        1 byte (5-bits),          |
//0,1,2,3,  4                         |
//#SEND ARRAY
//IP,  Flags, Running+Pause+Debug+Exit, Error, MEMORY MAP, Display[720p], |
//8,   1,     1 byte (5-bits),          1024,  0xD800000,  0x2A3000,      |
//0,3, 7,     8,                        9,     0x409       0xD800409,     0xDAA3409|
//MEM = bytearray(0xD800000) #Full MemoryMap: 216 MiB



