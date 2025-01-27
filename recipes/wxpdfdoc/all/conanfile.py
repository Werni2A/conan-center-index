import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, get, rmdir
from conan.tools.gnu import Autotools

required_conan_version = ">=2.0.0"


class WxPdfDocConan(ConanFile):
    name = "wxpdfdoc"
    description = "wxPdfDocument allows wxWidgets applications to generate PDF documents."
    license = "wxWindows"
    url = "https://github.com/utelle/wxpdfdoc"
    homepage = "https://utelle.github.io/wxpdfdoc/"
    topics = ("wxwidgets", "pdf")
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
        # Supports 3.0.x, 3.1.x and 3.2.x as defined in the repository readme
        self.requires("wxwidgets/[>=3.0.0 <3.3]", transitive_headers=True, transitive_libs=True)

    def build_requirements(self):
        # The build configuration is already pregenerated and checked into
        # the repository. Calling premake is therefore not necessary.
        # Readme specifies premake 5.0.0-beta2
        # self.tool_requires("premake/5.0.0-beta2")
        pass

    def build(self):
        src_folder = os.path.join(self.source_folder, f"wxpdfdoc-{self.version}")
        wxwidgets_root = self.dependencies["wxwidgets"].package_folder
        autotools = Autotools(self)
        autotools.autoreconf(build_script_folder=src_folder)
        wx_config = os.path.join(wxwidgets_root, "bin", "wx-config")
        autotools.configure(build_script_folder=src_folder, args=[f"--with-wx-config={wx_config}"])
        autotools.make()

    def package(self):
        src_folder = os.path.join(self.source_folder, f"wxpdfdoc-{self.version}")

        autotools = Autotools(self)
        autotools.install()

        copy(self, "LICENCE.txt", dst=os.path.join(self.package_folder, "licenses"), src=src_folder)

        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.libs = ["wxcode_gtk2u_pdfdoc-3.2"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.builddirs = ["lib/pkgconfig"]
        self.cpp_info.set_property("pkg_config_name", "wxpdfdoc")
