"""
Created: 1/14/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
import os
from setuptools import find_packages, setup

'''
The "here" and "about" and classifiers are directly borrowed from 
Kenneth Reitz I'm always browsing around his GitHub to see how he's 
doing things. https://github.com/kennethreitz/
'''
here = os.path.abspath(os.path.dirname(__file__))

about = {}

with open(os.path.join(here, "budgeting", "__version__.py")) as f:
    exec(f.read(), about)

setup(
    name="budgeting",
    version=about["__version__"],
    description=("I'm not happy with the budgeting tools available and "
                 "also somewhat leery of sending personal info to apps "
                 "like Personal Capital or Mint. I'd like to create a "
                 "stand alone web app to run locally on my computer. "
                 "I'd like to explore GraphQL, Flask and better "
                 "testing of my code. "),
    author=about["__author__"],
    author_email=about["__email__"],
    url="https://github.com/EmilianoJordan/BudgetingInPython",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.6",
    setup_requires=[],
    include_package_data=True,
    license="Apache 2.0",
    classifiers=[
        "License :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=[
        'flask==1.*',
        'flask-sqlalchemy==2.*',
        'psycopg2==2.*',
        'flask-migrate==2.*',
        'flask_sslify',
        'flask_login',
        # 'click'
        'flask-restful',
        'passlib==1.*',
        'flask_httpauth==3.*'
    ],
    extras_require={
        'testing': [
            'requests==2.*',
            'pytest==4.*'
        ]
    }
)
