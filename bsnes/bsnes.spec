%global commit 77fa7d9e0c7698461cf2757c76010ce21ab3589d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190906
%global with_snapshot 0

%ifarch x86_64
%global build_with_lto    0
%endif

%global with_gtk2 1
%global with_libao 0
%global with_openal 0

%if 0%{?with_gtk2}
%global toolkit gtk2
%else
%global toolkit gtk3
%endif

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           bsnes
Version:        109
Release:        1%{?gver}%{?dist}
Summary:        Nintendo SNES emulator

License:        GPLv3 and BSD

URL:            https://bsnes.byuu.org/

%global vc_url  https://github.com/byuu/%{name}
%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif #{?with_snapshot}

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(alsa)
%if 0%{?with_libao}
BuildRequires:  pkgconfig(ao)
%endif
BuildRequires:  pkgconfig(gl)
%if 0%{?with_gtk2}
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(gtksourceview-2.0)
%else
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtksourceview-3.0)
%endif
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpulse-simple)
%if 0%{?with_openal}
BuildRequires:  pkgconfig(openal)
%endif
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xv)
Requires:       hicolor-icon-theme

%description
bsnes is a Super Nintendo / Super Famicom emulator that began development on
October 14th, 2004. It focuses on performance, features, and ease of use.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup %{name}-%{version} -p1
%endif

sed -i -e 's|-L/usr/local/lib ||g' -i hiro/GNUmakefile

sed -e "/handle/s|/usr/local/lib|%{_libdir}|g" -i nall/dl.hpp

%if !0%{?with_ao}
  sed -e "/ruby +=/s|audio.ao\b||" -i ruby/GNUmakefile
%endif
%if !0%{?with_openal}
  sed -e "/ruby +=/s|audio.openal\b||" -i ruby/GNUmakefile
%endif


%build
export flags="%(echo %{build_cxxflags} | sed -e 's/-O2\b/-O3/')"
export options="%{build_ldflags}"

%make_build -C %{name} target=%{name} verbose \
  build=performance local=false hiro=%{toolkit} \
%if 0%{?build_with_lto}
  lto=true \
%endif
%{nil}


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}/out/%{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}/{Database,Firmware,Locale}/
cp -rp %{name}/Database/* %{buildroot}%{_datadir}/%{name}/Database/
cp -rp %{name}/Locale/* %{buildroot}%{_datadir}/%{name}/Locale/

find %{buildroot}%{_datadir} -name '.gitgnore' -delete

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}/target-%{name}/resource/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{256x256,scalable}/apps
install -pm0644 %{name}/target-%{name}/resource/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

install -pm0644 %{name}/target-%{name}/resource/%{name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

for res in 16 22 24 32 36 48 64 72 96 128 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert %{name}/target-%{name}/resource/%{name}.png \
    -filter Lanczos -resize ${res}x${res} ${dir}/%{name}.png
done


%files
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.*


%changelog
* Sat Sep 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 109-1
- Initial spec
