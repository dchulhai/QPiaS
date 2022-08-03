*****
QPiaS
*****

Quantum Particle-in-a-Sandbox

Author
======
Dhabih V. Chulhai (chulhaid@uindy.edu)

If you use this code with your students and / or have any feedback, please feel free to reach out to me. I'd love to hear how it's being used.

Citation
========
Use the following to cite this code:

- Chulhai, D. V. QPiaS: Quantum Particle-in-a-Sandbox. https://github.com/dchulhai/QPiaS, 2021.

Installing and Running QPiaS
============================

Windows Users
-------------

The following instructions assume some comfort with using Windows and Windows PowerShell.

1. Install Python3 from the Microsoft Store.
    
2. Use the Package Installer for Python (pip) to install necessary Python packages. Open Windows PowerShell and type:

    ``pip3 install numpy scipy pygame matplotlib``

If you run into errors, make sure that you're using the most up-to-date version of pip by typing:

    ``pip3 install --upgrade pip``
    
3. Download QPiaS (https://github.com/dchulhai/QPiaS) and extract into a known folder / location.

4. Ensure the location of QPiaS is included in your system's `PYTHONPATH`. Search for ``Edit the system environment variables'', which opens a ``System Properties'' panel. Go to ``Advanced'' tab and click on ``Environment Variables''. Under ``System Variables'' edit (or create, if it does not exist) a variable called `PYTHONPATH` and include the location of QPiaS in the ``Variable value''.
    
5. Run qpias by typing into PowerShell (you may need to close and reopen PowerShell after the previous step):

    ``python3 -m qpias``
    
QPiaS may also be launched from a Python interface (such as IPython) by typing:

>>> import qpias
>> qpias.Start_Game()

MacOS Users
-----------

The following instructions assume that you are familiar with using the terminal on MacOS.

1. Up-to-date MacOS comes with Python3 and its Package Installer for Python (pip) already installed, however, you may need to install the ``Developer Tools'' to use it. Open up a Terminal window and check if Python3 is ready to use by typing:

    ``python3 --version``

You may be prompted at this time to install Developer Tools if it is not already installed.

2. Install the necessary python packages using pip, for example with

    ``pip3 install numpy scipy pygame matplotlib``

If you run into errors, make sure that you're using the most up-to-date version of pip by typing:

    ``pip3 install --upgrade pip``
    
3. Download QPiaS (https://github.com/dchulhai/QPiaS) and extract into a known location.

4. Ensure that the QPiaS main directory is included in your ``PYTHONPATH`` system variable. For instance, if the main QPiaS directory is located at ``/Users/Name/Desktop/QPiaS`` directory, open up your ```/.bash\_profile`` file (or create one if it doesn't exist), for example with ``vi ~/.bash_profile`` and include the following line:

    ``export PYTHONPATH=$PYTHONPATH:/Users/Name/Desktop/QPiaS``
    
5. Run QPiaS from the terminal by typing:

    ``python3 -m qpias``
    
QPiaS may also be launched from a Python interface (such as IPython) by typing:

>>> import qpias
>>> qpias.Start_Game()

Linux/Unix Users
----------------

The following instructions assume that you are familiar with using the terminal and installing packages on Linux/Unix systems.

1. Ensure that Python3 and its Package Installer for Python (pip) are installed. For Debian, Ubuntu, Mint, and other Debian-based distributions, use:

    ``sudo apt install python3 python3-pip``

for Red Hat, Fedora, CentOS, and similar distributions, use:

    ``sudo dnf install python3 python3-pip``

2. Install the necessary python packages using pip, for example with

    ``pip3 install numpy scipy pygame matplotlib``

If you run into errors, make sure that you're using the most up-to-date version of pip by typing:

    ``pip3 install --upgrade pip``
    
3. Download QPiaS and extract into a known location, either from GitHub
(https://github.com/dchulhai/QPiaS) or using git

    ``git clone https://github.com/dchulhai/QPiaS.git``

4. Ensure that the QPiaS main directory is included in your \texttt{PYTHONPATH} system variable by including a line similar to the one below in your ``.bashrc`` file

    ``export PYTHONPATH=$PYTHONPATH:/location/to/QPiaS``
    
5. Run QPiaS from the terminal by typing:

    ``python3 -m qpias``
    
QPiaS may also be launched from a Python interface (such as IPython) by typing:

>>> import qpias
>>> qpias.Start_Game()

Copyright
=========

    Quantum Particle-in-a-Sandbox simulates the time-dependent quantum
    mechanical wave function for any arbitrary potential.
    Copyright (C) 2021 Dhabih V. Chulhai

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    | You may contact me using the email: chulhaid@uindy.edu
    | Or the address:
    | Department of Chemistry,
    | University of Indianapolis
    | 1400 E Hanna Ave,
    | Indianapolis, IN 46227

