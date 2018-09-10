%global gitcommitid ade83733715d07dea6cf9324f59b6265c91662b8
%global shortcommit %(c=%{gitcommitid}; echo ${c:0:7})
%global date 20150729
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           steamwm
Version:        0
Release:        0.1%{?gver}%{?dist}
Summary:        Various window management fixes for the Linux Steam client

License:        WTFPL
URL:            https://github.com/dscharrer/steamwm

ExclusiveArch:  x86_64 i686

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{gitcommitid}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif
Source1:        http://sam.zoy.org/wtfpl/COPYING
Source2:        %{name}

BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  libX11-devel
BuildRequires:  libstdc++-static
Requires:       steam
%ifarch x86_64
Requires:       %{name}(x86-32) = %{version}-%{release}
%endif


%description
steamwm fixes various window management for the Linux Steam client.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{gitcommitid}
%else
%autosetup -n %{name}-%{version}
%endif

cp %{S:1} COPYING
touch -r README.md COPYING

chmod -x noframe.patch %{name}.cpp

sed -n -e '3,35p' %{name}.cpp | sed -re 's,^#//(| ),,g' %{name}.cpp > README.run
touch -r README.md README.run

%build
g++ %{build_cxxflags} -shared -fPIC -x c++ %{name}.cpp -o %{name}.so \
  %{build_ldflags} -lX11 -static-libgcc -static-libstdc++ -DSONAME=%{name}.so


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{S:2} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_libdir}/%{name}
install -pm0755 %{name}.so %{buildroot}%{_libdir}/%{name}/%{name}.so


%files
%license COPYING
%doc README.md README.run noframe.patch
%{_bindir}/%{name}
%{_libdir}/%{name}/%{name}.so


%changelog
* Fri Aug 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-0.1.20150729gitade8373
- Initial spec
