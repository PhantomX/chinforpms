%global commit e4a6ba94efe4b2dd6400d7ba78234fa8edade407
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190329
%global with_snapshot 1

# Enable ffmpeg support
%bcond_with ffmpeg
# Enable Qt build (build broken, vulkan issues)
%bcond_with qt

%global commit1 0a4a794b7d83dc14d1ca795bbede108ffd8bb775
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 addrlib

%global commit2 7f4abd84d11e13193ea95c506a03eb4d7cf928e3
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 libbinrec

%global commit3 6ccd467094973824d89efb16cbc553e279f79823
%global shortcommit3 %(c=%{commit1}; echo ${c:0:7})
%global srcname3 Catch

%global commit4 6b780c98c767cf1a9f36b06070db8cf07243354f
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 cpptoml

%global commit5 6f722e657dd094f52f35a96ea2e11e63322e2403
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 excmd

%global commit6 383948922fef42ab0e2de628563c1c1caf6c19d9
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 fixed_point

%global commit7 295a0d84d947be5cd623daa240b0ce038c560063
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 fmt

%global commit8 f32808fdc4f684e51b2efc9f91ab71dc082d0ad0
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})
%global srcname8 glbinding

%global commit9 1bc601c674aecc2fee0dee8ff7a118db76b4c439
%global shortcommit9 %(c=%{commit9}; echo ${c:0:7})
%global srcname9 glslang

%global commit10 292615c3c2812bdb224843faa41310b30c1e483a
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 gsl-lite

%global commit11 00418d13e369bf53cc4b8f817eb10b8ce65f0904
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 imgui

%global commit12 863b8892dd2ad4492779f9366301b68979a4ad4d
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 ovsocket

%global commit13 79f4d90c19a1ffad613c89b470e11b313275e982
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 cpp-peglib

%global commit14 b6b9d835c588c35227410a9830e7a4586f90777a
%global shortcommit14 %(c=%{commit14}; echo ${c:0:7})
%global srcname14 spdlog


%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url  https://github.com/decaf-emu

Name:           decaf-emu
Version:        0
Release:        1%{?gver}%{?dist}
Summary:        A researching Wii U emulator

# OFL: ttf fonts
License:        GPLv3+ and OFL
URL:            https://github.com/%{name}/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        %{vc_url}/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        %{vc_url}/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/philsquared/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        https://github.com/skystrife/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        https://github.com/exjam/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
Source6:        https://github.com/johnmcfarlane/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        https://github.com/fmtlib/%{srcname7}/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
Source8:        https://github.com/cginternals/%{srcname8}/archive/%{commit8}/%{srcname8}-%{shortcommit8}.tar.gz
Source9:        https://github.com/KhronosGroup/%{srcname9}/archive/%{commit9}/%{srcname9}-%{shortcommit9}.tar.gz
Source10:       %{vc_url}/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
Source11:       https://github.com/ocornut/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
Source12:       https://github.com/exjam/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit12}.tar.gz
Source13:       https://github.com/yhirose/%{srcname13}/archive/%{commit13}/%{srcname13}-%{shortcommit13}.tar.gz
Source14:       https://github.com/gabime/%{srcname14}/archive/%{commit14}/%{srcname14}-%{shortcommit14}.tar.gz

Patch0:         0001-Use-system-libraries.patch
Patch1:         0001-Fix-includes.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
%if %{with ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
%endif
BuildRequires:  cmake(cereal)
BuildRequires:  pugixml-devel
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(sdl2)
#BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(zlib)
%if %{with qt}
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Widgets)
%endif

%if %{with qt}
BuildRequires:  icoutils
%endif
BuildRequires:  hicolor-icon-theme
BuildRequires:  shared-mime-info

Requires:       dejavu-sans-fonts

%description
%{name} is a researching Wii U emulator.


%package sdl
Summary:        A researching Wii U emulator (SDL version)
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description sdl
%{name} is a researching Wii U emulator.

