%bcond_with check

Name:           xbyak
Version:        6.67
Release:        100%{?dist}
Summary:        A C++ JIT assembler for x86

Epoch:          1

License:        License:        BSD-3-Clause
URL:            https://github.com/herumi/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# exception testing of allocator gets hung up on glibc double free check
Patch0:         xbyak-disable-noexecption-test3.patch

BuildArch:      noarch
ExclusiveArch:  x86_64

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  sed

%if %{with check}
# check
#  -m32
BuildRequires:  glibc-devel(x86-32), libstdc++(x86-32)
BuildRequires:  nasm, yasm
%endif


%description
Xbyak is a C++ header library that enables dynamically to
assemble x86(IA32), x64(AMD64, x86-64) mnemonic.

The pronunciation of Xbyak is kəi-bja-k, かいびゃく.
It is named from a Japanese word 開闢, which means the beginning
of the world.

%package devel
Summary:        A C++ JIT assembler for x86
Provides:       xbyak-static = %{version}-%{release}

%description devel
Xbyak is a C++ header library that enables dynamically to
assemble x86(IA32), x64(AMD64, x86-64) mnemonic.

The pronunciation of Xbyak is kəi-bja-k, かいびゃく.
It is named from a Japanese word 開闢, which means the beginning
of the world.


%prep
%autosetup -p1

sed -e 's/\r//' -i COPYRIGHT readme.txt doc/*.md

%build
%cmake
%cmake_build


%install
%cmake_install


%if %{with check}
%check
make test
%endif

%files devel
%doc readme.txt doc/*.md sample
%license COPYRIGHT
%{_includedir}/xbyak/*.h
%{_libdir}/cmake/%{name}


%changelog
* Tue Dec 06 2022 Phantom X <megaphantomx at hotmail dot com> - 1:6.67-100
- 6.67

* Thu Oct 27 2022 Tom Rix <trix@redhat.com> - 6.63-3
- Make check optional

* Mon Oct 24 2022 Tom Rix <trix@redhat.com> - 6.63-2
- Add tests, samples
- Change license to BSD-3-Clause
- Check directory ownership
- Package as static library

* Fri Oct 21 2022 Tom Rix <trix@redhat.com> - 6.63-1
- Initial release
