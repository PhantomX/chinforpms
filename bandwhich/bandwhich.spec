%bcond_with bin

%if %{with bin}
%global _build_id_links none
%undefine _debugsource_packages
%else
# Use vendor tarball
%bcond_without vendor
%endif

%global vc_id   acd1b0a95dbc2ee245648f2d5ef75494cf1cba54
%global vendor_hash d13224b2fd01d467dbc91c7035c9fb0d

Name:           bandwhich
Version:        0.23.1
Release:        1%{?dist}
Summary:        Terminal bandwidth utilization tool

License:        MIT
URL:            https://github.com/imsnif/%{name}

%if %{with bin}
Source0:        %{url}/releases/download/v%{version}/%{name}-v%{version}-x86_64-unknown-linux-gnu.tar.gz
Source1:        %{url}/raw/%{vc_id}/LICENSE.md
Source2:        %{url}/raw/%{vc_id}/README.md
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%if %{with vendor}
# rust2rpm -t fedora -V --no-rpmautospec --ignore-missing-license-files ./Cargo.toml %%{version}
Source1:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-%{version}-vendor.tar.xz/%{vendor_hash}/%{name}-%{version}-vendor.tar.xz
%endif

Patch0:         bandwhich-fix-metadata-auto.patch
%endif

%if %{with bin}
ExclusiveArch:  x86_64
%else
ExclusiveArch:  %{rust_arches}
%endif

