# coding: utf-8

# https://forum.omz-software.com/topic/2808/bug-objc_util-and-dir

from objc_util import ObjCClass

all = ObjCClass.get_names('')


def out_log(log):
  print('\n'.join(log))


def main_log():
  out = [cls for cls in all if '_' != cls[0]]
  out_log(out)


def _all_log():
  out = [cls for cls in all]
  out_log(out)


def dunder_log():
  out = [cls for cls in all if '_' == cls[0]]
  out_log(out)


def pyobj_log():
  out = [cls for cls in all if ('OM' == cls[:2]) or ('PA' == cls[:2]) or ('PY' == cls[:2])]
  out_log(out)


if __name__ == '__main__':
  pyobj_log()

