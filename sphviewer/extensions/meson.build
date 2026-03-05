py.install_sources(
  ['__init__.py'],
  subdir: 'sphviewer/extensions',
)

ext_c_args = ['-std=c99', '-w', '-ffast-math']
ext_deps = [numpy_dep, openmp_dep]

py.extension_module(
  'scene',
  'scenemodule.c',
  dependencies: ext_deps,
  c_args: ext_c_args,
  install: true,
  subdir: 'sphviewer/extensions',
)

py.extension_module(
  'render',
  'rendermodule.c',
  dependencies: ext_deps,
  c_args: ext_c_args,
  install: true,
  subdir: 'sphviewer/extensions',
)
