try:
    from setuptools import setup, find_packages
    from setuptools.command.install import install as _install
except ImportError:
    from distutils.core import setup


class Install(_install):
    def run(self):
        _install.do_egg_install(self)

setup(
    name='CORD19-NER',
    packages=["cord19_ner"],
    version='0.0.4',
    author='Raphaël GAZZOTTI',
    author_email='raphael.gazzotti@inria.fr',
    cmdclass={'install': Install},
    install_requires=['tqdm', 'requests', 'cord-19-tools'],
    setup_requires=[]
)