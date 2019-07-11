%global commit bd5484299779080bd24e97b0a1f50603447a623a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190528
%global with_snapshot 1

%global apiid 17349
%global apihash 344583e45741c457fe1862106095a5eb

%ifarch x86_64
%global build_with_lto    1
%endif

%global optflags %(echo %{optflags} | sed -e 's/ -g\\b/ -g1/')

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           kepka
# If rc, use "~" instead "-", as ~rc1
Version:        2.0.0~rc2
Release:        2%{?gver}%{?dist}
Summary:        Unofficial Telegram desktop messaging app

License:        GPLv3+
URL:            https://github.com/procxx/%{name}

%global ver     %{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}
%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{ver}/%{name}-%{ver}.tar.gz
%endif
Source1:        thunar-sendto-%{name}.desktop

Patch0:         0001-Use-system-libraries.patch
Patch1:         %{name}-system-fonts.patch
Patch2:         0001-Do-not-show-unread-counter-on-muted-chats.patch
Patch3:         0001-Always-display-scrollbars.patch
Patch4:         0001-Fix-API-ENV.patch

ExclusiveArch:  i686 x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake

BuildRequires:  guidelines-support-library-devel
BuildRequires:  mapbox-variant-devel
BuildRequires:  ffmpeg-devel >= 3.1
BuildRequires:  openal-soft-devel
BuildRequires:  qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires:  libstdc++-devel
BuildRequires:  range-v3-devel
BuildRequires:  openssl-devel
BuildRequires:  minizip-compat-devel
BuildRequires:  zlib-devel
BuildRequires:  xz-devel
BuildRequires:  python3

BuildRequires:  alsa-lib-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  opus-devel

Requires:       qt5-qtimageformats%{?_isa}
Requires:       hicolor-icon-theme

Requires:       qt5-qtimageformats%{?_isa}
Requires:       hicolor-icon-theme
Requires:       open-sans-fonts


%description
Kepka is a messaging app with a focus on speed and security, it’s super
fast, simple and free. You can use Kepka on all your devices at the same
time — your messages sync seamlessly across any of your phones, tablets or
computers.

With Kepka you can send messages, photos, videos and files of any type
(doc, zip, mp3, etc), as well as create groups for up to 200 people. You can
write to your phone contacts and find people by their usernames. As a result,
Kepka is like SMS and email combined — and can take care of all your
personal or business messaging needs.

%prep
# Unpacking main source archive...
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{ver} -p1
%endif

rm -rf Telegram/ThirdParty/minizip

find Telegram/ThirdParty/libtgvoip -type f \( -name "*.cpp" -o -name "*.h" \) -exec sed -e 's/\r//' -i {} ';'

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}

%if 0%{?build_with_lto}
export CC=gcc
export CXX=g++

RPM_NCPUS=%(echo %{_smp_mflags} | sed 's/-j//')
RPM_FLTO_FLAGS="-flto=$RPM_NCPUS -fuse-linker-plugin -fdisable-ipa-cdtor"
export CFLAGS="%{optflags} $RPM_FLTO_FLAGS"
export CXXFLAGS="%{optflags} $RPM_FLTO_FLAGS"
export LDFLAGS="%{build_ldflags} $RPM_FLTO_FLAGS"
%endif

export API_ID=%{apiid}
export API_HASH=%{apihash}

%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DPACKAGED_BUILD:BOOL=TRUE \
%if 0%{?build_with_lto}
  -DCMAKE_AR:FILEPATH=%{_bindir}/gcc-ar \
  -DCMAKE_NM:FILEPATH=%{_bindir}/gcc-nm \
  -DCMAKE_RANLIB:FILEPATH=%{_bindir}/gcc-ranlib \
%endif
%{nil}

%make_build
popd


%install
%make_install -C %{_target_platform}

rm -rf %{buildroot}%{_datadir}/kservices5

mkdir -p %{buildroot}%{_datadir}/Thunar/sendto
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/Thunar/sendto \
  %{S:1}


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/Thunar/sendto/thunar-sendto-%{name}.desktop
%{_metainfodir}/%{name}.appdata.xml


%changelog
* Wed Jul 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.0.0~rc2-2.20190528gitbd54842
- Snapshot

* Fri May 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.0.0~rc2-1
- chinforpms

* Fri Jul 27 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 2.0.0-1
- Updated to version 2.0.0.

* Thu Dec 21 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.0-1
- Initial SPEC release.
