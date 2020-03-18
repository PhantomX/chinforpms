Name:           pysdl2
Version:        0.9.7
Release:        1%{?dist}
Summary:        Python wrapper around the SDL2 library

License:        CC0
URL:            https://github.com/marcusva/py-sdl2

%global pkgversion %(c=%{version}; echo ${c//./_})
Source0:        %{url}/archive/rel_%{pkgversion}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%description
PySDL2 is a wrapper around the SDL2 library and as such similar to the
discontinued PySDL project. In contrast to PySDL, it has no licensing
restrictions, nor does it rely on C code, but uses ctypes instead.

%package     -n python3-sdl2
Summary:        Python 3 wrapper around the SDL2 library

Requires:       SDL2
Requires:       SDL2_gfx
Requires:       SDL2_image
Requires:       SDL2_mixer
Requires:       SDL2_ttf

%{?python_provide:%python_provide python3-sdl2}
Provides:       pysdl2 = %{version}-%{release}

%description -n python3-sdl2
PySDL2 is a wrapper around the SDL2 library and as such similar to the
discontinued PySDL project. In contrast to PySDL, it has no licensing
restrictions, nor does it rely on C code, but uses ctypes instead.


%prep
%autosetup -n py-sdl2-rel_%{pkgversion}

%build
%py3_build

%install
%py3_install


%files -n python3-sdl2
%license COPYING.txt
%doc AUTHORS.txt README.md
%{python3_sitelib}/sdl2
%{python3_sitelib}/*-*.egg-info

%changelog
* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.9.7-1
- 0.9.7

* Mon Apr 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.9.6-1
- 0.9.6

* Sat Apr 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.9.5-2
- Drop python2 support

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.5-1
- First spec
