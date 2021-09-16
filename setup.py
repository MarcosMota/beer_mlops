from setuptools import find_packages, setup

setup(
    name='beer_ml',
    description='Machine Learning Project ',
    author='Marcos Mota',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    version='0.0.4',
    license='MIT',
)