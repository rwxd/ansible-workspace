from setuptools import setup
from os import path
from subprocess import check_output

with open("./requirements.txt") as f:
    required = f.read().splitlines()

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = '1.0.0'

try:
    version = (
        check_output(['git', 'describe', '--tags']).strip().decode().replace('v', '')
    )
except:
    pass

setup(
    name='ansible_workspace',
    version=version,
    description='Create a workspace for multiple tools to easier develop ansible playbooks with roles.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='rwxd',
    author_email='rwxd@pm.me',
    url="https://github.com/rwxd/ansible_workspace",
    license='MIT',
    packages=['ansible_workspace'],
    install_requires=required,
    entry_points={
        "console_scripts": ["ansible-workspace = ansible_workspace.__main__:main"]
    },
    classifiers=[],
)
