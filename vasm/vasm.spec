# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

# Build only m68k for blastem
%bcond_with m68k

%if %{with m68k}
%global cpu_list m68k
%global syntax_list mot
%global doc_list cpu_m68k syntax_mot vasm
%else
%global cpu_list 6502 6800 6809 arm c16x jagrisc m68k pdp11 ppc qnice test tr3200 vidcore x86 z80
%global syntax_list std madmac mot oldstyle
%global doc_list cpu_6502 cpu_jagrisc cpu_x86 output_bin output_test syntax_mot vasm_main cpu_6800 cpu_m68k cpu_z80 output_elf output_tos syntax_oldstyle cpu_arm cpu_ppc interface output_hunk output_vobj syntax_std cpu_c16x cpu_tr3200 output_aout output_srec syntax_madmac vasm
%endif

%global pkgver %%(c=%{version}; echo ${c//./_})

Name:           vasm
Version:        1.9
Release:        1%{?dist}
Summary:        Portable 6502 6800 arm c16x jagrisc m68k ppc vidcore x86 z80 assembler

License:        VASMBSD
URL:            http://sun.hasenbraten.de/vasm/

Source0:        http://phoenix.owl.de/tags/%{name}%{pkgver}.tar.gz

BuildRequires:  gcc
BuildRequires:  texinfo


%description
vasm is a portable and retargetable assembler to create linkable objects in
various formats or absolute code.

%prep
%autosetup -n %{name}

sed \
  -e 's|-O2|%{build_cflags}|g' \
  -e 's|-lm|%{build_ldflags} -Wl,-z,noexecstack \0|g' \
  -i Makefile

%build
for cpu in %{cpu_list}; do
  for syntax in %{syntax_list}; do
    %make_build CPU=${cpu} SYNTAX=${syntax}
  done
done

mkdir builddoc
for doc in %{doc_list} ;do
  makeinfo --plaintext --force --no-validate doc/${doc}.texi -o builddoc/${doc}
done

%install
mkdir -p %{buildroot}%{_bindir}
for cpu in %{cpu_list}; do
  for syntax in %{syntax_list}; do
    install -pm0755 "vasm${cpu}_${syntax}" %{buildroot}%{_bindir}/
  done
done

install -pm0755 vobjdump %{buildroot}%{_bindir}/

%files
%doc builddoc/*
%{_bindir}/*


%changelog
* Wed Mar 16 2022 - 1.9-1
- 1.9

* Sat Mar 27 2021 - 1.8j-1
- Initial spec
