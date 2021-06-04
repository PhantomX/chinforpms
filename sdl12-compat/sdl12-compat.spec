%global commit ebcbb11caf34f5ee99377a8da4c98f9770c694b8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210519
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           sdl12-compat
Version:        1.2.50
Release:        2%{?gver}%{?dist}
Summary:        SDL 1.2 runtime compatibility library using SDL 2.0

License:        zlib and MIT
URL:            https://github.com/libsdl-org/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif


BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(sdl2)


%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio device.

This code is a compatibility layer; it provides a binary-compatible API for
programs written against SDL 1.2, but it uses SDL 2.0 behind the scenes.

If you are writing new code, please target SDL 2.0 directly and do not use
this layer.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif


%build
%cmake
%cmake_build


%install
%cmake_install

rm -fv %{buildroot}%{_libdir}/*.so

mkdir -p %{buildroot}%{_libdir}/%{name}
mv %{buildroot}%{_libdir}/*.so.* %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/%{name}" \
  > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%files
%license LICENSE.txt
%doc BUGS.txt README.md
%{_libdir}/%{name}/*.so.*
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%changelog
* Sun May 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.50-2.20210519gitebcbb11
- Bump

* Tue Oct 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.2.50-1.20190403gitdc55edfe5d2f
- Initial spec