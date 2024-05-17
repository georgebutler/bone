#version 330

#if defined VERTEX_SHADER

in vec3 in_position;

uniform mat4 m_camera;
uniform mat4 m_proj;

out vec3 v_texcoord;

void main() {
    v_texcoord = in_position;
    mat4 view = mat4(mat3(m_camera));  // Remove translation from the view matrix
    gl_Position = m_proj * view * vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;

uniform samplerCube skybox;

in vec3 v_texcoord;

void main() {
    fragColor = texture(skybox, v_texcoord);
}
#endif
