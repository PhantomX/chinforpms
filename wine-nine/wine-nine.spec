%undefine _hardened_build

%global commit 7f32544d22b45c178cb6a91008723fa206586873
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190202
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global winecommonver 3.0

%global pkgname wine-nine-standalone

Name:           wine-nine
Version:        0.2
Release:        1%{?gver}%{?dist}
Summary:        Wine D3D9 interface library for Mesa's Gallium Nine statetracker

Epoch:          2

License:        LGPLv2+
URL:            https://github.com/iXit/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        ninewinecfg
Source2:        wineninecfg

Source100:      wine-ninecfg.desktop

Patch0:         %{name}-optflags.patch

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(d3d)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xproto)
BuildRequires:  wine-devel

Requires:       wine-common >= %{winecommonver}
Requires:       wine-desktop >= %{winecommonver}
Enhances:       wine

Requires:       mesa-dri-drivers%{?_isa}
Requires:       mesa-libd3d%{?_isa}
Provides:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}%{?_isa} < %{?epoch:%{epoch}:}%{version}-%{release}


%ifarch x86_64
Requires:       %{name}(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Provides:       ninewinecfg.exe.so%{?_isa} = %{?epoch:%{epoch}:}%{version}
Provides:       d3d9-nine.dll.so%{?_isa} = %{?epoch:%{epoch}:}%{version}

%description
%{summary} and tool to setting it.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

sed -e "/strip =/s|=.*|= 'true'|g" -i tools/cross-wine%{__isa_bits}.in

mesonarray(){
  echo -n "$1" | sed -e "s|\s\s| |g" -e "s|\s*$||g" -e "s|\\\\||g" -e "s|'|\\\'|g" -e "s| |', '|g"
}

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
# https://bugzilla.redhat.com/show_bug.cgi?id=1406093
TEMP_CFLAGS="`echo "%{build_cflags}" | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"
TEMP_CFLAGS="`mesonarray "$TEMP_CFLAGS"`"

TEMP_LDFLAGS="`mesonarray "%{build_ldflags}"`"

sed -e "s|RPM_OPT_FLAGS|$TEMP_CFLAGS|g" -i tools/cross-wine%{__isa_bits}.in
sed -e "s|RPM_LD_FLAGS|$TEMP_LDFLAGS|g" -i tools/cross-wine%{__isa_bits}.in

./bootstrap.sh

%build

meson \
  --cross-file tools/cross-wine%{__isa_bits} \
  --buildtype "release" \
  %{_target_platform}

pushd %{_target_platform}
ninja -v %{?_smp_mflags}

winebuild --dll --fake-module -E ../d3d9-nine/d3d9.spec -F d3d9-nine.dll -o d3d9-nine.dll.fake
winebuild --exe --fake-module ninewinecfg/ninewinecfg.res -o ninewinecfg.exe.fake
popd


%install
mkdir -p %{buildroot}/%{_libdir}/wine
mkdir -p %{buildroot}/%{_libdir}/wine/fakedlls

install -pm0755 %{_target_platform}/ninewinecfg/ninewinecfg.exe.so \
  %{buildroot}/%{_libdir}/wine/ninewinecfg.exe.so
install -pm0755 %{_target_platform}/ninewinecfg.exe.fake \
  %{buildroot}/%{_libdir}/wine/fakedlls/ninewinecfg.exe

install -pm0755 %{_target_platform}/d3d9-nine/d3d9-nine.dll.so \
  %{buildroot}/%{_libdir}/wine/d3d9-nine.dll.so
install -pm0755 %{_target_platform}/d3d9-nine.dll.fake \
  %{buildroot}/%{_libdir}/wine/fakedlls/d3d9-nine.dll

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 %{S:1} %{buildroot}/%{_bindir}/ninewinecfg
%if 0%{?staging}
install -pm0755 %{S:2} %{buildroot}/%{_bindir}/wineninecfg
%endif

mkdir -p %{buildroot}%{_datadir}/applications
# install desktop file
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{S:100}


%files
%doc README.rst
%license LICENSE
%{_bindir}/ninewinecfg
%if 0%{?staging}
%{_bindir}/wineninecfg
%endif
%{_libdir}/wine/d3d9-nine.dll.so
%{_libdir}/wine/ninewinecfg.exe.so
%{_libdir}/wine/fakedlls/d3d9-nine.dll
%{_libdir}/wine/fakedlls/ninewinecfg.exe
%{_datadir}/applications/wine-ninecfg.desktop


%changelog
* Sun Feb 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:0.2-1
- 0.2.0.0 final
- Update urls

* Mon Jan 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.2.0.0-2.20190121git13e9b40
- New snapshot

* Tue Jan 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.2.0.0-1.20190115gitacc17f4
- New snapshot

* Mon Jan 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.1.0.0-2.20190107git136dca6
- Fix fake dll module name

* Mon Jan 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.1.0.0-1.20190107git136dca6
- Change to Nine Standalone

* Sat Dec 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.0_2-2
- Add upstream patches

* Sun Mar 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.0_2-1
- 3.0_2

* Fri Jan 26 2018 Phantom X <megaphantomx at bol dot com dot br>
- 3.0_1

* Wed Nov 22 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0_3-2
- Fix desktop file

* Tue Nov 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0_3-1
- Initial spec
