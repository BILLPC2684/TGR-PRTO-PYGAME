#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <stdbool.h>

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
 bool     Pause=false, Running[2]={0};
 uint8_t  *MEM=malloc(0xD800000), *ROMPG[33][0x0800000], Page[2]={0};
 uint32_t IP=0x0000000,SP=0x97FFDFF,SPMAX=SP,IPS=0,i,j,k;
 uint16_t REG[2][8]; //A,B,C,D,E,F,G,H
 char command[10];
 for (i=0;i<33;++i){ROMPG[i] = malloc(0x0800000);}
// for(i=0;i<0x0800000;i++) { MEM[IP] = &ROMPG[0][i];IP++; } printf("%x\n",IP);
// for(i=0;i<0x0800000;i++) { MEM[IP] = &ROMPG[1][i];IP++; } printf("%x\n",IP);
// for(i=0;i<0x0800000;i++) { MEM[IP] = &SAV     [i];IP++; } printf("%x\n",IP);
// for(i=0;i<0xC000000;i++) { if(IP>0x3400000){printf("%x,%x\n",i,IP);} MEM[IP] = &RAM     [i];IP++; } printf("%x\n",IP);
 void updateROM() { int j,i; for(j=0;j<2;j++) { for(i=0;i<0x0800000;i++) { printf("ROMPG[%d:%7x][%7x]\n",j,i,i+(0x0800000*j)); MEM[i+(0x0800000*j)] = ROMPG[Page[j]][i]; } } }
 
 //testing
 MEM[0] = 0xFF;
 ROMPG[1][0] = 15;
 MEM[0x0800000] = 0x7F;
 printf("EMU Service: Before:\nROMPG[0]: %d\nMEM[0]:   %d\n",ROMPG[1][0],MEM[0x0800000]);
 updateROM();
 printf(">>>> 1\n");memset(MEM, 0, sizeof(MEM));printf(">>>> 2\n"); Page[0]=0;Page[1]=1;printf(">>>> 2\n"); Running[0]=0;Running[1]=0;printf(">>>> 3\n"); Pause=false; for(j=0;j<33;j++){for(i=0;i<0x0800000;i++){ROMPG[j][i]=0;}} printf(">>>> 4\n");
 IP=0x0000000; SP=0x97FFDFF; SPMAX=SP; IPS=0; printf(">>>> 5\n"); for(i=0;i<2;i++){memset(REG[i],0,2*sizeof(REG[i]));} printf(">>>> 6\n");
 printf("[A: %4x, B: %4x, C: %4x, D: %4x, E: %4x, F: %4x, G: %4x, H: %4x]\n",REG[i][0],REG[i][1],REG[i][2],REG[i][3],REG[i][4],REG[i][5],REG[i][6],REG[i][7]);
 printf("EMU Service: After:\nROMPG[0]: %d\nMEM[0]:   %d\n",ROMPG[1][0],MEM[0x0800000]);
 updateROM();
 
 while(1) {
  memset(buffer, 0, sizeof(buffer));
  valread = read(client,buffer,sizeof(buffer));
  memcpy(command,&buffer,10);
  
  if (valread > 0) {
   printf("EMU Service: "); for(i=0;i<sizeof(buffer);i++) { printf("%c", buffer[i]); } printf("\nEMU Service: %s\n",buffer);
   //for(int i=0;i<sizeof(buffer);i++) { printf("%c", (buffer[i]<32)?'.':buffer[i]); } printf("\n%s\n",buffer);
   if        (strstr(command, "init")!=NULL) {
    printf("Starting CPU initalization...\n");
    printf(">>>> 1\n");memset(MEM, 0, sizeof(MEM));printf(">>>> 2\n"); Page[0]=0;Page[1]=1;printf(">>>> 2\n"); Running[0]=0;Running[1]=0;printf(">>>> 3\n"); Pause=false; for(j=0;j<33;j++){for(i=0;i<0x0800000;i++){ROMPG[j][i]=0;}} printf(">>>> 4\n");
    IP=0x0000000; SP=0x97FFDFF; SPMAX=SP; IPS=0; printf(">>>> 5\n"); for(i=0;i<2;i++){memset(REG[i],0,2*sizeof(REG[i]));} printf(">>>> 6\n"); updateROM(); //A,B,C,D,E,F,G,H
    printf(">>>> 7\n");
   } else if (strstr(command, "pause")!=NULL) {
    printf("EMU Service: Emulation Paused!!\n");
//   } else if (strstr(command, "")!=NULL) {
//   } else if (strstr(command, "")!=NULL) {
//   } else if (strstr(command, "")!=NULL) {
//   } else if (strstr(command, "")!=NULL) {
   } else if (strstr(command, "quit")!=NULL) { send(client, "quit", 4, 0); break; }
   //send(client, buffer, strlen(buffer), 0); //Echoing
 }}
 close(client); shutdown(TGRsock, SHUT_RDWR); return 0;
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


