Name:           mp3val
Version:        0.1.8
Release:        1%{?dist}
Summary:        A free software tool to validate and fix MPEG audio files

License:        GPLv2
URL:            http://mp3val.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.gz

Patch01:        mp3val-0.1.8-gcc5.patch

BuildRequires:  gcc-c++


%description
MP3val is a small, high-speed, free software tool for checking MPEG
audio files' integrity. It can be useful for finding corrupted files.
MP3val is also able to fix most of the problems.

%prep
%setup -q -n %{name}-%{version}-src

%{__sed} -i -e 's/\r//' Makefile.* *.cpp *.h

%patch01

%{__sed} -i \
  -e "/^CXXFLAGS/s|-O2|%{optflags}|g" \
  -e '/$(CXX)/s|$(CXXFLAGS)|\0 $(LDFLAGS)|g' \
  Makefile.linux

%build

export LDFLAGS="%{__global_ldflags}"
%make_build -f Makefile.linux

%install
rm -rf $RPM_BUILD_ROOT

%{__mkdir_p} %{buildroot}%{_bindir}
install -pm 0755 %{name} %{buildroot}%{_bindir}/

%files
%license COPYING
%doc changelog.txt manual.html
%{_bindir}/%{name}

%changelog
* Sun Jul 17 2016 Phantom X <megaphantomx at bol dot com dot br> - 0.1.8
- First spec.
