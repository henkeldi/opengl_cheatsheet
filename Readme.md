
# PyOpenGL 4.5 Cheatsheet

## Import

```python
from OpenGL.GL import *
```

## OpenGL context

* [GLFW Window](doc/GLFW.md)
* [EGL Offscreen context](doc/EGL.md)

## Framebuffer

```python
fbo = np.empty(1, dtype=np.uint32)
glCreateFramebuffers(len(fbo), fbo)

glNamedFramebufferTexture(fbo, attachment, attachement_id, level)

glNamedFramebufferRenderbuffer(fbo, attachment, GL_RENDERBUFFER, attachement_id)

# attachment:
# GL_COLOR_ATTACHMENT{i}
# GL_DEPTH_ATTACHMENT
# GL_STENCIL_ATTACHMENT
# GL_DEPTH_STENCIL_ATTACHMENT

glNamedFramebufferDrawBuffers(fbo, 2, np.array( (GL_COLOR_ATTACHMENT0,GL_COLOR_ATTACHMENT1),dtype=np.uint32 ) )
```

## Buffers

```python
vertices = <numpy array>

buf = np.empty(1, dtype=np.uint32)
glCreateBuffers(len(buf), buf)
# code = 0 if not dynamic else GL_DYNAMIC_STORAGE_BIT | GL_MAP_WRITE_BIT| GL_MAP_PERSISTENT_BIT
glNamedBufferStorage(buf, vertices.nbytes, vertices, code)


glBindBuffer(<type> ,buf)
# GL_ELEMENT_ARRAY_BUFFER
# GL_DRAW_INDIRECT_BUFFER
# GL_SHADER_STORAGE_BUFFER
```

## VAO

```python
vao = np.empty(1, dtype=np.uint32)
glCreateVertexArrays(len(vao), vao)

glVertexArrayAttribFormat(vao, attribindex, size, attribtype, normalized, relativeoffset)
glVertexArrayAttribBinding(vao, attribindex, i)
glEnableVertexArrayAttrib(vao, attribindex)

glVertexArrayVertexBuffer(vao, i, vbo, offset, stride)

glVertexArrayElementBuffer(vao, ebo_id)

glBindVertexArray(vao)
```

## Shader

```python
program = glCreateProgram()

shader = glCreateShader(<shader_type>)
# GL_VERTEX_SHADER
# GL_TESS_CONTROL_SHADER
# GL_TESS_EVALUATION_SHADER
# GL_GEOMETRY_SHADER 
# GL_FRAGMENT_SHADER 
# GL_COMPUTE_SHADER

glShaderSource(shader, shader_code)
glCompileShader(shader)

if not glGetShaderiv(shader, GL_COMPILE_STATUS):
    print glGetShaderInfoLog(shader)

glAttachShader(program, shader)

glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    print glGetProgramInfoLog(program)

glDeleteShader(shader)

glUseProgram(program)
```

## Texture

```python
tex = np.empty(1, dtype=np.uint32)
glCreateTextures(tex_type, len(tex), tex)
glTextureStorage2D(tex, levels, internalformat, W, H)

glTextureParameteri(tex, GL_TEXTURE_MIN_FILTER, min_filter)
glTextureParameteri(tex, GL_TEXTURE_MAG_FILTER, max_filter)

glTextureParameteri(tex, GL_TEXTURE_WRAP_S, wrap_s)
glTextureParameteri(tex, GL_TEXTURE_WRAP_T, wrap_t)
glTextureParameteri(tex, GL_TEXTURE_WRAP_R, wrap_r)

glTextureSubImage2D(tex, level, xoffset, yoffset, 
    width, height, data_format, data_type, pixels)

glGenerateTextureMipmap(tex)

handle = glGetTextureHandleNV(tex)
glMakeTextureHandleResidentNV(handle)

glMakeTextureHandleNonResidentNV(handle)

```

## Renderbuffer

```python
rb = np.empty(1, dtype=np.uint32)
glCreateRenderbuffers(len(rb), rb)
glNamedRenderbufferStorage(rb, internalformat, W, H)

# glNamedRenderbufferStorageMultisample(rb, samples, internalformat, W, H)
```


## Render loop

```python
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT |  GL_STENCIL_BUFFER_BIT)
glViewport(0, 0, W, H)

glNamedBufferSubData(buf, offset, nbytes, data)

# glDrawElementsIndirect(GL_TRIANGLES, GL_UNSIGNED_INT, ctypes.c_void_p(obj_id*20))
# glDrawArraysIndirect(GL_TRIANGLES, ctypes.c_void_p(obj_id*16))
# glDrawArrays(GL_TRIANGLES, 0, 4) # First, count
# glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, None)
```