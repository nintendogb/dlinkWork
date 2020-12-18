from setuptools import setup, find_packages

setup(
    name='pythonClient',
    version='3.0',
    description='This is python version of apiscan',
    author='Ted Kao',
    author_email='nintendogb@gmail.com',
    packages=find_packages(),
    install_requires=[
        "nose",
        "requests",
        "wget",
        "simplejson",
        "redis",
        "flask-restful",
        "flask-login",
        "tornado",
        "beautifulsoup4",
        "websockets",
        "magicfile",
        "pycryptodome",
        "PyJWT",
    ],
)
