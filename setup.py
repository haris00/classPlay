from setuptools import setup, find_packages

setup(
    name='classPlay',
    author='Haris Tanvir',
    url='https://github.com/haris00/classPlay',
    description='Web app that allows students to answer professor questions in class',
    license='Not decided yet',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask_wtf',
        'flask_bcrypt',
        'flask_login',
        'psycopg2',
        'Flask-And-Redis'
    ]
)
