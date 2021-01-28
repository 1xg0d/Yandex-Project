import os

GRAVITY = 0.3

CURRENT_PATH = os.path.dirname(__file__) # Where your .py file is located
ASSETS_PATH = os.path.join(CURRENT_PATH, 'assets') # The resource folder path
SOUNDS_PATH = os.path.join(CURRENT_PATH, 'sounds')
downflap = os.path.join(ASSETS_PATH, 'fedka-downflap.png')
midflap = os.path.join(ASSETS_PATH, 'fedka-midflap.png')
upflap = os.path.join(ASSETS_PATH, 'fedka-upflap.png')
pipe_red = os.path.join(ASSETS_PATH, 'pipe-red.png')
base = os.path.join(ASSETS_PATH, 'base.png')
background = os.path.join(ASSETS_PATH, 'background.png')
message = os.path.join(ASSETS_PATH, 'message.png')
font = os.path.join(CURRENT_PATH, '04B_19.ttf')
wing = os.path.join(SOUNDS_PATH, 'sfx_wing.wav')
hit = os.path.join(SOUNDS_PATH, 'sfx_hit.wav')
point = os.path.join(SOUNDS_PATH, 'sfx_point.wav')
main = os.path.join(SOUNDS_PATH, 'main.wav')