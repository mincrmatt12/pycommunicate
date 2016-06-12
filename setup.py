from setuptools import setup, find_packages


def get_markdown():
    with open('README.md') as f:
        return f.read()


requires = '''click
eventlet
Flask
Flask-SocketIO
itsdangerous
Jinja2
MarkupSafe
python-engineio
python-socketio
six
Werkzeug
wheel'''.splitlines()


setup(
    name='pycommunicate',
    version='0.0.7',
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
