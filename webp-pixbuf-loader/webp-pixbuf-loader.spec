%global gitcommitid 9b92950d49d7939f90ba7413deb7ec6b392b2054
%global shortcommit %(c=%{gitcommitid}; echo ${c:0:7})
%global date 20160328
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global         loaders_dir %(pkg-config --variable gdk_pixbuf_moduledir gdk-pixbuf-2.0)

Name:           webp-pixbuf-loader
Version:        0
Release:        2%{?gver}%{?dist}
Summary:        WebM GDK Pixbuf Loader library

License:        LGPLv2+
URL:            https://github.com/aruiz/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{gitcommitid}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif
Source1:        https://www.gnu.org/licenses/old-licenses/lgpl-2.0.txt#/lgpl-2.0

Patch0:         %{name}-nowrite.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= 2.22
BuildRequires:  pkgconfig(libwebp) >= 0.4.3

Requires:       gdk-pixbuf2%{?_isa}


%description
%{summary}.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{gitcommitid} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

cp -p %{S:1} COPYING

sed \
  -e 's|${INSTALL_LIB_DIR}/gdk-pixbuf-2.0/${GDK_PIXBUF_BINARY_VERSION}/loaders|%{loaders_dir}|g' \
  -i CMakeLists.txt

%build
mkdir build
pushd build
%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON

%make_build

popd


%install
%make_install -C build


%files
%license COPYING
%doc README
%{loaders_dir}/*.so


%changelog
* Sat Sep 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-2.20160328git9b92950
- Disable write support, applications are crashing on image files writing
- Fix snapshot build tag

* Sat Sep 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-1.20160328git9b92950
- Initial spec
