%define _legacy_common_support 1

%define LIBSTDCXXDATE 20040818
%define DATE 20040701
%define gcc_version 3.2.3
%define gcc_release 68
%define _unpackaged_files_terminate_build 0
%define multilib_64_archs sparc64 ppc64 s390x x86_64
%define build_java 0
%define _default_patch_fuzz 2
%ifarch s390x
%define multilib_32_arch s390
%endif
%ifarch sparc64
%define multilib_32_arch sparc
%endif
%ifarch ppc64
%define multilib_32_arch ppc
%endif
%ifarch x86_64
%define multilib_32_arch i386
%endif

# No time to fix debug proper packaging
%ifarch %{ix86}
%global debug_package %{nil}
%global __strip /bin/true
%endif

Summary:        The compatibility GNU Compiler Collection
Name:           compat-gcc-32
Version:        %{gcc_version}
Release:        %{gcc_release}.16%{?dist}.8

License:        GPLv2+ with exceptions
URL:            http://gcc.gnu.org

Source0:        https://dl.bintray.com/phantomx/tarballs/gcc-%{gcc_version}-%{DATE}.tar.bz2
Source2:        https://dl.bintray.com/phantomx/tarballs/libstdc++-3.3.4-%{LIBSTDCXXDATE}.tar.bz2
Source3:        dummylib.sh

ExcludeArch:    %{arm} aarch64 ppc64le

# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# Need .weakref support
BuildRequires:  gcc
BuildRequires:  binutils >= 2.16.91.0.5-1
BuildRequires:  zlib-devel, gettext, dejagnu, bison, flex, texinfo
# Make sure pthread.h doesn't contain __thread tokens
BuildRequires:  glibc-devel >= 2.2.90-12, glibc-static
BuildRequires:  %{_prefix}/share/i18n/locales/de_DE
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need .weakref support
Requires: binutils >= 2.16.91.0.5-1
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires:       glibc-devel >= 2.2.90-12
Requires:       libgcc >= 3.4.0
%ifarch %{multilib_64_archs} sparc sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires:  /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
Provides:       bundled(libiberty)

Patch1:         gcc32-multi32-hack.patch
Patch2:         gcc32-ice-hack.patch
Patch3:         gcc32-ppc64-m32-m64-multilib-only.patch
Patch4:         gcc32-bison-1.875c.patch
Patch5:         gcc32-i386-prefetch-sse.patch
Patch6:         gcc32-convert-move.patch
Patch7:         gcc32-libjava-jar-timestamps.patch
Patch8:         gcc32-c++-friend-templ-member.patch
Patch9:         gcc32-c++-scope-nesting.patch
Patch10:        gcc32-libstdc++-symver.patch
Patch11:        gcc32-java-intlex.patch
Patch12:        gcc32-java-nan.patch
Patch13:        gcc32-dwarf2-pruning-keep-spec.patch
Patch14:        gcc32-java-bytecode.patch
Patch15:        gcc32-pr3581.patch
Patch16:        gcc32-libstdc++-limits.patch
Patch17:        gcc32-ppc64-crtsavres.patch
Patch18:        gcc32-s390-reload-dup.patch
Patch19:        gcc32-ppc-altivec-ap.patch
Patch20:        gcc32-ppc-mpowerpc64.patch
Patch21:        gcc32-null-pointer-check-noncc0.patch
Patch22:        gcc32-ppc-movdi_internal64.patch
Patch23:        gcc32-c++-reregister-specialization.patch
Patch24:        gcc32-c++-pr7566.patch
Patch25:        gcc32-c++-pass-by-invisible-ref.patch
Patch26:        gcc32-c++-unitialized-self-ref.patch
Patch27:        gcc32-tablejump-cleanup.patch
Patch28:        gcc32-libstdc++-fully-dynamic-strings.patch
Patch29:        gcc32-Winline-doc.patch
Patch30:        gcc32-ia64-expand_load_address.patch
Patch31:        gcc32-demangle-pr16240.patch
Patch32:        gcc32-debug-cdtor.patch
Patch33:        gcc32-cxa_demangle-ambiguity.patch
Patch34:        gcc32-c++-pr10558.patch
Patch35:        gcc32-libstdc++-pr9659.patch
Patch36:        gcc32-libstdc++-symver2.patch
Patch37:        gcc32-pr19005.patch
Patch38:        gcc32-rh149250.patch
Patch39:        gcc32-rh156185.patch
Patch40:        gcc32-rh156291.patch
Patch41:        gcc32-pr18300.patch
Patch42:        gcc32-gnuc-rh-release.patch
Patch43:        gcc32-weakref.patch
Patch44:        gcc32-pr13106.patch
Patch45:        gcc32-ppc64-stack-boundary.patch
Patch46:        gcc32-pr12799.patch
Patch47:        gcc32-pr13041.patch
Patch48:        gcc32-pr26208.patch
Patch49:        gcc32-rh173224.patch
Patch50:        gcc32-rh180778.patch
Patch51:        gcc32-rh181894.patch
Patch52:        gcc32-rh186252.patch
Patch53:        gcc32-pr26208-workaround.patch
Patch54:        gcc32-libgcc_eh-hidden.patch
Patch55:        gcc32-java-zoneinfo.patch
Patch56:        gcc32-CVE-2006-3619.patch
Patch57:        gcc32-rh226706.patch

