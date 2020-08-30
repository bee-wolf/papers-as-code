import setuptools

with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author='BeeWolf',
    author_email='mandygu925@gmail.com',
    name='text-preprocessor',
    license='MIT',
    description='text-preprocessor is a library for preprocessing textual data',
    version='v0.0.1',
    long_description=README,
    url='https://github.com/bee-wolf/text-preprocessor',
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=[],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)
