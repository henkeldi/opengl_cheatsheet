#version 450 core

layout (location=0) in vec2 position;
layout (location=1) in vec3 color;

out vec3 vs_color;

void main(){
	gl_Position = vec4(position.x, position.y, 0.0, 1.0);
	vs_color = color;
}