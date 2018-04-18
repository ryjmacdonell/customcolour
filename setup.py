"""
Setup script for the customcolour package
"""
from setuptools import setup
from setuptools import find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='customcolour',
    version='0.1',
    description=('A library of tools for transforming and creating' +
                 'custom matplotlib colormaps'),
    long_description=readme(),
    keywords='customcolour custom colormap matplotlib plotting',
    url='https://github.com/ryjmacdonell/customcolour',
    author='Ryan J. MacDonell',
    author_email='rmacd054@uottawa.ca',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Visualization'
                 ],
    install_requires=['numpy']
      )
