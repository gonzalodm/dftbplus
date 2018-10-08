#------------------------------------------------------------------------------#
#  DFTB+: general package for performing fast atomistic simulations            #
#  Copyright (C) 2018  DFTB+ developers group                                  #
#                                                                              #
#  See the LICENSE file for terms of usage and distribution.                   #
#------------------------------------------------------------------------------#
#

'''Tests for dp_bands.'''

import sys
import os.path
import unittest
import tempfile
import common
from dptools.scripts.common import ScriptError
import dptools.scripts.dp_bands as dp_bands


SCRIPTDIR = os.path.dirname(sys.argv[0])


class Xyz2genTest(common.TestWithWorkDir):
    '''General tests for dp_bands'''

    def setUp(self):
        self.inputdir = os.path.join(SCRIPTDIR, 'dp_bands')
        self.workroot = './'
        common.TestWithWorkDir.setUp(self)

    def test_one_spinchannel(self):
        '''Single spin channel and one k-point with enumeration'''
        infile = self.get_input('band.out')
        reffile = self.get_input('band_tot.dat')
        outfile = self.get_output('band_tot.dat')
        outprefix = self.get_output('band')
        cmdargs = [infile, outprefix]
        dp_bands.main(cmdargs)
        self.assertTrue(common.nxy_file_equals(outfile, reffile))

    def test_no_enumeration(self):
        '''Single spin channel and one k-point without enumeration'''
        infile = self.get_input('band.out')
        reffile = self.get_input('band_no-enumeration_tot.dat')
        outfile = self.get_output('band_no-enumeration_tot.dat')
        outprefix = self.get_output('band_no-enumeration')
        cmdargs = ['-N', infile, outprefix]
        dp_bands.main(cmdargs)
        self.assertTrue(common.nxy_file_equals(outfile, reffile))

    def test_two_spinchannels(self):
        '''Two spin channels and multiple k-points'''
        infile = self.get_input('band-separate-spins.out')
        reffile_s1 = self.get_input('band-separate-spins_s1.dat')
        reffile_s2 = self.get_input('band-separate-spins_s2.dat')
        outfile_s1 = self.get_output('band-separate-spins_s1.dat')
        outfile_s2 = self.get_output('band-separate-spins_s2.dat')
        outprefix = self.get_output('band-separate-spins')
        cmdargs = ['-s', infile, outprefix]
        dp_bands.main(cmdargs)
        self.assertTrue(common.nxy_file_equals(outfile_s1, reffile_s1))
        self.assertTrue(common.nxy_file_equals(outfile_s2, reffile_s2))

    def test_fail_superfluous_arguments(self):
        '''Failing due to superfluous arguments.'''
        infile = self.get_input('band.out')
        outprefix = self.get_output('band')
        cmdargs = [infile, outprefix, 'something']
        with self.assertRaises(ScriptError):
            dp_bands.main(cmdargs)

    def test_fail_missing_arguments(self):
        '''Failing due to missing arguments.'''
        infile = self.get_input('band.out')
        cmdargs = [infile]
        with self.assertRaises(ScriptError):
            dp_bands.main(cmdargs)

    def test_fail_invalid_infile(self):
        '''Failing due to invalid input file.'''
        temp_file = tempfile.NamedTemporaryFile(dir=self.workroot)
        tempname = temp_file.name
        temp_file.close()
        nonexisting_infile = os.path.join(self.workdir, tempname)
        outprefix = self.get_output('band')
        cmdargs = [nonexisting_infile, outprefix]
        with self.assertRaises(ScriptError):
            dp_bands.main(cmdargs)


if __name__ == '__main__':
    unittest.main()
