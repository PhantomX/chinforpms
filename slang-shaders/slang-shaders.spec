%global commit 2707c34b59ac041c1c71a1b81e2a61025b4bc5a8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20251223

BuildArch:      noarch

%global dist .%{date}git%{shortcommit}%{?dist}


Name:           slang-shaders
Version:        1766
Release:        1%{?dist}
Summary:        Collection of slang shaders from libretro

License:        GPL-1.0-only AND GPL-2.0-or-later AND GPL-3.0-or-later AND MIT AND AND Public domain AND Unlicense
URL:            https://github.com/libretro/%{name}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  make

%description
This is a collection of the slang (Vulkan GLSL) shaders from the libretro
project. Every program or library implementing the RetroArch shader pipeline can
use these shaders. RetroArch and librashader are two examples of those projects.


%prep
%autosetup -n %{name}-%{commit}

find . -type f \( -name "*.h" -o -name '*.slang*' \) -exec chmod -x {} ';'
find . -type f \( -name "*.h" -o -name '*.slang*' \) -exec sed 's/\r//' -i {} ';'

sed -e 's|$(PREFIX)/share|%{_datadir}|g' -i Makefile


%build
%make_build


%install
%make_install

rm -f %{buildroot}%{_datadir}/libretro/shaders/shaders_slang/README.md


%files
%doc README.md
%dir %{_datadir}/libretro/shaders/shaders_slang
%{_datadir}/libretro/shaders/shaders_slang/*


%changelog
* Thu Feb 06 2025 Phantom X <megaphantomx at hotmail dot com> - 1640-1.20250204git2304625
- Initial spec

