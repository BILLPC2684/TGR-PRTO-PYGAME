//####################################//#################################################//
//# THE GAME RAZER © 2022 BILLPC2684 #//# https://github.com/BILLPC2684/TGR-PRTO-PYGAME #//
//#       Service(Server) FILE       #//#################################################//
//####################################//#################################################//
//####################################//
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
#include <sys/poll.h>

typedef struct {
 bool     PrintDebugs;
 bool     *Pause,Running[2],Debug;
 uint8_t  *MEM,*ROMPG[33],Page[2],LED[3],id;
 uint32_t IP[2],SP[2],SPMIN[2],SPMAX[2];
 uint64_t time,IPS,TIPS,IPC,frames,FPS;
 uint16_t REG[2][8]; //A,B,C,D,E,F,G,H
 float  RunQuality;
 bool   UInput[14][2];
 char   Title_Name[23];
 bool   Title_lock;
 double RAMUsage;
 double VRAMUsage;
} SystemSRT;

SystemSRT sys;

void *CPU_EXEC(int coreid);
void *CPU_CLOCK(void *null);

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

void bin_dump(uint64_t u) { int i=63; while (i-->0) { printf("%hhu",(u&(uint64_t)pow(2,i))?1:0); } printf("\n"); }

void dumpData(char *name, unsigned char *data, int size, bool use_non, int start, int end) {
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
 for (int i=start;i<end;i++) {
  if (i >= size) { break; }
  if (j > 15) {
   bytes[j-1] = data[i];
   if (data[i] < 0x10) { printf("0"); }
   printf("%x|",data[i]);
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
   if (data[i] < 0x10) { printf("0"); } printf("%x ",data[i]);
   bytes[j-1] = data[i];
  } j++; l++;
 }
 if (j > 0) {
  for (int i=j; i < 16; i++) {
   printf("-- ");
   bytes[j-1] = 0x00;
  } printf("--|");
  for (int i=0; i < l; i++) {
   if (use_non) { printf("%c",ascii_non[bytes[i]]); }
    else        { printf("%c",ascii[bytes[i]]); }
  }
  for (int i=j; i < 16; i++) {
   printf(" ");
  } printf(" |\n");
 } printf("|_______|_______________________________________________|________________|\n\\Size: 0x%x/%d Bytes(",size,size);
 if (size < 1024) { printf("%i KB)\n",size/1024); } else { printf("%i MB)\n",size/1024/1024); }
}

void crop(char *dst, char *src, size_t mn, size_t mx) {
 const int len = mx - mn; src += mn;
 for (int i = 0; i < len; i++) { dst[i] = src[i]; }
 dst[len] = '\0';
}
void updateROM() { int j,i; for(j=0;j<2;j++) { for(i=0;i<0x0800000;i++) { /*printf("sys.ROMPG[%d:%7x][%7x]\n",j,i,i+(0x0800000*j));*/ sys.MEM[i+(0x0800000*j)] = sys.ROMPG[sys.Page[j]][i]; } } }

