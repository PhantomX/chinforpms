%global smoothver 0.8.74

%global sanitize 0

%global pkgname superfast

Name:           freac-%{pkgname}-codecs
Version:        1.0~pre3
Release:        1%{?dist}
Summary:        SuperFast Codecs for fre:ac

License:        GPLv2
URL:            http://www.freac.org/

%global ver     %(echo %{version} | tr '~' '-' | tr '_' '-')
%if 0%{sanitize}
Source0:        https://github.com/enzo1982/superfast/archive/v%{ver}/%{pkgname}-%{ver}.tar.gz
%else
Source0:        %{pkgname}-%{ver}.tar.xz
%endif
Source1:        Makefile

Patch0:         %{name}-clean.patch

BuildRequires:  gcc-c++
BuildRequires:  freac-cdk-devel
BuildRequires:  smooth-devel >= %{smoothver}

Requires:       freac%{?_isa}


%description
This package provides multi-threaded MP3, Opus and Speex codec drivers for use
with the fre:ac audio converter. The components use multiple instances of the
respective codecs in parallel to provide faster processing on systems with
multiple CPU cores.


%prep
%if 0%{sanitize}
%autosetup -n %{pkgname}-%{ver} -p1
for i in coreaudio faac fdkaac ;do
  rm -rf components/$i
done
%else
%setup -q -n %{pkgname}-%{ver}
%endif

sed -e 's/\r//' -i Readme*

sed -e 's|-L$(prefix)/lib |-L%{_libdir} |g' -i Makefile-commands


%build
%set_build_flags

%make_build \
  prefix=/usr libdir=%{_libdir}


%install

%make_install \
  prefix=/usr libdir=%{_libdir}

chmod +x %{buildroot}%{_libdir}/boca/*.so*


%files
%license COPYING
%doc Readme.md
%{_libdir}/boca/*.so*


%changelog
* Wed Jan 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.0~pre3-1
- Initial spec
