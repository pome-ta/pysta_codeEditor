# coding: utf-8

# https://forum.omz-software.com/topic/2808/bug-objc_util-and-dir

from objc_util import ObjCClass

all = ObjCClass.get_names('')
[print(cls) for cls in all if '_' != cls[0]]

# --- _all
#print('\n'.join(ObjCClass.get_names('')))
