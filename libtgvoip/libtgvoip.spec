%global commit f77531160a2ef4cd2fd27f68186f2768033b594d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20191230
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           libtgvoip
Version:        2.4.4
Release:        101%{?gver}%{?dist}
Summary:        VoIP library for Telegram clients

# Libtgvoip shared library - Public Domain.
# Bundled webrtc library - BSD with patented echo cancellation algorithms.
License:        Public Domain and BSD
URL:            https://github.com/grishka/%{name}

%global tg_url  https://github.com/telegramdesktop/%{name}
%if 0%{?with_snapshot}
Source0:        %{tg_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif
Patch0:         %{name}-build-fixes.patch

Patch100:       %{tg_url}/pull/6.patch#/%{name}-gh-pull6.patch
Patch200:       %{name}-link-libraries.patch

Provides:       bundled(webrtc-audio-processing) = 0.3

BuildRequires:  pulseaudio-libs-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  openssl-devel
BuildRequires:  json11-devel
BuildRequires:  opus-devel
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gyp

%description
Provides VoIP library for Telegram clients.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       json11-devel%{?_isa}

%description devel
%{summary}.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -p1
%endif

sed \
  -e 's|@prefix@|%{_prefix}|g' \
  -e 's|@exec_prefix@|%{_prefix}|g' \
  -e 's|@libdir@|%{_libdir}|g' \
  -e 's|@includedir@|%{_includedir}|g' \
  tgvoip.pc.in > tgvoip.pc

%build
export VOIPVER="%{version}"
gyp --format=cmake --depth=. --generator-output=. -Goutput_dir=out -Gconfig=Release %{name}.gyp

pushd out/Release
    %cmake .
    %make_build
popd

%install
# Installing shared library...
mkdir -p %{buildroot}%{_libdir}/pkgconfig
%global major %(echo %{version} | cut -d. -f1)
%global minor %(echo %{version} | cut -d. -f1-2)
install -m 0755 -p out/Release/lib.target/%{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so.%{version}"
ln -s %{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so.%{major}"
ln -s %{name}.so.%{major} "%{buildroot}%{_libdir}/%{name}.so"

install -pm0644 tgvoip.pc %{buildroot}%{_libdir}/pkgconfig/

# Installing additional development files...
mkdir -p "%{buildroot}%{_includedir}/%{name}/audio"
mkdir -p "%{buildroot}%{_includedir}/%{name}/video"
find . -maxdepth 1 -type f -name "*.h" -exec install -m 0644 -p '{}' %{buildroot}%{_includedir}/%{name} \;
find audio -maxdepth 1 -type f -name "*.h" -exec install -m 0644 -p '{}' %{buildroot}%{_includedir}/%{name}/audio \;
find video -maxdepth 1 -type f -name "*.h" -exec install -m 0644 -p '{}' %{buildroot}%{_includedir}/%{name}/video \;

ln -sf %{name} %{buildroot}%{_includedir}/tgvoip


%files
%license UNLICENSE
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/%{name}/
%{_includedir}/tgvoip
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/tgvoip.pc


%changelog
* Mon Jan 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.4.4-101.20191230gitf775311
- Change to internal telegram fork
- pkgconfig file

* Wed Mar 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.4.4-100
- 2.4.4

* Sat Jan 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.4.2-100.chinfo
- 2.4.2
- RPMFusion sync

* Tue Dec 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.4-100.chinfo
- 2.4
- RPMFusion sync

* Mon Dec 03 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.3-100.chinfo
- 2.3

* Sun Sep 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.2.4-100.chinfo
- 2.2.4
- RPMFusion sync

* Wed Aug 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.2.3-100.chinfo
- Fix unresolved symbols

* Mon Aug 27 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 2.2.3-2
- Added upstream patch with proxy fix.

* Fri Aug 24 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 2.2.3-1
- Updated to 2.2.3 (regular release).

* Fri Jul 20 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 2.2-1
- Updated to 2.2 (regular release).

* Mon Jul 02 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 2.1.1-1
- Updated to 2.1.1 (regular release).

* Tue Jun 05 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 2.1-0.1.20180604git6a8f543
- Updated to 2.1 (snapshot).

* Tue May 29 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 2.0-0.3.20180528git83ac2c6
- Updated to latest snapshot.

* Sun May 27 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 2.0-0.2.20180525gitd2453dd
- Updated to latest snapshot.

* Thu May 24 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 2.0-0.1.20180515gitb52eb58
- Updated to 2.0-alpha4 (snapshot).

* Fri Dec 29 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.3-1
- Updated to 1.0.3 (regular release).

* Sat Nov 18 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.1-2.20171111git6a0b3b2
- Provide compactibility with 1.0.

* Sat Nov 18 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.1-1.20171111git6a0b3b2
- Updated to 1.0.1-git.

* Fri Aug 04 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0-3.20170801gitbfd5cfe
- Fixed build on other architectures. Build against regular OpenSSL.

* Wed Aug 02 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0-2.20170801gitbfd5cfe
- Updated to latest snapshot. Small SPEC fixes. Added virtual provides.

* Tue Aug 01 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0-1.20170727git01f2701
- Initial release.
