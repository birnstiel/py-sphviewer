# from distutils.core import setup, Extension
try:
    from setuptools import setup, Extension
    from setuptools.command.build_ext import build_ext
except ImportError:
    from distutils.core import setup, Extension
    from distutils.command.build_ext import build_ext

from distutils.errors import CompileError

import numpy as np

# First we find out what link/etc. flags we want based on the compiler.


def has_flags(compiler, flags, include_dirs=None):
    """
    This checks whether our C compiler allows for a flag to be passed,
    by compiling a small test program.
    """
    import tempfile
    from distutils.errors import CompileError

    with tempfile.NamedTemporaryFile("w", suffix=".c") as f:
        f.write(
            "#include <omp.h>\nint main (int argc, char **argv) { return omp_get_max_threads(); }")
        try:
            compiler.compile([f.name], extra_postargs=flags,
                             include_dirs=include_dirs or [])
        except CompileError:
            return False
    return True


# Build a build extension class that allows for finer selection of flags.

class BuildExt(build_ext):
    # Never check these; they're always added.
    # Note that we don't support MSVC here.
    compile_flags = {"unix": ["-std=c99", "-w",
                              "-ffast-math", "-I{:s}".format(np.get_include())]}

    def build_extensions(self):
        import sys
        import os
        ct = self.compiler.compiler_type
        opts = self.compile_flags.get(ct, [])
        links = []

        # Collect potential include/lib dirs for OpenMP (conda-forge, homebrew)
        omp_include_dirs = [os.path.join(sys.prefix, "include")]
        omp_lib_dirs = [os.path.join(sys.prefix, "lib")]

        # Check for the presence of -fopenmp; if it's there we're good to go!
        if has_flags(self.compiler, ["-fopenmp"], include_dirs=omp_include_dirs):
            # Generic case, this is what GCC accepts
            opts += ["-fopenmp"]
            links += ["-lgomp"]

        elif has_flags(self.compiler, ["-Xpreprocessor", "-fopenmp"],
                       include_dirs=omp_include_dirs):
            # clang on macOS with omp from conda-forge (llvm-openmp) or homebrew
            opts += ["-Xpreprocessor", "-fopenmp"]
            opts += ["-I" + d for d in omp_include_dirs]
            links += ["-lomp"]
            links += ["-L" + d for d in omp_lib_dirs]

        else:

            raise CompileError("Unable to compile C extensions on your machine, as we can't find OpenMP. "
                               "If you are on MacOS, try `brew install libomp` and try again. "
                               "If you are on Windows, please reach out on the GitHub and we can try "
                               "to find a solution.")

        for ext in self.extensions:
            ext.extra_compile_args = opts
            ext.extra_link_args = links

        build_ext.build_extensions(self)


extensions = [
    Extension(path, sources=[source])
    for path, source in {
        "sphviewer/extensions/scene": "sphviewer/extensions/scenemodule.c",
        "sphviewer/extensions/render": "sphviewer/extensions/rendermodule.c",
        "sphviewer/tools/makehsv": "sphviewer/tools/makehsvmodule.c",
    }.items()
]

# __version__ is set in the below file, but use this here to avoid warnings.
__version__ = None
exec(open("sphviewer/version.py").read())

setup(
    name="py-sphviewer",
    version=__version__,
    description="Py-SPHViewer is a framework for rendering particles using the smoothed particle hydrodynamics scheme.",
    author="Alejandro Benitez Llambay",
    author_email="bllalejandro@gmail.com",
    url="https://github.com/alejandrobll/py-sphviewer",
    packages=["sphviewer", "sphviewer.extensions", "sphviewer.tools"],
    include_dirs=[np.get_include()],
    requires=["pykdtree", "numpy", "matplotlib", "scipy"],
    install_requires=["pykdtree", "numpy", "matplotlib", "scipy"],
    package_data={"sphviewer": ["*.c", "*.txt"]},
    cmdclass=dict(build_ext=BuildExt),
    ext_modules=extensions,
    license="GNU GPL v3",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: 3D Rendering",
        "Topic :: Multimedia :: Graphics :: Viewers",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Utilities",
    ],
    keywords="smoothed particle hydrodynamics render particles nbody galaxy formation dark matter sph cosmology movies",
)