Patch60:        gcc32-obstack-lvalues.patch
Patch61:        gcc32-fc4-compile.patch
Patch62:        gcc32-s390x-compile.patch
Patch63:        gcc32-bison.patch

Patch100:       compat-libstdc++33-incdir.patch
Patch101:       compat-libstdc++33-limits.patch
Patch102:       compat-libstdc++33-symver.patch
Patch103:       compat-libstdc++33-v3.patch
Patch104:       compat-libstdc++33++-fully-dynamic-strings.patch
Patch105:       compat-libstdc++33++-symver2.patch
Patch106:       compat-libstdc++33-cxa_demangle-ambiguity.patch
Patch107:       compat-libstdc++33-ldbl.patch

# MDK patches
Patch202:       gcc31-c++-diagnostic-no-line-wrapping.patch
Patch203:       gcc32-pr7434-testcase.patch
Patch204:       gcc33-pr8213-testcase.patch
Patch206:       gcc33-x86_64-biarch-testsuite.patch
Patch214:       gcc32-mklibgcc-serialize-crtfiles.patch
Patch215:       gcc33-c++-classfn-member-template.patch
Patch219:       gcc33-pr11631.patch
Patch220:       gcc33-pr13179.patch

# openSUSE patches
# (blino) edited to drop rs600 part
Patch301:       gcc-unwind-glibc216.patch

Patch401:       ucontext.patch

Patch500:       gcc33-pr6387.patch


%define _gnu    %{nil}

%ifarch sparc sparcv9
%define gcc_target_platform sparc64-%{_vendor}-linux
%endif
%ifarch ppc
%define gcc_target_platform ppc64-%{_vendor}-linux
%endif
%ifnarch sparc sparcv9 ppc
%define gcc_target_platform %{_target_cpu}-%{_vendor}-linux
%endif

%description
This package includes a GCC 3.2.3-RH compatibility compiler.

%package -n compat-libstdc++-33
Summary: Compatibility standard C++ libraries
Obsoletes:      compat-libstdc++ < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      compat-gcc-32 < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      compat-gcc-32-c++ < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      compat-gcc-32-g77 < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n compat-libstdc++-33
The compat-libstdc++ package contains compatibility standard C++ library
from GCC 3.3.4.

