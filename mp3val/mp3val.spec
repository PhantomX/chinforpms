Name:           mp3val
Version:        0.1.8
Release:        1%{?dist}
Summary:        A free software tool to validate and fix MPEG audio files

License:        GPL-2.0-only
URL:            http://mp3val.sourceforge.net/

Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.gz

Patch01:        mp3val-0.1.8-gcc5.patch

BuildRequires:  make
BuildRequires:  gcc-c++


%description
MP3val is a small, high-speed, free software tool for checking MPEG
audio files' integrity. It can be useful for finding corrupted files.
MP3val is also able to fix most of the problems.

%prep
%autosetup -n %{name}-%{version}-src -N

%{__sed} -i -e 's/\r//' Makefile.* *.cpp *.h

%autopatch

%{__sed} -i \
  -e "s|^CXXFLAGS=|CXXFLAGS?=|g" \
  -e '/$(CXX)/s|$(CXXFLAGS)|\0 $(LDFLAGS)|g' \
  Makefile.linux

%build
%set_build_flags
%make_build -f Makefile.linux

%install
mkdir -p %{buildroot}%{_bindir}
install -pm 0755 %{name} %{buildroot}%{_bindir}/

%files
%license COPYING
%doc changelog.txt manual.html
%{_bindir}/%{name}

%changelog
* Sun Jul 17 2016 Phantom X <megaphantomx at bol dot com dot br> - 0.1.8
- First spec.
