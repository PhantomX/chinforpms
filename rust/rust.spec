# Only x86_64 and i686 are Tier 1 platforms at this time.
# https://forge.rust-lang.org/platform-support.html
%global rust_arches x86_64

# The channel can be stable, beta, or nightly
%{!?channel: %global channel stable}

# To bootstrap from scratch, set the channel and date from src/stage0.txt
# e.g. 1.10.0 wants rustc: 1.9.0-2016-05-24
# or nightly wants some beta-YYYY-MM-DD
# Note that cargo matches the program version here, not its crate version.
%global bootstrap_rust 1.31.1
%global bootstrap_cargo 1.31.0
%global bootstrap_channel %{bootstrap_rust}
%global bootstrap_date 2018-12-20

# Only the specified arches will use bootstrap binaries.
#global bootstrap_arches %%{rust_arches}

# Using llvm-static may be helpful as an opt-in, e.g. to aid LLVM rebases.
%bcond_with llvm_static

# We can also choose to just use Rust's bundled LLVM, in case the system LLVM
# is insufficient.  Rust currently requires LLVM 5.0+.
%if 0%{?rhel} && !0%{?epel}
%bcond_without bundled_llvm
%else
%bcond_with bundled_llvm
%endif

# libgit2-sys expects to use its bundled library, which is sometimes just a
# snapshot of libgit2's master branch.  This can mean the FFI declarations
# won't match our released libgit2.so, e.g. having changed struct fields.
# So, tread carefully if you toggle this...
%bcond_without bundled_libgit2

%if 0%{?rhel}
%bcond_without bundled_libssh2
%else
%bcond_with bundled_libssh2
%endif

# LLDB only works on some architectures
%ifarch %{arm} aarch64 %{ix86} x86_64
# LLDB isn't available everywhere...
%if !0%{?rhel}
%bcond_without lldb
%else
%bcond_with lldb
%endif
%else
%bcond_with lldb
%endif

Name:           rust
Version:        1.32.0
Release:        100%{?dist}
Epoch:          1
Summary:        The Rust Programming Language
License:        (ASL 2.0 or MIT) and (BSD and MIT)
# ^ written as: (rust itself) and (bundled libraries)
URL:            https://www.rust-lang.org
ExclusiveArch:  %{rust_arches}

%if "%{channel}" == "stable"
%global rustc_package rustc-%{version}-src
%else
%global rustc_package rustc-%{channel}-src
%endif
Source0:        https://static.rust-lang.org/dist/%{rustc_package}.tar.xz

# https://github.com/rust-dev-tools/rls-analysis/pull/160
Patch1:         0001-Try-to-get-the-target-triple-from-rustc-itself.patch

# https://github.com/rust-lang/rust/pull/57453
Patch2:         0001-lldb_batchmode.py-try-import-_thread-for-Python-3.patch

# Get the Rust triple for any arch.
%{lua: function rust_triple(arch)
  local abi = "gnu"
  if arch == "armv7hl" then
    arch = "armv7"
    abi = "gnueabihf"
  elseif arch == "ppc64" then
    arch = "powerpc64"
  elseif arch == "ppc64le" then
    arch = "powerpc64le"
  end
  return arch.."-unknown-linux-"..abi
end}

%global rust_triple %{lua: print(rust_triple(rpm.expand("%{_target_cpu}")))}

%if %defined bootstrap_arches
# For each bootstrap arch, add an additional binary Source.
# Also define bootstrap_source just for the current target.
%{lua: do
  local bootstrap_arches = {}
  for arch in string.gmatch(rpm.expand("%{bootstrap_arches}"), "%S+") do
    table.insert(bootstrap_arches, arch)
  end
  local base = rpm.expand("https://static.rust-lang.org/dist/%{bootstrap_date}"
                          .."/rust-%{bootstrap_channel}")
  local target_arch = rpm.expand("%{_target_cpu}")
  for i, arch in ipairs(bootstrap_arches) do
    print(string.format("Source%d: %s-%s.tar.xz\n",
                        i, base, rust_triple(arch)))
    if arch == target_arch then
      rpm.define("bootstrap_source "..i)
    end
  end
end}
%endif

