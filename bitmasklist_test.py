#!/usr/bin/python3
# SPDX-License-Identifier: GPL-2.0-only
#
# Copyright (C) 2025 Red Hat, Inc.
# John Kacur <jkacur@redhat.com>

""" Module to test bitmasklist functionality """

import sys
from procfs import bitmasklist

class BitmasklistTest:
    """ class to run the bitmasklist test """
    # Assume true (passed) until proven false
    # Many tests can be run, but just one failure is recorded overall here
    unit_test_result = 0   # Assume true (passed) until proven false

    def __init__(self, line, nr_entries, expected_result):
        self.result = 0    # Assume pass
        self.line = line
        self.nr_entries = nr_entries    # Corresponds to the number of cpus
        self.expected_result = expected_result

    # A failure in any single test is recorded as an overall failure
    def set_unit_test_result(self):
        """ set unit_test_result to fail if any test fails """
        if BitmasklistTest.unit_test_result == 1:
            return
        if self.result == 1:
            BitmasklistTest.unit_test_result = 1
        return

    # This is the function that actually runs the test
    def bitmasklist_test(self):
        """ Run the test """
        print("\n##################\n")
        cpu = bitmasklist(self.line, self.nr_entries)
        print("Converted : ", self.line, "\nto ", cpu)
        if cpu == self.expected_result:
            self.result = 0
            print("PASS")
        else:
            self.result = 1
            print("expected : ", self.expected_result)
            print("FAIL")
        self.set_unit_test_result()

# CPU 2
t = \
    BitmasklistTest("00000000,00000000,00000000,00000000,00000000,00000004", 44, [2])
t.bitmasklist_test()

# CPU 34
t = \
    BitmasklistTest("00000000,00000000,00000000,00000000,00000004,00000000", 44, [34])
t.bitmasklist_test()

# CPU 30
t = \
    BitmasklistTest("00000000,00000000,00000000,00000000,00000000,40000000", 44, [30])
t.bitmasklist_test()

# CPU 0, 32
t = \
    BitmasklistTest("00000000,00000000,00000000,00000000,00000001,00000001", 44, [0, 32])
t.bitmasklist_test()

# cpu 0-15
t = \
    BitmasklistTest("ffff", 44, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
t.bitmasklist_test()

#cpu 0-71
t = \
    BitmasklistTest("ff,ffffffff,ffffffff", 96, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71])
t.bitmasklist_test()

sys.exit(BitmasklistTest.unit_test_result)