int main(int argc, char const* argv[]) {
 sys.PrintDebugs = true;
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

 dumpData("File", "test", 4, true, 0, 4);
 
 //       Full MemoryMap: 216 MiB | 32 8MB ROM sys.Pages + BIOS sys.Page
 uint32_t i,j,k;
 char command[10],dummystr[1024],REGchar[8] = {'A','B','C','D','E','F','G','H'};
 sys.MEM = malloc(0xD800000);sys.Page[0]=0;sys.Page[1]=1;sys.Running[0]=0;sys.Running[1]=0;sys.Pause=false;for(i=0;i<33;i++){sys.ROMPG[i]=malloc(0x0800000);}
 sys.IP[0]=0;sys.IP[1]=0;sys.SP[0]=0x97FFDFF;sys.SP[1]=0x97DFDFF;sys.SPMIN[0]=0x97DFE00;sys.SPMIN[1]=0x97BFE00;sys.SPMAX[0]=sys.SP[0];sys.SPMAX[1]=sys.SP[1];sys.IPS=0;for(j=0;j<2;j++){for(i=0;i<8;i++){sys.REG[j][i]=0;}};updateROM();
// *sys.ROMPG[33]={[0 ... 32]=malloc(0x0800000)};


// uint8_t  *SAV = malloc(0x0800000), *RAM = malloc(0xC000000), **sys.MEM = malloc(0xD800000), *sys.ROMPG[33] = {malloc(0x0800000)}, sys.Page[2]={0};
// bool     sys.Pause=false, sys.Running[2]={0}, sys.Debug=false;
// uint8_t  *sys.MEM=malloc(0xD800000), *sys.ROMPG[33]={[0 ... 32]=malloc(0x0800000)}, sys.Page[2]={0}, sys.RGB[3]={0}, sys.id=0,sys.id2=0;
// uint32_t sys.IP[2]={0},sys.SP[2]={0x97FFDFF,0x97DFDFF},sys.SPMIN[2]={0x97DFE00,0x97BFE00},sys.SPMAX[2]={sys.SP[0],sys.SP[1]},i,j,k;
// uint64_t sys.time,sys.IPS,sys.TIPS;
// uint16_t sys.REG[2][8]; //A,B,C,D,E,F,G,H
// for(j=0;j<33;j++){for(i=0;i<0x0800000;i++){sys.ROMPG[j][i]=0;}}
// for(i=0;i<0x0800000;i++) { sys.MEM[sys.IP] = &sys.ROMPG[0][i];sys.IP++; } printf("%x\n",sys.IP);
// for(i=0;i<0x0800000;i++) { sys.MEM[sys.IP] = &sys.ROMPG[1][i];sys.IP++; } printf("%x\n",sys.IP);
// for(i=0;i<0x0800000;i++) { sys.MEM[sys.IP] = &SAV     [i];sys.IP++; } printf("%x\n",sys.IP);

 pthread_t call_CPU0;
 pthread_create(&call_CPU0, NULL, CPU_EXEC, 0);
 pthread_t call_CPU1;
 pthread_create(&call_CPU1, NULL, CPU_EXEC, 1);
 pthread_t call_CLOCK;
 pthread_create(&call_CLOCK, NULL, CPU_CLOCK, NULL);

//testing
/* sys.MEM[0] = 0xFF;
 sys.ROMPG[1][0] = 15;
 sys.MEM[0x0800000] = 0x7F;
 printf("EMU Service: Before:\nsys.ROMPG[0]: %d\nsys.MEM[0]:   %d\n",sys.ROMPG[1][0],sys.MEM[0x0800000]);
 updateROM();
 printf(">>>> 1\n");memset(sys.MEM, 0, sizeof(sys.MEM));printf(">>>> 2\n"); sys.Page[0]=0;sys.Page[1]=1;printf(">>>> 2\n"); sys.Running[0]=0;sys.Running[1]=0;printf(">>>> 3\n"); sys.Pause=false; for(j=0;j<33;j++){for(i=0;i<0x0800000;i++){sys.ROMPG[j][i]=0;}} printf(">>>> 4\n");
 sys.IP=0x0000000; sys.SP=0x97FFDFF; sys.SPMAX=sys.SP; sys.IPS=0; printf(">>>> 5\n"); for(j=0;j<2;j++){for(i=0;i<8;i++){sys.REG[j][i]=0;}}; printf(">>>> 6\n");
 updateROM();
 printf("[A: %4x, B: %4x, C: %4x, D: %4x, E: %4x, F: %4x, G: %4x, H: %4x]\n",sys.REG[i][0],sys.REG[i][1],sys.REG[i][2],sys.REG[i][3],sys.REG[i][4],sys.REG[i][5],sys.REG[i][6],sys.REG[i][7]);
 printf("EMU Service: After:\nsys.ROMPG[0]: %d\nsys.MEM[0]:   %d\n",sys.ROMPG[1][0],sys.MEM[0x0800000]);
 updateROM();
 */
 struct pollfd sockfd;
 uint8_t ret;
 uint16_t timeouts=0;
 
 sockfd.fd = TGRsock; // your socket handler
 sockfd.events = POLLIN;
 while(1) {
  memset(buffer, 0, sizeof(buffer));
  ret = poll(&client, 1, 5); // 1ms for timeout
//  if(ret!=0){printf(">>>> ret: %i\n",ret);}
  switch (ret) {
    case -1: printf("SOCKET ERROR"); printf("EMU Service: A Communication Error Has Occored With The Client!\n"); close(client); shutdown(TGRsock, SHUT_RDWR); return -1; // Error
    case 0: valread=0,timeouts++; break; // Timeout
    default:  valread = read(client,buffer,sizeof(buffer)),timeouts=0;
  }  memcpy(command,&buffer,10);
  printf("ret: %d | timeouts: %d\n",ret,timeouts);
  if (timeouts == 0xFFFF) { printf("EMU Service: CRITIAL ERROR CLIENT HAS TIMED OUT!!! (Client Has Not Responded In %d Attempts!)\n",0xFFFF); close(client); shutdown(TGRsock, SHUT_RDWR); return -1; }
  if (valread > 0) {
   if (sys.PrintDebugs) { printf("EMU Service: \""); for(i=0;i<sizeof(buffer);i++) { printf("%c", buffer[i]); } printf("\" | \"%s\"\n",buffer); }
   //for(int i=0;i<sizeof(buffer);i++) { printf("%c", (buffer[i]<32)?'.':buffer[i]); } printf("\n%s\n",buffer);
   if        (strstr(command, "init"  )!=NULL) {
    printf("EMU Service: Starting CPU initalization...\n");
    memset(sys.MEM,0,sizeof(sys.MEM));sys.Page[0]=0;sys.Page[1]=1;sys.Running[0]=0;sys.Running[1]=0;sys.Pause=false;for(j=0;j<33;j++){for(i=0;i<0x0800000;i++){sys.ROMPG[j][i]=0;}}
    sys.IP[0]=0;sys.IP[1]=0;sys.SP[0]=0x97FFDFF;sys.SP[1]=0x97DFDFF;sys.IPS=0;for(j=0;j<2;j++){for(i=0;i<8;i++){sys.REG[j][i]=0;}};updateROM();
   } else if (strstr(command, "pause" )!=NULL) {
    printf("EMU Service: Emulation sys.Paused!!\n");
   } else if (strstr(command, "ping"  )!=NULL) { printf("ping"); send(client, "pong", 4, 0);
   } else if (strstr(command, "debug" )!=NULL) { sys.Debug=buffer[5]; printf("EMU Service: sys.Debug mode %s\n",(sys.Debug==1)?"activated":"deactivated");
   } else if (strstr(command, "uplrom")!=NULL) { printf("EMU Service: Downloading ROMBank[%i]...\n", buffer[6]); for(i=7;i<0x0800007;i++){sys.ROMPG[buffer[6]][i-7]=buffer[i];}
   } else if (strstr(command, "run"   )!=NULL) { sys.Running[buffer[3]]=true; printf("EMU Service: Running CPU Core #%d\n", buffer[3]);
   } else if (strstr(command, "stop"  )!=NULL) { sys.Running[buffer[4]]=false;printf("EMU Service: Stopping CPU Core #%d\n",buffer[4]);
   } else if (strstr(command, "quit"  )!=NULL) { send(client, "quit", 4, 0); break;
   } else if (strstr(command, "tick"  )!=NULL) { printf("tock"); send(client, sprintf(dummystr,"tock%c%c",sys.Running[0]?1:0,sys.Running[1]?1:0), 6, 0); }
   //send(client, buffer, strlen(buffer), 0); //Echoing
//  for(sys.id=0;sys.id<2;sys.id++) {
  }
 } printf("ret:%d\nEMU Service: Shutting down...",ret); close(client); shutdown(TGRsock, SHUT_RDWR); return 0;
}