%prep
%setup -q -n gcc-%{gcc_version}-%{DATE} -a2
mv gcc-3.3.4-%{LIBSTDCXXDATE}/libstdc++-v3 libstdc++33-v3
%ifarch sparc ppc
#%patch1 -p0 -b .multi32-hack~
%endif
%patch2 -p0 -b .ice-hack~
%patch3 -p0 -b .ppc64-m32-m64-multilib-only~
%patch4 -p0 -b .bison-1.875c~
%patch5 -p0 -b .i386-prefetch-sse~
%patch6 -p0 -b .convert-move~
%patch7 -p0 -b .libjava-jar-timestamps~
%patch8 -p0 -b .c++-friend-templ-member~
#%patch9 -p0 -b .c++-scope-nesting~
%patch10 -p0 -b .libstdc++-symver~
%patch11 -p0 -b .java-intlex~
%patch12 -p0 -b .java-nan~
%patch13 -p0 -b .dwarf2-pruning-keep-spec~
%patch14 -p0 -b .java-bytecode~
%patch15 -p0 -b .pr3581~
%patch16 -p0 -b .libstdc++-limits~
%patch17 -p0 -b .ppc64-crtsavres~
%patch18 -p0 -b .s390-reload-dup~
%patch19 -p0 -b .ppc-altivec-ap~
%patch20 -p0 -b .ppc-mpowerpc64~
%patch21 -p0 -b .null-pointer-check-noncc0~
%patch22 -p0 -b .ppc-movdi_internal64~
%patch23 -p0 -b .c++-reregister-specialization~
%patch24 -p0 -b .c++-pr7566~
%patch25 -p0 -b .c++-pass-by-invisible-ref~
%patch26 -p0 -b .c++-unitialized-self-ref~
%patch27 -p0 -b .tablejump-cleanup~
%patch28 -p0 -b .libstdc++-fully-dynamic-strings~
%patch29 -p0 -b .Winline-doc~
%patch30 -p0 -b .ia64-expand_load_address~
%patch31 -p0 -b .demangle-pr16240~
%patch32 -p0 -b .debug-cdtor~
%patch33 -p0 -b .cxa_demangle-ambiguity~
%patch34 -p0 -b .c++-pr10558~
%patch35 -p0 -b .libstdc++-pr9659~
%patch36 -p0 -b .libstdc++-symver2~
%patch37 -p0 -b .pr19005~
%patch38 -p0 -b .rh149250~
%patch39 -p0 -b .rh156185~
%patch40 -p0 -b .rh156291~
%patch41 -p0 -b .pr18300~
%patch42 -p0 -b .gnuc-rh-release~
%patch43 -p0 -b .weakref~
%patch44 -p0 -b .pr13106~
%patch45 -p0 -b .ppc64-stack-boundary~
%patch46 -p0 -b .pr12799~
%patch47 -p0 -b .pr13041~
%patch48 -p0 -b .pr26208~
%patch49 -p0 -b .rh173224~
%patch50 -p0 -b .rh180778~
%patch51 -p0 -b .rh181894~
%patch52 -p0 -b .rh186252~
%patch53 -p0 -b .pr26208-workaround~
%patch54 -p0 -b .libgcc_eh-hidden~
%patch55 -p0 -b .java-zoneinfo~
%patch56 -p0 -b .CVE-2006-3619~
%patch57 -p0 -b .rh226706~

%patch60 -p0 -b .obstack-lvalues~
%patch61 -p0 -b .fc4-compile~
%patch62 -p0 -b .s390x-compile~
%patch63 -p0 -b .bison~

%patch100 -p0 -b .compat-libstdc++33-incdir~
%patch101 -p0 -b .compat-libstdc++33-limits~
%patch102 -p0 -b .compat-libstdc++33-symver~
%patch103 -p0 -b .compat-libstdc++33-v3~
%patch104 -p0 -b .compat-libstdc++33++-fully-dynamic-strings~
%patch105 -p0 -b .compat-libstdc++33++-symver2~
%patch106 -p0 -b .compat-libstdc++33-cxa_demangle-ambiguity~
%patch107 -p0 -b .compat-libstdc++33-ldbl.patch~

# MDK patches
%patch202 -p1 -b .c++-diagnostic-no-line-wrapping
%patch203 -p1 -b .pr7434-testcase
%patch204 -p1 -b .pr8213-testcase
%patch206 -p1 -b .x86_64-biarch-testsuite
%patch214 -p1 -b .mklibgcc-serialize-crtfiles
%patch215 -p1 -b .c++-classfn-member-template
%patch219 -p1 -b .pr11631-testcase
%patch220 -p1 -b .pr13179

# openSUSE patches
%patch301 -p1 -b .unwind

%patch401 -p1 -b .ucontext

%patch500 -p1 -b .pr6387