%ifarch %{bootstrap_arches}
%global bootstrap_root rust-%{bootstrap_channel}-%{rust_triple}
%global local_rust_root %{_builddir}/%{bootstrap_root}/usr
Provides:       bundled(%{name}-bootstrap) = %{bootstrap_rust}
%else
BuildRequires:  cargo >= %{bootstrap_cargo}
%if 0%{?fedora} >= 27
BuildRequires:  (%{name} >= %{bootstrap_rust} with %{name} <= %{version})
%else
BuildRequires:  %{name} >= %{bootstrap_rust}
BuildConflicts: %{name} > %{version}
%endif
%global local_rust_root %{_prefix}
%endif

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ncurses-devel
BuildRequires:  curl
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(zlib)

%if %without bundled_libgit2
BuildRequires:  pkgconfig(libgit2) >= 0.27
%endif

%if %without bundled_libssh2
# needs libssh2_userauth_publickey_frommemory
BuildRequires:  pkgconfig(libssh2) >= 1.6.0
%endif

%if 0%{?rhel} && 0%{?rhel} <= 7
%global python python2
%else
%global python python3
%endif
BuildRequires:  %{python}

%if %with bundled_llvm
BuildRequires:  cmake3 >= 3.4.3
Provides:       bundled(llvm) = 8.0.0~svn
%else
BuildRequires:  cmake >= 2.8.11
%if 0%{?epel}
%global llvm llvm5.0
%endif
%if %defined llvm
%global llvm_root %{_libdir}/%{llvm}
%else
%global llvm llvm
%global llvm_root %{_prefix}
%endif
BuildRequires:  %{llvm}-devel >= 5.0
%if %with llvm_static
BuildRequires:  %{llvm}-static
BuildRequires:  libffi-devel
%endif
%endif

# make check needs "ps" for src/test/run-pass/wait-forked-but-failed-child.rs
BuildRequires:  procps-ng

# debuginfo-gdb tests need gdb
BuildRequires:  gdb

# TODO: work on unbundling these!
Provides:       bundled(libbacktrace) = 8.1.0
Provides:       bundled(miniz) = 1.16~beta+r1

# Virtual provides for folks who attempt "dnf install rustc"
Provides:       rustc = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       rustc%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

# Always require our exact standard library
Requires:       %{name}-std-static%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

# The C compiler is needed at runtime just for linking.  Someday rustc might
# invoke the linker directly, and then we'll only need binutils.
# https://github.com/rust-lang/rust/issues/11937
Requires:       /usr/bin/cc

