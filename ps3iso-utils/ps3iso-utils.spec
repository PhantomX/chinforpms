%global commit 878090980a9042c61901920fed1b034af215e8c7
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220309

%global gver .%{date}git%{shortcommit}

Name:           ps3iso-utils
Version:        0
Release:        1%{?gver}%{?dist}
Summary:        PS3 ISO Utilities

License:        GPL-3.0-or-later
URL:            https://github.com/bucanero/%{name}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  make


%description
Estwald's PS3 ISO utilities.


%prep
%autosetup -n %{name}-%{commit} -p1

sed -e 's/\r//' -i readme.txt

sed \
  -e '/^CFLAGS/s|:=|?=|' \
  -e '/^LDFLAGS/d' \
  -e 's|@$(CC)|$(CC)|' \
  -i */Makefile


%build
%set_build_flags

for i in extract make patch split ;do
%make_build -C ${i}ps3iso
done

%install
mkdir -p %{buildroot}%{_bindir}

for i in extract make patch split ;do
install -pm0755 ${i}ps3iso/${i}ps3iso %{buildroot}%{_bindir}/
done


%files
%license LICENSE
%doc README.md readme.txt
%{_bindir}/extractps3iso
%{_bindir}/makeps3iso
%{_bindir}/patchps3iso
%{_bindir}/splitps3iso


%changelog
* Sat Mar 11 2023 Phantom X <megaphantomx at hotmail dot com> - 0-1.20220309git8780909
- Initial spec
