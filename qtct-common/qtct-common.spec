BuildArch:      noarch

Name:           qtct-common
Version:        1
Release:        1%{?dist}
Summary:        Common files for qt5ct and qt6ct

License:        LicenseRef-Fedora-Public-Domain
URL:            https://github.com/PhantomX/chinforpms

Source0:        60-qtct.sh

Requires:       (qt6ct or qt5ct)
Requires:       xorg-x11-xinit
Enhances:       qt5ct
Enhances:       qt6ct


%description
%{summary}.

This contains a xinit profile.


%prep
%autosetup -c -T


%build


%install
mkdir -p %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d
install -pm0755 %{S:0} \
  %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/60-qtct.sh


%files
%{_sysconfdir}/X11/xinit/xinitrc.d/60-qtct.sh


%changelog
* Fri Oct 31 2025 Phantom X <megaphantomx at hotmail dot com> - 1-1
- Initial spec
