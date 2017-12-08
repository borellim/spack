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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install r-rcurl
#
# You can edit this file again by typing:
#
#     spack edit r-rcurl
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class RRcurl(RPackage):
    """A wrapper for 'libcurl' <http://curl.haxx.se/libcurl/> Provides
       functions to allow one to compose general HTTP requests and provides
       convenient functions to fetch URIs, get & post forms, etc. and process
       the results returned by the Web server. This provides a great deal of
       control over the HTTP/FTP/... connection and the form of the request
       while providing a higher-level interface than is available just using
       R socket connections. Additionally, the underlying implementation is
       robust and extensive, supporting FTP/FTPS/TFTP (uploads and downloads),
       SSL/HTTPS, telnet, dict, ldap, and also supports cookies, redirects,
       authentication, etc."""

    homepage = "https://cran.rstudio.com/web/packages/RCurl/index.html"
    url      = "https://cran.rstudio.com/src/contrib/RCurl_1.95-4.8.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RCurl"

    version('1.95-4.8', '9c8aaff986eb2792c89dd3ae54d21580')

    depends_on('r-bitops', type=('build', 'run'))
    depends_on('curl')
