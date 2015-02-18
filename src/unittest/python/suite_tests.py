#!/usr/bin/env python
"""Testing FoBiS.py"""
# import doctest
import os
import unittest
from fobis.config import __config__
from fobis.fobis import build
from fobis.fobis import clean
from fobis.fobos import Fobos


class SuiteTest(unittest.TestCase):
  """Testing suite for FoBiS.py."""

  @staticmethod
  def run_build(directory):
    """
    Method for running the build function into a selected directory.

    Parameters
    ----------
    directory : str
      relative path to tested directory
    """
    print("Testing " + directory)
    old_pwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/' + directory)
    __config__.reset()
    __config__.get_cli(['clean', '-f', 'fobos'])
    Fobos(filename=__config__.cliargs.fobos)
    clean()
    __config__.reset()
    __config__.get_cli(['build', '-f', 'fobos'])
    Fobos(filename=__config__.cliargs.fobos)
    try:
      build()
      build_ok = os.path.exists(directory)
    except:
      if directory == 'build-test6':
        with open('building-errors.log') as logerror:
          build_ok = 'Unclassifiable statement' in list(logerror)[-1]
        os.remove('building-errors.log')
    __config__.reset()
    __config__.get_cli(['rule', '-f', 'fobos', '-ex', 'finalize'])
    fobos = Fobos(filename=__config__.cliargs.fobos)
    fobos.rule_execute(rule=__config__.cliargs.execute)
    __config__.get_cli(['clean', '-f', 'fobos'])
    Fobos(filename=__config__.cliargs.fobos)
    clean()
    os.chdir(old_pwd)
    return build_ok

  @staticmethod
  def run_clean(directory):
    """
    Method for running the clean function into a selected directory.

    Parameters
    ----------
    directory : str
      relative path to tested directory
    """
    print("Testing " + directory)
    old_pwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/' + directory)
    __config__.reset()
    __config__.get_cli(['build', '-f', 'fobos'])
    Fobos(filename=__config__.cliargs.fobos)
    build()
    __config__.reset()
    __config__.get_cli(['clean', '-f', 'fobos'])
    Fobos(filename=__config__.cliargs.fobos)
    clean()
    clean_ok = not os.path.exists(directory)
    os.chdir(old_pwd)
    return clean_ok

  def test_buildings(self):
    """Testing buildings."""
    num_failures = 0
    failed = []

    for test in range(8):
      build_ok = self.run_build('build-test' + str(test + 1))
      if not build_ok:
        failed.append('build-test' + str(test + 1))
        num_failures += 1

    for test in range(1):
      clean_ok = self.run_clean('clean-test' + str(test + 1))
      if not clean_ok:
        failed.append('clean-test' + str(test + 1))
        num_failures += 1

    if len(failed) > 0:
      for fail in failed:
        print(fail)
    self.assertEquals(num_failures, 0)
    return


if __name__ == "__main__":
  unittest.main()
