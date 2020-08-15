%global commit 3489a85fbf86e9d4ef5e42a6cdf9ec5dd649e50b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200614
%global with_snapshot 1

%ifnarch %{ix86} ppc64 s390x
%global build_with_pgo    1
%endif

%ifarch x86_64
%global build_with_lto    1
%endif

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname Flips

Name:           flips
Version:        1.40
Release:        2%{?gver}%{?dist}
Summary:        A patcher for IPS and BPS files

License:        GPLv3+
URL:            https://github.com/Alcaro/Flips

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif

BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(gtk+-3.0)
Requires:       hicolor-icon-theme

Provides:       bundled(libdivsufsort) = 2.0.1


%description
Floating IPS (or Flips) is a patcher for IPS and BPS files, aiming for a simple
interface yet plenty of power under the hood.

This packages provides the GTK+ frontend.


%package gtk
Summary:        A patcher for IPS and BPS files (GTK+ frontend)
Requires:       hicolor-icon-theme
Provides:       bundled(libdivsufsort) = 2.0.1

%description gtk
Floating IPS (or Flips) is a patcher for IPS and BPS files, aiming for a simple
interface yet plenty of power under the hood.

This packages provides the GTK+ frontend.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

sed \
  -e 's|<binary>flips</binary>|<binary>%{name}-gtk</binary>|' \
  -i data/com.github.Alcaro.%{pkgname}.metainfo.xml


%build
RPM_CXX_FLAGS="%{build_cxxflags}"
# make.sh flags
RPM_CXX_FLAGS+=" -fomit-frame-pointer -fmerge-all-constants -fvisibility=hidden"
RPM_CXX_FLAGS+=" -fno-exceptions -fno-unwind-tables -fno-asynchronous-unwind-tables"
RPM_CXX_FLAGS+=" -ffunction-sections -fdata-sections -Wl,--gc-sections"

%if 0%{?build_with_lto}
RPM_CXX_FLAGS="$(echo ${RPM_CXX_FLAGS} | sed -e 's/-O2\b/-O3/')"
RPM_CXX_FLAGS+=" -flto=%{_smp_build_ncpus} -fuse-linker-plugin"
%endif

%if 0%{?build_with_pgo}
RPM_PGOGEN_FLAGS="-fprofile-generate -lgcov"
RPM_PGOUSE_FLAGS="-fprofile-use"
export OMP_NUM_THREADS=1
RPM_CXX_FLAGS+=" -fprofile-dir=obj/"
%endif

export CXX=g++
export CFLAGS=""
export RPM_CXX_FLAGS
export LFLAGS="%{build_ldflags} $RPM_CXX_FLAGS"

unset DISPLAY

run_make(){
rm -rf obj/* %{name}-$1
%make_build TARGET=$1 FNAME_cli=%{name}-cli FNAME_gtk=%{name}-gtk CXXFLAGS="$RPM_CXX_FLAGS $RPM_PGOGEN_FLAGS"

%if 0%{?build_with_pgo}
./%{name}-$1 --create --bps-delta profile/firefox-10.0esr.tar profile/firefox-17.0esr.tar /dev/null
./%{name}-$1 --create --bps-delta-moremem profile/firefox-10.0esr.tar profile/firefox-17.0esr.tar /dev/null
rm -f %{name}-$1
%make_build TARGET=$1 FNAME_cli=%{name}-cli FNAME_gtk=%{name}-gtk CXXFLAGS="$RPM_CXX_FLAGS $RPM_PGOUSE_FLAGS"
%endif
}

run_make cli
run_make gtk

%install
%make_install TARGET=gtk FNAME_gtk=%{name}-gtk

install -pm0755 %{name}-cli %{buildroot}%{_bindir}/%{name}

desktop-file-edit \
  --set-key=Exec \
  --set-value="%{name}-gtk" \
  --remove-category=GNOME \
  --remove-category=GTK \
  --remove-category=RevisionControl \
  %{buildroot}%{_datadir}/applications/com.github.Alcaro.%{pkgname}.desktop

rm -rf %{buildroot}%{_datadir}/icons/hicolor/symbolic

desktop-file-validate %{buildroot}%{_datadir}/applications/com.github.Alcaro.%{pkgname}.desktop

appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/com.github.Alcaro.%{pkgname}.metainfo.xml


%files
%license COPYING*
%doc README.md bps_spec.md
%{_bindir}/%{name}


%files gtk
%license COPYING*
%{_bindir}/%{name}-gtk
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*%{pkgname}*
%{_metainfodir}/*.metainfo.xml


%changelog
* Sat Aug 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1.40-2.20200614git3489a85
- New snapshot

* Mon May 25 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.40-1.20200426gita218454
- Initial spec
