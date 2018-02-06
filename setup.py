from distutils.core import setup

setup(name='instruction_graph',
      version='0.1.1',
      author='Aaron Roth and others',
      # TODO update these
      url='about:blank',
      description="An implementation of instruction graph.",
      long_description="This package provide the Instruction Graph framework."
                       "Use it to control robots or other agents. See documentation on the github.",
      # py_modules=['instruction_graph',
      #            'instruction_graph.core',
      #            'instruction_graph.example'],
      provides='instruction_graph',
      # scripts=['TextCommunicator.py'],
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

