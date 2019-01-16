%undefine _hardened_build
%global winecommonver 3.0

%global commit acc17f4e854a2c9f292f22242abc65ec7494de99
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190115
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

# Set to 1 if will be used with wine staging
%global staging 1

%global pkgname nine

Name:           wine-%{pkgname}
Version:        0.2.0.0
Release:        1%{?gver}%{?dist}
Summary:        Wine D3D9 interface library for Mesa's Gallium Nine statetracker

Epoch:          1

License:        LGPLv2+
URL:            https://github.com/dhewg/nine

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
Provides:       wine-nine%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      wine-nine%{?_isa} < %{?epoch:%{epoch}:}%{version}-%{release}

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%ifarch x86_64
Requires:       wine-nine(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
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

%if 0%{?staging}
sed -e 's|DWINE_STAGING=0|DWINE_STAGING=1|g' -i meson.build
%endif

sed -e "/strip =/s|=.*|= 'true'|g" -i tools/cross-wine%{__isa_bits}.in

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
# https://bugzilla.redhat.com/show_bug.cgi?id=1406093
TEMP_CFLAGS="`echo %{build_cflags} | sed -e 's/-O2/-O1/'`"
TEMP_CFLAGS="`echo $TEMP_CFLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"
TEMP_CFLAGS="`echo $TEMP_CFLAGS | sed "s| |', '|g"`"

TEMP_LDFLAGS="`echo %{build_ldflags} | sed "s| |', '|g"`"

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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.rst
%license COPYING.LIB LICENSE
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
