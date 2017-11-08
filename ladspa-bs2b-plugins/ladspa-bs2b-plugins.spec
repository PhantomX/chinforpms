%global srcname0 ladspa-bs2b

Name:           %{srcname0}-plugins
Version:        0.9.1
Release:        1%{?dist}
Summary:        Bauer stereophonic-to-binaural DSP effect LADSPA plugin

License:        GPLv2
URL:            http://bs2b.sourceforge.net
Source0:        https://downloads.sourceforge.net/bs2b/%{srcname0}-%{version}.tar.gz

BuildRequires:  ladspa-devel
BuildRequires:  pkgconfig(libbs2b)
Requires:       ladspa

Provides:       %{srcname0} = %{version}-%{release}

%description
%{summary}

%prep
%autosetup -n %{srcname0}-%{version}


%build
%configure
%make_build


%install
%make_install

find %{buildroot}%{_libdir} -name '*.la' -delete

%files
%license COPYING
%doc AUTHORS
%{_libdir}/ladspa/*.so


%changelog
* Tue Nov 07 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.1-1
- Initial spec
