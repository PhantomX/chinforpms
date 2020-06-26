Name:           vvvvvv-data
Version:        20161020
Release:        1%{?dist}
Summary:        VVVVVV Make and Play data files

License:        Free for no-commercial use
URL:            http://distractionware.com/blog/category/vvvvvv-make-and-play/

%global year    %(echo %{version} | cut -c1-4)
%global monthday %(echo %{version} | cut -c5-8)

# Windows release is better to extract
Source0:        http://www.flibitijibibo.com/VVVVVV-MP-%{monthday}%{year}.zip

BuildArch:      noarch

BuildRequires:  unzip
Requires:       vvvvvv >= 2.0

%description
%{summary}.

%prep
%autosetup -n VVVVVV-MP


%build

%install
mkdir -p %{buildroot}%{_datadir}/VVVVVV
install -pm 0644 data.zip %{buildroot}%{_datadir}/VVVVVV/


%files
%{_datadir}/VVVVVV/data.zip


%changelog
* Fri Jan 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 20161020-1
- Initial spec
