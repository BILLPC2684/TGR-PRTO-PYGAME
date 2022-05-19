from pygame import *
# MAKE SURE ALL VARIBLES AND COMMAS(,) ARE CORRECT! #

emulation = [
 ## Debug Mode ##
 True, # True/False
]

video = [
 ## Video Zoom ##
 1, # 1x Minimum Default | 4x Maximum

 ### BELOW IS ONLY ENABLED WITH 2x+ ZOOM ###

 ## Pixelate ##
 False, # True/False

 ## ScanLines ##
 False, # True/False

 ## Fuzz Emulation ##
 False, # True/False
]

controllers = [[
 ### GOTO https://www.pygame.org/docs/ref/key.html for more information ###
 ### CONTROLLER INPUT HASN'T BEEN IMPLIMENTED YET!!! ###

 ## PLAYER 1 ##
 K_z, #A
 K_x, #B
 K_c, #C
 K_a, #X
 K_s, #Y
 K_d, #Z
 K_q, #L
 K_w, #R
 K_RETURN, #Start
 K_BACKSPACE, #Select
 K_UP, #Up
 K_DOWN, #Down
 K_LEFT, #Left
 K_RIGHT, #Rright
],[
 ## PLAYER 2 ##
 K_KP1, #A
 K_KP5, #B
 K_KP3, #C
 K_KP7, #X
 K_KP_DIVIDE, #Y
 K_KP9, #Z
 K_KP0, #L
 K_KP_PERIOD, #R
 K_KP_ENTER, #Start
 K_KP_PLUS, #Select
 K_KP8, #Up
 K_KP2, #Down
 K_KP4, #Left
 K_KP6, #Rright
]]
