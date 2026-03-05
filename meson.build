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

# OpenMP – prefer conda env libomp to avoid Homebrew/conda runtime conflict.
# With no-build-isolation the build runs inside the pixi/conda env, so
# $CONDA_PREFIX points to the active env.  If llvm-openmp is installed there
# we construct the dependency manually so the extension links against the same
# libomp that numpy/scipy already loaded.
fs = import('fs')
conda_prefix = run_command('sh', '-c', 'printf "%s" $CONDA_PREFIX', check: false).stdout().strip()
conda_libomp = conda_prefix / 'lib' / 'libomp.dylib'
if conda_prefix != '' and fs.is_file(conda_libomp)
  openmp_dep = declare_dependency(
    compile_args: ['-Xpreprocessor', '-fopenmp',
                   '-I' + conda_prefix / 'include'],
    link_args:    ['-L' + conda_prefix / 'lib', '-lomp'],
  )
  message('OpenMP: using conda env libomp at ' + conda_libomp)
else
  openmp_dep = dependency('openmp', required: false)
  if not openmp_dep.found()
    warning('OpenMP not found – building without parallelism.')
  endif
endif

subdir('sphviewer')