# ALL Rust libraries are private, because they don't keep an ABI.
%global _privatelibs lib(.*-[[:xdigit:]]{16}*|rustc.*)[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$
%global __provides_exclude_from ^(%{_docdir}|%{rustlibdir}/src)/.*$
%global __requires_exclude_from ^(%{_docdir}|%{rustlibdir}/src)/.*$

# While we don't want to encourage dynamic linking to Rust shared libraries, as
# there's no stable ABI, we still need the unallocated metadata (.rustc) to
# support custom-derive plugins like #[proc_macro_derive(Foo)].  But eu-strip is
# very eager by default, so we have to limit it to -g, only debugging symbols.
%if 0%{?fedora} >= 27
# Newer find-debuginfo.sh supports --keep-section, which is preferable. rhbz1465997
%global _find_debuginfo_opts --keep-section .rustc
%else
%global _find_debuginfo_opts -g
%undefine _include_minidebuginfo
%endif

# Use hardening ldflags.
%global rustflags -Clink-arg=-Wl,-z,relro,-z,now

%if %{without bundled_llvm}
%if 0%{?fedora} || 0%{?rhel} > 7 || 0%{?scl:1}
%global llvm_has_filecheck 1
%endif
%if "%{llvm_root}" != "%{_prefix}"
# https://github.com/rust-lang/rust/issues/40717
%global library_path $(%{llvm_root}/bin/llvm-config --libdir)
%endif
%endif

%description
Rust is a systems programming language that runs blazingly fast, prevents
segfaults, and guarantees thread safety.

This package includes the Rust compiler and documentation generator.


%package std-static
Summary:        Standard library for Rust

%description std-static
This package includes the standard libraries for building applications
written in Rust.


%package debugger-common
Summary:        Common debugger pretty printers for Rust
BuildArch:      noarch

%description debugger-common
This package includes the common functionality for %{name}-gdb and %{name}-lldb.


%package gdb
Summary:        GDB pretty printers for Rust
BuildArch:      noarch
Requires:       gdb
Requires:       %{name}-debugger-common = %{?epoch:%{epoch}:}%{version}-%{release}

%description gdb
This package includes the rust-gdb script, which allows easier debugging of Rust
programs.


%if %with lldb

%package lldb
Summary:        LLDB pretty printers for Rust

# It could be noarch, but lldb has limited availability
#BuildArch:      noarch

Requires:       lldb
Requires:       python2-lldb
Requires:       %{name}-debugger-common = %{?epoch:%{epoch}:}%{version}-%{release}

%description lldb
This package includes the rust-lldb script, which allows easier debugging of Rust
programs.

%endif


%package doc
Summary:        Documentation for Rust
# NOT BuildArch:      noarch
# Note, while docs are mostly noarch, some things do vary by target_arch.
# Koji will fail the build in rpmdiff if two architectures build a noarch
# subpackage differently, so instead we have to keep its arch.

%description doc
This package includes HTML documentation for the Rust programming language and
its standard library.


%package -n cargo
Summary:        Rust's package manager and build tool
%if %with bundled_libgit2
Provides:       bundled(libgit2) = 0.27
%endif
%if %with bundled_libssh2
Provides:       bundled(libssh2) = 1.8.1~dev
%endif
# For tests:
BuildRequires:  git
# Cargo is not much use without Rust
Requires:       rust

%description -n cargo
Cargo is a tool that allows Rust projects to declare their various dependencies
and ensure that you'll always get a repeatable build.


%package -n cargo-doc
Summary:        Documentation for Cargo
BuildArch:      noarch
# Cargo no longer builds its own documentation
# https://github.com/rust-lang/cargo/pull/4904
Requires:       rust-doc = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n cargo-doc
This package includes HTML documentation for Cargo.


%package -n rustfmt
Summary:        Tool to find and fix Rust formatting issues
Requires:       cargo

# The component/package was rustfmt-preview until Rust 1.31.
Obsoletes:      rustfmt-preview < 1.0.0
Provides:       rustfmt-preview = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n rustfmt
A tool for formatting Rust code according to style guidelines.


%package -n rls
Summary:        Rust Language Server for IDE integration
%if %with bundled_libgit2
Provides:       bundled(libgit2) = 0.27
%endif
%if %with bundled_libssh2
Provides:       bundled(libssh2) = 1.8.1~dev
%endif
Requires:       rust-analysis
# /usr/bin/rls is dynamically linked against internal rustc libs
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

# The component/package was rls-preview until Rust 1.31.
Obsoletes:      rls-preview < 1.31.6
Provides:       rls-preview = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n rls
The Rust Language Server provides a server that runs in the background,
providing IDEs, editors, and other tools with information about Rust programs.
It supports functionality such as 'goto definition', symbol search,
reformatting, and code completion, and enables renaming and refactorings.


%package -n clippy
Summary:        Lints to catch common mistakes and improve your Rust code
Requires:       cargo
# /usr/bin/clippy-driver is dynamically linked against internal rustc libs
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

# The component/package was clippy-preview until Rust 1.31.
Obsoletes:      clippy-preview <= 0.0.212
Provides:       clippy-preview = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n clippy
A collection of lints to catch common mistakes and improve your Rust code.


%package src
Summary:        Sources for the Rust standard library
BuildArch:      noarch

%description src
This package includes source files for the Rust standard library.  It may be
useful as a reference for code completion tools in various editors.


%package analysis
Summary:        Compiler analysis data for the Rust standard library
Requires:       rust-std-static%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description analysis
This package contains analysis data files produced with rustc's -Zsave-analysis
feature for the Rust standard library. The RLS (Rust Language Server) uses this
data to provide information about the Rust standard library.


%prep

%ifarch %{bootstrap_arches}
%setup -q -n %{bootstrap_root} -T -b %{bootstrap_source}
./install.sh --components=cargo,rustc,rust-std-%{rust_triple} \
  --prefix=%{local_rust_root} --disable-ldconfig
test -f '%{local_rust_root}/bin/cargo'
test -f '%{local_rust_root}/bin/rustc'
%endif

%setup -q -n %{rustc_package}

pushd vendor/rls-analysis
%patch1 -p1
popd
%patch2 -p1

%if "%{python}" == "python3"
sed -i.try-py3 -e '/try python2.7/i try python3 "$@"' ./configure
%endif

%if %without bundled_llvm
rm -rf src/llvm/
%endif

# We never enable emscripten.
rm -rf src/llvm-emscripten/

# We never enable other LLVM tools.
rm -rf src/tools/clang
rm -rf src/tools/lld
rm -rf src/tools/lldb

# extract bundled licenses for packaging
sed -e '/*\//q' src/libbacktrace/backtrace.h \
  >src/libbacktrace/LICENSE-libbacktrace

%if %{with bundled_llvm} && 0%{?epel}
mkdir -p cmake-bin
ln -s /usr/bin/cmake3 cmake-bin/cmake
%global cmake_path $PWD/cmake-bin
%endif

%if %{without bundled_llvm} && %{with llvm_static}
# Static linking to distro LLVM needs to add -lffi
# https://github.com/rust-lang/rust/issues/34486
sed -i.ffi -e '$a #[link(name = "ffi")] extern {}' \
  src/librustc_llvm/lib.rs
%endif

# The configure macro will modify some autoconf-related files, which upsets
# cargo when it tries to verify checksums in those files.  If we just truncate
# that file list, cargo won't have anything to complain about.
find vendor -name .cargo-checksum.json \
  -exec sed -i.uncheck -e 's/"files":{[^}]*}/"files":{ }/' '{}' '+'


%build

%if %without bundled_libgit2
# convince libgit2-sys to use the distro libgit2
export LIBGIT2_SYS_USE_PKG_CONFIG=1
%endif

%if %without bundled_libssh2
# convince libssh2-sys to use the distro libssh2
export LIBSSH2_SYS_USE_PKG_CONFIG=1
%endif

%{?cmake_path:export PATH=%{cmake_path}:$PATH}
%{?library_path:export LIBRARY_PATH="%{library_path}"}
%{?rustflags:export RUSTFLAGS="%{rustflags}"}

# We're going to override --libdir when configuring to get rustlib into a
# common path, but we'll fix the shared libraries during install.
%global common_libdir %{_prefix}/lib
%global rustlibdir %{common_libdir}/rustlib

%ifarch %{arm} %{ix86}
# full debuginfo is exhausting memory; just do libstd for now
# https://github.com/rust-lang/rust/issues/45854
%if (0%{?fedora} && 0%{?fedora} < 27) || (0%{?rhel} && 0%{?rhel} <= 7)
# Older rpmbuild didn't work with partial debuginfo coverage.
%global debug_package %{nil}
%define enable_debuginfo --disable-debuginfo --disable-debuginfo-only-std --disable-debuginfo-tools --disable-debuginfo-lines
%else
%define enable_debuginfo --enable-debuginfo --enable-debuginfo-only-std --disable-debuginfo-tools --disable-debuginfo-lines
%endif
%else
%define enable_debuginfo --enable-debuginfo --disable-debuginfo-only-std --enable-debuginfo-tools --disable-debuginfo-lines
%endif

%configure --disable-option-checking \
  --libdir=%{common_libdir} \
  --build=%{rust_triple} --host=%{rust_triple} --target=%{rust_triple} \
  --local-rust-root=%{local_rust_root} \
  %{!?with_bundled_llvm: --llvm-root=%{llvm_root} \
    %{!?llvm_has_filecheck: --disable-codegen-tests} \
    %{!?with_llvm_static: --enable-llvm-link-shared } } \
  --disable-rpath \
  %{enable_debuginfo} \
  --enable-extended \
  --enable-vendor \
  --enable-verbose-tests \
  --release-channel=%{channel}

%{python} ./x.py build
%{python} ./x.py doc


%install
%{?cmake_path:export PATH=%{cmake_path}:$PATH}
%{?library_path:export LIBRARY_PATH="%{library_path}"}
%{?rustflags:export RUSTFLAGS="%{rustflags}"}

DESTDIR=%{buildroot} %{python} ./x.py install

# Make sure the shared libraries are in the proper libdir
%if "%{_libdir}" != "%{common_libdir}"
mkdir -p %{buildroot}%{_libdir}
find %{buildroot}%{common_libdir} -maxdepth 1 -type f -name '*.so' \
  -exec mv -v -t %{buildroot}%{_libdir} '{}' '+'
%endif

# The shared libraries should be executable for debuginfo extraction.
find %{buildroot}%{_libdir} -maxdepth 1 -type f -name '*.so' \
  -exec chmod -v +x '{}' '+'

# The libdir libraries are identical to those under rustlib/.  It's easier on
# library loading if we keep them in libdir, but we do need them in rustlib/
# to support dynamic linking for compiler plugins, so we'll symlink.
(cd "%{buildroot}%{rustlibdir}/%{rust_triple}/lib" &&
 find ../../../../%{_lib} -maxdepth 1 -name '*.so' |
 while read lib; do
   # make sure they're actually identical!
   cmp "$lib" "${lib##*/}"
   ln -v -f -s -t . "$lib"
 done)

# Remove installer artifacts (manifests, uninstall scripts, etc.)
find %{buildroot}%{rustlibdir} -maxdepth 1 -type f -exec rm -v '{}' '+'

# Remove backup files from %%configure munging
find %{buildroot}%{rustlibdir} -type f -name '*.orig' -exec rm -v '{}' '+'

# https://fedoraproject.org/wiki/Changes/Make_ambiguous_python_shebangs_error
# We don't actually need to ship any of those python scripts in rust-src anyway.
find %{buildroot}%{rustlibdir}/src -type f -name '*.py' -exec rm -v '{}' '+'

# FIXME: __os_install_post will strip the rlibs
# -- should we find a way to preserve debuginfo?

# Remove unwanted documentation files (we already package them)
rm -f %{buildroot}%{_docdir}/%{name}/README.md
rm -f %{buildroot}%{_docdir}/%{name}/COPYRIGHT
rm -f %{buildroot}%{_docdir}/%{name}/LICENSE
rm -f %{buildroot}%{_docdir}/%{name}/LICENSE-APACHE
rm -f %{buildroot}%{_docdir}/%{name}/LICENSE-MIT
rm -f %{buildroot}%{_docdir}/%{name}/LICENSE-THIRD-PARTY
rm -f %{buildroot}%{_docdir}/%{name}/*.old

# Sanitize the HTML documentation
find %{buildroot}%{_docdir}/%{name}/html -empty -delete
find %{buildroot}%{_docdir}/%{name}/html -type f -exec chmod -x '{}' '+'

# Create the path for crate-devel packages
mkdir -p %{buildroot}%{_datadir}/cargo/registry

# Cargo no longer builds its own documentation
# https://github.com/rust-lang/cargo/pull/4904
mkdir -p %{buildroot}%{_docdir}/cargo
ln -sT ../rust/html/cargo/ %{buildroot}%{_docdir}/cargo/html

%if %without lldb
rm -f %{buildroot}%{_bindir}/rust-lldb
rm -f %{buildroot}%{rustlibdir}/etc/lldb_*.py*
%endif


%check
%{?cmake_path:export PATH=%{cmake_path}:$PATH}
%{?library_path:export LIBRARY_PATH="%{library_path}"}
%{?rustflags:export RUSTFLAGS="%{rustflags}"}

# The results are not stable on koji, so mask errors and just log it.
%{python} ./x.py test --no-fail-fast || :
%{python} ./x.py test --no-fail-fast cargo || :
%{python} ./x.py test --no-fail-fast clippy || :
%{python} ./x.py test --no-fail-fast rls || :
%{python} ./x.py test --no-fail-fast rustfmt || :


%ldconfig_scriptlets


%files
%license COPYRIGHT LICENSE-APACHE LICENSE-MIT
%license src/libbacktrace/LICENSE-libbacktrace
%doc README.md
%{_bindir}/rustc
%{_bindir}/rustdoc
%{_libdir}/*.so
%{_mandir}/man1/rustc.1*
%{_mandir}/man1/rustdoc.1*
%dir %{rustlibdir}
%dir %{rustlibdir}/%{rust_triple}
%dir %{rustlibdir}/%{rust_triple}/lib
%{rustlibdir}/%{rust_triple}/lib/*.so
%{rustlibdir}/%{rust_triple}/codegen-backends/


%files std-static
%dir %{rustlibdir}
%dir %{rustlibdir}/%{rust_triple}
%dir %{rustlibdir}/%{rust_triple}/lib
%{rustlibdir}/%{rust_triple}/lib/*.rlib


%files debugger-common
%dir %{rustlibdir}
%dir %{rustlibdir}/etc
%{rustlibdir}/etc/debugger_*.py*


%files gdb
%{_bindir}/rust-gdb
%{rustlibdir}/etc/gdb_*.py*


%if %with lldb
%files lldb
%{_bindir}/rust-lldb
%{rustlibdir}/etc/lldb_*.py*
%endif


%files doc
%docdir %{_docdir}/%{name}
%dir %{_docdir}/%{name}
%dir %{_docdir}/%{name}/html
%{_docdir}/%{name}/html/*/
%{_docdir}/%{name}/html/*.html
%{_docdir}/%{name}/html/*.css
%{_docdir}/%{name}/html/*.js
%{_docdir}/%{name}/html/*.svg
%{_docdir}/%{name}/html/*.woff
%license %{_docdir}/%{name}/html/*.txt


%files -n cargo
%license src/tools/cargo/LICENSE-APACHE src/tools/cargo/LICENSE-MIT src/tools/cargo/LICENSE-THIRD-PARTY
%doc src/tools/cargo/README.md
%{_bindir}/cargo
%{_mandir}/man1/cargo*.1*
%{_sysconfdir}/bash_completion.d/cargo
%{_datadir}/zsh/site-functions/_cargo
%dir %{_datadir}/cargo
%dir %{_datadir}/cargo/registry


%files -n cargo-doc
%docdir %{_docdir}/cargo
%dir %{_docdir}/cargo
%{_docdir}/cargo/html


%files -n rustfmt
%{_bindir}/rustfmt
%{_bindir}/cargo-fmt
%doc src/tools/rustfmt/{README,CHANGELOG,Configurations}.md
%license src/tools/rustfmt/LICENSE-{APACHE,MIT}


%files -n rls
%{_bindir}/rls
%doc src/tools/rls/{README.md,COPYRIGHT,debugging.md}
%license src/tools/rls/LICENSE-{APACHE,MIT}


%files -n clippy
%{_bindir}/cargo-clippy
%{_bindir}/clippy-driver
%doc src/tools/clippy/{README.md,CHANGELOG.md}
%license src/tools/clippy/LICENSE-{APACHE,MIT}


%files src
%dir %{rustlibdir}
%{rustlibdir}/src


%files analysis
%{rustlibdir}/%{rust_triple}/analysis/


%changelog
* Mon Mar 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.32.0-100
- Temporary package only to build Waterfox

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Josh Stone <jistone@redhat.com> - 1.32.0-1
- Update to 1.32.0.

* Mon Jan 07 2019 Josh Stone <jistone@redhat.com> - 1.31.1-9
- Update to 1.31.1 for RLS fixes.

* Thu Dec 06 2018 Josh Stone <jistone@redhat.com> - 1.31.0-8
- Update to 1.31.0 -- Rust 2018!
- clippy/rls/rustfmt are no longer -preview

* Thu Nov 08 2018 Josh Stone <jistone@redhat.com> - 1.30.1-7
- Update to 1.30.1.

* Thu Oct 25 2018 Josh Stone <jistone@redhat.com> - 1.30.0-6
- Update to 1.30.0.

* Mon Oct 22 2018 Josh Stone <jistone@redhat.com> - 1.29.2-5
- Rebuild without bootstrap binaries.

* Sat Oct 20 2018 Josh Stone <jistone@redhat.com> - 1.29.2-4
- Re-bootstrap armv7hl due to rhbz#1639485

* Fri Oct 12 2018 Josh Stone <jistone@redhat.com> - 1.29.2-3
- Update to 1.29.2.

* Tue Sep 25 2018 Josh Stone <jistone@redhat.com> - 1.29.1-2
- Update to 1.29.1.
- Security fix for str::repeat (pending CVE).

* Thu Sep 13 2018 Josh Stone <jistone@redhat.com> - 1.29.0-1
- Update to 1.29.0.
- Add a clippy-preview subpackage

* Mon Aug 13 2018 Josh Stone <jistone@redhat.com> - 1.28.0-3
- Use llvm6.0 instead of llvm-7 for now

* Tue Aug 07 2018 Josh Stone <jistone@redhat.com> - 1.28.0-2
- Rebuild for LLVM ppc64/s390x fixes

* Thu Aug 02 2018 Josh Stone <jistone@redhat.com> - 1.28.0-1
- Update to 1.28.0.

* Tue Jul 24 2018 Josh Stone <jistone@redhat.com> - 1.27.2-4
- Update to 1.27.2.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Josh Stone <jistone@redhat.com> - 1.27.1-2
- Update to 1.27.1.
- Security fix for CVE-2018-1000622

* Thu Jun 21 2018 Josh Stone <jistone@redhat.com> - 1.27.0-1
- Update to 1.27.0.

* Tue Jun 05 2018 Josh Stone <jistone@redhat.com> - 1.26.2-4
- Rebuild without bootstrap binaries.

* Tue Jun 05 2018 Josh Stone <jistone@redhat.com> - 1.26.2-3
- Update to 1.26.2.
- Re-bootstrap to deal with LLVM symbol changes.

* Tue May 29 2018 Josh Stone <jistone@redhat.com> - 1.26.1-2
- Update to 1.26.1.

* Thu May 10 2018 Josh Stone <jistone@redhat.com> - 1.26.0-1
- Update to 1.26.0.

* Mon Apr 16 2018 Dan Callaghan <dcallagh@redhat.com> - 1.25.0-3
- Add cargo, rls, and analysis

* Tue Apr 10 2018 Josh Stone <jistone@redhat.com> - 1.25.0-2
- Filter codegen-backends from Provides too.

* Thu Mar 29 2018 Josh Stone <jistone@redhat.com> - 1.25.0-1
- Update to 1.25.0.

* Thu Mar 01 2018 Josh Stone <jistone@redhat.com> - 1.24.1-1
- Update to 1.24.1.

* Wed Feb 21 2018 Josh Stone <jistone@redhat.com> - 1.24.0-3
- Backport a rebuild fix for rust#48308.

* Mon Feb 19 2018 Josh Stone <jistone@redhat.com> - 1.24.0-2
- rhbz1546541: drop full-bootstrap; cmp libs before symlinking.
- Backport pr46592 to fix local_rebuild bootstrapping.
- Backport pr48362 to fix relative/absolute libdir.

* Thu Feb 15 2018 Josh Stone <jistone@redhat.com> - 1.24.0-1
- Update to 1.24.0.

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.23.0-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Feb 06 2018 Josh Stone <jistone@redhat.com> - 1.23.0-3
- Use full-bootstrap to work around a rebuild issue.
- Patch binaryen for GCC 8

* Thu Feb 01 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.23.0-2
- Switch to %%ldconfig_scriptlets

* Mon Jan 08 2018 Josh Stone <jistone@redhat.com> - 1.23.0-1
- Update to 1.23.0.

* Thu Nov 23 2017 Josh Stone <jistone@redhat.com> - 1.22.1-1
- Update to 1.22.1.

* Thu Oct 12 2017 Josh Stone <jistone@redhat.com> - 1.21.0-1
- Update to 1.21.0.

* Mon Sep 11 2017 Josh Stone <jistone@redhat.com> - 1.20.0-2
- ABI fixes for ppc64 and s390x.

* Thu Aug 31 2017 Josh Stone <jistone@redhat.com> - 1.20.0-1
- Update to 1.20.0.
- Add a rust-src subpackage.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Josh Stone <jistone@redhat.com> - 1.19.0-2
- Use find-debuginfo.sh --keep-section .rustc

* Thu Jul 20 2017 Josh Stone <jistone@redhat.com> - 1.19.0-1
- Update to 1.19.0.

* Thu Jun 08 2017 Josh Stone <jistone@redhat.com> - 1.18.0-1
- Update to 1.18.0.

* Mon May 08 2017 Josh Stone <jistone@redhat.com> - 1.17.0-2
- Move shared libraries back to libdir and symlink in rustlib

* Thu Apr 27 2017 Josh Stone <jistone@redhat.com> - 1.17.0-1
- Update to 1.17.0.

* Mon Mar 20 2017 Josh Stone <jistone@redhat.com> - 1.16.0-3
- Make rust-lldb arch-specific to deal with lldb deps

* Fri Mar 17 2017 Josh Stone <jistone@redhat.com> - 1.16.0-2
- Limit rust-lldb arches

* Thu Mar 16 2017 Josh Stone <jistone@redhat.com> - 1.16.0-1
- Update to 1.16.0.
- Use rustbuild instead of the old makefiles.
- Update bootstrapping to include rust-std and cargo.
- Add a rust-lldb subpackage.

* Thu Feb 09 2017 Josh Stone <jistone@redhat.com> - 1.15.1-1
- Update to 1.15.1.
- Require rust-rpm-macros for new crate packaging.
- Keep shared libraries under rustlib/, only debug-stripped.
- Merge and clean up conditionals for epel7.

* Fri Dec 23 2016 Josh Stone <jistone@redhat.com> - 1.14.0-2
- Rebuild without bootstrap binaries.

* Thu Dec 22 2016 Josh Stone <jistone@redhat.com> - 1.14.0-1
- Update to 1.14.0.
- Rewrite bootstrap logic to target specific arches.
- Bootstrap ppc64, ppc64le, s390x. (thanks to Sinny Kumari for testing!)

* Thu Nov 10 2016 Josh Stone <jistone@redhat.com> - 1.13.0-1
- Update to 1.13.0.
- Use hardening flags for linking.
- Split the standard library into its own package
- Centralize rustlib/ under /usr/lib/ for multilib integration.

* Thu Oct 20 2016 Josh Stone <jistone@redhat.com> - 1.12.1-1
- Update to 1.12.1.

* Fri Oct 14 2016 Josh Stone <jistone@redhat.com> - 1.12.0-7
- Rebuild with LLVM 3.9.
- Add ncurses-devel for llvm-config's -ltinfo.

* Thu Oct 13 2016 Josh Stone <jistone@redhat.com> - 1.12.0-6
- Rebuild with llvm-static, preparing for 3.9

* Fri Oct 07 2016 Josh Stone <jistone@redhat.com> - 1.12.0-5
- Rebuild with fixed eu-strip (rhbz1380961)

* Fri Oct 07 2016 Josh Stone <jistone@redhat.com> - 1.12.0-4
- Rebuild without bootstrap binaries.

* Thu Oct 06 2016 Josh Stone <jistone@redhat.com> - 1.12.0-3
- Bootstrap aarch64.
- Use jemalloc's MALLOC_CONF to work around #36944.
- Apply pr36933 to really disable armv7hl NEON.

* Sat Oct 01 2016 Josh Stone <jistone@redhat.com> - 1.12.0-2
- Protect .rustc from rpm stripping.

* Fri Sep 30 2016 Josh Stone <jistone@redhat.com> - 1.12.0-1
- Update to 1.12.0.
- Always use --local-rust-root, even for bootstrap binaries.
- Remove the rebuild conditional - the build system now figures it out.
- Let minidebuginfo do its thing, since metadata is no longer a note.
- Let rust build its own compiler-rt builtins again.

* Sat Sep 03 2016 Josh Stone <jistone@redhat.com> - 1.11.0-3
- Rebuild without bootstrap binaries.

* Fri Sep 02 2016 Josh Stone <jistone@redhat.com> - 1.11.0-2
- Bootstrap armv7hl, with backported no-neon patch.

* Wed Aug 24 2016 Josh Stone <jistone@redhat.com> - 1.11.0-1
- Update to 1.11.0.
- Drop the backported patches.
- Patch get-stage0.py to trust existing bootstrap binaries.
- Use libclang_rt.builtins from compiler-rt, dodging llvm-static issues.
- Use --local-rust-root to make sure the right bootstrap is used.

* Sat Aug 13 2016 Josh Stone <jistone@redhat.com> 1.10.0-4
- Rebuild without bootstrap binaries.

* Fri Aug 12 2016 Josh Stone <jistone@redhat.com> - 1.10.0-3
- Initial import into Fedora (#1356907), bootstrapped
- Format license text as suggested in review.
- Note how the tests already run in parallel.
- Undefine _include_minidebuginfo, because it duplicates ".note.rustc".
- Don't let checks fail the whole build.
- Note that -doc can't be noarch, as rpmdiff doesn't allow variations.

* Tue Jul 26 2016 Josh Stone <jistone@redhat.com> - 1.10.0-2
- Update -doc directory ownership, and mark its licenses.
- Package and declare licenses for libbacktrace and hoedown.
- Set bootstrap_base as a global.
- Explicitly require python2.

* Thu Jul 14 2016 Josh Stone <jistone@fedoraproject.org> - 1.10.0-1
- Initial package, bootstrapped
