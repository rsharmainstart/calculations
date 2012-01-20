from calculations.numeric import lcm, filterDivisors, firstDivisor, Integer
from calculations.partition import Partitions

__author__ = 'Daniel Lytkin'

class Field:
    """Finite field.
    Can be called as Field(order) or Field(base, pow) where base^pow is the order of the field.
    'order' must be a prime power, otherwise the wrong field will be created.

    """
    def __init__(self, *arg):
        if len(arg)==1:
            if arg[0] <= 1:
                raise ValueError("Field order must be at least 2")
            self._base = firstDivisor(arg[0])
            self._pow = 1
            self._order = self._base
            while self._order < arg[0]:
                self._pow += 1
                self._order *= self._base
        elif len(arg)==2:
            self._base, self._pow = arg[0], arg[1]
            if self._pow < 1 or self._base < 2:
                raise ValueError("Field order must be at least 2")
            self._order = self._base ** self._pow

    def order(self):
        return self._order
    def char(self):
        return self._base
    def pow(self):
        return self._pow

class Group:
    """Interface for finite groups with method to calculate their spectra
    """
    def spectrum(self):
        raise NotImplementedError()

    def order(self):
        raise NotImplementedError()

class SporadicGroup(Group):
    _groups = {
        "M11" : (( 5, 6, 8, 11 ), Integer((2, 4), (3,2), 5, 11)),
        "M12" : (( 6, 8, 10, 11 ), Integer((2, 6), (3, 3), 5, 11)),
        "M22" : (( 5, 6, 7, 8, 11 ), Integer((2, 7), (3, 2), 5, 7, 11)),
        "M23" : (( 6, 8, 11, 14, 15, 23 ), Integer((2, 7), (3, 2), 5, 7, 11, 23)),
        "M24" : (( 8, 10, 11, 12, 14, 15, 21, 23 ), Integer((2, 10), (3, 3), 5, 7, 11, 23)),
        "J1" : (( 6, 7, 10, 11, 15, 19 ), Integer((2, 3), 3, 5, 7, 11, 19)),
        "J2" : (( 7, 8, 10, 12, 15 ), Integer((2, 7), (3, 3), (5, 2), 7)),
        "J3" : (( 8, 9, 10, 12, 15, 17, 19 ), Integer((2, 7), (3, 5), 5, 17, 19)),
        "J4" : (( 16, 23, 24, 28, 29, 30, 31, 35, 37, 40, 42, 43, 44, 66 ),
                Integer((2, 21), (3, 3), 5, 7, (11, 3), 23, 29, 31, 37, 43)),
        "Co1" : (( 16, 22, 23, 24, 26, 28, 33, 35, 36, 39, 40, 42, 60 ),
                 Integer((2, 21), (3, 9), (5, 4), (7, 2), 11, 13, 23)),
        "Co2" : (( 11, 16, 18, 20, 23, 24, 28, 30 ), Integer((2, 18), (3, 6), (5, 3), 7, 11, 23)),
        "Co3" : (( 14, 18, 20, 21, 22, 23, 24, 30 ), Integer((2, 10), (3, 7), (5, 3), 7, 11, 23)),
        "Fi22" : (( 13, 14, 16, 18, 20, 21, 22, 24, 30 ), Integer((2, 17), (3, 9), (5, 2), 7, 11, 13)),
        "Fi23" : (( 16, 17, 22, 23, 24, 26, 27, 28, 35, 36, 39, 42, 60 ),
                  Integer((2, 18), (3, 13), (5, 2), 7, 11, 13, 17, 23)),
        "Fi24'" : (( 16, 17, 22, 23, 24, 26, 27, 28, 29, 33, 35, 36, 39, 42, 45, 60 ),
                   Integer((2, 21), (3, 16), (5, 2), (7, 3), 11, 13, 17, 23, 29)),
        "HS" : (( 7, 8, 11, 12, 15, 20 ), Integer((2, 9), (3, 2), (5, 3), 7, 11)),
        "McL" : (( 8, 9, 11, 12, 14, 30 ), Integer((2, 7), (3, 6), (5, 3), 7, 11)),
        "He" : (( 8, 10, 12, 15, 17, 21, 28 ), Integer((2, 10), (3, 3), (5, 2), (7, 3), 17)),
        "Ru" : (( 14, 15, 16, 20, 24, 26, 29 ), Integer((2, 14), (3, 3), (5, 3), 7, 13, 29)),
        "Suz" : (( 11, 13, 14, 15, 18, 20, 21, 24 ), Integer((2, 13), (3, 7), (5, 2), 7, 11, 13)),
        "O'N" : (( 11, 12, 15, 16, 19, 20, 28, 31 ), Integer((2, 9), (3, 4), 5, (7, 3), 11, 19, 31)),
        "HN" : (( 9, 12, 14, 19, 21, 22, 25, 30, 35, 40 ), Integer((2, 14), (3, 6), (5, 6), 7, 11, 19)),
        "Ly" : (( 18, 22, 24, 25, 28, 30, 31, 33, 37, 40, 42, 67 ),
                Integer((2, 8), (3, 7), (5, 6), 7, 11, 31, 37, 67)),
        "Th" : (( 19, 20, 21, 24, 27, 28, 30, 31, 36, 39 ),
                Integer((2, 15), (3, 10), (5, 3), (7, 2), 13, 19, 31)),
        "B" : (( 25, 27, 31, 32, 34, 36, 38, 39, 40, 42, 44, 46, 47, 48, 52, 55, 56, 60, 66, 70 ),
               Integer((2, 41), (3, 13), (5, 6), (7, 2), 11, 13, 17, 19, 23, 31, 47)),
        "M" : (( 32, 36, 38, 40, 41, 45, 48, 50, 51, 54, 56, 57, 59, 60, 62, 66, 68, 69, 70, 71, 78, 84,
                87, 88, 92, 93, 94, 95, 104, 105, 110, 119 ), Integer((2, 46), (3, 20), (5, 9), (7, 6),
            (11, 2), (13, 3), 17, 19, 23, 29, 31, 41, 47, 59, 71)),
        "2F4(2)'" : (( 10, 12, 13, 16 ), Integer((2, 11), (3, 3), (5, 2), 13))
    }

    def __init__(self, name):
        self._name = name

    def spectrum(self):
        return SporadicGroup._groups.get(self._name)[0]

    def order(self):
        return SporadicGroup._groups.get(self._name)[1]

    def __str__(self):
        return self._name

    @staticmethod
    def getAllGroups():
        return SporadicGroup._groups.keys()

class AlternatingGroup(Group):
    def __init__(self, degree):
        self._degree = degree
        self._spectrum = None
        self._order = None

    def spectrum(self):
        if self._spectrum is None:
            n = self._degree
            partitions = filter(lambda x: (len(x)+n) % 2 == 0, Partitions(n))
            self._spectrum = [reduce(lcm, partition) for partition in partitions]
            self._spectrum.sort(reverse=True)
            self._spectrum = filterDivisors(self._spectrum, reverse=True)
        return self._spectrum

    def order(self):
        if self._order is None:
            self._order = reduce(lambda x, y: x*y, xrange(3, self._degree+1))
        return self._order

    def __str__(self):
        return "Alt({})".format(self._degree)

class ClassicalGroup(Group):
    def __init__(self, name, dimension, *field):
        pass