This is the SDL version.


%package qt
Summary:        A researching Wii U emulator (Qt version)
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       hicolor-icon-theme

%description qt
%{name} is a researching Wii U emulator.

This is the Qt version.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

tar -xf %{S:1} -C libraries/addrlib --strip-components 1
tar -xf %{S:2} -C libraries/libbinrec --strip-components 1
tar -xf %{S:3} -C libraries/catch --strip-components 1
tar -xf %{S:4} -C libraries/cpptoml --strip-components 1
tar -xf %{S:5} -C libraries/excmd --strip-components 1
tar -xf %{S:6} -C libraries/fixed_point --strip-components 1
tar -xf %{S:7} -C libraries/fmt --strip-components 1
tar -xf %{S:8} -C libraries/glbinding --strip-components 1
tar -xf %{S:9} -C libraries/glslang --strip-components 1
tar -xf %{S:10} -C libraries/gsl-lite --strip-components 1
tar -xf %{S:11} -C libraries/imgui --strip-components 1
tar -xf %{S:12} -C libraries/ovsocket --strip-components 1
tar -xf %{S:13} -C libraries/cpp-peglib --strip-components 1
tar -xf %{S:14} -C libraries/spdlog --strip-components 1

sed -e 's|" "lib|" "ffmpeg/lib|g' -i CMakeModules/FindFFMPEG.cmake

%if 0%{?with_snapshot}
  sed \
    -e 's|@GIT_REV@|%{commit}|g' \
    -e 's|@GIT_BRANCH@|HEAD|g' \
    -e 's|@GIT_DESC@|%{shortcommit}|g' \
    -e 's|@BUILD_FULLNAME@|chinforpms %{version}-%{release}|g' \
    -i src/decaf_buildinfo.h.in
%endif

%if %{with qt}
icotool -x resources/decaf.ico
%endif

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}

%if 0%{?with_snapshot}
export CI=true
export TRAVIS=true
export TRAVIS_REPO_SLUG=%{name}/%{name}-nightly
export TRAVIS_TAG="%{version}-%{release}"
%endif

export CXXFLAGS="%(pkg-config --silence-errors --cflags-only-I libavformat || :) %{build_cxxflags} -fpermissive"

#FIXME: vulkan failing to build
%cmake .. \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
  -DOpenGL_GL_PREFERENCE=GLVND \
  -DDECAF_VULKAN:BOOL=OFF \
%if %{with qt}
  -DDECAF_QT:BOOL=ON \
%endif
%if !%{with ffmpeg}
  -DDECAF_FFMPEG:BOOL=OFF \
%endif
%{nil}

%make_build

popd


%install
%make_install -C %{_target_platform}

rm -rf %{buildroot}%{_datadir}/doc

rm -f %{buildroot}%{_datadir}/%{name}/resources/fonts/DejaVuSansMono.ttf
ln -sf ../../../fonts/dejavu/DejaVuSans.ttf \
  %{buildroot}%{_datadir}/%{name}/resources/fonts/DejaVuSansMono.ttf

%if %{with qt}
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=%{name}
Type=Application
Comment=A researching Wii U emulator
Exec=decaf-qt
Icon=%{name}
Terminal=false
Categories=Game;Emulator;
EOF

for res in 16 32 48 128 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 decaf_?_${res}x${res}x32.png ${dir}/%{name}.png
done

%endif


%files
%license LICENSE.md resources/fonts/NotoSansCJK.LICENSE
%doc README.md
%{_bindir}/decaf-cli
%{_datadir}/%{name}/


%files sdl
%license LICENSE.md
%{_bindir}/decaf-sdl


%if %{with qt}
%files qt
%license LICENSE.md
%{_bindir}/decaf-qt
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%endif


%changelog
* Wed Apr 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-2.20190423gitb9e51f0
- Initial spec
