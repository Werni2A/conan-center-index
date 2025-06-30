import os

from conan import ConanFile
from conan.tools.files import copy, get
from conan.tools.layout import basic_layout
from conan.tools.premake import Premake, PremakeDeps, PremakeToolchain

required_conan_version = ">=2.18.0"


class WxSqLite3Conan(ConanFile):
    name = "wxsqlite3"
    description = "wxSQLite3 is a C++ wrapper around the SQLite database designed for use in wxWidgets applications."
    license = "LGPL-3.0+ WITH WxWindows-exception-3.1"
    url = "https://github.com/utelle/wxsqlite3"
    homepage = "https://utelle.github.io/wxsqlite3/docs/html/index.html"
    topics = ("wxwidgets", "sqlite", "sqlite3", "sql", "database")
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = '*'
    package_type = "library"
    options = { "shared": [True, False] }
    default_options = { "shared": False }

    def layout(self):
        basic_layout(self)

    def generate(self):
        deps = PremakeDeps(self)
        deps.generate()
        tc = PremakeToolchain(self)
        tc.generate()

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def requirements(self):
        # https://github.com/utelle/wxsqlite3/blob/v4.10.8/premake/wxwidgets.lua#L146
        self.requires("wxwidgets/[>=2.8.0 <3.3]", transitive_headers=True, transitive_libs=True)

    def build_requirements(self):
        # Readme specifies premake 5.0.0-beta5
        self.tool_requires("premake/5.0.0-beta6")

    def generate(self):
        deps = PremakeDeps(self)
        deps.generate()
        tc = PremakeToolchain(self)
        tc.generate()

    def build(self):
        premake = Premake(self)
        premake.configure()
        premake.build(workspace="wxsqlite3_vc17", targets=["wxsqlite3"])

    def package(self):
        copy(self, "*", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
        copy(self, "*", os.path.join(self.source_folder, "lib", "vc14x_x64_lib"), os.path.join(self.package_folder, "lib"))

    def package_info(self):
        self.cpp_info.libs = ["wxsqlite3"]

