%global commit b0fa2cec0bb28bd68c4060e4bdf91fe2bcdb8776
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220312
%global with_snapshot 1

%global commit1 51edeb63ec3f456f4950922c5011c326a062fbce
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 libmd5

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global md5_ver 1.6

%global pkgname HDiffPatch

%global vermajor %%(echo %{version} | cut -d. -f2-)
%global verminor %%(echo %{version} | cut -d. -f1)

Name:           hdiffpatch
Version:        4.1.2
Release:        1%{?gver}%{?dist}
Summary:        Command-line tools for Diff & Patch between binary files or directories

License:        MIT
URL:            https://github.com/sisong/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        https://github.com/sisong/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz

Patch0:         0001-Makefile-package-build-fixes.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(libzstd) >= 1.5.0
BuildRequires:  pkgconfig(lzmasdk-c)
BuildRequires:  pkgconfig(zlib)
Requires:       lib%{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(md5-deutsch) = %{md5_ver}

%description
HDiffPatch is a C\C++ library and command-line tools for Diff & Patch between
binary files or directories; cross-platform; run fast; create small 
delta/differential; support large files and limit memory requires when
diff & patch.

%package -n lib%{name}
Summary:        A library for Diff & Patch between binary files or directories
Provides:       bundled(md5-deutsch) = %{md5_ver}

%description -n lib%{name}
The lib%{name} package contains the dynamic libraries needed for %{name}.

%package -n lib%{name}-devel
Summary:        %{summary} development files
Requires:       lib%{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n lib%{name}-devel
The lib%{name}-devel package contains the development files libraries for
lib%{name} usage.


%prep
%autosetup -n %{pkgname}-%{?gver:%{commit}}%{!?gver:%{version}} -p1

mkdir libmd5
tar -xf %{S:1} -C libmd5 --strip-components 1

sed \
  -e 's|_RPM_MINOR_|%{verminor}|g' \
  -e 's|_RPM_MAJOR_|%{vermajor}|g' \
  -i Makefile

cat > lib%{name}.pc <<'EOF'
prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: %{name}
Description: Library for Diff & Patch between binary files or directories
Version: %{version}
Requires.private: bzip2 libzstd lzmasdk-c zlib
Cflags: -I${includedir}/%{pkgname}
Libs: -L${libdir} -l%{name}
EOF


%build
%set_build_flags
%make_build


%install
%make_install BINDIR=%{_bindir} LIBDIR=%{_libdir} INCDIR=%{_includedir}

mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -pm0644 lib%{name}.pc %{buildroot}%{_libdir}/pkgconfig/


%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/hdiffz
%{_bindir}/hpatchz

%files -n lib%{name}
%license LICENSE
%{_libdir}/lib%{name}.so.*

%files -n lib%{name}-devel
%{_includedir}/%{pkgname}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc


%changelog
* Thu Mar 17 2022 Phantom X <megaphantomx at hotmail dot com> - 4.1.2-1.20220312gitb0fa2ce
- Initial spec