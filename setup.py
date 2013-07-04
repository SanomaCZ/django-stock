from os import system
from os.path import dirname, join
from setuptools import setup
from distutils.core import Command
import stock

install_requires = [
    'Django>=1.5.1,<1.6',
    'South==0.7.6',
    'Pillow>=2.0',
    'sorl-thumbnail==11.12',
    'django-grappelli==2.4.5',
    'uwsgi==1.9.13',
    'raven==3.4.0',

]

tests_require = [
    'nose',
    'coverage',
]

setup_requires = []

with open('README.rst') as readmefile:
    long_description = readmefile.read()


class BumpVersion(Command):
    description = "Bump version automatically (by your CI tool)"
    user_options = [
        ('commit', None, 'Commit changed files to VCS (no push)'),
        ('tag', None, 'Create release tag in VCS (no push)'),
    ]
    boolean_options = ['commit', 'tag']

    def initialize_options(self):
        self.commit = False
        self.tag = False

    def finalize_options(self):
        pass

    def run(self):
        v = stock.__version__
        new_version = v[:-1] + (v[-1] + 1, )
        new_version_str = '.'.join(map(str, new_version))
        initfile = join(dirname(stock.__file__), '__init__.py')

        with open(initfile, 'r') as ifile:
            print "Reading old package init file..."
            istr = ifile.read()
            istr = istr.replace(str(v), str(new_version))

        with open(initfile, 'w') as ifile:
            print "Writing new init file with version %s..." % new_version_str
            ifile.write(istr)

        if self.commit:
            print "Committing version file to VCS..."
            system('git commit %s -m "Version bump %s"' % (initfile, new_version_str))

        if self.tag:
            print "Creating tag r/%s in VCS..." % new_version_str
            system('git tag r/%s' % new_version_str)


class MakeStatic(Command):
    description = "Compile LESS files into CSS, combine javascripts etc"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        params = {
            'pth': 'stock/project_static',
            'lessc_opts': '--yui-compress --verbose -O2',
            'xjs_opts': ''
        }
        system('lessc %(lessc_opts)s %(pth)s/less/master.less %(pth)s/css/master.css' % params)
        system('r.js %(xjs_opts)s -o %(pth)s/_dev/build.js' % params)


setup(
    name='stock',
    version=stock.__versionstr__,
    description='stock',
    long_description=long_description,
    author='Sanoma Online Dev',
    author_email='online-dev@sanomamedia.cz',
    license='Proprietal',
    #url='',

    packages=('stock',),
    include_package_data=True,

    cmdclass={
        'bump_version': BumpVersion,
        'make_static': MakeStatic
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: Proprietal",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires=install_requires,
    test_suite='nose.collector',
    tests_require=tests_require,
    setup_requires=setup_requires,
    entry_points={
        'console_scripts': [
            'stock-manage = stock.custom_manage:main',
        ],
    },
)