sed -i -e 's/struct siginfo/siginfo_t/' gcc/config/*/linux*.h

%ifarch ppc ppc64 s390 s390x
sed -i -e 's/-lm @LIBUNWIND_FLAG@/-lm @LIBUNWIND_FLAG@ -lnldbl_nonshared/' \
  libstdc++33-v3/src/Makefile.{am,in}
%endif
# Don't need to test C, only check-g++ and libstdc++-v33's make check
sed -i -e 's/\$(RUNTEST) --tool gcc/: $(RUNTEST) --tool gcc/' \
  gcc/Makefile.in
sed -i -e 's/\$\$runtest \$(RUNTESTDEFAULTFLAGS)/: $$runtest $(RUNTESTDEFAULTFLAGS)/' \
  libstdc++-v3/testsuite/Makefile.in
perl -pi -e 's/3\.2\.4/3.2.3/' gcc/version.c
perl -pi -e 's/"%{gcc_version}"/"%{gcc_version} \(release\)"/' gcc/version.c
perl -pi -e 's/\((prerelease|experimental|release|Red Hat[^)]*)\)/\(Red Hat Linux %{gcc_version}-%{gcc_release}\)/' gcc/version.c

cp -a libstdc++33-v3/config/cpu/i{4,3}86/atomicity.h

./contrib/gcc_update --touch

%build

# Disable this. No time to test
%global _lto_cflags %{nil}

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

mkdir -p ld_hack
cat > ld_hack/ld <<\EOF
#!/bin/sh
case " $* " in *\ -r\ *) exec /usr/bin/ld "$@";; esac
exec /usr/bin/ld --build-id "$@"
EOF
chmod 755 ld_hack/ld
export PATH=`pwd`/ld_hack/${PATH:+:$PATH}

if [ ! -f /usr/lib/locale/de_DE/LC_CTYPE ]; then
  mkdir locale
  localedef -f ISO-8859-1 -i de_DE locale/de_DE
  export LOCPATH=`pwd`/locale:/usr/lib/locale
fi

CC='gcc -std=gnu89 -fcommon'
OPT_FLAGS="$(echo %{optflags} | sed -e 's/-fno-rtti//g' -e 's/-fno-exceptions//g')"
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-m64//g;s/-m32//g;s/-m31//g')"
%ifarch %{ix86}
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-mtune=pentium4/-mcpu=i686/g')"
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-mtune=generic/-mcpu=i686/g')"
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-mtune=atom/-mcpu=i686/g')"
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-msse2//g')"
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-mfpmath=sse//g')"
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-mstackrealign//g')"
OPT_FLAGS="$OPT_FLAGS -fPIC"
%endif
%ifarch x86_64
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-mtune=nocona//g')"
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-mtune=generic//g')"
%endif
%ifarch sparc sparcv9 sparc64
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g')"
%endif
%ifarch s390 s390x
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-march=z9-109//g;s/-mtune=z10//g')"
%endif
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-Wall//g' -e 's/-Wp,-D_FORTIFY_SOURCE=2//g')"
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-fexceptions//g' -e 's/-fasynchronous-unwind-tables//g')"
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-fstack-protector\(-strong\)\?//g')"
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/--param=ssp-buffer-size=[0-9]*//g')"
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-grecord-gcc-switches//g' -e 's/-Werror=format-security//g')"
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-fstack-clash-protection//g' -e 's/-fcf-protection//g')"
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//g')"
OPT_FLAGS="$(echo $OPT_FLAGS | sed -e 's,-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1,,g')"
%ifarch sparc64
cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -std=gnu89 -fcommon -m64 "$@"
EOF
chmod +x gcc64
CC=`pwd`/gcc64
%endif
%ifarch ppc64
if gcc -m64 -xc -S /dev/null -o - > /dev/null 2>&1; then
  cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -std=gnu89 -fcommon -m64 "$@"
EOF
  chmod +x gcc64
  CC=`pwd`/gcc64
fi
%endif
CC="$CC" CFLAGS="$OPT_FLAGS" CXXFLAGS="$OPT_FLAGS" XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
  GCJFLAGS="$OPT_FLAGS" \
  ../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
  --enable-shared --enable-threads=posix --disable-checking \
  --with-system-zlib --enable-__cxa_atexit \
  --enable-languages=c,c++ --disable-libgcj \
%ifarch sparc sparcv9
  --host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%ifarch ppc
  --host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifnarch sparc sparcv9 ppc
  --host=%{gcc_target_platform}
%endif

%make_build BOOT_CFLAGS="$OPT_FLAGS" bootstrap-lean
#make_build BOOT_CFLAGS="$OPT_FLAGS" bootstrap

