%global smoothver 0.8.74

%global codec   faac fdkaac

%global pkgname superfast

Name:           freac-%{pkgname}-codecs-freeworld
Version:        1.0~pre3
Release:        1%{?dist}
Summary:        SuperFast Codecs for fre:ac - freeworld

License:        GPLv2
URL:            http://www.freac.org/

%global ver     %(echo %{version} | tr '~' '-' | tr '_' '-')
Source0:        https://github.com/enzo1982/superfast/archive/v%{ver}/%{pkgname}-%{ver}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  freac-cdk-devel
BuildRequires:  smooth-devel >= %{smoothver}

Requires:       freac-%{pkgname}-codecs%{?_isa} = %{version}
Requires:       freac%{?_isa}


%description
This package provides multi-threaded AAC codec drivers for use with the fre:ac
audio converter. The components use multiple instances of the respective codecs
in parallel to provide faster processing on systems with multiple CPU cores.


%prep
%autosetup -n %{pkgname}-%{ver} -p1

sed -e 's/\r//' -i Readme*

sed -e 's|-L$(prefix)/lib |-L%{_libdir} |g' -i Makefile-commands


%build
export CFLAGS="%{build_cflags}"
export CXXFLAGS="%{build_cxxflags}"
export LDFLAGS="%{build_ldflags}"

for i in %{codec} ;do
%make_build -C components/$i \
  prefix=/usr libdir=%{_libdir}
done


%install
for i in %{codec} ;do
%make_install -C components/$i \
  prefix=/usr libdir=%{_libdir}
done

chmod +x %{buildroot}%{_libdir}/boca/*.so*


%files
%license COPYING
%doc Readme.md
%{_libdir}/boca/*.so*


%changelog
* Wed Jan 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.0~pre3-1
- Initial spec
