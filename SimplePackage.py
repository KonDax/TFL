import urllib.request
from zipfile import ZipFile
import re
import os

class Package:
    def __init__(self, name: str, version: str , path: str = ""):
        self.name = name
        self.version = version
        self.path = path
        self.dependencies = []
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
    def search_dependencies_by_path(self) -> list:
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
        dependencies = []
        for dependence in dependencies_raw:
            dependencies.append(re.findall(r'id=".*?"', dependence) + re.findall(r'version=".*?"', dependence))
        return dependencies
    def clear_memory(self) -> None:
        try:
            if self.path != "":
                os.remove(self.path)
        except Exception as e:
            print(f"Error: {e}")