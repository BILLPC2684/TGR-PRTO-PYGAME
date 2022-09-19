;;;;;;;;;;;;;;;;;;;;;;;;
;Name: Base64-Test.asm ;
;Author: BILLPC2684    ;
;Libary: True          ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; ._____________.                   ;; REGS: A,B,C,D,E,F,G,H ;
; |TGR_EMORY_MAP|___________________::::::::::::::::::::::::;;
; |Name:"."."."."Length:"."."Starting:"."Ending:".".Size:."| ;
; |\ROM BANK0: . 0x0800000 > 0x0000000 - 0x07FFFFF[. 8  MB]| ;
; |\ROM BANK1: . 0x0800000 > 0x0800000 - 0x0FFFFFF[. 8  MB]| ;
; |\SAV: . . . . 0x0800000 > 0x1000000 - 0x17FFFFF[. 8  MB]| ;
; |\WRAM:. . . . 0x7fbfe00 > 0x1800000 - 0x97BFDFF[127.9MB]| ;
; |\Stack: . . . 0x0040000 > 0x97BFE00 - 0x97FFDFF[256  KB]| ;
; |\I/O SRAM:. . 0x0000200 > 0x97BFE00 - 0x97FFFFF[512  BT]| ;
; |\VRAM:. . . . 0x4000000 > 0x9800000 - 0xD7FFFFF[.64  MB]| ;
; |\TOTAL: . . . 0xD800000 . . . . . . . . . . . . . . . . | ;
; |________________________________________________________| ;
;                                                            ;
;0x8FBFCFE - 0x8FBFCFF[  2 byte ]: b64_In/Out_lengths        ;
;0x8FBFD00 - 0x8FBFD7F[128 bytes]: b64_In_buffer             ;
;0x8FBFD80 - 0x8FBFDFF[128 bytes]: b64_Out_buffer            ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

base64:{65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,48,49,50,51,52,53,54,55,56,57,43,47,61}
b64_string:{85,109,70,122,99,71,74,108,99,110,74,53,65,69,78,121,98,51,78,122,73,69,74,118,100,119,65,70,119,84,111,69,65,73,103,107,89,69,76,65,103,65,70,65,65,89,103,65,69,79,65,103,65,70,103,65,81,103,107,89,69,65,73,103,66,72,56,65,65,122,56,65,66,109,81,73,65,65,61,61}
%define b64_Out_buffer 0x8FBFD80

b64_decode: ;Starting function (call this)
 push A                   ;\.
 push B                   ; \.
 push C                   ;  \.
 push D                   ;   \. PUSHING ALL REGS INTO STACK!!
 push E                   ;   /'
 push F                   ;  /'
 push G                   ; /'
 push H                   ;/'
 rmem 0x8FBFCFE,H         ;reads b64_In_lengths to H
 dec H                    ;decrement H
 jmp [b64_init]           ;continue the program

;REGS SETUP:
; A \. address of b64_string or base64
; B /'
; C \. address of b64_in_buffer
; D /'
; E Data Dummy or index of base64(decoding)
; F N/A
; G ----------\. Address of b64_in_buffer-1
; H Length or /'
b64_load:
 wmem 0x8FBFCFE,80        ;sets b64_In_lengths to the fixed length with b64_string
 rmem 0x8FBFCFE,H         ;copy b64_In_lengths to H
 lmov A,B,[b64_string]    ;AB Address of b64_string
 lmov C,D,0x08FBFD00      ;CD Address of b64_in_buffer
 b64_load_loop:
  dec H
  rmem A,B,E              ;reading b64_string[AB] to E
  wmem C,D,E              ;writing b64_In_buffer[CD] as E
  cmpeq B,0xFFFF          ;if true: B has OverFlowed!
   inc A                  ;\inc A in Address:b64_string
  inc B                   ;\B will overflow to 0
  cmpeq D,0xFFFF          ;if true: D has OverFlowed!
   inc C                  ;\inc c in Address:b64_In_buffer
  inc D                   ;\D will overflow to 0
 cmpeq H,0                ;if H is 0
  jmp [b64_init]        ;\True: break loop into b64_decode???? Did you mean [b64_init] ?
 jmp [b64_load_loop]      ;\False: coninue loop
