#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import CMake, ConanFile, tools

class LibExpatConan(ConanFile):
    name = "expat"     
    package_revision = "-r2"
    upstream_version = "2.2.5"
    version = "{0}{1}".format(upstream_version, package_revision)
    description = "Fast XML parser in C"
    url = "https://git.ircad.fr/conan/conan-expat"
    license = "MIT"
    exports = ['patches/CMakeLists.txt', 'patches/FindEXPAT.cmake']
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def configure(self):
        del self.settings.compiler.libcxx

    def requirements(self):
        self.requires("common/1.0.0@sight/stable")

    def source(self):
        tools.get("https://github.com/libexpat/libexpat/archive/R_{0}.tar.gz".format(self.upstream_version.replace(".", "_")))
        os.rename('libexpat-R_' + self.upstream_version.replace(".", "_"), self.source_subfolder)

    def build(self):
        #Import common flags and defines
        import common
        shutil.copyfile("patches/CMakeLists.txt", "CMakeLists.txt")

        cmake = CMake(self, parallel=True)

        #Set common flags
        cmake.definitions["CMAKE_C_FLAGS"] = common.get_c_flags()
        cmake.definitions["CMAKE_CXX_FLAGS"] = common.get_cxx_flags()

        cmake.definitions['BUILD_doc'] = False
        cmake.definitions['BUILD_examples'] = False
        cmake.definitions['BUILD_tests'] = False
        cmake.definitions['BUILD_tools'] = False
        cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = True
        cmake.definitions['BUILD_shared'] = self.options.shared

        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("FindEXPAT.cmake", src="patches", dst=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

