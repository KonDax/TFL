import argparse
import urllib.request
import zipfile
from zipfile import ZipFile


class CLI:
    def __init__(self):
        # self.params = self.cmd_line()
        # self.print_args()
        package_path = self.load_package_url("Microsoft.Extensions.DependencyInjection", "10.0.0")
        self.load_packages(package_path)


    def cmd_line(self):
        params = {}
        parser = argparse.ArgumentParser(description="CLI")

        parser.add_argument('--package-name', '-p',
                            type=str,
                            required=True,
                            help="Name of package"
                            )

        parser.add_argument('--url', '-u',
                            type=str,
                            required=True,
                            help="Url of package"
                            )

        parser.add_argument('--work-mode', '-wd',
                            type=int,
                            default=1,
                            help="Working mode with the test repository"
                            )

        parser.add_argument('--package-version', '-pv',
                            type=str,
                            default="latest",
                            help="Package version"
                            )

        parser.add_argument('--max-depth', '-d',
                            type=int,
                            default=5,
                            help="Максимальная глубина анализа зависимостей."
                            )

        args = parser.parse_args()
        # print(args)

        params['package_name'] = args.package_name
        params['url'] = args.url
        params['work_mode'] = args.work_mode
        params['package_version'] = args.package_version
        params['max_depth'] = args.max_depth
        return params

    def print_args(self):
        print(f"package-name:\t{self.params['package_name']}")
        print(f"url:\t\t{self.params['url']}")
        print(f"work_mode:\t{self.params['work_mode']}")
        print(f"package_version:\t\t{self.params['package_version']}")
        print(f"max_depth:\t{self.params['max_depth']}")

    def load_package_url(self, package_name: str, version_name: str) -> str:
        packages_url = f"https://www.nuget.org/api/v2/package/{package_name}/{version_name}"
        print(f'load from {packages_url}')
        with urllib.request.urlopen(packages_url) as response:
            compressed_data = response.read()
        package_path = f'{package_name}.{version_name}.nupkg'
        with open(package_path, 'wb') as f:
            f.write(compressed_data)
        print(f"Сохранено в: {package_path}")
        return package_path

    def load_packages(self, package_path: str = ''):
        file = ZipFile(package_path)
        print(*file.namelist(), sep="\n")
        print()
        with file.open("Microsoft.Extensions.DependencyInjection.nuspec") as f:
            print(*f.readlines(), sep="\n")


cli = CLI()
url1 = "https://www.nuget.org/api/v2/package/Newtonsoft.Json/13.0.4"
url2 = "https://www.nuget.org/api/v2/package/System.Security.Cryptography.Pkcs/10.0.0"
url3 = "https://www.nuget.org/api/v2/package/Microsoft.EntityFrameworkCore/10.0.0"