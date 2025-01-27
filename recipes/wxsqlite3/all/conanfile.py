import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, get, rmdir
from conan.tools.gnu import Autotools

required_conan_version = ">=2.0.0"


class WxSqLite3Conan(ConanFile):
    name = "wxsqlite3"
    description = "wxSQLite3 is a C++ wrapper around the SQLite database designed for use in wxWidgets applications."
    license = "LGPL-3.0+ WITH WxWindows-exception-3.1"
    url = "https://github.com/utelle/wxsqlite3"
    homepage = "https://utelle.github.io/wxsqlite3/docs/html/index.html"
    topics = ("wxwidgets", "sqlite", "sqlite3", "sql", "database")
    generators = "AutotoolsDeps", "AutotoolsToolchain"

    package_type = "static-library"
    settings = "os", "arch", "compiler", "build_type"

    def validate(self):
        if self.settings.os != "Linux":
            # We depend on wxWidgets Windows support that is not yet available on CCI.
            # Requires https://github.com/conan-io/conan-center-index/pull/26170
            raise ConanInvalidConfiguration(
                "This package is currently supported on Linux only."
            )

    def source(self):
        get(self, **self.conan_data["sources"][self.version])

    def requirements(self):
        # https://github.com/utelle/wxsqlite3/blob/c78e2dc916d7fa9611de4017a36ef38ac8c86420/premake/wxwidgets.lua#L146
        # Specifies a version in range [>=2.8 <3.2] but 3.2 works as well
        self.requires("wxwidgets/[>=2.8.0 <3.3]", transitive_headers=True, transitive_libs=True)

    def build_requirements(self):
        # The build configuration is already pregenerated and checked into
        # the repository. Calling premake is therefore not necessary.
        # Readme specifies premake 5.0.0-alpha15
        # self.tool_requires("premake/5.0.0-alpha15")
        pass

    def build(self):
        autotools = Autotools(self)
        src_folder = os.path.join(self.source_folder, f"wxsqlite3-{self.version}")
        autotools.autoreconf(build_script_folder=src_folder)
        wxwidgets_root = self.dependencies["wxwidgets"].package_folder
        wx_config = os.path.join(wxwidgets_root, "bin", "wx-config")
        autotools.configure(
            build_script_folder=src_folder, args=[f"--with-wx-config={wx_config}"]
        )
        autotools.make()

    def package(self):
        autotools = Autotools(self)
        autotools.install()

        license_files = [
            "COPYING.txt",
            "GPL-3.0.txt",
            "LGPL-3.0.txt",
            "LICENSE.spdx",
            "LICENSE.txt",
            "WxWindows-exception-3.1.txt",
        ]

        src_folder = os.path.join(self.source_folder, f"wxsqlite3-{self.version}")

        for license_file in license_files:
            copy(
                self,
                license_file,
                dst=os.path.join(self.package_folder, "licenses"),
                src=src_folder,
            )

        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.libs = ["wxcode_gtk2u_wxsqlite3-3.2"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.builddirs = ["lib/pkgconfig"]
        self.cpp_info.set_property("pkg_config_name", "wxsqlite3")
