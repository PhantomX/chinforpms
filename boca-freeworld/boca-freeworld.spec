%global smoothver 0.9.9

%global systemlibs systemlibexpat,systemliburiparser,systemlibxspf,systemzlib

%global decoder alac faad2 fdkaac mac
%global encoder faac fdkaac mac voaacenc

%global pkgname boca

%global vc_url https://github.com/enzo1982/BoCA

%global ver     %%(echo %{version} | tr '~' '-' | tr '_' '-')

Name:           %{pkgname}-freeworld
Version:        1.0.7
Release:        1%{?dist}
Summary:        Component development kit for fre:ac - freeworld codecs

License:        GPL-2.0-only
URL:            http://www.freac.org/

Source0:        %{vc_url}/releases/download/v%{version}/%{pkgname}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  smooth-devel >= %{smoothver}

Requires:       %{pkgname}%{?_isa} = %{version}

Obsoletes:      freac-cdk-freeworld < 1.2
Provides:       freac-cdk-freeworld = 1.2


%description
The fre:ac Component Development Kit (CDK) enables software developers
to create custom BoCA components for fre:ac development releases.

This build contains freeworld codecs, like AAC.


%prep
%autosetup -n %{pkgname}-%{ver} -p1

sed -e 's/\r//' -i Readme*

sed -e 's|winegcc|\0-disabled|g' -i Makefile-options

sed \
  -e 's|-L$(prefix)/lib\b||g' \
  -e 's|-L/usr/X11R6/lib -L/usr/local/lib||g' \
  -i Makefile runtime/Makefile Makefile-commands

sed -e 's|/lib/|/%{_lib}/|g' -i runtime/common/utilities.cpp

sed -e 's| $(OFLAGS)||g' -i components/decoder/alac/alac/Makefile


%build
%make_build -C runtime \
  config=%{systemlibs} \
  prefix=/usr libdir=%{_libdir}

for i in %{decoder} ;do
%make_build -C components/decoder/$i \
  config=%{systemlibs} \
  prefix=/usr libdir=%{_libdir}
done
for i in %{encoder} ;do
%make_build -C components/encoder/$i \
  config=%{systemlibs} \
  prefix=/usr libdir=%{_libdir}
done

%install
for i in %{decoder} ;do
%make_install -C components/decoder/$i \
  config=%{systemlibs} \
  prefix=/usr libdir=%{_libdir}
done
for i in %{encoder} ;do
%make_install -C components/encoder/$i \
  config=%{systemlibs} \
  prefix=/usr libdir=%{_libdir}
done

chmod +x %{buildroot}%{_libdir}/boca/*.so*

rm -rf %{buildroot}%{_includedir}
rm -f %{buildroot}%{_libdir}/*.so


%files
%license COPYING
%doc Readme.md
%{_libdir}/boca/*.so*


%changelog
* Thu Apr 06 2023 Phantom X <megaphantomx at hotmail dot com> - 1.0.7-1
- 1.0.7

* Thu Mar 03 2022 Phantom X <megaphantomx at hotmail dot com> - 1.0.6a-1
- 1.0.6a

* Fri Aug 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1.0.5-1
- 1.0.5

* Mon Mar 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1.0.4-1
- 1.0.4

* Mon Nov 30 2020 Phantom X <megaphantomx at hotmail dot com> - 1.0.3-1
- 1.0.3

* Sat Jul 04 2020 Phantom X <megaphantomx at hotmail dot com> - 1.0.2-1
- 1.0.2

* Wed Apr 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.0.1-1
- 1.0.1

* Tue Mar 31 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.0-1
- 1.0

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.0~rc1-1
- 1.0-rc1

* Sat Feb 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.0~beta3-1
- Initial spec
- Replaces freac-cdk-freeworld
