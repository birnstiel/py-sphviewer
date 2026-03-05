project(
  'py-sphviewer',
  'c',
  version: '1.2.4',
  license: 'GPL-3.0-or-later',
  default_options: ['warning_level=0'],
)

py = import('python').find_installation(pure: false)

# numpy include path
numpy_inc = run_command(
  py, '-c', 'import numpy; print(numpy.get_include())',
  check: true,
).stdout().strip()

numpy_dep = declare_dependency(
  include_directories: include_directories(numpy_inc),
)

# OpenMP – optional, falls back to serial build
openmp_dep = dependency('openmp', required: false)
if not openmp_dep.found()
  warning('OpenMP not found – building without parallelism. Install llvm-openmp (conda) or libomp (brew) for better performance.')
endif

subdir('sphviewer')
