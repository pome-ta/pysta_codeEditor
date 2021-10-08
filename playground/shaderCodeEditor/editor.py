import ui
from objc_util import ObjCClass, on_main_thread, ObjCInstance

import pdbg


class CodeEditorView:
  def __init__(self, mode='python', ext_kb=True, *args, **kwargs):
    valid_modes = {
      'python': 'OMPythonSyntaxHighlighter',
      'html': 'OMHTMLSyntaxHighlighter',
      'javascript': 'OMJavaScriptSyntaxHighlighter',
      'markdown': 'OMMarkdownSyntaxHighlighter',
      'text': 'OMBaseSyntaxHighlighter'
    }
    if mode not in valid_modes:
      raise ValueError('invalid syntax mode')
    
    OMTextEditorView = ObjCClass('OMTextEditorView')
    
    OMSyntaxHighlighterTheme = ObjCClass('OMSyntaxHighlighterTheme')
    SyntaxHighlighter = ObjCClass(valid_modes[mode])
    
    PA2UITheme = ObjCClass('PA2UITheme')
    theme_dict = PA2UITheme.sharedTheme().themeDict().mutableCopy()
    #theme_dict.autorelease()
    theme_dict['font-family'] = 'Source Code Pro'
    theme_dict['font-size'] = 16
    theme = OMSyntaxHighlighterTheme.alloc().initWithDictionary_(theme_dict)
    
    #f = CGRect(CGPoint(0, 0), CGSize(100.0, 100.0))
    f = ((0.0, 0.0), (100.0, 100.0))
    self.editor_view = OMTextEditorView.alloc().initWithFrame_syntaxHighlighterClass_theme_(f, SyntaxHighlighter, theme)
    self.editor_view.textView().setAutocapitalizationType_(0)
    self.editor_view.textView().setAutocorrectionType_(1)
    flex_width, flex_height = (1 << 1), (1 << 4)
    self.editor_view.setAutoresizingMask_(flex_width | flex_height)
    #margins = UIEdgeInsets(16, 10, 16, 10)
    #self.editor_view.setMarginsForPortrait_landscape_(margins, margins)
    if ext_kb:
      kb_types = {
        'python': 'KeyboardAccessoryTypePythonCompact',
        'markdown': 'KeyboardAccessoryTypeMarkdownWithoutSnippets',
        'html': 'KeyboardAccessoryTypeHTML',
        'javascript': 'KeyboardAccessoryTypeHTML'
      }
      kb_type = kb_types.get(mode)
      if kb_type:
        OMKeyboardAccessoryView = ObjCClass('OMKeyboardAccessoryView')
        accessory_view = OMKeyboardAccessoryView.alloc().initWithType_dark_(kb_type, False)#.autorelease()
        self.editor_view.setKeyboardAccessoryView_(accessory_view)
    
    self.editor_view.setOpaque_(0)
    self.editor_view.setBackgroundColor_((0.0, 0.0, 0.0, 0.0))

class MainView(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    #self.bg_color = 'maroon'
    
    self.cev = CodeEditorView()
    self.objc_instance.addSubview_(self.cev.editor_view)


if __name__ == '__main__':
  view = MainView()
  #view.present(style='fullscreen', orientations=['portrait'])
  view.present()



