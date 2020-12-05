# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install log-io-vol
#
# You can edit this file again by typing:
#
#     spack edit log-io-vol
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class LogIoVol(AutotoolsPackage):
    """A VOL driver that enable log-based storage layout for datasets."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/DataLib-ECP/log_io_vol/wiki"
    git      = "https://github.com/DataLib-ECP/log_io_vol.git"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['khou2020']

    # FIXME: Add proper versions and checksums here.
    version('master', branch='master')

    # Config options
    variant('shared', default=True, description='Enable shared library')
    variant('zlib', default=True, description='Enable metadata compression with zlib')
    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')

    # FIXME: Add dependencies if required.
    depends_on('mpi')
    depends_on('autoconf', when='@master', type='build')
    depends_on('automake', when='@master', type='build')
    depends_on('libtool', when='@master',  type='build')
    depends_on('m4',       type='build')
    depends_on('hdf5@1.12.0',  type=('build', 'link'))
    depends_on('zlib', when='+zlib', type=('build', 'link'))

    @when('@master')
    def autoreconf(self, spec, prefix):
        with working_dir(self.configure_directory):
            autoreconf('-i')

    def configure_args(self):
        args = ['--with-mpi=%s' % self.spec['mpi'].prefix,
                'SEQ_CC=%s' % spack_cc]

        flags = {
            'CFLAGS': [],
            'CXXFLAGS': [],
            'FFLAGS': [],
            'FCFLAGS': [],
        }

        if '+pic' in self.spec:
            flags['CFLAGS'].append(self.compiler.cc_pic_flag)
            flags['CXXFLAGS'].append(self.compiler.cxx_pic_flag)
            flags['FFLAGS'].append(self.compiler.f77_pic_flag)
            flags['FCFLAGS'].append(self.compiler.fc_pic_flag)

        for key, value in sorted(flags.items()):
            if value:
                args.append('{0}={1}'.format(key, ' '.join(value)))

        return args