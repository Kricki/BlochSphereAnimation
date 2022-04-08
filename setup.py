from setuptools import setup, find_packages


with open('README.md') as fp:
    long_description = fp.read()

CLASSIFIERS = """
Development Status :: 3 - Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
Programming Language :: Python :: 3.10
Topic :: Software Development
Topic :: Scientific/Engineering
"""

setup(
    name='BlochSphereAnimation',
    version='0.1.0',
    author='',
    author_email='kricki@posteo.de',
    url='',
    description='AAnimation of qubit states and gates on Bloch sphere.',
    long_description=long_description,
    packages=find_packages(),
    classifiers=[f for f in CLASSIFIERS.split('\n') if f],
    install_requires=['numpy', 'matplotlib', 'qutip', 'imageio'],
    zip_safe=False,
)
