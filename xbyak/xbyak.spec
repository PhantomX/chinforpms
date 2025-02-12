%bcond_with check

Name:           xbyak
Version:        7.22
Release:        100%{?dist}
Summary:        A C++ JIT assembler for x86

Epoch:          1

License:        BSD-3-Clause
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
* Wed Feb 12 2025 Phantom X <megaphantomx at hotmail dot com> - 1:7.22.1-100
- 7.22

* Wed Nov 06 2024 Phantom X <megaphantomx at hotmail dot com> - 1:7.21-100
- 7.21

* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 1:7.07.1-100
- 7.07.1

* Mon Aug 05 2024 Phantom X <megaphantomx at hotmail dot com> - 1:7.07-100
- 7.07

* Thu Mar 07 2024 Phantom X <megaphantomx at hotmail dot com> - 1:7.06-100
- 7.06

* Fri Feb 09 2024 Phantom X <megaphantomx at hotmail dot com> - 1:7.05-100
- 7.05

* Wed Aug 23 2023 Phantom X <megaphantomx at hotmail dot com> - 1:6.73-100
- 6.73

* Thu Apr 20 2023 Phantom X <megaphantomx at hotmail dot com> - 1:6.69.1-100
- 6.69.1

* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 1:6.69-100
- 6.69

* Mon Jan 09 2023 Phantom X <megaphantomx at hotmail dot com> - 1:6.68-100
- 6.68

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
