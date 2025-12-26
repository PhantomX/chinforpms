%global with_extra_flags -O3
%{?with_extra_flags:%global _pkg_extra_cflags %{?_pkg_extra_cflags} %{?with_extra_flags}}
%{?with_extra_flags:%global _pkg_extra_cxxflags %{?_pkg_extra_cxxflags} %{?with_extra_flags}}

%global commit 432c4e3b2a9f233cd742d1de764cced7ff337e48
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20231221
%bcond snapshot 0

%bcond libao 0
%bcond openal 0

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global rashader_ver 0.9.2
%global vc_url  https://github.com/ares-emulator/%{name}

Name:           ares
Version:        147
Release:        1%{?dist}
Summary:        Multi-system emulator

License:        ISC AND GPL-3.0-only AND BSD-2-Clause AND BSD-3-Clause AND MIT

URL:            https://ares-emu.net/

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

Patch11:        0001-Use-system-libraries.patch
Patch500:       0001-CHD-fix-for-patched-libchdr.patch

BuildRequires:  desktop-file-utils
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(alsa)
%if %{with libao}
BuildRequires:  pkgconfig(ao)
%endif
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpulse-simple)
BuildRequires:  pkgconfig(libchdr)
BuildRequires:  pkgconfig(librashader) >= %{rashader_ver}
BuildRequires:  pkgconfig(libudev)
%if %{with openal}
BuildRequires:  pkgconfig(openal)
%endif
BuildRequires:  pkgconfig(sdl3)
BuildRequires:  cmake(VulkanHeaders)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xv)

Requires:       hicolor-icon-theme
Requires:       librashader%{?_isa} >= %{rashader_ver}
Requires:       slang-shaders
Requires:       vulkan-loader%{?_isa}


%description
ares is a multi-system emulator with an uncompromising focus on
accuracy and code readability.

It requires a CPU with SSE4.2 instructions.


%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -N -p1
%autopatch -M 499 -p1

rm -rf thirdparty/{libchdr,librashader,MoltenVK,slang-shaders}

find . -type f \( -name "*.cpp" -o -name "*.h" -o -name "*.hpp" -o -name '*.slang*' \) -exec chmod -x {} ';'

find -name '.gitignore' -delete

cp -a nall/nall/file.hpp nall/nall/file-chd.hpp
cp -a nall/nall/file-buffer.hpp nall/nall/file-buffer-chd.hpp
%patch -P 500 -p1

sed -e '/\.github/d' -i CMakeLists.txt

sed -e 's|/usr/lib /usr/local/lib|%{_libdir}|g' -i cmake/finders/*.cmake

sed -e "/handle/s|/usr/local/lib|%{_libdir}|g" -i nall/nall/dl.hpp

sed -e 's|ARES_ENABLE_LIBRASHADER|ARES_BUNDLE_SHADERS|' -i desktop-ui/CMakeLists.txt


%build
%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DCMAKE_SKIP_RPATH:BOOL=ON \
%if %{without snapshot}
  -DARES_BUILD_OFFICIAL:BOOL=ON \
%endif
  -DARES_BUILD_LOCAL:BOOL=OFF \
  -DARES_ENABLE_MINIMUM_CPU:BOOL=OFF \
  -DENABLE_IPO:BOOL=OFF \
  -DARES_SKIP_DEPS:BOOL=ON \
%if %{without libao}
  -DARES_ENABLE_AO:BOOL=OFF \
%endif
%if %{without openal}
  -DARES_ENABLE_OPENAL:BOOL=OFF \
%endif
  -DARES_ENABLE_LIBRASHADER:BOOL=ON \
  -DARES_BUNDLE_SHADERS:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install

for res in 16 22 24 32 36 48 64 72 96 128 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  for icon in %{name} ;do
    magick desktop-ui/resource/%{name}.png \
      -filter Lanczos -resize ${res}x${res} ${dir}/${icon}.png
  done
done


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_bindir}/sourcery
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/Database/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.*


%changelog
* Tue Dec 23 2025 Phantom X <megaphantomx at hotmail dot com> - 147-1
- 147

* Wed Aug 27 2025 Phantom X <megaphantomx at hotmail dot com> - 146-1
- 146

* Thu Jul 10 2025 Phantom X <megaphantomx at hotmail dot com> - 145-1
- 145

* Tue Apr 29 2025 Phantom X <megaphantomx at hotmail dot com> - 144-1
- 144

* Tue Feb 18 2025 Phantom X <megaphantomx at hotmail dot com> - 143-1
- 143

* Wed Feb 05 2025 Phantom X <megaphantomx at hotmail dot com> - 142-1
- 142
- cmake
- Unbundle slang-shaders

* Fri Nov 15 2024 Phantom X <megaphantomx at hotmail dot com> - 141-1
- 141

* Tue Aug 27 2024 Phantom X <megaphantomx at hotmail dot com> - 140-1
- 140

* Thu Jun 20 2024 Phantom X <megaphantomx at hotmail dot com> - 139-1
- 139

* Wed May 15 2024 Phantom X <megaphantomx at hotmail dot com> - 138-1
- 138

* Tue Apr 02 2024 Phantom X <megaphantomx at hotmail dot com> - 137-1
- 137
- BR: librashader

* Thu Mar 28 2024 Phantom X <megaphantomx at hotmail dot com> - 136-1
- 136

* Tue Jan 23 2024 Phantom X <megaphantomx at hotmail dot com> - 135-1
- 135

* Wed Nov 22 2023 Phantom X <megaphantomx at hotmail dot com> - 134-1
- 134

* Sat Jul 22 2023 Phantom X <megaphantomx at hotmail dot com> - 133-1
- 133

* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 132-2.20230316gitbe869f9
- gcc 13 build fix

* Wed Mar 08 2023 Phantom X <megaphantomx at hotmail dot com> - 132-1
- 132

* Thu Dec 29 2022 Phantom X <megaphantomx at hotmail dot com> - 131-1.20221227git92bf0c6
- 131

* Sun Nov 13 2022 Phantom X <megaphantomx at hotmail dot com> - 130.1-1.20221111git1622ac0
- Initial spec