# Fix up libstdc++.so's
for d in `pwd`/%{gcc_target_platform}/libstdc++-v3 `pwd`/%{gcc_target_platform}/*/libstdc++-v3; do
  test -d $d || continue
  d33=`dirname $d`/libstdc++33-v3
  pushd $d/src
    sh %{SOURCE3} .libs/libstdc++.so .libs/ll.so linker.map
    rm .libs/libstdc++.so; mv .libs/ll.so .libs/libstdc++.so
    f=`basename .libs/libstdc++.so.5.0.*`
    f33=`basename $d33/src/.libs/libstdc++.so.5.0.*`
    cp -a $d33/src/.libs/libstdc++.so.5.0.* .libs/
    if [ "$f" != "$f33" ]; then
      ln -sf $f33 .libs/libstdc++.so.5
      ln -sf $f33 .libs/$f
    fi
  popd
  pushd $d33/src
    sh %{SOURCE3} .libs/libstdc++.so .libs/ll.so libstdc++*.ver
    rm .libs/libstdc++.so; mv .libs/ll.so .libs/libstdc++.so
  popd
done

# Make sure we are using system libgcc_s, as system libc might
# use unwinding features that require it.
mv gcc/libgcc_s.so.1{,.bak}
ln -sf /%{_lib}/libgcc_s.so.1 gcc/libgcc_s.so.1

# run the tests.
#make %{?_smp_mflags} -k check || :
#sed -ie s/libstdc++-v3/libstdc++33-v3/g `find $(find %{gcc_target_platform} -type d -a -name libstdc++33-v3) -name \*.sum`
#echo ====================TESTING=========================
#( ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
#echo ====================TESTING END=====================

%install
export PATH=`pwd`/obj-%{gcc_target_platform}/ld_hack/${PATH:+:$PATH}

perl -pi -e \
  's~href="l(ibstdc|atest)~href="http://gcc.gnu.org/onlinedocs/libstdc++/l\1~' \
  libstdc++-v3/docs/html/documentation.html
ln -sf documentation.html libstdc++-v3/docs/html/index.html
find libstdc++-v3/docs/html -name CVS | xargs rm -rf

cd obj-%{gcc_target_platform}

if [ ! -f /usr/lib/locale/de_DE/LC_CTYPE ]; then
  export LOCPATH=`pwd`/locale:/usr/lib/locale
fi

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ and libjava Makefiles
# make -C %{gcc_target_platform}/libstdc++-v3

make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install

FULLPATH=%{buildroot}%{_prefix}/lib/gcc-lib/%{gcc_target_platform}/%{gcc_version}
FULLPATH33=%{buildroot}%{_prefix}/lib/gcc-lib/%{gcc_target_platform}/3.3.4

rm -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a
rm -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a
rm -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.so*

for d in %{gcc_target_platform}/libstdc++-v3 %{gcc_target_platform}/*/libstdc++-v3; do
  test -d $d || continue
  d33=`dirname $d`/libstdc++33-v3
  b=""
  test x"$d" != x%{gcc_target_platform}/libstdc++-v3 && b=/`basename $(dirname $d)`
  install -m 644 $d/libsupc++/.libs/libsupc++.a $FULLPATH$b/
  install -m 644 $d/src/.libs/libstdc++.a $FULLPATH$b/
  strip -g $FULLPATH$b/*.a
  install -m 644 $d/src/.libs/libstdc++.so $FULLPATH$b/

  mkdir -p $FULLPATH33$b
  install -m 644 $d33/libsupc++/.libs/libsupc++.a $FULLPATH33$b/
  install -m 644 $d33/src/.libs/libstdc++.a $FULLPATH33$b/
  strip -g $FULLPATH33$b/*.a
  install -m 644 $d33/src/.libs/libstdc++.so $FULLPATH33$b/
done

mkdir -p %{buildroot}/%{_lib}
install -m755 %{gcc_target_platform}/libstdc++33-v3/src/.libs/libstdc++.so.5.0* \
  %{buildroot}%{_prefix}/%{_lib}/
/sbin/ldconfig -n %{buildroot}%{_prefix}/%{_lib}/

rm -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s*

cd ..

for i in %{buildroot}%{_prefix}/bin/{*gcc,*++,gcov}; do
  mv -f $i ${i}32
done

rm -f %{buildroot}%{_prefix}/lib*/{libiberty.a,*/libiberty.a}
rm -f %{buildroot}/lib*/libgcc_s*

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
%else
%ifarch sparc sparcv9 ppc
rm -f %{buildroot}%{_prefix}/lib64/lib*.so*
rm -f %{buildroot}%{_prefix}/lib64/lib*.a
%endif
%endif

