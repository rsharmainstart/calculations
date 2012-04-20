"""
Copyright 2012 Daniel Lytkin.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""
import itertools
from spectrum.calculations import numeric
from spectrum.calculations.numeric import Integer
from spectrum.graph.graph import Graph

__author__ = 'Daniel Lytkin'

class PrimeGraph(Graph):
    def __init__(self, spectrum):
        Graph.__init__(self)
        for elem in spectrum:
            factors = Integer(elem).factorize().keys()
            self.add_vertices(factors)
            self.add_edges(itertools.combinations(factors, 2))


class FastGraph(Graph):
    def __init__(self, spectrum):
        Graph.__init__(self)
        for elem in spectrum:
            self._add_element(elem)

    def _add_element(self, a):
        """Add new spectrum element
        """
        # these are the indices of future neighbors of a
        neighbors = []
        # memorize initial length so that we don't have to process newly added
        # vertices
        l = len(self._vertices)
        for i in range(l):
            b = self._vertices[i]
            d = numeric.gcd(a, b)
            if d == 1: continue
            bd = numeric.prime_part(b, d)
            if bd == 1:
                self._vertices[i] = d
                for neighbor in neighbors:
                    self._set_adjacency(i, neighbor, True)
                neighbors.append(i)
            else:
                self._vertices[i] = bd
                dIndex = self.clone_vertex(i, d)
                for neighbor in neighbors:
                    self._adjacency[dIndex][neighbor] = True
                neighbors.append(dIndex)

            a = numeric.prime_part(a, d)
            if a == 1: break
        if a > 1:
            index = self._add_vertex(a)
            for neighbor in neighbors:
                self._set_adjacency(index, neighbor, True)

