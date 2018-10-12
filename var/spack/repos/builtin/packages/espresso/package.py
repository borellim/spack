##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import glob
import os.path

from spack import *


class Espresso(Package):
    """Quantum-ESPRESSO is an integrated suite of Open-Source computer codes
    for electronic-structure calculations and materials modeling at the
    nanoscale. It is based on density-functional theory, plane waves, and
    pseudopotentials.
    """

    homepage = 'http://quantum-espresso.org'
    url = 'http://www.qe-forge.org/gf/download/frsrelease/204/912/espresso-5.3.0.tar.gz'

    version(
        '6.3-backports-20181003',
        git='https://gitlab.com/QEF/q-e.git',
        commit='29c951ebbfc3b2248d0308102d05c4c081db891e'
    )

    version(
        '6.3-backports-20180919',
        git='https://gitlab.com/QEF/q-e.git',
        commit='90a2aa88298f5005b8ab8f5fcc354c5870481d68'
    )

    version(
        '6.3',
        '1b67687d90d1d16781d566d44d14634c',
        url='https://gitlab.com/QEF/q-e/-/archive/qe-6.3/q-e-qe-6.3.tar.gz'
    )

    version(
        '6.2.2-git-20180305-a027060a11',
        git='https://gitlab.com/QEF/q-e.git',
        commit='a027060a11b37deacfc2aacc1d869ef7748001af'
    )

    version(
        '6.2.1',
        'e9d92b51a8b9983766a89a164bfac36f',
        url='http://qe-forge.org/gf/download/frsrelease/247/1132/qe-6.2.1.tar.gz'
    )

    version(
        '6.2.0',
        '016e7f22dba2086cc80c0f98447ddf1b',
        url='http://qe-forge.org/gf/download/frsrelease/244/1114/qe-6.2.tar.gz'
    )

    version(
        '6.1.0',
        'db398edcad76e085f8c8a3f6ecb7aaab',
        url='http://www.qe-forge.org/gf/download/frsrelease/240/1075/qe-6.1.tar.gz'
    )

    version(
        '5.4.0',
        '8bb78181b39bd084ae5cb7a512c1cfe7',
        url='http://www.qe-forge.org/gf/download/frsrelease/211/968/espresso-5.4.0.tar.gz'
    )
    version('5.3.0', '6848fcfaeb118587d6be36bd10b7f2c3')

    variant('mpi', default=True, description='Builds with mpi support')
    variant('openmp', default=False, description='Enables openMP support')
    variant('scalapack', default=True, description='Enables scalapack support')
    variant('elpa', default=True, description='Uses elpa as an eigenvalue solver')

    # Support for HDF5 has been added starting in version 6.1.0 and is
    # still experimental, therefore we default to False for the variant
    variant('hdf5', default=False, description='Builds with HDF5 support')

    # Added by Marco for QE 6.2
    variant('oldxml', default=False, description='Use the old XML format for machine-readable output')

    # Added by Marco - WARNING: dummy variant!
    #variant('perftools', default=False, description='Dummy variant to distinguish build with CrayPAT')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')
    depends_on('scalapack', when='+scalapack+mpi')

    depends_on('fftw+mpi', when='+mpi')
    depends_on('fftw~mpi', when='~mpi')
    depends_on('elpa+openmp', when='+elpa+openmp')
    depends_on('elpa~openmp', when='+elpa~openmp')
    depends_on('hdf5', when='+hdf5')

    patch('dspev_drv_elpa.patch', when='@6.1: ^elpa@2016.05.004')
    #patch('dspev_drv_elpa.patch', when='@6.1: ^elpa@2016.05.003')
    patch('fix_make_install_v6.3.patch', when='@6.3')

    # We can't ask for scalapack or elpa if we don't want MPI
    conflicts(
        '+scalapack',
        when='~mpi',
        msg='scalapack is a parallel library and needs MPI support'
    )

    conflicts(
        '+elpa',
        when='~mpi',
        msg='elpa is a parallel library and needs MPI support'
    )

    # Elpa is formally supported by @:5.4.0, but QE configure searches
    # for it in the wrong folders (or tries to download it within
    # the build directory). Instead of patching Elpa to provide the
    # folder QE expects as a link, we issue a conflict here.
    conflicts('+elpa', when='@:5.4.0')
    conflicts('+hdf5', when='@:5.4.0')

    # Spurious problems running in parallel the Makefile
    # generated by the configure
    parallel = False

    def install(self, spec, prefix):

        prefix_path = prefix.bin if 'espresso@:5.4.0' in spec else prefix
        options = ['-prefix={0}'.format(prefix_path)]

        if '+mpi' in spec:
            options.append('--enable-parallel=yes')
        else:
            options.append('--enable-parallel=no')

        if '+openmp' in spec:
            options.append('--enable-openmp')

        if '+scalapack' in spec:
            scalapack_option = 'intel' if '^intel-mkl' in spec else 'yes'
            options.append('--with-scalapack={0}'.format(scalapack_option))

        if '+elpa' in spec:

            # Spec for elpa
            elpa = spec['elpa']

            # Find where the Fortran module resides
            elpa_module = find(elpa.prefix, 'elpa.mod')

            # Compute the include directory from there: versions
            # of espresso prior to 6.1 requires -I in front of the directory
            elpa_include = '' if 'espresso@6.1:' in spec else '-I'
            elpa_include += os.path.dirname(elpa_module[0])

            options.extend([
                '--with-elpa-include={0}'.format(elpa_include),
                '--with-elpa-lib={0}'.format(elpa.libs[0])
            ])

        if '+hdf5' in spec:
            options.append('--with-hdf5={0}'.format(spec['hdf5'].prefix))

        # Add a list of directories to search
        search_list = []
        for dependency_spec in spec.dependencies():
            search_list.extend([
                dependency_spec.prefix.lib,
                dependency_spec.prefix.lib64
            ])

        search_list = " ".join(search_list)

        options.extend([
            'LIBDIRS={0}'.format(search_list),
            'F90={0}'.format(env['SPACK_FC']),
            'CC={0}'.format(env['SPACK_CC'])
        ])

        configure(*options)

        if '+oldxml' in spec:
            filter_file(r'(^\s*MANUAL_DFLAGS\s*=)', r'\1 -D__OLDXML', 'make.inc')

        # Work around a bug in 6.3 which prevents cp.x from compiling if __OLDXML is set
        if spec.version == Version('6.3') and '+oldxml' in spec:
            print "WARNING: skipping target cp because it won't compile with -D__OLDXML"
            for target in ['pwall','ld1','upf','tddfpt','xspectra','gwl']:
                make(target)
        else:
            make('all')

        if 'platform=darwin' in spec:
            mkdirp(prefix.bin)
            for filename in glob.glob("bin/*.x"):
                install(filename, prefix.bin)
        else:
            make('install')
