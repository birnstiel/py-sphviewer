py.install_sources(
  [
    '__init__.py',
    'Blend.py',
    'camera_tools.py',
    'cmaps.py',
    'hsv_tools.py',
    'QuickView.py',
  ],
  subdir: 'sphviewer/tools',
)

py.extension_module(
  'makehsv',
  'makehsvmodule.c',
  dependencies: [numpy_dep, openmp_dep],
  c_args: ['-std=c99', '-w', '-ffast-math'],
  install: true,
  subdir: 'sphviewer/tools',
)
