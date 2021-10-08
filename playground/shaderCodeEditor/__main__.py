# xxx: ui.View に統合
from pathlib import Path
import scene
import ui

src = '''
precision highp float;

uniform float u_time;
uniform vec2 u_sprite_size;
uniform float u_scale;
uniform sampler2D u_texture;
uniform vec4 u_tint_color;
uniform vec4 u_fill_color;
varying vec2 v_tex_coord;


float saturate(float f){
   return clamp(f, 0.0, 1.0);
}

vec2 rotate(vec2 uv, vec2 center, float angle){
  vec2 c1 = center * vec2(-1.0);
  vec2 adduv = c1 + uv;
  
  float a1 = sin(angle) * -1.0;
  float a2 = cos(angle);
  vec2 ap1 = vec2 (a2, a1);
  vec2 ap2 = vec2(sin(angle), a2);
  
  float uu = dot(adduv, ap1);
  float vv = dot(adduv, ap2);
  
  vec2 uuvv = vec2(uu, vv);
  vec2 result = center + uuvv;
  return result;
}

void main(){
  float t = u_time;
  vec2 uv = v_tex_coord;
  //uv = (uv - vec2(0.5)) * 2.0;
  
  vec2 p = abs((uv- vec2(0.5)) / 0.5);
  float l = 1.0 - length(p);
  
  float n = saturate(l) * 10.0;
  
  float pi = acos(-1.0);
  float m = (t * 0.5) * (pi * 2.0);
  
  float o = n + m;
  
  vec2 mix = rotate(uv, vec2(0.5), o);
  
  //mix = mix / 2.0 + vec2(0.5);
  uv = uv / 2.0 + vec2(0.5);
  //if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0)discard;
  gl_FragColor = vec4(mix, 0.0, 1.0);
  //gl_FragColor = texture2D(u_texture,uv.xy);
  
}
'''


class ShaderScene(scene.Scene):
  def setup(self):

    self.shdr = scene.SpriteNode(parent=self)
    #self.shdr.texture = img
    _x = self.size.x * .88
    _y = self.size.y * .64
    self.shdr.size = (_x, _x)
    #shdr.size=self.size
    self.shdr.shader = scene.Shader(src)
    self.shdr.shader.set_uniform('u_resolution', (_x, _x))
    # todo: Initial position before touching
    self.shdr.shader.set_uniform('u_offset', (0.5, 0.5))

  def did_change_size(self):
    # todo: Center the image
    self.shdr.position = self.size / 2
    _x = self.size.x * .88
    _y = self.size.y * .64
    self.shdr.size = (_x, _x)


class MainView(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    #interval = 60
    #self.update_interval = 1 / interval
    self.bg_color = 'maroon'

    self.shader_scene = ShaderScene()
    self.ui_scene = scene.SceneView()
    self.ui_scene.shows_fps = True
    self.ui_scene.frame_interval = 2  # 30fps
    self.ui_scene.scene = self.shader_scene

    self.add_subview(self.ui_scene)

  def layout(self):
    self.ui_scene.width = self.width
    self.ui_scene.height = self.height
    self.shader_scene.did_change_size()


if __name__ == '__main__':
  view = MainView()
  view.present(style='fullscreen', orientations=['portrait'])

