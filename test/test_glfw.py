
import cyglfw3 as glfw
import atexit

@atexit.register
def on_exit():
    glfw.Terminate()

print '%d.%d.%d' % glfw.GetVersion()

print glfw.GetVersionString()

# error codes: http://www.glfw.org/docs/latest/group__errors.html

def glfw_error_callback(e, description):
    print e, description
    #glfw.NOT_INITIALIZED
    #glfw.NO_CURRENT_CONTEXT:
    #glfw.INVALID_ENUM:
    #glfw.INVALID_VALUE
    #glfw.OUT_OF_MEMORY
    #glfw.API_UNAVAILABLE
    #glfw.VERSION_UNAVAILABLE
    #glfw.PLATFORM_ERROR
    #glfw.FORMAT_UNAVAILABLE
    #glfw.NO_WINDOW_CONTEXT

glfw.SetErrorCallback(glfw_error_callback)

if not glfw.Init():
    exit(-1)
    # Handle initialization failure

monitor_id = 0

mon = glfw.GetMonitors()
for m in mon:
    mode = glfw.GetVideoMode(m)
    W, H = glfw.GetMonitorPhysicalSize(m)
    print mode.width, mode.height
    print glfw.GetMonitorPos(m)
    print glfw.GetMonitorName(m)

W = 1024
H = int(W / (16./9.))

window = glfw.CreateWindow(W, H, "My Title", None, None)
glfw.MakeContextCurrent(window)

def center_pos(monitor_id):
    xpos = glfw.GetMonitorPos(mon[monitor_id])[0]+glfw.GetVideoMode(mon[monitor_id]).width/2-W/2
    ypos = glfw.GetMonitorPos(mon[monitor_id])[1]+glfw.GetVideoMode(mon[monitor_id]).height/2-H/2
    glfw.SetWindowPos(window, xpos, ypos)

center_pos(monitor_id)

w,h  = glfw.GetFramebufferSize(window)

def key_callback(window, key, scancode, action, mods):
    global monitor_id
    if key == glfw.KEY_E and action == glfw.PRESS:
        monitor_id = (monitor_id + 1)% len(mon)
        center_pos( monitor_id )
    if key == glfw.KEY_N and action == glfw.PRESS:
        glfw.SetInputMode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)

glfw.SetKeyCallback(window, key_callback)

def character_callback(window, codepoint):
    print codepoint

#glfw.SetCharCallback(window, character_callback)

def charmods_callback(window, codepoint, mods):
    print codepoint, mods

glfw.SetCharModsCallback(window, charmods_callback)

def cursor_pos_callback(window, xpos, ypos):
    pass
    #print xpos, ypos

glfw.SetCursorPosCallback(window, cursor_pos_callback)

#glfw.SetInputMode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
#glfwSetCursor(window, glfw.CURSOR_NORMAL);

def cursor_enter_callback(window, entered):
    pass

glfw.SetCursorEnterCallback(window, cursor_enter_callback);

from scipy import misc
import numpy as np
from PIL import Image

def create_cursor_from_pixels(pixels, W, H):
    image = glfw.Image()
    im = 255*np.ones( (H,W,4), dtype=np.uint8)
    im[:,:,:pixels.shape[2]] = pixels
    image.pixels = im
    return glfw.CreateCursor(image, W/2, H/2)

def create_cursor(icon_path, W, H):
    pixels = Image.open(icon_path)
    pixels = np.array(pixels.resize((W, H), Image.ANTIALIAS))
    return create_cursor_from_pixels(pixels, W, H)

#glfw.IconifyWindow(window)
#glfw.RestoreWindow(window)

cursor = create_cursor('/home/dimitri/Pictures/Screenshot from 2017-08-06 15-04-26.png', 128, 128)
glfw.SetCursor(window, cursor)

i = 0
while not glfw.WindowShouldClose(window):

    glfw.SwapBuffers(window)
    glfw.PollEvents()

glfw.SetWindowTitle(window, "My Window")

glfw.SetWindowShouldClose(window, True)
