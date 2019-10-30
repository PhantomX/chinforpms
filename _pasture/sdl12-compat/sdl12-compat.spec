%global commit dc55edfe5d2f
%global date 20190403
%global with_snapshot 1

%global sdl2_version %(pkg-config --silence-errors --modversion sdl2 2>/dev/null || echo 2.0.10)

%if 0%{?with_snapshot}
%global gver .%{date}git%{commit}
%endif

Name:           sdl12-compat
Version:        1.2.50
Release:        1%{?gver}%{?dist}
Summary:        Compatibility layer that provides SDL 1.2 API backed by SDL2

License:        zlib and MIT
URL:            http://www.libsdl.org

Source0:        https://hg.libsdl.org/sdl12-compat/archive/%{commit}.tar.bz2#/%{name}-%{commit}.tar.bz2

Patch0:         0001-Disable-test_program-build.patch


BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  pkgconfig(sdl2)
Requires:       SDL2%{_isa} >= %{sdl2_version}


%description
%{summary}.


%prep
%autosetup -n %{name}-%{commit} -p1

sed \
  -e 's|/usr/local/include/SDL2|%(pkg-config --variable=includedir sdl2)/SDL2|g' \
  -e 's|/usr/X11/include|%{_includedir}/X11|g' \
  -i CMakeLists.txt


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
%{nil}

%make_build
popd


%install
mkdir -p %{buildroot}%{_libdir}/%{name}
chmod +x %{_target_platform}/*.so.*
cp -a %{_target_platform}/*.so.* %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/%{name}" \
  > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%files
%license COPYING
%doc BUGS README README-SDL.txt
%{_libdir}/%{name}/*.so.*
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%changelog
* Tue Oct 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.2.50-1.20190403gitdc55edfe5d2f
- Initial spec
