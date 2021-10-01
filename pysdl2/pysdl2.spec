%global pkgname py-sdl2

Name:           pysdl2
Version:        0.9.9
Release:        2%{?dist}
Summary:        Python wrapper around the SDL2 library

License:        CC0
URL:            https://github.com/marcusva/py-sdl2

Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz

Patch0:         0001-skip-some-tests.patch

BuildArch:      noarch
BuildRequires:  python3-devel

# Tests
BuildRequires:  SDL2
BuildRequires:  SDL2_gfx
BuildRequires:  SDL2_image
BuildRequires:  SDL2_mixer
BuildRequires:  SDL2_ttf
BuildRequires:  %{py3_dist pyopengl}
BuildRequires:  %{py3_dist pytest}

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
%autosetup -n %{pkgname}-%{version} -p1

# These tests fail on COPR
rm -f sdl2/test/{audio_test,sdlmixer_test,version_test}.py

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files sdl2


%check
%{pytest}
%{__python3} setup.py test


%files -n python3-sdl2 -f %{pyproject_files}
%license doc/copying.rst
%doc AUTHORS.txt README.md


%changelog
* Thu Sep 30 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.9-2
- Disable one more test

* Sun Sep 05 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.9-1
- 0.9.9
- Update to best packaging practices
- Add tests

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.9.7-1
- 0.9.7

* Mon Apr 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.9.6-1
- 0.9.6

* Sat Apr 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.9.5-2
- Drop python2 support

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.5-1
- First spec
