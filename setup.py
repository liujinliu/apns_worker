# -*- coding: utf-8 -*-
import sys
import os
import setuptools
from version import __VERSION__

def _setup():
    setuptools.setup(
        name='apns_worker',
        version=__VERSION__,
        description='apns worker',
        author='Gary',
        author_email='514371547@qq.com',
        url='',
        install_requires=['tornado==4.2','toamqp'],
        packages=['apns_worker', 'apns_worker.api',
                  'apns_worker.mq'],
        package_dir={'': 'src'},
        entry_points={
            'console_scripts': [
                'worker-apns-start=apns_worker.cmd:worker_start'
                ]
            },
        classifiers=[
            'Development Status :: 4 - Beta Development Status',
            'Environment :: Console',
            'Topic :: Utilities',
        ],
    )

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'publish':
            os.system('make publish')
            sys.exit()
        elif sys.argv[1] == 'release':
            if len(sys.argv) < 3:
                type_ = 'patch'
            else:
                type_ = sys.argv[2]
            assert type_ in ('major', 'minor', 'patch')

            os.system('bumpversion --current-version {} {}'
                      .format(__VERSION__, type_))
            sys.exit()

    _setup()


if __name__ == '__main__':
    main()
