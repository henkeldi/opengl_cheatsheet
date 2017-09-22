#version 450 core

layout (location=0) out vec4 color;

in vec3 vs_color;

void main(){
	color = vec4(vs_color, 1.0);
}