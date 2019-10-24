from setuptools import setup, find_packages

setup(
    name='pirc',
    packages=find_packages(),
    install_requires=['numpy', 'scikit-learn', 'adafruit-adxl345', 'adafruit-ads1x15', 'Pillow', 'configparser'],
    entry_points={'console_scripts' : ['pirc=pirc:pirc']},
    py_modules=['pirc','libpirc'],
    version='20191024b',
    description='Self-driving RC car',
    long_description= """ Self-driving RC car """,
    author='Nicola Ferralis',
    author_email='ferralis@mit.edu',
    url='https://github.com/feranick/Pi-bot',
    download_url='https://github.com/feranick/Pi-bot',
    keywords=['Machine learning', 'physics', 'RC-cars'],
    license='GPLv2',
    platforms='any',
    classifiers=[
     'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
     'Development Status :: 5 - Production/Stable',
     'Programming Language :: Python',
     'Programming Language :: Python :: 3',
     'Programming Language :: Python :: 3.6',
     'Programming Language :: Python :: 3.7',
     'Intended Audience :: Science/Research',
     'Topic :: Scientific/Engineering :: Physics',
     ],
)
