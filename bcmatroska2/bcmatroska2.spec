Name:           bcmatroska2
Version:        0.23
Release:        1%{?dist}
Summary:        C Library to Deal with Matroska Files

License:        GPLv2
URL:            https://www.linphone.org
Source0:        https://www.linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz
Source1:        https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt#/gpl-2.0

BuildRequires:  cmake
BuildRequires:  gcc

%description
%{summary}.

%package devel
Summary:        Development libraries for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description devel
%{summary}.

Development files.


%prep
%autosetup

cp %{SOURCE1} COPYING

%build
mkdir builddir
pushd builddir
%cmake .. \
  -DCMAKE_INSTALL_INCLUDEDIR:PATH=/usr/include/%{name} \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DENABLE_STATIC:BOOL=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON

%make_build

popd

%install

%make_install -C builddir


%files
%license COPYING
%{_libdir}/lib%{name}.so.*

%files devel
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}
%{_datadir}/%{name}/cmake/*.cmake


%changelog
* Fri Sep 22 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.23-1
- Initial spec
