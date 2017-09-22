# -*- coding: utf-8 -*-
import numpy as np

import cyglfw3 as glfw
import atexit

from OpenGL.GL import *

@atexit.register
def on_exit():
    glfw.Terminate()

W = 1024
H = int(W / (16./9.))
window_title = "OpenGL Test"
monitor = 0

def glfw_error_callback(code, description):
    print 'GLFW Error', code, description
    exit(-1)

glfw.SetErrorCallback(glfw_error_callback)

assert glfw.Init()

glfw.WindowHint(glfw.SAMPLES, 16)

window = glfw.CreateWindow(W, H, window_title, None, None)
glfw.MakeContextCurrent(window)

def center_pos(monitor_id, W, H):
    # W, H: window dimensions
    mon = glfw.GetMonitors()
    xpos = glfw.GetMonitorPos(mon[monitor_id])[0]+glfw.GetVideoMode(mon[monitor_id]).width/2-W/2
    ypos = glfw.GetMonitorPos(mon[monitor_id])[1]+glfw.GetVideoMode(mon[monitor_id]).height/2-H/2
    glfw.SetWindowPos(window, xpos, ypos)

center_pos(monitor, W, H)

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

def add_shader(program, file, type):
    shader = glCreateShader(type)
    with open(file, 'r') as f:
        glShaderSource(shader, f.read())
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        print glGetShaderInfoLog(shader)
        exit(-1)
    glAttachShader(program, shader)

program = glCreateProgram()
add_shader(program, 'shader.vs', GL_VERTEX_SHADER)
add_shader(program, 'shader.frag', GL_FRAGMENT_SHADER)
glLinkProgram(program)

if not glGetProgramiv(program, GL_LINK_STATUS):
    print glGetProgramInfoLog(program)
    exit(-1)

glUseProgram(program)

vertices = np.array([-0.5, -0.5, 0.5, -0.5, -0.5, 0.5, 0.5, 0.5], dtype=np.float32)
colors = np.array([255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 255, 255, 255, 0], dtype=np.uint8)
indices = np.array([0, 1, 2, 2, 1, 3], dtype=np.uint8)
ibo_data = np.array([6, 1, 0, 0, 0], dtype=np.uint32)

buf = np.empty(4, dtype=np.uint32)
glCreateBuffers(len(buf), buf)
glNamedBufferStorage(buf[0], vertices.nbytes, vertices, 0)
glNamedBufferStorage(buf[1], colors.nbytes, colors, 0)
glNamedBufferStorage(buf[2], indices.nbytes, indices, 0)
glNamedBufferStorage(buf[3], ibo_data.nbytes, ibo_data, 0)

vao = np.empty(1, dtype=np.uint32)
glCreateVertexArrays(len(vao), vao)

glVertexArrayAttribFormat(vao, 0, 2, GL_FLOAT, GL_FALSE, 0)
glVertexArrayVertexBuffer(vao, 0, buf[0], 0, 2*4)
glEnableVertexArrayAttrib(vao, 0)

glVertexArrayAttribBinding(vao, 0, 0)

glVertexArrayAttribFormat(vao, 1, 3, GL_UNSIGNED_BYTE, GL_TRUE, 0)
glVertexArrayVertexBuffer(vao, 1, buf[1], 0, 3)
glEnableVertexArrayAttrib(vao, 1)

glVertexArrayAttribBinding(vao, 1, 1)

glVertexArrayElementBuffer(vao, buf[2])

glBindVertexArray(vao)
glBindBuffer(GL_DRAW_INDIRECT_BUFFER, buf[3])

while not glfw.WindowShouldClose(window):
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.8, 0.8, 0.0, 1.0)
    glViewport(0, 0, W, H)

    #glDrawArrays(GL_TRIANGLES, 0, 6)
    #glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, None)
    glDrawElementsIndirect(GL_TRIANGLES, GL_UNSIGNED_BYTE, ctypes.c_void_p(0*20))

    glfw.SwapBuffers(window)
    glfw.PollEvents()
    update_fps_counter()