%if %{without bin}
BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  rust-packaging
%if %{with vendor}
# for i in * ;do echo "Provides:       bundled(crate(${i%%-*})) = ${i##*-}";done
Provides:       bundled(crate(addr2line)) = 0.24.2
Provides:       bundled(crate(adler2)) = 2.0.0
Provides:       bundled(crate(aho-corasick)) = 1.1.3
Provides:       bundled(crate(allocator-api2)) = 0.2.18
Provides:       bundled(crate(android_system_properties)) = 0.1.5
Provides:       bundled(crate(android-tzdata)) = 0.1.1
Provides:       bundled(crate(anstream)) = 0.6.15
Provides:       bundled(crate(anstyle)) = 1.0.8
Provides:       bundled(crate(anstyle-parse)) = 0.2.5
Provides:       bundled(crate(anstyle-query)) = 1.1.1
Provides:       bundled(crate(anstyle-wincon)) = 3.0.4
Provides:       bundled(crate(anyhow)) = 1.0.89
Provides:       bundled(crate(async-trait)) = 0.1.83
Provides:       bundled(crate(autocfg)) = 1.4.0
Provides:       bundled(crate(backtrace)) = 0.3.74
Provides:       bundled(crate(bitflags)) = 2.6.0
Provides:       bundled(crate(bumpalo)) = 3.16.0
Provides:       bundled(crate(byteorder)) = 1.5.0
Provides:       bundled(crate(bytes)) = 1.7.2
Provides:       bundled(crate(cassowary)) = 0.3.0
Provides:       bundled(crate(castaway)) = 0.2.3
Provides:       bundled(crate(cc)) = 1.1.28
Provides:       bundled(crate(cfg-if)) = 1.0.0
Provides:       bundled(crate(chrono)) = 0.4.38
Provides:       bundled(crate(clap)) = 4.5.19
Provides:       bundled(crate(clap_builder)) = 4.5.19
Provides:       bundled(crate(clap_complete)) = 4.5.32
Provides:       bundled(crate(clap_derive)) = 4.5.18
Provides:       bundled(crate(clap_lex)) = 0.7.2
Provides:       bundled(crate(clap_mangen)) = 0.2.23
Provides:       bundled(crate(clap-verbosity-flag)) = 2.2.2
Provides:       bundled(crate(colorchoice)) = 1.0.2
Provides:       bundled(crate(compact_str)) = 0.8.0
Provides:       bundled(crate(console)) = 0.15.8
Provides:       bundled(crate(core-foundation-sys)) = 0.8.7
Provides:       bundled(crate(crc32fast)) = 1.4.2
Provides:       bundled(crate(crossterm)) = 0.28.1
Provides:       bundled(crate(crossterm_winapi)) = 0.9.1
Provides:       bundled(crate(data-encoding)) = 2.6.0
Provides:       bundled(crate(deranged)) = 0.3.11
Provides:       bundled(crate(derivative)) = 2.2.0
Provides:       bundled(crate(derive-new)) = 0.5.9
Provides:       bundled(crate(either)) = 1.13.0
Provides:       bundled(crate(encode_unicode)) = 0.3.6
Provides:       bundled(crate(enum-as-inner)) = 0.6.1
Provides:       bundled(crate(equivalent)) = 1.0.1
Provides:       bundled(crate(errno)) = 0.3.9
Provides:       bundled(crate(flate2)) = 1.0.34
Provides:       bundled(crate(foldhash)) = 0.1.3
Provides:       bundled(crate(form_urlencoded)) = 1.2.1
Provides:       bundled(crate(futures)) = 0.3.31
Provides:       bundled(crate(futures-channel)) = 0.3.31
Provides:       bundled(crate(futures-core)) = 0.3.31
Provides:       bundled(crate(futures-executor)) = 0.3.31
Provides:       bundled(crate(futures-io)) = 0.3.31
Provides:       bundled(crate(futures-macro)) = 0.3.31
Provides:       bundled(crate(futures-sink)) = 0.3.31
Provides:       bundled(crate(futures-task)) = 0.3.31
Provides:       bundled(crate(futures-timer)) = 3.0.3
Provides:       bundled(crate(futures-util)) = 0.3.31
Provides:       bundled(crate(getrandom)) = 0.2.15
Provides:       bundled(crate(gimli)) = 0.31.1
Provides:       bundled(crate(glob)) = 0.3.1
Provides:       bundled(crate(hashbrown)) = 0.15.0
Provides:       bundled(crate(heck)) = 0.5.0
Provides:       bundled(crate(hermit-abi)) = 0.3.9
Provides:       bundled(crate(hex)) = 0.4.3
Provides:       bundled(crate(hostname)) = 0.3.1
Provides:       bundled(crate(iana-time-zone)) = 0.1.61
Provides:       bundled(crate(iana-time-zone-haiku)) = 0.1.2
Provides:       bundled(crate(idna)) = 0.4.0
Provides:       bundled(crate(idna)) = 0.5.0
Provides:       bundled(crate(indexmap)) = 2.6.0
Provides:       bundled(crate(insta)) = 1.40.0
Provides:       bundled(crate(instability)) = 0.3.2
Provides:       bundled(crate(ipconfig)) = 0.3.2
Provides:       bundled(crate(ipnet)) = 2.10.1
Provides:       bundled(crate(ipnetwork)) = 0.20.0
Provides:       bundled(crate(is_terminal_polyfill)) = 1.70.1
Provides:       bundled(crate(itertools)) = 0.13.0
Provides:       bundled(crate(itoa)) = 1.0.11
Provides:       bundled(crate(js-sys)) = 0.3.70
Provides:       bundled(crate(lazy_static)) = 1.5.0
Provides:       bundled(crate(libc)) = 0.2.159
Provides:       bundled(crate(linked-hash-map)) = 0.5.6
Provides:       bundled(crate(linux-raw-sys)) = 0.4.14
Provides:       bundled(crate(lock_api)) = 0.4.12
Provides:       bundled(crate(log)) = 0.4.22
Provides:       bundled(crate(lru)) = 0.12.5
Provides:       bundled(crate(lru-cache)) = 0.1.2
Provides:       bundled(crate(match_cfg)) = 0.1.0
Provides:       bundled(crate(memchr)) = 2.7.4
Provides:       bundled(crate(miniz_oxide)) = 0.8.0
Provides:       bundled(crate(mio)) = 1.0.2
Provides:       bundled(crate(no-std-net)) = 0.6.0
Provides:       bundled(crate(num-conv)) = 0.1.0
Provides:       bundled(crate(num_threads)) = 0.1.7
Provides:       bundled(crate(num-traits)) = 0.2.19
Provides:       bundled(crate(object)) = 0.36.5
Provides:       bundled(crate(once_cell)) = 1.20.2
Provides:       bundled(crate(packet-builder)) = 0.7.0
Provides:       bundled(crate(parking_lot)) = 0.12.3
Provides:       bundled(crate(parking_lot_core)) = 0.9.10
Provides:       bundled(crate(paste)) = 1.0.15
Provides:       bundled(crate(percent-encoding)) = 2.3.1
Provides:       bundled(crate(pin-project-lite)) = 0.2.14
Provides:       bundled(crate(pin-utils)) = 0.1.0
Provides:       bundled(crate(pnet)) = 0.34.0
Provides:       bundled(crate(pnet_base)) = 0.34.0
Provides:       bundled(crate(pnet_datalink)) = 0.34.0
Provides:       bundled(crate(pnet_macros)) = 0.34.0
Provides:       bundled(crate(pnet_macros_support)) = 0.34.0
Provides:       bundled(crate(pnet_packet)) = 0.34.0
Provides:       bundled(crate(pnet_sys)) = 0.34.0
Provides:       bundled(crate(pnet_transport)) = 0.34.0
Provides:       bundled(crate(powerfmt)) = 0.2.0
Provides:       bundled(crate(ppv-lite86)) = 0.2.20
Provides:       bundled(crate(procfs)) = 0.17.0
Provides:       bundled(crate(procfs-core)) = 0.17.0
Provides:       bundled(crate(proc-macro2)) = 1.0.87
Provides:       bundled(crate(proc-macro-crate)) = 3.2.0
Provides:       bundled(crate(quick-error)) = 1.2.3
Provides:       bundled(crate(quote)) = 1.0.37
Provides:       bundled(crate(rand)) = 0.8.5
Provides:       bundled(crate(rand_chacha)) = 0.3.1
Provides:       bundled(crate(rand_core)) = 0.6.4
Provides:       bundled(crate(ratatui)) = 0.28.1
Provides:       bundled(crate(redox_syscall)) = 0.5.7
Provides:       bundled(crate(regex)) = 1.11.0
Provides:       bundled(crate(regex-automata)) = 0.4.8
Provides:       bundled(crate(regex-syntax)) = 0.8.5
Provides:       bundled(crate(relative-path)) = 1.9.3
Provides:       bundled(crate(resolv-conf)) = 0.7.0
Provides:       bundled(crate(roff)) = 0.2.2
Provides:       bundled(crate(rstest)) = 0.23.0
Provides:       bundled(crate(rstest_macros)) = 0.23.0
Provides:       bundled(crate(rustc-demangle)) = 0.1.24
Provides:       bundled(crate(rustc_version)) = 0.4.1
Provides:       bundled(crate(rustix)) = 0.38.37
Provides:       bundled(crate(rustversion)) = 1.0.17
Provides:       bundled(crate(ryu)) = 1.0.18
Provides:       bundled(crate(scopeguard)) = 1.2.0
Provides:       bundled(crate(semver)) = 1.0.23
Provides:       bundled(crate(serde)) = 1.0.210
Provides:       bundled(crate(serde_derive)) = 1.0.210
Provides:       bundled(crate(shlex)) = 1.3.0
Provides:       bundled(crate(signal-hook)) = 0.3.17
Provides:       bundled(crate(signal-hook-mio)) = 0.2.4
Provides:       bundled(crate(signal-hook-registry)) = 1.4.2
Provides:       bundled(crate(similar)) = 2.6.0
Provides:       bundled(crate(simplelog)) = 0.12.2
Provides:       bundled(crate(slab)) = 0.4.9
Provides:       bundled(crate(smallvec)) = 1.13.2
Provides:       bundled(crate(socket2)) = 0.5.7
Provides:       bundled(crate(static_assertions)) = 1.1.0
Provides:       bundled(crate(strsim)) = 0.11.1
Provides:       bundled(crate(strum)) = 0.26.3
Provides:       bundled(crate(strum_macros)) = 0.26.4
Provides:       bundled(crate(syn)) = 1.0.109
Provides:       bundled(crate(syn)) = 2.0.79
Provides:       bundled(crate(termcolor)) = 1.4.1
Provides:       bundled(crate(thiserror)) = 1.0.64
Provides:       bundled(crate(thiserror-impl)) = 1.0.64
Provides:       bundled(crate(time)) = 0.3.36
Provides:       bundled(crate(time-core)) = 0.1.2
Provides:       bundled(crate(time-macros)) = 0.2.18
Provides:       bundled(crate(tinyvec)) = 1.8.0
Provides:       bundled(crate(tinyvec_macros)) = 0.1.1
Provides:       bundled(crate(tokio)) = 1.40.0
Provides:       bundled(crate(toml_datetime)) = 0.6.8
Provides:       bundled(crate(toml_edit)) = 0.22.22
Provides:       bundled(crate(tracing)) = 0.1.40
Provides:       bundled(crate(tracing-attributes)) = 0.1.27
Provides:       bundled(crate(tracing-core)) = 0.1.32
Provides:       bundled(crate(trust-dns-proto)) = 0.23.2
Provides:       bundled(crate(trust-dns-resolver)) = 0.23.2
Provides:       bundled(crate(unicode-bidi)) = 0.3.17
Provides:       bundled(crate(unicode-ident)) = 1.0.13
Provides:       bundled(crate(unicode-normalization)) = 0.1.24
Provides:       bundled(crate(unicode-segmentation)) = 1.12.0
Provides:       bundled(crate(unicode-truncate)) = 1.1.0
Provides:       bundled(crate(unicode-width)) = 0.1.14
Provides:       bundled(crate(unicode-width)) = 0.2.0
Provides:       bundled(crate(url)) = 2.5.2
Provides:       bundled(crate(utf8parse)) = 0.2.2
Provides:       bundled(crate(wasi-0.11.0+wasi-snapshot)) = preview1
Provides:       bundled(crate(wasm-bindgen)) = 0.2.93
Provides:       bundled(crate(wasm-bindgen-backend)) = 0.2.93
Provides:       bundled(crate(wasm-bindgen-macro)) = 0.2.93
Provides:       bundled(crate(wasm-bindgen-macro-support)) = 0.2.93
Provides:       bundled(crate(wasm-bindgen-shared)) = 0.2.93
Provides:       bundled(crate(widestring)) = 1.1.0
Provides:       bundled(crate(winapi)) = 0.3.9
Provides:       bundled(crate(winapi-i686-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(winapi-util)) = 0.1.9
Provides:       bundled(crate(winapi-x86_64-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.48.5
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.48.5
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.52.6
Provides:       bundled(crate(windows-core)) = 0.52.0
Provides:       bundled(crate(windows_i686_gnu)) = 0.48.5
Provides:       bundled(crate(windows_i686_gnu)) = 0.52.6
Provides:       bundled(crate(windows_i686_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_i686_msvc)) = 0.48.5
Provides:       bundled(crate(windows_i686_msvc)) = 0.52.6
Provides:       bundled(crate(windows-sys)) = 0.48.0
Provides:       bundled(crate(windows-sys)) = 0.52.0
Provides:       bundled(crate(windows-sys)) = 0.59.0
Provides:       bundled(crate(windows-targets)) = 0.48.5
Provides:       bundled(crate(windows-targets)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.52.6
Provides:       bundled(crate(winnow)) = 0.6.20
Provides:       bundled(crate(winreg)) = 0.50.0
Provides:       bundled(crate(zerocopy)) = 0.7.35
Provides:       bundled(crate(zerocopy-derive)) = 0.7.35
%endif
%endif

%description
%{name} is a CLI utility for displaying current network utilization by process,
connection and remote IP/hostname.


%prep
%if %{with bin}
%autosetup -c

cp -p %{S:1} %{S:2} %{S:3} .
%else
%autosetup -p1 %{?with_vendor:-a1}

sed -e '/^packet-builder/s|, git =.*$| }|g' -i Cargo.toml

%if %{with vendor}
%cargo_prep -v vendor
%endif

%generate_buildrequires
%if %{with vendor}
%cargo_vendor_manifest
%else
%cargo_generate_buildrequires
%endif
%endif


%build
%if %{without bin}
%cargo_build
mv target/release/%{name} .
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%endif

%install
mkdir -p %{buildroot}%{_sbindir}
install -pm0755 %{name} %{buildroot}%{_sbindir}/


%files
%license LICENSE.md
%doc README.md
%{_sbindir}/%{name}


%changelog
* Fri Nov 15 2024 Phantom X <megaphantomx at hotmail dot com> - 0.23.1-1
- 0.23.1
- Source support, with vendored tarball switch

* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 0.23.0-1
- 0.23.0

* Wed Mar 06 2024 Phantom X <megaphantomx at hotmail dot com> - 0.22.2-1
- 0.22.2

* Fri Feb 18 2022 Phantom X <megaphantomx at hotmail dot com> - 0.20.0-1
- Initial spec
