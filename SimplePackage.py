import urllib.request
from zipfile import ZipFile
import re
import os

class Package:
    def __init__(self, name: str, version: str , path: str = ""):
        self.name: str = name
        self.version: str = version
        self.path: str = path
        self.dependencies: list[Package] = []
    def load_package_url(self, url: str) -> str | None:
        package_url = url + "/" + self.name + "/" + self.version
        print(f'load from {package_url}')
        try:
            with urllib.request.urlopen(package_url) as response:
                compressed_data = response.read()
            path = f'{self.name}.{self.version}.nupkg'
            with open(path, 'wb') as f:
                f.write(compressed_data)
            print(f"Сохранено в: {path}")
            self.path = path
            return path
        except Exception as e:
            print(f"Error: {e}")

    def get_dependencies_by_path(self) -> list:
        file_zip = ZipFile(self.path)
        # print(*file_zip.namelist(), sep="\n")
        # print()
        file_conf = ""
        for fileName in file_zip.namelist():
            if fileName.endswith(".nuspec"):
                file_conf = fileName
                break
        with file_zip.open(file_conf) as f:
            file_str = f.read().decode("utf-8")
            # print(file_str)
        dependencies_raw = re.findall(r"<dependency .*>", file_str)
        # print(*dependencies_raw, sep="\n")
        for dependence in dependencies_raw:
            package1 = Package(re.search(r'id=".*?"', dependence).group()[4:-1],
                                 re.search(r'version=".*?"', dependence).group()[9:-1])
            for package2 in self.dependencies:
                comp = Package.compare(package2, package1)
                if comp == "<" or comp == "==":
                    self.dependencies.remove(package2)
            self.dependencies.append(package1)
        return self.dependencies

    def get_dependencies_from_file(self, file_name) -> list | None:
        with open(file_name, "r", encoding='utf-8') as f:
            lines = f.read().strip().split('\n')
        for line in lines:
            if ':' in line:
                package, deps = line.split(':', 1)
                if package.strip() == self.name:
                    self.dependencies = [Package(dep.strip(), "1.0.0") for dep in deps.strip().split(',') if dep.strip()]
                    return self.dependencies
        return None

    @staticmethod
    def compare(self, other):
        if self.name != other.name:
            return "!="
        for digit1, digit2 in zip(self.version, other.version):
            if "." not in [digit1, digit2] and int(digit1) < int(digit2):
                return "<"
            if "." not in [digit1, digit2] and int(digit1) > int(digit2):
                return ">"
        return "=="

    def clear_memory(self) -> None:
        try:
            if self.path != "":
                os.remove(self.path)
                path = ""
        except Exception as e:
            print(f"Error: {e}")