rm -rf %{buildroot}%{_prefix}/{lib/gcc-lib,bin,include,share}
find %{buildroot} -name '*.la' -delete

# No time to fix debug proper packaging
%ifarch %{ix86}
  strip --strip-unneeded %{buildroot}%{_prefix}/%{_lib}/libstdc++.so.5*
%endif


%files -n compat-libstdc++-33
%{_prefix}/%{_lib}/libstdc++.so.5*

%changelog
* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 3.2.3-68.16.8
- gcc 10 fix

* Tue Mar 17 2020 Phantom X <megaphantomx at bol dot com dot br> - 3.2.3-68.16.7
- Bring to new Fedora

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-68.16.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-68.16.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-68.16.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-68.16.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-68.16.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-68.16.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 10 2016 Jakub Jelinek  <jakub@redhat.com> 3.2.3-68.16
- add dist tag

* Thu May  5 2016 Jakub Jelinek  <jakub@redhat.com> 3.2.3-68.15
- buildrequire data files for localedef
- use -std=gnu89 in the host compiler

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-68.14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-68.13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-68.12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul  7 2014 Jakub Jelinek  <jakub@redhat.com> 3.2.3-68.11
- fix build on Fedora21+ (#1106076)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-68.10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 19 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.2.3-68.9
- Exlclude ARM as HFP was not supported until gcc 4.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-68.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 20 2013 Jakub Jelinek  <jakub@redhat.com> 3.2.3-68.7
- use siginfo_t instead of struct siginfo

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-68.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 15 2012 Jon Ciesla <limburgher@gmail.com> - 3.2.3-68.5
- Provides: bundled(libiberty)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-68.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-68.3
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-68.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-68.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 17 2009 Jakub Jelinek  <jakub@redhat.com> 3.2.3-68
- strip -march=z9-109 and -mtune=z10 from OPT_FLAGS on s390, s390x
  (#523209)
- make sure to use system libgcc_s.so.1 instead of gcc32 one during
  testing

* Tue Jul 28 2009 Jakub Jelinek  <jakub@redhat.com> 3.2.3-67
- replace -mtune=generic in $RPM_OPT_FLAGS with something that
  GCC 3.2.3 groks

* Mon Mar  9 2009 Jakub Jelinek  <jakub@redhat.com> 3.2.3-66
- fix up for latest bison

* Sat Feb 14 2009 Dennis Gilmore <dennis@ausil.us> - 3.2.3-65
- fix to build 32 bit sparc sparcv9

* Tue Jul 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.3-64
- fix license tag
- apply patches with fuzz=2

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.2.3-63
- Autorebuild for GCC 4.3

* Tue Oct  9 2007 Jakub Jelinek  <jakub@redhat.com> 3.2.3-62
- rebuilt

* Mon Aug 21 2006 Jakub Jelinek  <jakub@redhat.com> 3.2.3-61
- fix the ppc*/s390* math *l stub changes

* Fri Aug 18 2006 Jakub Jelinek  <jakub@redhat.com> 3.2.3-60
- on ppc*/s390* make sure all needed math *l stubs are included

* Thu Aug 10 2006 Jakub Jelinek  <jakub@redhat.com> 3.2.3-59
- fix cleaning up the buildroot before debuginfo generation

* Thu Aug 10 2006 Jakub Jelinek  <jakub@redhat.com> 3.2.3-58
- include only compat-libstdc++-33 subpackage

* Thu Aug  3 2006 Jakub Jelinek  <jakub@redhat.com> 3.2.3-57
- in 64-bit builds remove 32-bit /usr/lib/lib* libraries from the
  buildroots (and similarly on 32-bit builds remove 64-bit /usr/lib64/lib*)
  before AutoReq generation

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.2.3-55.fc5.1
- rebuild

* Sat Feb 11 2006 Jakub Jelinek  <jakub@redhat.com> 3.2.3-55.fc5
- replace -mtune=generic in $RPM_OPT_FLAGS with something that
  GCC 3.2.3 groks

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.2.3-54.fc5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.2.3-54.fc5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan  4 2006 Jakub Jelinek  <jakub@redhat.com> 3.2.3-54.fc5
- rebuilt with new gcc, massage $RPM_OPT_FLAGS, as GCC 3.2.3-RH doesn't
  grok -fstack-protector etc.
- make sure glibc and glibc-devel for all multilib arches is installed
  for building (#170601)
- fix compat-libstdc++-33 %%description (#171684)
- disable os_defines.h changes introduced in 3.2.3-45 also for
  IBM xlC compiler (#146196, IT#75174)
- fix pushdecl_class_level for OVERLOADs (Mark Mitchell,
  Alexandre Oliva, #156185)
- reword diagnostics about unresolved overloaded type
  (Alexandre Oliva, #156291, IT#70101)
- fix x86_64 compiler hang when passing object with 3+ base classes by value
  (Zak Kipling, PR target/18300, #164421, #171940, IT#76454)
- predefine __GNUC_RH_RELEASE__ macro to rpm's %%{release} (Alexandre Oliva)
- weakref attribute support, use it in <bits/gthr.h> various C++ headers
  are using (Alexandre Oliva, #165728, IT#73356)
- don't warn in templates about missing return if return type is dependent
  on template parameters (Alexandre Oliva, PR c++/13106, #169044, IT#77857)
- ensure ppc64 keeps stack 16 byte aligned even with dynamic allocation
  (alloca, VLAs), but don't rely on it in the generated code
  (Alexandre Oliva, #169111, IT#76136)
- fix invalid CC clobberation on i?86/x86_64 (Eric Botcazou,
  PR optimization/12799, #169654)
- don't assume hard frame pointer register is STACK_BOUNDARY aligned
  if frame pointer isn't used and the register has been reused
  for something else (Eric Botcazou, PR optimization/13041, #169845)
- fix libstdc++ seekoff bug (Scott Snyder, #151692, IT#66065,
  PR libstdc++/9659)
- don't use .symver directives in libstdc++.a, instead
  provide hidden aliases for the obsolete symbols (#151732, IT#64710)
- fix a strength reduction bug (Jan Hubicka, #149250, IT#66328)
- fix xchgb constraints on i386 (#156104, IT#69633, PR target/19005)
- change __cxa_demangle to match cxx-abi change
  http://www.codesourcery.com/archives/cxx-abi-dev/msg01877.html
  (Jason Merrill, #133406)
- fix ICE on invalid use of template without arguments as primary
  expression (Mark Mitchell, #149492, PR c++/10558)
- fix c++filt/__cxa_demangle segfault on invalidly mangled names
  generated by G++ 3.4 (Ian Lance Taylor, #145781, PR c++/16240)
- disable os_defines.h changes introduced in 3.2.3-45 for non-GCC
  compilers (#144725, #146196)
- fix debugging information in in-charge constructors and
  destructors (Mark Mitchell, #146416, PR debug/11098)
- fix delete_null_pointer_checks on non-cc0 targets (Alan Modra, #141694,
  IT#54408, PR rtl-optimization/14279)
- fix some reload related issues on ppc64 (David Edelsohn, #139099,
  IT#45622, PRs target/16239, target/8480, optimization/8328)
- fix ICE in regenerate_decl_from_template (Mark Mitchell, #142418,
  PR c++/7053)
- fix ICE when printing jump to case label... crosses initialization
  warning (Gabriel Dos Reis, #140830, PR c++/7566)
- fix corner case in passing by invisible reference (Alexandre Oliva,
  IT#54891, #141270)
- fix ICE on code that uses value of reference in reference's initializer
  (Alexandre Oliva, #141274, IT#36304)
- avoid moving jumptable away from corresponding jump even if there is an
  intervening barrier (Josef Zlomek, #131378)
- with -D_GLIBCXX_FULLY_DYNAMIC_STRING, STL should now avoid
  _S_empty_rep_storage (Paolo Carlini, #131030, IT#45103, PR libstdc++/16612)
- document -Winline only works for languages that use RTL inliner (Java,
  Ada, #141272, IT#28331)

* Tue Mar  8 2005 Jakub Jelinek  <jakub@redhat.com> 3.2.3-47.fc4
- new compatibility package