//##SERVER VERSION
//#RECV ARRAY
//Uinput,   sys.Running+sys.Pause+sys.Debug+Exit, |
//4,        1 byte (5-bits),          |
//0,1,2,3,  4                         |
//#SEND ARRAY
//sys.IP,  Flags, sys.Running+sys.Pause+sys.Debug+Exit, Error, sys.MEMORY MAP, Disys.SPlay[720p], |
//8,   1,     1 byte (5-bits),          1024,  0xD800000,  0x2A3000,      |
//0,3, 7,     8,                        9,     0x409       0xD800409,     0xDAA3409|
//sys.MEM = bytearray(0xD800000) #Full sys.MEMoryMap: 216 MiB


void *CPU_CLOCK(void *null) {
 sleep(1);
 while (true) {
  sleep(1/1000); //0.1 secs
  sys.time++;
  //if (sys.time% 100 == 0) { printf("sys.time: %d\n",sys.time); }
//  if (sys.time%(1000/8) == 0) { CPU_ticked = true; }
  if (sys.time%1000 == 0) {
   sys.IPS = sys.IPC;
   sys.FPS = sys.frames;
   sys.TIPS = sys.TIPS+sys.IPS;
   sys.RunQuality = (double)(sys.IPC/24000000)*100;
//    printf(">>>> %d\n",sys.IPC/24000000);
  }if (sys.time%1100 == 0) {
   sys.IPC = 0;
   sys.frames = 0;
  }
 }
}
/* double dummy; int i;
 printf(0);
 printf("EMU: Service: sys.MEM[0x0000000]: %x\n",sys.MEM[0]);
 printf(1);
 sleep(1);
 while (true) {
  sleep(1/1000); //0.1 secs
  sys.time++;
  //if (sys.time% 100 == 0) { printf("sys.time: %d\n",sys.time); }
//  if (sys.time%(1000/8) == 0) { CPU_ticked = true; }
  if (sys.time%1000 == 0) {
//   if (p == true) {
   dummy=0.0;for(i=0x1800000;i<0x97BFDFF+1;i++){dummy+=sys.MEM[i]/255;}sys.RAMUsage=dummy;
   dummy=0.0;for(i=0x9800000;i<0xD7FFFFF+1;i++){dummy+=sys.MEM[i]/255;}sys.VRAMUsage=dummy;
//   }
   sys.IPS = sys.IPC;
   sys.FPS = sys.frames;
   sys.TIPS = sys.TIPS+sys.IPS;
   sys.RunQuality = (double)(sys.IPC/24000000)*100;
//    printf(">>>> %d\n",sys.IPC/24000000);
  }if (sys.time%1100 == 0) {
   sys.IPC = 0;
   sys.frames = 0;
  }
 }
}*/

