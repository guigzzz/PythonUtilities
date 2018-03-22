import subprocess
import platform
import os
from urllib.parse import urljoin
from argparse import ArgumentParser

# detect correct line-break character
if platform.system() == 'Windows': linebreak = '\r\n'
else:
    if platform.system() not in ['Linux', 'Darwin']:
        print(repr('> WARNING: unknown platform type, defaulting line-break to \n'))
    linebreak = '\n'

# requests and xml libraries are optional
# they allow the code to provide more info on the packages
CONFIG = {}
CONFIG['package_info'] = True
try:
    from requests import get
    from lxml import html
except ImportError:
    CONFIG['package_info'] = False
    

class Package:
    def __init__(self, string):
        space_split = string.split(' ')

        self.package_name = space_split[0]
        self.installed_version = space_split[1].replace('(', '').replace(')', '')
        self.new_version = space_split[4]
        self.install_type = space_split[5]

        if CONFIG['package_info']:
            self.package_info = self.getPackageInfo()

    def __repr__(self):
        main = '{}: {} -> {} {}'.format(
            self.package_name, self.installed_version,
            self.new_version, self.install_type
            )
        if CONFIG['package_info']:
            main += ' [{}]'.format(self.package_info)

        return main

    def getPackageInfo(self):
        """
        Fetch short package description from pypi
        """
        pypi_url = urljoin('https://pypi.python.org/pypi/', self.package_name + '/' + self.new_version)
        with get(pypi_url) as r:
            t = r.text.encode('utf-8')

        return html.fromstring(t).xpath('//body/div/div/div/div/p/text()')[0]

class PackageUpdater:
    def __init__(self, log_output = False, log_path = None):
        self.packages = self.__getOutdatedPackages()
        self.log_output = log_output
        self.log_path = log_path

    def __getOutdatedPackages(self):
        """
        Get a list of outdated pip packages
        """
        command_res = subprocess.run(
            ['pip', 'list', '--outdated', '--format=legacy'], 
            stdout = subprocess.PIPE
            ).stdout.decode('utf-8')

        splits = command_res.split(linebreak)
        if(splits[-1] == ''): splits = splits[:-1]

        return [Package(p_str) for p_str in splits]

    def showOutdatedPackages(self):
        """
        Print parsed list of outdated packages
        """
        for i, p in enumerate(self.packages):
            print('{} - {}'.format(i, p))

    def __updatePackage(self, pckg):
        """
        Given a package object, upgrade it to the newest version
        Also check if logs needs to be saved
        """
        command_res = subprocess.run(
            ['pip', 'install', '--upgrade', pckg.package_name], 
            stdout = subprocess.PIPE
            ).stdout.decode('utf-8')
        print('> Updating: {}'.format(pckg.package_name))

        if(self.log_output):
            if self.log_path is None: self.log_path = 'pipupdatelogs'

            if not os.path.exists(self.log_path): os.mkdir(self.log_path)

            with open(os.path.join(self.log_path, pckg.package_name), 'w') as f:
                f.write(command_res)

    def updatePackages(self, selected = None):
        """
        Update all or certain packages
        """
        if selected is None:
            selected = self.packages
        else:
            selected = [self.packages[i] for i in selected]

        if selected == []:
            print('> No packages to update.')
            return

        print('> UPDATE PLAN')
        for i, p in enumerate(selected): print('{} - {}'.format(i, p))
        print()

        inp = input('> Good to go? [Y/n]')
        if(inp in 'Yy' or inp == None):
            for p in selected:
                self.__updatePackage(p)
        else:
            print('> Operation Cancelled')

        
if __name__ == '__main__':
    
    parser = ArgumentParser()
    parser.add_argument('-s', '--show', help="display outdated packages", action="store_true")
    parser.add_argument('-a', '--all', help="force update all packages", action="store_true")
    parser.add_argument('-i', '--install', nargs="+", type=int, help="install only selected packages using indices", )
    parser.add_argument('-l', '--log', help="whether to log the output of the pip commands", action="store_true")

    args = parser.parse_args()

    pu = PackageUpdater(log_output=args.log)
    if args.show:
        pu.showOutdatedPackages()
    if args.all:
        pu.updatePackages()
    if args.install:
        pu.updatePackages(selected=args.install)

