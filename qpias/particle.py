#!/usr/bin/env python3

import numpy as np
from numpy import linalg
import scipy as sp
from scipy import linalg, integrate


class Particle():
    """Store all the information about the particle.

    :param nmax: Maximum size of the basis set, default 40
    :type nmax: int, optional

    :param length: Length of the box in which particle lives, default 1
    :type length: float, optional

    :param mass: Mass of the particle, default 1
    :type mass: float, optional

    :param potential: Potential surface for the particle, default None
        (particle-in-a-box)
    :type potential: numpy.ndarray, optional

    :param emax: The maximum energy eigenvectors to use to describe wave
        functions, default None
    :type emax: float

    :var numpy.ndarray x: Coordinates to use for wave function.

    :var numpy.ndarray basis: Basis functions in position space.
        See :py:func:`generate_basis_functions`.

    :var numpy.ndarray momenta: Basis functions in momentum space.
        See :py:func:`generate_basis_functions`.

    :var numpy.ndarray V: Potential energy matrix. See 

    :var float average_energy: The average energy of the particle.

    """

    def __init__(self, nmax=40, length=1, mass=1, potential=None, emax=None):
        """Initializes the :py:class:`Particle` class."""

        self.nmax = nmax
        self.length = length
        self.mass = mass
        self._emax = emax

        # if no potential given, set potential to zero
        if potential is not None:
            self.potential = potential
        else:
            self.potential = np.zeros((500))

        self.x = np.linspace(0, self.length, self.xpoints)

        # set some defaults
        self.basis = None
        self.momenta = None
        self.V = None
        self.H = None
        self.average_energy = None

    @property
    def xpoints(self):
        """Number of points along the potential surface."""
        return len(self.potential)

    def generate_basis_functions(self):
        r"""Creates a basis set based on the solutions to the
        one-dimensional particle-in-a-box without a potential.

        Stores results in :attr:`Particle.basis` and
        :attr:`Particle.momenta`.

        The basis set in position space is defined as

        .. math::

            \chi_n(x) = \sqrt{\frac{2}{L}} \sin\left( \frac{n\pi x}{L} \right)
            \:\:\: n=1,2,\cdots,n_\text{max}

        The basis set in momentum space is defined as

        .. math::

            \chi_n(k) = \frac{k\pi}{L}
            \:\:\: k=\pm 1,\pm 2,\cdots,\pm n_\text{max}

        """
        basis = np.zeros((self.nmax, len(self.x)))
        for i in range(self.nmax):
            basis[i] = ( np.sqrt(2/self.length)
                     * np.sin((i+1)*np.pi*self.x/self.length) )
        self.basis = basis
        
        # calculate momenta basis functions
        momenta = np.arange(-self.nmax,self.nmax+1) * np.pi / self.length
        momenta = np.delete(momenta, int(len(momenta)/2))
        self.momenta = momenta

    def generate_hamiltonian(self, potential=None):
        r"""Creates the hamiltonian matrix elements. Stores the information
        in :attr:`Particle.H`.

        :param potential: Potential to use, default None
        :type potential: numpy.ndarray, optional

        See also, :meth:`generate_potential_matrix`.

        .. math::

            \mathbf{H}_{mn} = \mathbf{T}_{mn} + \mathbf{V}_{mn}

        The kinetic energy matrix is calculated as:

        .. math::

            \mathbf{T}_{mn} = \begin{cases}\frac{n^2 \times \pi^2}
            {2 \times m \times L^2} & \text{if } n = m \\
            0 & \text{if } n \neq m\end{cases}

        """
        H = np.zeros((self.nmax, self.nmax))

        # Create kinetic energy matrix
        for i in range(self.nmax):
            n = i+1
            H[i,i] += n**2 * np.pi**2 / (2 * self.mass * self.length**2)

        # Create potential energy matrix
        self.generate_potential_matrix(potential)

        # add potential energy to hamiltonian
        H += self.V
        self.H = H

    def generate_potential_matrix(self, potential=None):
        r"""Creates the potential energy matrix elements. Stores the
        information in :attr:`Particle.V`.

        :param potential: Potential to use, default None
        :type potential: numpy.ndarray, optional

        .. math::

            \mathbf{V}_{nm} = \int_0^L \chi_n^*(x) V(x) \chi_m(x) dx

        """
        # set potential to zero if none given
        if potential is None: potential = self.potential
        if potential is None:
            potential = np.zeros((self.xpoints))
            self.potential = potential

        # calculate the potential energy matrix
        V = np.zeros((self.nmax, self.nmax))
        for i in range(self.nmax):
            ni = i+1 
            for j in range(i, self.nmax):
                nj = j+1
                V[i,j] = ((2/self.length) * sp.integrate.simps(np.sin(
                          ni*np.pi*self.x/self.length)
                       * np.sin(nj*np.pi*self.x/self.length) * potential, self.x)) 
                V[j,i] = V[i,j]
        self.V = V

    def calculate_wave_functions(self, H=None, potential=None):
        """Calculates the wave functions (eigenvectors) and energies (eigenvalues)
        by diagonalizing the hamiltonian.

        :param H: Hamiltonian matrix, default None
        :type H: numpy.ndarray, optional

        :param potential: Potential to use, default None
        :type potential: numpy.ndarray, optional

        Stores results in :attr:`Particle.wave_functions`, 
        :attr:`Particle.dpsi_dx`, :attr:`Particle.d2psi_dx2`,
        :attr:`Particle.energies`, and :attr:`Particle.average_energy`.

        """
        # can only specify one of the hamiltonian or potential
        if H is not None and potential is not None:
            raise Exception('Cannot specify both "H" and "potential"!')
        elif potential is not None:
            self.generate_hamiltonian(potential=potential)
            H = self.H
        elif H is None:
            if self.H is None: self.generate_hamiltonian(potential=potential)
            H = self.H

        # diagonalize the hamiltonian
        energies, coefficients = np.linalg.eigh(H)
        if self._emax is None: self._emax = energies[18]
        idx = np.where(energies > self._emax*1.2)
        try:
            self.nmax = idx[0][0]
        except IndexError:
            self.nmax = len(energies)
        self.energies = energies[:self.nmax]
        coefficients = coefficients[:self.nmax,:self.nmax]

        # normalize the coefficients
        for i in range(self.nmax):
            integral = (coefficients[:,i]*coefficients[:,i]).sum()
            coefficients[:,i] /= np.sqrt(integral)

        # generate the wave functions from the basis set
        if self.basis is None:
            self.generate_basis_functions()
        self.wave_functions = np.dot(coefficients.T, self.basis)

        # operator matrices
        self.get_operator_matrices(coefficients)

        # set the initial wave function as the lowest energy eigenfunction
        self.C = np.zeros((len(self.energies)), dtype=complex)
        self.C[0] = 1

        # calculate wave function property: d \psi / dx
        d1_basis = np.zeros((self.nmax, len(self.x)))
        for i in range(self.nmax):
            n = i + 1
            d1_basis[i] = ( (n * np.pi / self.length)
                    * np.sqrt(2/self.length)
                    * np.cos( n * np.pi * self.x / self.length) )
        self.dpsi_dx = np.dot(coefficients.T, d1_basis)

        # calculate the wave function property: d^2 \psi / dx^2
        d2_basis = np.zeros((self.nmax, len(self.x)))
        for i in range(self.nmax):
            n = i + 1
            d2_basis[i] = ( (-1 * n**2 * np.pi**2 / self.length**2)
                    * np.sqrt(2/self.length)
                    * np.sin( n * np.pi * self.x / self.length) )
        self.d2psi_dx2 = np.dot(coefficients.T, d2_basis)

        # calculate and set the particle (average) energy
        self.average_energy = self.energies[0]

    def get_operator_matrices(self, C):
        r"""Calculates the operator matrices :math:`<\hat{x}>`,
        :math:`<\hat{x}^2>`, :math:`<\hat{p}>`, and :math:`<\hat{p}^2>`
        to get average and uncertainties in the position and
        momentum of our particle.
        """

        # first, generate the <x> matrix in the basis set
        xmat_basis = np.zeros((self.nmax, self.nmax))
        for i in range(self.nmax):
            n = i + 1
            for j in range(i, self.nmax):
                m = j + 1
                if n == m:
                    xmat_basis[i,i] = self.length / 2
                else:
                    if ((m-n)%2==1):
                        xmat_basis[i,j] -= ( (2 * self.length / np.pi**2)
                                           / ((m-n)**2) )
                    if ((m+n)%2==1):
                        xmat_basis[i,j] += ( (2 * self.length / np.pi**2)
                                           / ((m+n)**2) )
                    xmat_basis[j,i] = xmat_basis[i,j]

        # now generate the <x> matrix in the energy eigenfunction basis
        self._xmat = np.dot(C.T, np.dot(xmat_basis, C))

        # create <x^2> matrix
        x2mat_basis = np.zeros((self.nmax, self.nmax))
        for i in range(self.nmax):
            n = i + 1
            for j in range(i, self.nmax):
                m = j + 1
                if n == m:
                    x2mat_basis[i,i] = ( self.length**2 * ((2 * np.pi**2 * n**2)
                        - 3 ) / (6 * np.pi**2 * n**2) )
                else:
                    x2mat_basis[i,j] += ( self.length**2 * ( 2 * np.pi * (m-n)
                        * np.cos((m-n) * np.pi) ) / (np.pi**3 * (m-n)**3) )
                    x2mat_basis[i,j] -= ( self.length**2 * ( 2 * np.pi * (m+n)
                        * np.cos((m+n) * np.pi) ) / (np.pi**3 * (m+n)**3) )
                x2mat_basis[j,i] = x2mat_basis[i,j]
        self._x2mat = np.dot(C.T, np.dot(x2mat_basis, C))

        # create the <p> matrix
        pmat_basis = np.zeros((self.nmax, self.nmax), dtype=complex)
        for i in range(self.nmax):
            n = i + 1
            for j in range(i+1, self.nmax):
                m = j + 1
                if (m+n)%2 == 1:
                    pmat_basis[i,j] = 4j * m * n / (self.length
                        * (m**2 - n**2))
                    pmat_basis[j,i] = -pmat_basis[i,j]
        self._pmat = np.dot(C.T, np.dot(pmat_basis, C))

        # create the <p^2> matrix
        p2mat_basis = np.zeros((self.nmax, self.nmax), dtype=complex)
        for i in range(self.nmax):
            n = i + 1
            p2mat_basis[i,i] = n**2 * np.pi**2 / self.length**2
        self._p2mat = np.dot(C.T, np.dot(p2mat_basis, C))


    def get_wave_function(self, C=None, time=None):
        """Returns the wave function in position basis for a given
        set of coefficients and at a given time.

        :param numpy.ndarray C: Coefficients of the wave function in
            eigenfunctions basis. Default `None`.

        :param float time: Time parameter. Default `None`.

        :return: The wave function in position basis.
        :type: numpy.ndarray

        """

        if C is None: C = self.C
        if time is None: time = self.time
        time_function = np.exp(-1j * self.energies * time)
        self.Ct = C * time_function
        psi = np.einsum('i,ij->j', self.Ct, self.wave_functions)
        return psi


    def position_momentum_collapse(self, psi, x0=None, k0=None, momentum=False):
        r"""Collapse the wave function to a particle with a position/momentum
        with minimum uncertainty: :math:`\Delta_x \times \Delta_p = 1/2`
        For a position collapse: :math:`\Delta_x = L / 200`
        For a momentum collapse: :math:`\Delta_p = 5 / L`

        :returns: Tuple of the new wave function coefficients, the 
            collapsed position :math:`x_0` and the collaposed momentum
            :math:`p_0`.
        """

        # gaussian with for position wave function 
        if momentum:
            a = self.length / 10
        else:
            a = self.length / 200
 
        # if collapse location is not given, calculate it 
        if x0 is None:
 
            # get position probabilities 
            probabilities = (psi*psi.conjugate()).real
            total_probabilities = probabilities.sum()
            probabilities /= total_probabilities

            # find new collapse position
            x0 = self.x[np.random.choice(self.xpoints, p=probabilities)]

        # find the collapsed momentum (even for a collapsed position)
        # transform wave function from position to momentum basis
        if k0 is None:
            momenta = self.momenta
            psi_p = np.zeros((len(momenta)), dtype=complex)
            for ip in range(len(momenta)):
                psi_p[ip] = ( 1/np.sqrt(2*np.pi)
                    * sp.integrate.simps(psi * np.exp(1j * momenta[ip] * self.x),
                    self.x) )

            # normalize momentum distribution
            prob = (psi_p*psi_p.conjugate()).real
            total_prob = prob.sum()
            prob /= total_prob

            # collapse to a single momentum
            p_ix = np.random.choice(len(momenta), p=prob)
            k0 = momenta[p_ix]

        # find gaussian wave function
        y0 = ( np.sqrt(np.sqrt(1/(2*np.pi*a**2)))
            * np.exp(-0.25 * (self.x-x0)**2 / a**2)
            * np.exp(1j * k0 * self.x) )

        # find superposition of position wave function
        solution = sp.linalg.lstsq(self.wave_functions.T, y0) 
        C_new = solution[0]

        # normalize the coefficients
        temp = (C_new.conjugate() * C_new).real.sum()
        C_new /= np.sqrt(temp)

        return C_new, x0, k0

    def energy_collapse(self, n_change=0):
        """Collapses the wave function into one of the energy
        eigenfunctions based on its coefficients.

        :returns: Tuple of the new coefficient matrix and the energy
            of the collapsed wave function.

        """
    
        probabilities = (self.C*self.C.conjugate()).real
        n = np.random.choice(len(self.energies), p=probabilities) + n_change
        if n < 0: n = 0
        if n > self.nmax - 1: n = self.nmax - 1
        e0 = self.energies[n]
        C_new = np.zeros((len(self.energies)), dtype=complex)
        C_new[n] = 1.0

        return C_new, e0

