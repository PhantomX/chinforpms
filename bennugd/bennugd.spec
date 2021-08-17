%global date 20190530
%global snapshot_rev 353

%global sver .%{date}svn%{snapshot_rev}

Name:           bennugd
Version:        1.0.0
Release:        1%{?sver}%{?dist}
Summary:        A programming language to create games.

License:        zlib
URL:            https://www.bennugd.org

# To regenerate a snapshot:
# Use your regular webbrowser to open https://sourceforge.net/p/bennugd/code/r%%{snapshot_rev}/tarball
# This triggers the SourceForge instructure to generate a snapshot
# After that you can pull in the archive with:
# spectool -g bennugd.spec
Source0:        https://sourceforge.net/code-snapshots/svn/b/be/%{name}/code/%{name}-code-r%{snapshot_rev}.zip

Patch0:         0001-fix-build-flags.patch
Patch1:         0001-Versioned-libraries.patch
Patch2:         0001-Hardcode-modules-path.patch
Patch3:         0001-libdraw-staticinline.patch

ExclusiveArch:  %{ix86}

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(sdl)
BuildRequires:  pkgconfig(SDL_mixer)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(zlib)
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
Bennugd is a programming language to create games.


%package libs
Summary:        %{summary}
Provides:       %{name}-modules = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-modules%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%global __provides_exclude_from ^%{_libdir}/%{name}/modules/*.*\\.so$
%global __requires_exclude ^lib(blit|draw|font|grbase|joy|key|render|scroll|text|video).so$


%description libs
The %{name}-libs package contains the dynamic libraries and modules
needed for %{name}.


%prep
%autosetup -n %{name}-code-r%{snapshot_rev} -p1

sed \
  -e 's|_RPMLIBDIR_|%{_libdir}/%{name}|g' \
  -i core/bgdc/src/c_main.c core/bgdrtm/src/sysprocs.c

for i in core modules tools/moddesc ;do
  pushd $i
    autoreconf -ivf
  popd
done


%build
for i in core modules tools/moddesc ;do
  pushd $i
  chmod +x configure

  CFLAGS="%{build_cflags} -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE" \
  %configure \
%ifarch %{ix86}
    --build=i686-redhat-linux \
%endif
  %{nil}

  sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
  sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

  popd
done

for i in core modules tools/moddesc ;do
  %make_build -C $i
done


%install
for i in core modules tools/moddesc ;do
  %make_install -C $i
done

find %{buildroot} -name '*.la' -delete

rm -f %{buildroot}%{_libdir}/libbgdrtm.so
rm -f %{buildroot}%{_libdir}/libbgload.so
rm -f %{buildroot}%{_libdir}/libdraw.so

mv %{buildroot}%{_bindir}/moddesc %{buildroot}%{_bindir}/bgmoddesc

mkdir -p %{buildroot}%{_libdir}/%{name}/modules
mv %{buildroot}%{_libdir}/*.so %{buildroot}%{_libdir}/%{name}/modules/
ln -s ../../libdraw.so.0 %{buildroot}%{_libdir}/%{name}/modules/libdraw.so


%files
%license core/COPYING
%doc core/README
%{_bindir}/bg*

%files libs
%license modules/COPYING
%doc modules/README
%{_libdir}/*.so.*
%{_libdir}/%{name}/modules/*.so


%changelog
* Mon Aug 16 2021 Phantom X - 1.0.0-1.20190530svn353
- Initial spec
