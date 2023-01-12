from pygame import * #Required for User/Controller Inputs
# MAKE SURE ALL VARIBLES AND COMMAS(,) ARE CORRECT! #

emulation = [
 ## Debug Mode ##
 False, # True/False
]

video = [
 ## Video Zoom ##
 1, # 1-4 | Default: 1

 ### BELOW IS ONLY ENABLED WITH 2x+ ZOOM ###

 ## ScanLines ##
 False, # True/False | Default: False

 ## Pixelate ##
 False, # True/False | Default: False

 ## RGB-Fuzz Emulation ##
 False, # True/False | Default: False

 ## Force Aspect Ratio ##
 True,  # True/False | Default: True
 
 ## AutoDetect ScreenSize ##
 True,  # True/False | Default: True
 
 ###########################################
 
 ## Show Inputs ##
 True,  # True/False | Default: False
 
 ## HUD Occpacity ##
  75,   #   0 - 100  |75 Default
]

controllers = [[
 ### GOTO https://www.pygame.org/docs/ref/key.html for more information ###
 ### CONTROLLER INPUT HASN'T BEEN IMPLIMENTED YET!!! ###

 ## PLAYER 1 ##
 0,   #Type [Default:0]
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
 0,     #Type [Default:0]
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

service = [
 ### Enable AutoStaring Service ##
 False, # True/False | Default: True
 ## (if enabeld, MCAddress and MCPort is not used) ##
 
 ## ManualConnect Address ##
 "", #Default: "" or "localhost"
 ## ManualConnect Port ##
 1214, # 1-65535 | Default: 1213
]

## END OF SETTINGS ##



















































































































































































































































































































































#Wait that wasn't the end??
EasterEgg = False #WHAT IS THIS?!?! | True/False
#Who put this this here??
