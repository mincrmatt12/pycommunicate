from setuptools import setup, find_packages


def get_markdown():
    with open('README.md') as f:
        return f.read()


requires = '''click
eventlet
flask
Flask-SocketIO
itsdangerous
Jinja2
MarkupSafe
python-engineio
python-socketio
six
Werkzeug
wheel'''.splitlines()

with open('build.version', 'r') as build_version:
    dat = build_version.read().strip("\n").split(" ")

v = ""

if dat[3] == "master" or dat[2] == "<v>":
    v = dat[1]
else:
    v = dat[1] + "+" + dat[2]

setup(
    name='pycommunicate',
    version=v,
    description='A web library focusing on handling JS events server-side',
    long_description=get_markdown(),
    url='https://github.com/mincrmatt12/pycommunicate',
    author='mincrmatt12',
    author_email='nope@nope.com',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=requires,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers'
    ],
    include_package_data=True
)
