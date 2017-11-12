%global with_python3 1
%global pkgname PySDL2

Name:           pysdl2
Version:        0.9.5
Release:        1%{?dist}
Summary:        Python wrapper around the SDL2 library

License:        CC0
URL:            https://pysdl2.readthedocs.io
Source0:        https://bitbucket.org/marcusva/py-sdl2/downloads/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
%if %{with python3}
BuildRequires:  python3-devel
%endif # with python3

%description
PySDL2 is a wrapper around the SDL2 library and as such similar to the
discontinued PySDL project. In contrast to PySDL, it has no licensing
restrictions, nor does it rely on C code, but uses ctypes instead.

%package     -n python2-sdl2
Summary:        Python 3 wrapper around the SDL2 library

Requires:       SDL2
Requires:       SDL2_gfx
Requires:       SDL2_image
Requires:       SDL2_mixer
Requires:       SDL2_ttf

%{?python_provide:%python_provide python2-sdl2}

%description -n python2-sdl2
PySDL2 is a wrapper around the SDL2 library and as such similar to the
discontinued PySDL project. In contrast to PySDL, it has no licensing
restrictions, nor does it rely on C code, but uses ctypes instead.

Python 2 version.

%if %{with python3}
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

Python 3 version.
%endif # with python3


%prep
%autosetup -c
mv %{pkgname}-%{version} python2

%if %{with python3}
cp -a python2 python3
%endif # with python3

mkdir docs
cp -p python2/{AUTHORS,COPYING,README}.txt docs/

%build
pushd python2
%py2_build
popd

%if %{with python3}
pushd python3
%py3_build
popd
%endif # with python3


%install
%if %{with python3}
pushd python3
%py3_install
popd
%endif # with python3

pushd python2
%py2_install
popd


%files -n python2-sdl2
%license docs/COPYING.txt
%doc docs/AUTHORS.txt docs/README.txt
%{python2_sitelib}/sdl2
%{python2_sitelib}/%{pkgname}-*.egg-info

%if %{with python3}
%files -n python3-sdl2
%license docs/COPYING.txt
%doc docs/AUTHORS.txt docs/README.txt
%{python3_sitelib}/sdl2
%{python3_sitelib}/%{pkgname}-*.egg-info
%endif

%changelog
* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.5-1
- First spec
