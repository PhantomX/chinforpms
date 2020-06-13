%global sover 0

%bcond_with docs

%global commit 68eefbee2a53bcc08baea25fa6bd692672adf2eb
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200501
%global with_snapshot 1

# git describe
%global aom_version 1.0.0-errata1-avif-809-g68eefbee2

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           aom
Version:        1.0.0
Release:        100%{?gver}%{?dist}
Summary:        Royalty-free next-generation video format

License:        BSD
URL:            http://aomedia.org/
Source0:        https://aomedia.googlesource.com/%{name}/+archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  gcc
BuildRequires:  cmake3
%if %{with docs}
BuildRequires:  doxygen
%endif
BuildRequires:  git-core
BuildRequires:  graphviz
BuildRequires:  perl-interpreter
BuildRequires:  perl(Getopt::Long)
BuildRequires:  python3-devel
BuildRequires:  yasm

Provides:       av1 = %{version}-%{release}
Requires:       libaom%{?_isa} = %{version}-%{release}

%description
The Alliance for Open Media’s focus is to deliver a next-generation
video format that is:

 - Interoperable and open;
 - Optimized for the Internet;
 - Scalable to any modern device at any bandwidth;
 - Designed with a low computational footprint and optimized for hardware;
 - Capable of consistent, highest-quality, real-time video delivery; and
 - Flexible for both commercial and non-commercial content, including
   user-generated content.

This package contains the reference encoder and decoder.

%package -n libaom
Summary:        Library files for aom

%description -n libaom
Library files for aom, the royalty-free next-generation
video format.

%package -n libaom-devel
Summary:        Development files for aom
Requires:       libaom%{?_isa} = %{version}-%{release}

%description -n libaom-devel
Development files for aom, the royalty-free next-generation
video format.

%prep
%autosetup -p1 -c %{name}-%{commit}
# Set GIT revision in version
sed -i 's@set(aom_version "")@set(aom_version "%{aom_version}")@' build/cmake/version.cmake

%build
%cmake3 . -B %{_target_platform} \
  -DENABLE_CCACHE=1 \
  -DCMAKE_SKIP_RPATH=1 \
  -DCMAKE_BUILD_TYPE=Release \
%ifarch %{arm}
  -DAOM_NEON_INTRIN_FLAG=-mfpu=neon \
%endif
  -DCONFIG_WEBM_IO=1 \
  -DENABLE_DOCS=1 \
  -DCONFIG_ANALYZER=0 \
  -DFORCE_HIGHBITDEPTH_DECODING=0 \
%if %{without docs}
  -DENABLE_DOCS=0 \
%endif
%{nil}

%make_build -C %{_target_platform}


%install
%make_install -C %{_target_platform}

rm -f %{buildroot}%{_libdir}/*.a


%files
%doc AUTHORS CHANGELOG README.md
%license LICENSE PATENTS
%{_bindir}/aomdec
%{_bindir}/aomenc

%files -n libaom
%license LICENSE PATENTS
%{_libdir}/libaom.so.%{sover}
%{_libdir}/libaom.so.1.0.0

%files -n libaom-devel
%if %{with docs}
%doc %{_target_platform}/docs/html/
%endif
%{_includedir}/%{name}
%{_libdir}/libaom.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Tue May 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.0.0-100.20200501git68eefbe
- New snapshot

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-9.20190810git9666276
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 17:45:23 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.0-8.20190810git9666276
- Update to commit 9666276accea505cd14cbcb9e3f7ff5033da9172

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7.20180925gitd0076f5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6.20180925gitd0076f5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 25 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.0-5.20180925gitd0076f5
- Update to commit d0076f507a6027455540e2e4f25f84ca38803e07
- Set CONFIG_LOWBITDEPTH to 1
- Fix #1632658

* Thu Sep 13 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.0-4
- Split the package into libs/tools

* Tue Sep 11 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.0-3
- Update the archive in order to detect the correct version from the changelog

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.0-1
- First RPM release

