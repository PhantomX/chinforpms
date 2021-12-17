%global commit c2defffca391a865af77146dffe762419066af74
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211217
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           librw
Version:        0
Release:        0.1%{?gver}%{?dist}
Summary:        A re-implementation library of RenderWare graphics

License:        MIT
URL:            https://github.com/aap/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

Patch10:        0001-Add-soversion-to-library.patch


BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glfw3)

Provides:       bundled(glad) = 0.1.34
Provides:       bundled(lodepng) = 20200306


%description
This library is supposed to be a re-implementation of RenderWare graphics, or a
good part of it anyway.
It is intended to be cross-platform in two senses eventually: support rendering
on different platforms similar to RW; supporting all file formats for all
platforms at all times and provide way to convert to all other platforms.


%package        devel
Summary:        Development files for %{name}
Requires:       %{?epoch:%{epoch}:}%{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1


%build
%cmake \
  -DLIBRW_INSTALL:BOOL=ON \
  -DLIBRW_TOOLS:BOOL=OFF \
  -DLIBRW_PLATFORM:STRING=GL3 \
%{nil}

%cmake_build


%install

%cmake_install


%files
%license LICENSE
%doc README.md TODO
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/cmake/%{name}/


%changelog
* Wed Feb 17 2021 Phantom X <megaphantomx at hotmail dot com> - 0-0.1.20211217gitc2defff
- Initial spec

