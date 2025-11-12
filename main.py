import argparse
import urllib.request
import urllib.error
import re
from typing import AnyStr
from zipfile import ZipFile
from  SimplePackage import Package


class CLI:
    def __init__(self):
        self.params = self.cmd_line()
        self.print_args()
        self.packages = []

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
                            type=bool,
                            default=False,
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

    def search_dependencies(self):
        self.packages.append(Package(self.params["package_name"], self.params['package_version']))
        for package in self.packages:
            if package.load_package_url(self.params["url"]) is not None:
                print(package.search_dependencies_by_path())
            package.clear_memory()


# print(re.search(r'.*?.nuspec', "wethweth\nereryjeryj\nwetrhwerthwreth.nuspec"))
url1 = "https://www.nuget.org/api/v2/package/Newtonsoft.Json/13.0.4"
url2 = "https://www.nuget.org/api/v2/package/Microsoft.Extensions.DependencyInjection/10.0.0"
url3 = "https://www.nuget.org/api/v2/package/Microsoft.EntityFrameworkCore/10.0.0"
if __name__ == "__main__":
    cli = CLI()
    cli.search_dependencies()

