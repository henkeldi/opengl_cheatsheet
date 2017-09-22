
# EGL Offscreen Context Cheatsheet

### Import

```python
'''
if not os.environ.get( 'PYOPENGL_PLATFORM' ):
    os.environ['PYOPENGL_PLATFORM'] = 'egl'
'''

from OpenGL.EGL import *
```

### Create context

```python
major, minor = ctypes.c_long(), ctypes.c_long()
display = eglGetDisplay(EGL_DEFAULT_DISPLAY)
log.info( 'Display return value: %s', display)
log.info( 'Display address: %s', display.address)
if not eglInitialize(display, major, minor):
    raise RuntimeError('Unable to initialize')
log.info('EGL version %s.%s', major.value, minor.value)

num_configs = ctypes.c_long()
configs = (EGLConfig*2)()

eglChooseConfig(display, None, configs, 2, num_configs)

eglBindAPI(EGL_OPENGL_API)

ctx = eglCreateContext(display, configs[0], EGL_NO_CONTEXT, None)
if ctx == EGL_NO_CONTEXT:
    raise RuntimeError( 'Unable to create context' )

eglMakeCurrent( display, EGL_NO_SURFACE, EGL_NO_SURFACE, ctx )
```

### Terminate
```python
eglTerminate(display)
```