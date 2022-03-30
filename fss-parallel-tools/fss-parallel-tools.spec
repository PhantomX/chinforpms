Name:           fss-parallel-tools
Version:        1.49
Release:        3%{?dist}
Summary:        Parallel tar, rm and cp utilities

License:        UPL
URL:            https://blogs.oracle.com/cloud-infrastructure/post/announcing-parallel-file-tools-for-file-storage

# src.rpm as source, because Oracle...
Source0:        https://yum.oracle.com/repo/OracleLinux/OL7/developer/x86_64/getPackageSource/%{name}-%{version}-1.el7.src.rpm

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  help2man
Requires:       gzip
Requires:       pv


%description
%{summary}.


%prep
%setup -c -T
rpm2cpio %{S:0} | cpio -imdv --no-absolute-filenames
tar -xof %{name}-%{version}.tar.gz --strip-components 1
rm -f %{name}-%{version}.tar.gz

sed \
  -e '/^CFLAGS/s|-g -O1||g' \
  -e 's|^CFLAGS=|CFLAGS+=|g' \
  -e 's|^LDFLAGS=|LDFLAGS+=|g' \
  -i Makefile

%build
%set_build_flags
%make_build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1

for i in par{cp,rm,tar} ;do
  install -pm0755 $i %{buildroot}%{_bindir}/
  zcat $i.1.gz > %{buildroot}%{_mandir}/man1/$i.1
done


%files
%license LICENSE
%{_bindir}/*
%{_mandir}/man1/*.1*


%changelog
* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1.49-3
- Fix for package_note_file

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1.49-2
- Undefine _package_note_file

* Thu Jul 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.49-1
- Initial spec
