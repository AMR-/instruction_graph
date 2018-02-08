# from distutils.core import setup
from setuptools import setup

setup(name='instruction_graph',
      version='0.1.7',
      author='Aaron Roth and others',
      author_email='coralpeppercmu@gmail.com',
      # TODO update these - urls and descriptions
      url='https://www.cmu.edu',
      description="An implementation of instruction graph.",
      long_description='''
      Instruction Graph
      =================
      
      This package provides the Instruction Graph framework.
      
      Use it to control robots or other agents.
      
      See documentation on the github_ .

      .. _github: https://www.cmu.edu
      ''',
      packages=['instruction_graph',
                'instruction_graph.components',
                'instruction_graph.core',
                'instruction_graph.example'],
      # py_modules=['instruction_graph',
      #            'instruction_graph.core',
      #            'instruction_graph.example'],
      # requires=['klepto'],
      install_requires=['klepto'],
      # provides='instruction_graph',
      # scripts=['TextCommunicator.py'],
      scripts=['run_tests.py'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Other Environment',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'Topic :: Home Automation',
          'Topic :: Other/Nonlisted Topic',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Scientific/Engineering :: Artificial Life',
          'Topic :: Scientific/Engineering :: Human Machine Interfaces',
          # Topic :: Scientific/Engineering :: Visualization
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      license='MIT'
      )

# TODO - when develop scripts look at
#   https://setuptools.readthedocs.io/en/latest/setuptools.html#automatic-script-creation

