%bcond_with test

# Installed library version
%global lib_version 2111.0.0

Name:           abseil-cpp
Version:        20211102.0
Release:        100%{?dist}
Summary:        C++ Common Libraries

License:        ASL 2.0
URL:            https://abseil.io
Source0:        https://github.com/abseil/abseil-cpp/archive/%{version}/%{name}-%{version}.tar.gz

# Remove test assertions that use ::testing::Conditional, which is not in a
# released version of GTest. Not submitted upstream, as this is a workaround
# rather than a fix. https://github.com/abseil/abseil-cpp/issues/1063
Patch0:         abseil-cpp-20211102.0-gtest-unreleased-features.patch
# SysinfoTest.NominalCPUFrequency in absl_sysinfo_test fails occasionally
# on aarch64, but see:
#
# NominalCPUFrequency Test from SysInfoTest Suite Fails on M1 Mac
# https://github.com/abseil/abseil-cpp/issues/1053#issuecomment-961432444
#
# in which an upstream author opines:
#
#   If the only problem you are trying to solve is a failing test, this is safe
#   to ignore since this code is never called. I should consider stripping this
#   test out of the open source release. NominalCPUFrequency is only called in
#   code private to Google and we do have tests on the platforms we use it on.
#
# We therefore disable it on all architectures, since any future failures
# will also not be meaningful.
#
# Note also that this test is removed upstream in commit
# 732b5580f089101ce4b8cdff55bb6461c59a6720 (internal commit
# 7e8da4f14afd25d11713eee6b743ba31605332bf).
Patch1:         abseil-cpp-20211102.0-disable-nominalcpufrequency.patch

BuildRequires:  cmake
# The default make backend would work just as well; ninja is observably faster
BuildRequires:  ninja-build
BuildRequires:  gcc-c++

%if %{with test}
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel
%endif

%ifarch s390x
# Symbolize.SymbolizeWithMultipleMaps fails in absl_symbolize_test on s390x
# with LTO
# https://github.com/abseil/abseil-cpp/issues/1133
%global _lto_cflags %{nil}
%endif

%description
Abseil is an open-source collection of C++ library code designed to augment
the C++ standard library. The Abseil library code is collected from
Google's own C++ code base, has been extensively tested and used in
production, and is the same code we depend on in our daily coding lives.

In some cases, Abseil provides pieces missing from the C++ standard; in
others, Abseil provides alternatives to the standard for special needs we've
found through usage in the Google code base. We denote those cases clearly
within the library code we provide you.

Abseil is not meant to be a competitor to the standard library; we've just
found that many of these utilities serve a purpose within our code base,
and we now want to provide those resources to the C++ community as a whole.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers for %{name}

%prep
%autosetup -p1 -S gendiff

# Replace GTEST_FLAG_GET, which is not in a released version of GTest, with an
# appropriate default value. Not submitted upstream, as this is a workaround
# rather than a fix. https://github.com/abseil/abseil-cpp/issues/1063
#
# The find-then-sed pattern means we only discard mtimes on files that actually
# needed to be modified.
find . -type f -name '*.cc' \
    -exec gawk '/GTEST_FLAG_GET/ { print FILENAME ; nextfile }' '{}' '+' |
  xargs -r -t sed -r -i 's/GTEST_FLAG_GET/::testing::GTEST_FLAG/g'


%build
%cmake \
  -GNinja \
  -DABSL_USE_EXTERNAL_GOOGLETEST:BOOL=ON \
  -DABSL_FIND_GOOGLETEST:BOOL=ON \
%if %{with test}
  -DBUILD_TESTING:BOOL=ON \
%endif
  -DABSL_ENABLE_INSTALL:BOOL=ON \
  -DCMAKE_BUILD_TYPE:STRING=None \
  -DCMAKE_CXX_STANDARD:STRING=17
%cmake_build


%install
%cmake_install

%check
%if %{with test}
%ctest
%endif

%files
%license LICENSE
%doc FAQ.md README.md UPGRADES.md
%{_libdir}/libabsl_*.so.%{lib_version}

%files devel
%{_includedir}/absl
%{_libdir}/libabsl_*.so
%{_libdir}/cmake/absl
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 20211102.0-100
- Fedora 36 backport

* Tue Mar 15 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20211102.0-2
- Disable LTO on s390x to work around test failure
- Skip SysinfoTest.NominalCPUFrequency on all architectures; it fails
  occasionally on aarch64, and upstream says we should not care

* Fri Feb 18 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20211102.0-1
- Update to 20211102.0 (close RHBZ#2019691)
- Drop --output-on-failure, already in %%ctest expansion
- On s390x, instead of ignoring all tests, skip only the single failing test
- Use ninja backend for CMake: speeds up build with no downsides
- Drop patch for armv7hl

* Mon Jan 31 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20210324.2-4
- Fix test failure (fix RHBZ#2045186)

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210324.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210324.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Rich Mattes <richmattes@gmail.com> - 20210324.1-2
- Update to release 20210324.2
- Enable and run test suite

* Mon Mar 08 2021 Rich Mattes <richmattes@gmail.com> - 20200923.3-1
- Update to release 20200923.3

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200923.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 19 2020 Rich Mattes <richmattes@gmail.com> - 20200923.2-1
- Update to release 20200923.2
- Rebuild to fix tagging in koji (rhbz#1885561)

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200225.2-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200225.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 27 2020 Rich Mattes <richmattes@gmail.com> - 20200225.2-2
- Don't remove buildroot in install

* Sun May 24 2020 Rich Mattes <richmattes@gmail.com> - 20200225.2-1
- Initial package.
