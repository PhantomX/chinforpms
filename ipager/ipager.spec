%global aur_id cb0836507606ad791c007460f70d0db075f5f248
%global aur_git https://aur.archlinux.org/cgit/aur.git/plain/

Name:           ipager
Version:        1.1.0
Release:        3%{?dist}
Summary:        A themable desktop pager for fluxbox and other WMs

License:        MIT
URL:            http://www.useperl.ru/ipager/index.en.html
Source0:        https://slackware.uk/slacky/slackware-13.0/desktop/ipager/1.1.0/src/%{name}-%{version}.tar.gz

Patch0:         %{aur_git}/%{name}-1.1.0-20120429.patch?h=%{name}&id=%{aur_id}#/%{name}-1.1.0-20120429.patch
Patch1:         %{aur_git}/%{name}-1.1.0-20190902.patch?h=%{name}&id=%{aur_id}#/%{name}-1.1.0-20190902.patch
Patch2:         %{name}-env_flags.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  scons
BuildRequires:  pkgconfig(imlib2)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xmu)


%description
ipage' is a simple pager.


%prep
%autosetup

sed \
  -e "/^ipager_env.Append($/a\        LINKFLAGS = [ '-fPIC', '-pie' ]," \
  -e "s|'/usr/lib'|'%{_libdir}'|g" \
  -e 's|imlib2-config --cflags --libs|pkg-config imlib2 --cflags --libs|g' \
  -e 's|imlib2-config|true|g' \
  -i SConstruct

%build
unset CC
unset CXX
scons %{?_smp_mflags} \
  --cache-disable \
  PREFIX="%{_prefix}" \
  xinerama=true

%install
%set_build_flags
unset CC
unset CXX
scons \
  --cache-disable \
  PREFIX="%{_prefix}" \
  xinerama=true \
  DESTDIR="%{buildroot}" \
  install


%files
%license LICENSE
%doc README
%{_bindir}/%{name}


%changelog
* Sat Sep 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1.1.0-3
- Remove all imlib2-config references

* Sat Oct 03 2020 Phantom X <megaphantomx at hotmail dot com> - 1.1.0-2
- Unset compiler variables to please scons bullshit

* Wed May 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.1.0-1
- Initial spec
