%global aur_id cb0836507606ad791c007460f70d0db075f5f248
%global aur_git https://aur.archlinux.org/cgit/aur.git/plain/

Name:           ipager
Version:        1.1.0
Release:        1%{?dist}
Summary:        A themable desktop pager for fluxbox and other WMs

License:        MIT
URL:            http://www.useperl.ru/ipager/index.en.html
Source0:        https://gentoo.osuosl.org/distfiles/%{name}-%{version}.tar.gz

Patch0:         %{aur_git}/%{name}-1.1.0-20120429.patch?h=%{name}&id=%{aur_id}#/%{name}-1.1.0-20120429.patch
Patch1:         %{aur_git}/%{name}-1.1.0-20190902.patch?h=%{name}&id=%{aur_id}#/%{name}-1.1.0-20190902.patch
Patch2:         %{name}-env_flags.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  scons
BuildRequires:  pkgconfig(imlib2)
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
  -i SConstruct

%build
%set_build_flags
scons %{?_smp_mflags} \
  --cache-disable \
  PREFIX="%{_prefix}" \
  xinerama=true

%install
%set_build_flags
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
* Wed May 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.1.0-1
- Initial spec
