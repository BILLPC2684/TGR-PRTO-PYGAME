;this is a comment
mov a,1
loop:
 add a,b,a
 disp a
 add b,a,b
 disp b
 jmp [loop]
