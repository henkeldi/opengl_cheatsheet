
# CYGLFW3 Cheatsheet

## Basics

### Import

```python
import cyglfw3 as glfw
```

### Print Version
```python
print '%d.%d.%d' % glfw.GetVersion()
print glfw.GetVersionString()
```

### Initialize

```python
if not glfw.Init():
    # Handle initialization failure
```

### Query monitor info

```python
for monitor in glfw.GetMonitors():
    mode = glfw.GetVideoMode(monitor)
    W, H = glfw.GetMonitorPhysicalSize(monitor)
    print mode.width, mode.height
    # 1680 1050, 1920 1080
    print glfw.GetMonitorPos(monitor)
    # (1920, 0), (0, 0)
    print glfw.GetMonitorName(monitor)
    # DVI-D-0, HDMI-0
```

### Create Window

```python
glfw.WindowHint(glfw.CONTEXT_VERSION_MAJOR, 4)
glfw.WindowHint(glfw.CONTEXT_VERSION_MINOR, 5)
glfw.WindowHint(glfw.SAMPLES, 4)
window = glfw.CreateWindow(640, 480, "My Title", None, None)
glfw.MakeContextCurrent(window)
```

### Rendering loop
```python
while not glfw.WindowShouldClose(window):
    # render here

    glfw.SwapBuffers(window)
    glfw.PollEvents()
```

### Terminate
```python
glfw.Terminate()
```

### Close Window
```python
glfw.SetWindowShouldClose(window, True)
```

### Cursor

```python
glfw.SetInputMode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
# glfw.SetInputMode(window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
# glfw.SetInputMode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)

glfw.SetCursor(window, cursor)
# glfw.ARROW_CURSOR
# glfw.IBEAM_CURSOR 
# glfw.CROSSHAIR_CURSOR
# glfw.HAND_CURSOR
# glfw.HRESIZE_CURSOR
# glfw.VRESIZE_CURSOR
```

## Callbacks


### Error
```python
def glfw_error_callback(code, description):
    # glfw.NOT_INITIALIZED
    # glfw.NO_CURRENT_CONTEXT
    # glfw.INVALID_ENUM
    # glfw.INVALID_VALUE
    # glfw.OUT_OF_MEMORY
    # glfw.API_UNAVAILABLE
    # glfw.VERSION_UNAVAILABLE
    # glfw.PLATFORM_ERROR
    # glfw.FORMAT_UNAVAILABLE
    # glfw.NO_WINDOW_CONTEXT

glfw.SetErrorCallback(glfw_error_callback)
```

### Framebuffer
```python
def framebuffer_size_callback(window, width, height):
    pass

glfw.SetFramebufferSizeCallback(window, framebuffer_size_callback)
```

### Keyboard
```python
def key_callback(window, key, scancode, action, mods):
    # action: glfw.PRESS, glfw.RELEASE, glfw.REPEAT
    # mods: glfw.MOD_SHIFT, glfw.MOD_CONTROL, glfw.MOD_ALT, glfw.MOD_SUPER

def character_callback(window, codepoint):
    pass

def charmods_callback(window, codepoint, mods):
    pass

glfw.SetKeyCallback(window, key_callback)
glfw.SetCharCallback(window, character_callback)
glfw.SetCharModsCallback(window, charmods_callback)
```
GLFW-Keys [ext. link](http://www.glfw.org/docs/latest/group__keys.html)
### Mouse
```python
def cursor_pos_callback(window, xpos, ypos):
    pass

def cursor_enter_callback(window, entered):
    pass

def mouse_button_callback(button, action, mods):
    # button: glfw.MOUSE_BUTTON_LEFT, glfw.MOUSE_BUTTON_MIDDLE, glfw.MOUSE_BUTTON_RIGHT
    # action: glfw.PRESS, glfw.RELEASE

def scroll_callback(window, xoffset, yoffset):
    pass

glfw.SetCursorPosCallback(window, cursor_pos_callback)
glfw.SetCursorEnterCallback(window, cursor_enter_callback)
glfw.SetMouseButtonCallback(window, mouse_button_callback)
glfw.SetScrollCallback(window, scroll_callback)
```

### Drop
```python
def drop_callback(window, count, paths):
    pass

glfw.SetDropCallback(window, drop_callback)
```

## Advanced

### Cursors

```python
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

cursor = create_cursor('path/to/img.png', 128, 128)
glfw.SetCursor(window, cursor)
# glfw.DestroyCursor(cursor)
```

### Center window

```python
def center_pos(monitor_id, W, H):
    # W, H: window dimensions
    mon = glfw.GetMonitors()
    xpos = glfw.GetMonitorPos(mon[monitor_id])[0]+glfw.GetVideoMode(mon[monitor_id]).width/2-W/2
    ypos = glfw.GetMonitorPos(mon[monitor_id])[1]+glfw.GetVideoMode(mon[monitor_id]).height/2-H/2
    glfw.SetWindowPos(window, xpos, ypos)
```

### Framerate counter
```python
previous_second = glfw.GetTime()
frame_count = 0.0

def update_fps_counter():
    global previous_second, frame_count
    current_second = glfw.GetTime()
    elapsed_seconds = current_second - previous_second
    if elapsed_seconds > 0.25:
        previous_second = current_second
        fps = float(frame_count) / float(elapsed_seconds)
        glfw.SetWindowTitle(window, '%s @ FPS: %.2f' % (window_title, fps))
        frame_count = 0.0
    frame_count += 1.0
```
Source: [ext. link](http://antongerdelan.net/opengl/glcontext2.html)

### Terminate on exit

```python
import atexit

@atexit.register
def on_exit():
    glfw.Terminate()
```


# References
* GLFW guide [ext. link](http://www.glfw.org/docs/latest/)


