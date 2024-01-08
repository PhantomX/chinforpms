%global date 20211122
%global snapshot_rev 356

%global dist .%{date}svn%{snapshot_rev}%{?dist}

Name:           bennugd
Version:        1.0.0
Release:        4%{?dist}
Summary:        A programming language to create games

License:        Zlib
URL:            https://www.bennugd.org

# To regenerate a snapshot:
# Use your regular webbrowser to open https://sourceforge.net/p/bennugd/code/%%{snapshot_rev}/tarball
# This triggers the SourceForge instructure to generate a snapshot
# After that you can pull in the archive with:
# spectool -g bennugd.spec
Source0:        https://sourceforge.net/code-snapshots/svn/b/be/%{name}/code/%{name}-code-r%{snapshot_rev}.zip

Patch0:         0001-fix-build-flags.patch
Patch1:         0001-Versioned-libraries.patch
Patch2:         0001-Hardcode-modules-path.patch
Patch3:         0001-mod_wm-disable-gr_set_icon.patch

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
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
Bennugd is a programming language to create games.


%package libs
Summary:        %{summary} - libraries
Provides:       %{name}-modules = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-modules%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%global __provides_exclude_from ^%{_libdir}/%{name}/modules/*.*\\.so$
%global __requires_exclude ^lib(blit|draw|font|grbase|joy|key|render|scroll|text|video)\\.so$


%description libs
The %{name}-libs package contains the dynamic libraries and modules
needed for %{name}.


%prep
%autosetup -n %{name}-code-r%{snapshot_rev} -N -p1

find \( -name '*.c*' -or -name '*.h*' \) -exec sed -i 's/\r$//' {} \;

%autopatch -p1

for file in */COPYING */README ; 
do
  sed 's/\r//' -i ${file}
  iconv -f iso8859-1 -t utf-8 ${file} -o ${file}.conv && mv -f ${file}.conv ${file}
done;

sed \
  -e 's|_RPMLIBDIR_|%{_libdir}/%{name}|g' \
  -i core/bgdc/src/c_main.c core/bgdrtm/src/sysprocs.c

sed -e '/LDFLAGS/s| -s | |g' -i core/*/src/Makefile.am modules/*/Makefile.am

for i in core modules tools/moddesc ;do
  pushd $i
    autoreconf -ivf
  popd
done


%build
%set_build_flags
export CFLAGS+=" -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE"
for i in core modules tools/moddesc ;do
  pushd $i
  chmod +x configure

  %configure \
%ifarch %{ix86}
    --build=i686-redhat-linux \
%endif
  %{nil}

  sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
  sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
  # Dirty fix to old libtool issues
  sed -i -e "s! -shared ! $LDFLAGS\0!g" libtool

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
rm -f %{buildroot}%{_libdir}/libblit.so
rm -f %{buildroot}%{_libdir}/libdraw.so
rm -f %{buildroot}%{_libdir}/libgrbase.so

mv %{buildroot}%{_bindir}/moddesc %{buildroot}%{_bindir}/bgmoddesc

mkdir -p %{buildroot}%{_libdir}/%{name}/modules
mv %{buildroot}%{_libdir}/*.so %{buildroot}%{_libdir}/%{name}/modules/

# Dirty hack to fix module loading
for i in blit draw grbase; do
  ln -s ../../lib${i}.so.0 %{buildroot}%{_libdir}/%{name}/modules/lib${i}.so
done


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
* Sun Jan 07 2024 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-4.20211122svn356
- Remove strip from LDFLAGS

* Tue May 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-3.20211122svn356
- Add patch to fix sdl12-compat support

* Tue Aug 17 2021 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-2.20190530svn353
- Fix some rpmlint issues

* Mon Aug 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-1.20190530svn353
- Initial spec
