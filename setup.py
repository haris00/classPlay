from setuptools import setup

setup(
    name='classPlay',
    packages=['classPlay'],
    author='Haris Tanvir',
    url='https://github.com/haris00/classPlay',
    description='Web app that allows students to answer professor questions in class',
    license='Not decided yet',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ]
)
