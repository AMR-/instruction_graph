# coding=utf-8
# from distutils.core import setup
from setuptools import setup

setup(name='instruction_graph',
      version='0.2.4',
      author='Aaron Roth, Çetin Meriçli, and Steven D. Klee',
      author_email='coralpeppercmu@gmail.com',
      url='https://github.com/AMR-/instruction_graph',
      description="An implementation of Transferable Augmented Instruction Graph",
      long_description='''
      Instruction Graph
      =================
      
      This package provides the Transferable Augmented Instruction Graph framework.
      
      Use it to create and execute task plans for robots or other agents.  Task plans created using
      this library can be run on any robot that uses this library. In this manner, task plans become very transferable.
      Differences between physical and software differences in robots can be accounted for.
      
      See documentation on the github_ .

      .. _github: https://github.com/AMR-/instruction_graph
      ''',
      packages=['instruction_graph',
                'instruction_graph.components',
                'instruction_graph.core',
                'instruction_graph.example'],
      # py_modules=['instruction_graph',
      #            'instruction_graph.core',
      #            'instruction_graph.example'],
      # requires=['klepto'],
      install_requires=['klepto', 'enum34'],
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

