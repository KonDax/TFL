import argparse
import urllib.request
import urllib.error
import re
from typing import AnyStr
from zipfile import ZipFile
from SimplePackage import Package
from mermaid import Mermaid


class CLI:
    def __init__(self):
        self.params = self.cmd_line()
        # self.print_args()
        self.graph_dependencies: dict[Package, list[Package]] = {}
        self.visited: set[Package] = set()

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
                            required=True,
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

    def get_dependencies(self, package: Package) -> list[Package]:
        if self.params['work_mode']:
            return package.get_dependencies_from_file(self.params["url"])
        else:
            if package.load_package_url(self.params["url"]) is not None:
                deps = package.get_dependencies_by_path()
                package.clear_memory()
                return deps
            return []
    def recursive_dfs(self, start_package: Package, max_depth_recursive: int = 5) -> list[Package] | None:
        if max_depth_recursive <= 0:
            return []
        for package in self.visited.copy():
            comp = Package.compare(start_package, package)
            if comp == "==" or comp == "<":
                return None
            if comp == ">":
                self.visited.remove(package)
                del self.graph_dependencies[package]
        # if start_package in self.visited:
        #     return None
        dependencies = self.get_dependencies(start_package)
        # print(start_package.name, dependencies, self.visited, self.stack)
        if not dependencies:
            return []
        self.visited.add(start_package)
        for obj in dependencies:
            deps = self.recursive_dfs(obj, max_depth_recursive-1)
            if deps is not None:
                self.graph_dependencies[start_package] = deps
        self.graph_dependencies[start_package] = dependencies
        return None

    def get_graph_dependencies(self):
        package = Package(self.params["package_name"], self.params["package_version"])
        self.recursive_dfs(package, self.params["max_depth"])
        for [key, value] in self.graph_dependencies.items():
            print(f"{key.name}: {[i.name for i in value]}")

    def generate_mermaid(self, graph_title="Граф зависимостей"):
        mermaid_lines = ["graph TD"]

        for source_node, dependent_nodes in self.graph_dependencies.items():
            for target_node in dependent_nodes:
                mermaid_lines.append(f"\t{source_node.name}.{source_node.version} --> {target_node.name}.{target_node.version}")
                # mermaid_lines.append(f"\t{source_node.name} --> {target_node.name}")

        return "\n".join(mermaid_lines)

    def visualize_dependencies(self, output_file="dependency_graph.png"):
        mermaid_code = self.generate_mermaid()
        print(mermaid_code)
        mm = Mermaid(mermaid_code)
        mm.to_png(output_file)
        print(f"Граф сохранен как: {output_file}")
        return mermaid_code

url1 = "https://www.nuget.org/api/v2/package/Newtonsoft.Json/13.0.4"
url2 = "https://www.nuget.org/api/v2/package/Microsoft.Extensions.DependencyInjection/10.0.0"
url3 = "https://www.nuget.org/api/v2/package/Microsoft.EntityFrameworkCore/10.0.0"
test1 = r"python .\main.py -p A -u Test.txt -wd True -pv 1.0.0"
test2 = r"python .\main.py -p Microsoft.Extensions.DependencyInjection -u https://www.nuget.org/api/v2/package -pv 10.0.0 -d 3"
test3 = r"python .\main.py -p Newtonsoft.Json -u https://www.nuget.org/api/v2/package -pv 13.0.4 -d 3"
if __name__ == "__main__":
    cli = CLI()
    cli.get_graph_dependencies()
    cli.visualize_dependencies()


