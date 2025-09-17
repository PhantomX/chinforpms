# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

Name:           bh-fonts
Version:        1.0.3
Release:        8%{?dist}
Summary:        X.Org BH TTF fonts

License:        LicenseRef-Fedora-BH-Luxi
URL:            http://www.x.org

BuildArch:      noarch

%global priority 42

%global foundry           bh
%global fontlicense       LicenseRef-Fedora-BH-Luxi
%global fontlicenses      COPYING COPYRIGHT.BH
%global fontdocs          ChangeLog README
%global fontdocsex        %{fontlicenses}

%global archivename font-%{foundry}-ttf-%{version}

%global common_description %{expand:
X.Org Bigelow & Holmes TrueType fonts.}


%global fontfamily1       Luxi Sans
%global fontsummary1      BH variable-width sans-serif font faces
%global fontpkgheader1    %{expand:
Obsoletes: bh-fonts-common < %{version}-%{release}
Obsoletes: bh-sans-fonts < %{version}-%{release}
}
%global fonts1            luxis*.ttf
%global fontconfs1        %{S:11}
%global fontappstreams1   %{S:31}
%global fontdescription1  %{expand:
%{common_description}

This package consists of the BH Luxi sans-serif variable-width font faces.
}

%global fontfamily2       Luxi Serif
%global fontsummary2      BH variable-width serif font faces
%global fontpkgheader2    %{expand:
Obsoletes: bh-fonts-common < %{version}-%{release}
Obsoletes: bh-serif-fonts < %{version}-%{release}
}
%global fonts2            luxir*.ttf
%global fontconfs2        %{S:12}
%global fontappstreams2   %{S:32}
%global fontdescription2  %{expand:
%{common_description}

This package consists of the BH Luxi serif variable-width font faces.
}

%global fontfamily3       Luxi Mono
%global fontsummary3      BH monospace font faces
%global fontpkgheader3    %{expand:
Obsoletes: bh-fonts-common < %{version}-%{release}
Obsoletes: bh-mono-fonts < %{version}-%{release}
}
%global fonts3            luxim*.ttf
%global fontconfs3        %{S:13}
%global fontappstreams3   %{S:33}
%global fontdescription3  %{expand:
%{common_description}

This package consists of the BH sans-serif monospace font faces.
}

Source0:        http://xorg.freedesktop.org/releases/individual/font/%{archivename}.tar.bz2
Source11:       %{priority}-%{fontpkgname1}.conf
Source12:       %{priority}-%{fontpkgname2}.conf
Source13:       %{priority}-%{fontpkgname3}.conf
Source31:       %{fontpkgname1}.metainfo.xml
Source32:       %{fontpkgname2}.metainfo.xml
Source33:       %{fontpkgname3}.metainfo.xml

%description
%wordwrap -v common_description

%fontpkg -a

%fontmetapkg

%package   doc
Summary:   Optional documentation files of %{name}
BuildArch: noarch
%description doc
This package provides optional documentation files shipped with
%{name}.

%prep
%autosetup -n %{archivename}


%build
%fontbuild -a

%install
%fontinstall -a

%check
%fontcheck -a

%fontfiles -a

%files doc
%defattr(644, root, root, 0755)
%license %{fontlicenses}
%doc %{fontdocs}

%changelog
* Wed Sep 17 2025 Phantom X <megaphantomx at hotmail dot com> - 1.0.3-8
- Update license file

* Sat Sep 16 2023 - 1.0.3-7
- Set system-ui configuration

* Wed Sep 30 2020 - 1.0.3-6
- Update conf files

* Thu Mar 19 2020 - 1.0.3-5
- Convert to new fonts template

* Tue Oct 09 2018 - 1.0.3-4
- BR: gcc

* Thu Jun 15 2017 - 1.0.3-3
- BR: xorg-x11-font-utils

* Sun Feb 05 2017 - 1.0.3-2
- Try to follow Fedora font packaging guidelines

* Wed Dec 28 2016 - 1.0.3-1
- Initial spec