void *CPU_EXEC(int coreid) {
 uint32_t i,j,k;
 char command[10],REGchar[8] = {'A','B','C','D','E','F','G','H'};
 while(1) {
  if(sys.Running[coreid]) {
   uint8_t A   =  sys.MEM[(sys.IP[coreid]+1)%0xD800000] >> 4 ;       //4 \.
   uint8_t B   =  sys.MEM[(sys.IP[coreid]+1)%0xD800000] & 0xF;       //4 |-> A/B/C = 1.5 bytes
   uint8_t C   =  sys.MEM[(sys.IP[coreid]+2)%0xD800000] >> 4 ;       //4 /'
   int32_t IMM = (sys.MEM[(sys.IP[coreid]+2)%0xD800000] & 0xF) << 8; //4 \.
   IMM  = (IMM |  sys.MEM[(sys.IP[coreid]+3)%0xD800000])<< 8 ;       //8 |->  IMM  = 3.5 bytes
   IMM  = (IMM |  sys.MEM[(sys.IP[coreid]+4)%0xD800000])<< 8 ;       //8 |
   IMM |=         sys.MEM[(sys.IP[coreid]+5)%0xD800000];             //8 /'
   if (sys.Debug == true) {
    printf("\n[CPU:%d] IC: 0x%08x   \t>> [",coreid,sys.IP[coreid]);
    for(int i=0;i<6;i++){printf("0x%02x",sys.MEM[(sys.IP[coreid]+i)%0xD800000]);if(i<5){printf(", ");}}
    printf("]  [A:%2i, B:%2i, C:%2i, IMM:0x%07x] | [A:%c, B:%c, C:%c]\n\\REGs: [",A,B,C,IMM,REGchar[A],REGchar[B],REGchar[C]);
    for(int i=0;i<8;i++){printf("%c:0x%04x",REGchar[i],sys.REG[coreid][i]);if(i<7){printf(", ");}}
    printf("] | TotalRan: %li\n\\StackPointer: 0x%07x/%li | StackBase: 0x%07x/%li\n\\\\StackData:[",sys.TIPS,sys.SP,sys.SP,sys.SPMAX[coreid],sys.SPMAX[coreid]);
//    for (int i = sys.SPMAX[coreid]; i >= sys.SPMIN[coreid]; --i){ if((i+1)%2==0) { printf(" 0x"); } printf("%02x",sys.MEM[i]); if(i%16==0 && i != 0) { printf("\n"); } }
    printf("]\n \\instruction: "); //,sys.REG[coreid][0],sys.REG[coreid][1],sys.REG[coreid][2],sys.REG[coreid][3],sys.REG[coreid][4],sys.REG[coreid][5],sys.REG[coreid][6],sys.REG[coreid][7]);
   }
   
   switch(sys.MEM[sys.IP[coreid]%0xD800000]) { //* Instuctions
    case 0x00: //mov     A, B*/IMM, Flag        - moves B*/IMM, to A [* means Flag Enabled]
     if (sys.Debug == true) { printf("MOV\n"); }
     if (C >= 1) { sys.REG[coreid][A] = sys.REG[coreid][B]; }else{ sys.REG[coreid][A] = IMM; } break;
    case 0x01: //add     A, B/IMM, C           - adds A and B/IMM, to C
     if (sys.Debug == true) { printf("ADD\n"); }
     if (IMM >= 1) { sys.REG[coreid][C] = sys.REG[coreid][A]+IMM; }else{ sys.REG[coreid][A] = sys.REG[coreid][B]+sys.REG[coreid][C]; } break;
    case 0x02: //sub     A, B/IMM, C           - subtracts A and B/IMM, to C
     if (sys.Debug == true) { printf("SUB\n"); }
     if (IMM >= 1) { sys.REG[coreid][C] = sys.REG[coreid][A]-IMM; }else{ sys.REG[coreid][A] = sys.REG[coreid][B]-sys.REG[coreid][C]; } break;
    case 0x03: //mul     A, B/IMM, C           - multiplies A and B/IMM, to C
     if (sys.Debug == true) { printf("MUL\n"); }
     if (IMM >= 1) { sys.REG[coreid][C] = sys.REG[coreid][A]*IMM; }else{ sys.REG[coreid][A] = sys.REG[coreid][B]*sys.REG[coreid][C]; } break;
    case 0x04: //div     A, B/IMM, C           - divides A and B/IMM, to C
     if (sys.Debug == true) { printf("DIV\n"); }
     if (IMM >= 1) { sys.REG[coreid][C] = sys.REG[coreid][A]/IMM; }else{ sys.REG[coreid][A] = sys.REG[coreid][B]/sys.REG[coreid][C]; } break;
    case 0x05: //{b}and  A, B/IMM, C           - ands A and B/IMM, to C | both "band" or "and" works
     if (sys.Debug == true) { printf("AND\n"); }
     if (IMM >= 1) { sys.REG[coreid][C] = sys.REG[coreid][A]&IMM; }else{ sys.REG[coreid][A] = sys.REG[coreid][B]&sys.REG[coreid][C]; } break;
    case 0x06: //{b}or   A, B/IMM, C           - ors  A and B/IMM, to C | both "bor"  or "or"  works
     if (sys.Debug == true) { printf("OR\n"); }
     if (IMM >= 1) { sys.REG[coreid][C] = sys.REG[coreid][A]|IMM; }else{ sys.REG[coreid][A] = sys.REG[coreid][B]|sys.REG[coreid][C]; } break;
    case 0x07: //{b}xor  A, B/IMM, C           - xors A and B/IMM, to C | both "bxor" or "xor" works
     if (sys.Debug == true) { printf("XOR\n"); }
     if (IMM >= 1) { sys.REG[coreid][C] = sys.REG[coreid][A]^IMM; }else{ sys.REG[coreid][A] = sys.REG[coreid][B]^sys.REG[coreid][C]; } break;
    case 0x08: //bsl     A, B/IMM, C           - bitshifts A to the left  by B/IMM, to C
     if (sys.Debug == true) { printf("BSL\n"); }
     if (IMM >= 1) { sys.REG[coreid][C] = sys.REG[coreid][A]<<IMM; }else{ sys.REG[coreid][A] = sys.REG[coreid][B]<<sys.REG[coreid][C]; } break;
    case 0x09: //bsr     A, B/IMM, C           - bitshifts A to the right by B/IMM, to C
     if (sys.Debug == true) { printf("BSR\n"); }
     if (IMM >= 1) { sys.REG[coreid][C] = sys.REG[coreid][A]>>IMM; }else{ sys.REG[coreid][A] = sys.REG[coreid][B]>>sys.REG[coreid][C]; } break;
    case 0x0A: //{b}not  A                     - inverts A | both "bnot" or "not" works
     if (sys.Debug == true) { printf("NOT\n"); }
     sys.REG[coreid][A] = ~sys.REG[coreid][A]; break;
    case 0x0B: //split   A,   B,C, {IMM}       - splits A into B and C | if IMM is 0: 8-bit split else 4-bit split
     if (sys.Debug == true) { printf("SPLIT\n"); }
     if ((IMM % 0x2) == 0) { sys.REG[coreid][B] = sys.REG[coreid][A] & 0xFF; sys.REG[coreid][C] = sys.REG[coreid][A] >> 8; } else { sys.REG[coreid][B] = sys.REG[coreid][A] & 0xF; sys.REG[coreid][C] = sys.REG[coreid][A] >> 4; } break;
    case 0x0C: //combine A,B,   C, {IMM}       - combines A and B into C | IMM rules same as split
     if (sys.Debug == true) { printf("COMBINE\n"); }
     if ((IMM % 0x2) == 0) { sys.REG[coreid][C] = (sys.REG[coreid][A] << 8) | (sys.REG[coreid][B] & 0xFF); }else{ sys.REG[coreid][C] = (sys.REG[coreid][A] << 4) | (sys.REG[coreid][B] & 0xF); } break;
    case 0x0D: //jmp     [Label]/Address       - jumps to the given [Label] or Address
     if (sys.Debug == true) { printf("JUMP\n"); }
     if (sys.REG[coreid][C] >= 1) { sys.IP[coreid] = sys.REG[coreid][A]<<16|sys.REG[coreid][B]; }else{ sys.IP[coreid] = IMM; } break;
    case 0x0E: //led     {A,B,C}/{IMM}         - sets the System's LED color | IMM is #RRGGBB
     if (sys.Debug == true) { printf("LED\n"); }
     if (IMM > 0) { sys.LED[0],sys.LED[1],sys.LED[2]=IMM>>16,IMM>>8&0xFF,IMM&0xFF; }else{ sys.LED[0],sys.LED[1],sys.LED[2]=sys.REG[coreid][A],sys.REG[coreid][B],sys.REG[coreid][C]; } break;
    case 0x0F: //cmpeq   A, B,{C},{IMM}        - if A == B or {IMM} then continue, else skip 1 or {C} instructions
     if (sys.Debug == true) { printf("CMP=\n"); }
     if (C > 0xF) {  if (sys.REG[coreid][A] == IMM) { sys.IP[coreid] += 6 || sys.REG[coreid][C&0xF]*6; }
     }else if(sys.REG[coreid][A] == sys.REG[coreid][B]) { sys.IP[coreid] += 6 || sys.REG[coreid][C]*6; } break;
    case 0x10: //cmplt   A, B,{C},{IMM}        - if A == B or {IMM} then continue, else skip 1 or {C} instructions
     if (sys.Debug == true) { printf("CMP<\n"); }
     if (C > 0xF) {  if (sys.REG[coreid][A] <  IMM) { sys.IP[coreid] += 6 || sys.REG[coreid][C&0xF]*6; }
     }else if(sys.REG[coreid][A] <  sys.REG[coreid][B]) { sys.IP[coreid] += 6 || sys.REG[coreid][C]*6; } break;
    case 0x11: //cmpgt   A, B,{C},{IMM}        - if A == B or {IMM} then continue, else skip 1 or {C} instructions
     if (sys.Debug == true) { printf("CMP>\n"); }
     if (C > 0xF) {  if (sys.REG[coreid][A] >  IMM) { sys.IP[coreid] += 6 || sys.REG[coreid][C&0xF]*6; }
     }else if(sys.REG[coreid][A] >  sys.REG[coreid][B]) { sys.IP[coreid] += 6 || sys.REG[coreid][C]*6; } break;
     
    case 0x12: //wmem    A,   {B,C}            - Writes to A to MEM[B..C]
     if (sys.Debug == true) { printf("WMEM\n");}
     if ((sys.REG[coreid][B]<<16|sys.REG[coreid][C]) > 0x0FFFFFF){
      if (sys.Debug == true) {
       printf("EMU Service: Writing REG:%c to ",sys.REG[A]);
       switch(sys.REG[coreid][B]<<16|sys.REG[coreid][C]) {
        case 0x1000000: printf("SAV"); break;
        case 0x1800000: printf("WRAM"); break;
        case 0x97BFE00: printf("STACK"); break;
        case 0x97FFE00: printf("I/O"); break;
        case 0x9800000: printf("VRAM"); break;
       }
       printf("[0x%x]\n",(sys.REG[coreid][B]<<16|sys.REG[coreid][C])%0x3FFFFFF);
      }
      sys.MEM[sys.REG[coreid][B]<<16|sys.REG[coreid][C]]=sys.REG[coreid][A];
     } else {
      printf("EMU Service: Invalid Instuction, You cannot write to ROM!\n");
     } break;
    case 0x13: //rmem    A,   {B,C}            - Reads from MEM[B..C] to A
     if (sys.Debug == true) {
      printf("RMEM\nEMU Service: Reading ");
      switch(sys.REG[coreid][B]<<16|sys.REG[coreid][C]) {
       case 0x0000000: printf("ROM"); break;
       case 0x1000000: printf("SAV"); break;
       case 0x1800000: printf("WRAM"); break;
       case 0x97BFE00: printf("STACK"); break;
       case 0x97FFE00: printf("I/O"); break;
       case 0x9800000: printf("VRAM"); break;
      }
      printf("[0x%x] to REG:%c\n",  (sys.REG[coreid][B]<<16|sys.REG[coreid][C])%0x3FFFFFF,sys.REG[A]);
     }
     sys.REG[coreid][A]=sys.MEM[sys.REG[coreid][B]<<16|sys.REG[coreid][C]]; break;
     
    case 0x14: //hlt     {IMM}                 - Halts or Restarts the System/Device
     if (sys.Debug == true) { printf("HALT\n"); }
     printf("EMU Service: Stopping CPU Core #%d\n",coreid); sys.Running[coreid]=false;
     break;
    case 0x15: //disp    A, {B}, {C}           - Displays up to 3  (FOR DEBUG ONLY)
     if (sys.Debug == true) { printf("DISPLAY\n"); }
     
     break;
    case 0x16: //flags   A                     - read the CPU's Flags into A
     if (sys.Debug == true) { printf("FLAG\n"); }
     
     break;
    case 0x17: //icout   A, B                  - returns Instuction Pointer to A..B | example with 0x17F39: A would be 0x0001 and B would be 0x7F39
     if (sys.Debug == true) { printf("ICOUT\n"); }
     
     break;
    case 0x19: //page    PageID, ROMBANKID     - replaces ROMBANK ID of REG:B with Page ID of REG:A
     if (sys.Debug == true) { printf("PAGE\n"); }
     
     break;
    case 0x1A: //push    A                     - pushes A, into Stack
     if (sys.Debug == true) { printf("PUSH\n"); }
     
     break;
    case 0x1B: //pop     A                     - pops Stack, into A
     if (sys.Debug == true) { printf("POP\n"); }
     
     break;
    case 0x1C: //call    [Label]               - calls a Label as a Function [uses Stack]
     if (sys.Debug == true) { printf("CALL\n"); }
     
     break;
    case 0x1D: //ret                           - returns from a Function [uses Stack]
     if (sys.Debug == true) { printf("RET\n"); }
     
     break;
    case 0x1E: //swap                          - swaps the first 2 Items in Stack
     if (sys.Debug == true) { printf("SWAP\n"); }
     
     break;
    case 0x1F: //gclk    A/Reset               - grabs the current runtime in seconds, to A (or Reset it)
     if (sys.Debug == true) { printf("GCLK\n"); }
     
     break;
    case 0x20: //wait    A                     - waits for a certain [A]mount of seconds (FOR DEBUG ONLY)
     if (sys.Debug == true) { printf("WAIT\n"); }
     
     break;
    case 0xFF: //nop                           - what you expected me to do something? NOPe!
     if (sys.Debug == true) { printf("NOP\n"); }
     break;
    default: printf("[EMU Service] CPU#%i: Unknown Operation 0x%2x",coreid,sys.MEM[sys.IP[coreid]]); break;
   } sys.IP[coreid]+=6;
  }
 } printf("EMU Service: Starting CPU initalization...\n");
}

