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
    node = scene.Node(self.size / 2)
    self.background_color = '#708090'
    self.add_child(node)
    sp_node = scene.ShapeNode(parent=node)
    x_line = scene.ShapeNode(parent=node)
    x_path = ui.Path()
    x_path.move_to(0.0, self.size.y)
    x_path.line_to(self.size.x, self.size.y)
    x_line.path = x_path
    x_line.stroke_color = 'maroon'
    

    y_line = scene.ShapeNode(parent=node)
    y_path = ui.Path()
    y_path.move_to(self.size.x, 0.0)
    y_path.line_to(self.size.x, self.size.y)
    y_line.path = y_path
    y_line.stroke_color = 'maroon'
    
    '''
    cross_x_line = scene.ShapeNode(parent=node)
    cross_x_path = ui.Path()
    cross_x_path.move_to(0.0, self.size.y)
    cross_x_path.line_to(self.size.x, 0.0)
    cross_x_line.path = cross_x_path
    cross_x_line.stroke_color = 'darkslategray'
    
    cross_y_line = scene.ShapeNode(parent=node)
    cross_y_path = ui.Path()
    cross_y_path.move_to(0.0, 0.0)
    cross_y_path.line_to(self.size.x, self.size.y)
    cross_y_line.path = cross_y_path
    cross_y_line.stroke_color = 'darkslategray'
    '''
    

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

    sp_node.size = self.shdr.size
    sp_node.color = 'darkslategray'
    #sp_node.color = 'skyblue'
    self.did_change_size()

  def did_change_size(self):
    # todo: Center the image
    self.shdr.position = self.size / 2

  def touch_began(self, touch):
    self.set_uniform_touch(touch)

  def touch_moved(self, touch):
    self.set_uniform_touch(touch)

  def set_uniform_touch(self, touch):
    dx, dy = (self.shdr.position - touch.location)
    dx /= self.shdr.size[0]
    dy /= self.shdr.size[1]
    self.shdr.shader.set_uniform('u_offset', (dx, dy))
    
    '''
    if touch.location in self.shdr.frame:
      #local_touch = touch.location - self.shdr.frame
      #dx = local_touch[0]# / self.shdr.size[0]
      #dy = local_touch[1]# / self.shdr.size[1]
      dx, dy = self.shdr.position - touch.location
      dx /= self.shdr.size[0]
      dy /= self.shdr.size[1]
      self.shdr.shader.set_uniform('u_offset', (dx, dy))
    '''


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