b64_init:
 lmov G,H,0x8FBFCFF       ;GH Address of b64_in_buffer-1
 b64_Loop:
  cmpeq H,0xFFFF          ;if true: H has OverFlowed!
   inc G                  ;\inc G in Address:b64_in_buffer
  inc H                   ;\H will overflow to 0
  rmem G,H,C              ;reading b64_In_buffer[GH] to C
  disp C                  ;[DEBUG ONLY] displays C in terminal
  lmov A,B,[base64]       ;AB Address of base64
  mov E,-1                ;Index of base64
  dec B                   ;dec B in Adress:base64
  b64_Loop2:
   cmpeq B,0xFFFF         ;if true: B has OverFlowed!
    inc A                 ;\inc A in Address
   inc B                  ;\B will overflow to 0
   inc E                  ;inc E in Index:base64
   rmem A,B,D             ;reading base64[AB] to D
   cmpeq C,D              ;if true: C equals Dz
    jmp [b64_Loop2_bk]    ;\break Loop2
   cmpeq E,64             ;if E equals 64 then
    jmp [b64_Loop2_bk]    ;\true: break loop
   jmp [b64_Loop2]        ;\false: continue loop
 b64_Loop2_bk:
  mod E,64,E              ;modulo E by 64
  wmem G,H,E              ;writing b64_In_buffer[GH] to E
  disp G,H,E              ;[DEBUG ONLY] displays GH and E
  cmpgt A,H               ;if A is less then H
   jmp [b64_Loop]         ;\true: contine loop

;print("--------------------------\nPre-Out:")
;[print([i,(((8-len(bin(i)[2:]))*"0")+bin(i)[2:])]) for i in code]

rmem 0x8FBFCFE,H          ;reads b64_In_lengths to H
lmov A,B,[b64_string]     ;AB Address of b64_string
load E,0                  ;sets E as 0
disp E
disp E
disp E
loop_test0:
 cmpeq B,0xFFFF           ;if true: B has OverFlowed!
  inc A                   ;\inc A in Address
 inc B                    ;\B will overflow to 0
 rmem A,B,C               ;reading b64_string[AB] to C
 disp C                   ;displays C
 inc E
 cmpgt E,H                ;if E is less then H
  jmp [loop_test0]        ;\true: contine loop

lmov A,B,[b64_Out_buffer] ;AB Address of b64_string
load E,1                  ;sets E as 1
disp E
disp E
disp E
load E,0                  ;sets E as 0
loop_test1:
 cmpeq B,0xFFFF           ;if true: B has OverFlowed!
  inc A                   ;\inc A in Address
 inc B                    ;\B will overflow to 0
 rmem A,B,C               ;reading b64_string[AB] to C
 disp C                   ;displays C
 inc E
 cmpgt E,H                ;if E is less then H
  jmp [loop_test1]        ;\true: contine loop


hlt                       ;stops the program

;REGS SETUP:
; A \. address of b64_string or base64
; B /'
; C \. address of b64_in_buffer
; D /'
; E Data Dummy or index of base64(decoding)
; F N/A
; G ----------\. Address of b64_in_buffer-1
; H Length or /'

;A=-1 ;<<<<<<<<<<<<<<
;B=0
;F=0
jmp [Loop3]
Loop3_do0:

; D=(C<<2)%256
; A=A+1
; C=code[A]
; C=(C>>4)%256
; D=D|C
; A=A-1
; return
Loop3_do1:
; D=(C<<4)%256
; A=A+1
; C=code[A]
; C=(C>>2)%256
; D=D|C
; A=A-1
; return
Loop3_do2:
; D=(C<<6)%256
; A=A+1
; C=code[A]
; C=(C>>0)%256
; D=D|C
; A=A-1
; return
Loop3:
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
