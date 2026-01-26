# prevent library files from being installed
%global cargo_install_lib 0

# Use vendor tarball
%bcond vendor 1

%global vendor_hash dbbe1a91a23f8f93bf2b0d4e4ba4e552

%global pkgname LACT
%global appname io.github.ilya_zlobintsev.%{pkgname}

Name:           lact
Version:        0.8.4
Release:        1%{?dist}
Summary:        GPU control utility

License:        MIT
URL:            https://github.com/ilya-zlobintsev/%{pkgname}

Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%if %{with vendor}
# cargo vendor-filterer --versioned-dirs --platform=x86_64-unknown-linux-gnu && tar --numeric-owner -cvJf ../%%{name}-%%{version}-vendor.tar.xz vendor/
Source1:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-%{version}-vendor.tar.xz/%{vendor_hash}/%{name}-%{version}-vendor.tar.xz
%endif

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  librsvg2-tools
BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  rust-packaging
BuildRequires:  clang
BuildRequires:  clinfo
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  systemd
BuildRequires:  vulkan-tools
Requires:       hwdata
Requires:       libdrm%{?_isa}
Requires:       vulkan-tools%{?_isa}
Requires:       clinfo

Requires:       hicolor-icon-theme

%if %{with vendor}
# for i in * ;do echo "Provides:       bundled(crate(${i%%-*})) = ${i##*-}";done
Provides:       bundled(crate(adler2)) = 2.0.1
Provides:       bundled(crate(adler32)) = 1.2.0
Provides:       bundled(crate(aho-corasick)) = 1.1.4
Provides:       bundled(crate(allocator-api2)) = 0.2.21
Provides:       bundled(crate(amdgpu-sysfs)) = 0.19.3
Provides:       bundled(crate(android_system_properties)) = 0.1.5
Provides:       bundled(crate(anstream)) = 0.6.21
Provides:       bundled(crate(anstyle)) = 1.0.13
Provides:       bundled(crate(anstyle-parse)) = 0.2.7
Provides:       bundled(crate(anstyle-query)) = 1.1.5
Provides:       bundled(crate(anstyle-wincon)) = 3.0.11
Provides:       bundled(crate(anyhow)) = 1.0.100
Provides:       bundled(crate(arc-swap)) = 1.8.0
Provides:       bundled(crate(async-broadcast)) = 0.7.2
Provides:       bundled(crate(async-recursion)) = 1.1.1
Provides:       bundled(crate(async-trait)) = 0.1.89
Provides:       bundled(crate(autocfg)) = 1.5.0
Provides:       bundled(crate(base64)) = 0.22.1
Provides:       bundled(crate(basic-toml)) = 0.1.10
Provides:       bundled(crate(bindgen)) = 0.71.1
Provides:       bundled(crate(bitflags)) = 1.3.2
Provides:       bundled(crate(bitflags)) = 2.10.0
Provides:       bundled(crate(block-buffer)) = 0.10.4
Provides:       bundled(crate(bumpalo)) = 3.19.1
Provides:       bundled(crate(bytes)) = 1.11.0
Provides:       bundled(crate(cairo-rs)) = 0.21.5
Provides:       bundled(crate(cairo-sys-rs)) = 0.21.5
Provides:       bundled(crate(cc)) = 1.2.51
Provides:       bundled(crate(cexpr)) = 0.6.0
Provides:       bundled(crate(cfg_aliases)) = 0.2.1
Provides:       bundled(crate(cfg-expr)) = 0.20.5
Provides:       bundled(crate(cfg-if)) = 1.0.4
Provides:       bundled(crate(chrono)) = 0.4.42
Provides:       bundled(crate(clang-sys)) = 1.8.1
Provides:       bundled(crate(clap)) = 4.5.53
Provides:       bundled(crate(clap_builder)) = 4.5.53
Provides:       bundled(crate(clap_derive)) = 4.5.49
Provides:       bundled(crate(clap_lex)) = 0.7.6
Provides:       bundled(crate(colorchoice)) = 1.0.4
Provides:       bundled(crate(concurrent-queue)) = 2.5.0
Provides:       bundled(crate(condtype)) = 1.3.0
Provides:       bundled(crate(console)) = 0.15.11
Provides:       bundled(crate(cookie)) = 0.18.1
Provides:       bundled(crate(cookie_store)) = 0.22.0
Provides:       bundled(crate(core2)) = 0.4.0
Provides:       bundled(crate(core-foundation-sys)) = 0.8.7
Provides:       bundled(crate(cpufeatures)) = 0.2.17
Provides:       bundled(crate(crc32fast)) = 1.5.0
Provides:       bundled(crate(crossbeam-utils)) = 0.8.21
Provides:       bundled(crate(crypto-common)) = 0.1.7
Provides:       bundled(crate(darling)) = 0.20.11
Provides:       bundled(crate(darling)) = 0.21.3
Provides:       bundled(crate(darling_core)) = 0.20.11
Provides:       bundled(crate(darling_core)) = 0.21.3
Provides:       bundled(crate(darling_macro)) = 0.20.11
Provides:       bundled(crate(darling_macro)) = 0.21.3
Provides:       bundled(crate(dary_heap)) = 0.3.8
Provides:       bundled(crate(deranged)) = 0.5.5
Provides:       bundled(crate(diff)) = 0.1.13
Provides:       bundled(crate(digest)) = 0.10.7
Provides:       bundled(crate(displaydoc)) = 0.2.5
Provides:       bundled(crate(divan)) = 0.1.21
Provides:       bundled(crate(divan-macros)) = 0.1.21
Provides:       bundled(crate(document-features)) = 0.2.12
Provides:       bundled(crate(easy_fuser)) = 0.4.3
Provides:       bundled(crate(either)) = 1.15.0
Provides:       bundled(crate(encode_unicode)) = 1.0.0
Provides:       bundled(crate(endi)) = 1.1.1
Provides:       bundled(crate(enum_dispatch)) = 0.3.13
Provides:       bundled(crate(enumflags2)) = 0.7.12
Provides:       bundled(crate(enumflags2_derive)) = 0.7.12
Provides:       bundled(crate(equivalent)) = 1.0.2
Provides:       bundled(crate(errno)) = 0.3.14
Provides:       bundled(crate(event-listener)) = 5.4.1
Provides:       bundled(crate(event-listener-strategy)) = 0.5.4
Provides:       bundled(crate(fastrand)) = 2.3.0
Provides:       bundled(crate(field-offset)) = 0.3.6
Provides:       bundled(crate(filetime)) = 0.2.26
Provides:       bundled(crate(find-crate)) = 0.6.3
Provides:       bundled(crate(find-msvc-tools)) = 0.1.6
Provides:       bundled(crate(flate2)) = 1.1.5
Provides:       bundled(crate(fluent)) = 0.17.0
Provides:       bundled(crate(fluent-bundle)) = 0.16.0
Provides:       bundled(crate(fluent-langneg)) = 0.13.1
Provides:       bundled(crate(fluent-syntax)) = 0.12.0
Provides:       bundled(crate(flume)) = 0.11.1
Provides:       bundled(crate(fnv)) = 1.0.7
Provides:       bundled(crate(foldhash)) = 0.2.0
Provides:       bundled(crate(form_urlencoded)) = 1.2.2
Provides:       bundled(crate(fragile)) = 2.0.1
Provides:       bundled(crate(fuser)) = 0.16.0
Provides:       bundled(crate(futures)) = 0.3.31
Provides:       bundled(crate(futures-channel)) = 0.3.31
Provides:       bundled(crate(futures-core)) = 0.3.31
Provides:       bundled(crate(futures-executor)) = 0.3.31
Provides:       bundled(crate(futures-io)) = 0.3.31
Provides:       bundled(crate(futures-lite)) = 2.6.1
Provides:       bundled(crate(futures-macro)) = 0.3.31
Provides:       bundled(crate(futures-sink)) = 0.3.31
Provides:       bundled(crate(futures-task)) = 0.3.31
Provides:       bundled(crate(futures-util)) = 0.3.31
Provides:       bundled(crate(gdk4)) = 0.10.3
Provides:       bundled(crate(gdk4-sys)) = 0.10.3
Provides:       bundled(crate(gdk-pixbuf)) = 0.21.5
Provides:       bundled(crate(gdk-pixbuf-sys)) = 0.21.5
Provides:       bundled(crate(generic-array)) = 0.14.7
Provides:       bundled(crate(getrandom)) = 0.2.16
Provides:       bundled(crate(getrandom)) = 0.3.4
Provides:       bundled(crate(gio)) = 0.21.5
Provides:       bundled(crate(gio-sys)) = 0.21.5
Provides:       bundled(crate(glib)) = 0.21.5
Provides:       bundled(crate(glib-macros)) = 0.21.5
Provides:       bundled(crate(glib-sys)) = 0.21.5
Provides:       bundled(crate(glob)) = 0.3.3
Provides:       bundled(crate(gobject-sys)) = 0.21.5
Provides:       bundled(crate(graphene-rs)) = 0.21.5
Provides:       bundled(crate(graphene-sys)) = 0.21.5
Provides:       bundled(crate(gsk4)) = 0.10.3
Provides:       bundled(crate(gsk4-sys)) = 0.10.3
Provides:       bundled(crate(gtk4)) = 0.10.3
Provides:       bundled(crate(gtk4-macros)) = 0.10.3
Provides:       bundled(crate(gtk4-sys)) = 0.10.3
Provides:       bundled(crate(hashbrown)) = 0.16.1
Provides:       bundled(crate(heck)) = 0.5.0
Provides:       bundled(crate(hermit-abi)) = 0.5.2
Provides:       bundled(crate(hex)) = 0.4.3
Provides:       bundled(crate(http)) = 1.4.0
Provides:       bundled(crate(httparse)) = 1.10.1
Provides:       bundled(crate(i18n-config)) = 0.4.8
Provides:       bundled(crate(i18n-embed)) = 0.16.0
Provides:       bundled(crate(i18n-embed-fl)) = 0.10.0
Provides:       bundled(crate(i18n-embed-impl)) = 0.8.4
Provides:       bundled(crate(iana-time-zone)) = 0.1.64
Provides:       bundled(crate(iana-time-zone-haiku)) = 0.1.2
Provides:       bundled(crate(icu_collections)) = 2.1.1
Provides:       bundled(crate(icu_locale_core)) = 2.1.1
Provides:       bundled(crate(icu_normalizer)) = 2.1.1
Provides:       bundled(crate(icu_normalizer_data)) = 2.1.1
Provides:       bundled(crate(icu_properties)) = 2.1.2
Provides:       bundled(crate(icu_properties_data)) = 2.1.2
Provides:       bundled(crate(icu_provider)) = 2.1.1
Provides:       bundled(crate(ident_case)) = 1.0.1
Provides:       bundled(crate(idna)) = 1.1.0
Provides:       bundled(crate(idna_adapter)) = 1.2.1
Provides:       bundled(crate(indexmap)) = 2.12.1
Provides:       bundled(crate(inotify)) = 0.11.0
Provides:       bundled(crate(inotify-sys)) = 0.1.5
Provides:       bundled(crate(insta)) = 1.45.0
Provides:       bundled(crate(intl-memoizer)) = 0.5.3
Provides:       bundled(crate(intl_pluralrules)) = 7.0.2
Provides:       bundled(crate(is_terminal_polyfill)) = 1.70.2
Provides:       bundled(crate(itertools)) = 0.13.0
Provides:       bundled(crate(itoa)) = 1.0.16
Provides:       bundled(crate(js-sys)) = 0.3.83
Provides:       bundled(crate(kqueue)) = 1.1.1
Provides:       bundled(crate(kqueue-sys)) = 1.0.4
Provides:       bundled(crate(lazy_static)) = 1.5.0
Provides:       bundled(crate(libadwaita)) = 0.8.1
Provides:       bundled(crate(libadwaita-sys)) = 0.8.1
Provides:       bundled(crate(libc)) = 0.2.178
Provides:       bundled(crate(libcopes)) = 1.0.0
Provides:       bundled(crate(libdrm_amdgpu_sys)) = 0.8.8
Provides:       bundled(crate(libflate)) = 2.2.1
Provides:       bundled(crate(libflate_lz77)) = 2.2.0
Provides:       bundled(crate(libloading)) = 0.8.9
Provides:       bundled(crate(libredox)) = 0.1.11
Provides:       bundled(crate(linux-raw-sys)) = 0.11.0
Provides:       bundled(crate(litemap)) = 0.8.1
Provides:       bundled(crate(litrs)) = 1.0.0
Provides:       bundled(crate(lock_api)) = 0.4.14
Provides:       bundled(crate(log)) = 0.4.29
Provides:       bundled(crate(matchers)) = 0.2.0
Provides:       bundled(crate(memchr)) = 2.7.6
Provides:       bundled(crate(memoffset)) = 0.9.1
Provides:       bundled(crate(minimal-lexical)) = 0.2.1
Provides:       bundled(crate(miniz_oxide)) = 0.8.9
Provides:       bundled(crate(mio)) = 1.1.1
Provides:       bundled(crate(nanorand)) = 0.7.0
Provides:       bundled(crate(nix)) = 0.29.0
Provides:       bundled(crate(nix)) = 0.30.1
Provides:       bundled(crate(nom)) = 7.1.3
Provides:       bundled(crate(notify)) = 8.2.0
Provides:       bundled(crate(notify-types)) = 2.0.0
Provides:       bundled(crate(nu-ansi-term)) = 0.50.3
Provides:       bundled(crate(num-conv)) = 0.1.0
Provides:       bundled(crate(num_cpus)) = 1.17.0
Provides:       bundled(crate(num_threads)) = 0.1.7
Provides:       bundled(crate(num-traits)) = 0.2.19
Provides:       bundled(crate(nvml-wrapper)) = 0.11.0
Provides:       bundled(crate(nvml-wrapper-sys)) = 0.9.0
Provides:       bundled(crate(once_cell)) = 1.21.3
Provides:       bundled(crate(once_cell_polyfill)) = 1.70.2
Provides:       bundled(crate(ordered-stream)) = 0.2.0
Provides:       bundled(crate(os-release)) = 0.1.0
Provides:       bundled(crate(page_size)) = 0.6.0
Provides:       bundled(crate(pango)) = 0.21.5
Provides:       bundled(crate(pango-sys)) = 0.21.5
Provides:       bundled(crate(parking)) = 2.2.1
Provides:       bundled(crate(parking_lot)) = 0.12.5
Provides:       bundled(crate(parking_lot_core)) = 0.9.12
Provides:       bundled(crate(pciid-parser)) = 0.8.0
Provides:       bundled(crate(percent-encoding)) = 2.3.2
Provides:       bundled(crate(pin-project-lite)) = 0.2.16
Provides:       bundled(crate(pin-utils)) = 0.1.0
Provides:       bundled(crate(pkg-config)) = 0.3.32
Provides:       bundled(crate(plotters)) = 0.3.7
Provides:       bundled(crate(plotters-backend)) = 0.3.7
Provides:       bundled(crate(plotters-cairo)) = 0.8.0
Provides:       bundled(crate(potential_utf)) = 0.1.4
Provides:       bundled(crate(powerfmt)) = 0.2.0
Provides:       bundled(crate(pretty_assertions)) = 1.4.1
Provides:       bundled(crate(prettyplease)) = 0.2.37
Provides:       bundled(crate(proc-macro2)) = 1.0.103
Provides:       bundled(crate(proc-macro-crate)) = 3.4.0
Provides:       bundled(crate(proc-macro-error2)) = 2.0.1
Provides:       bundled(crate(proc-macro-error-attr2)) = 2.0.0
Provides:       bundled(crate(quote)) = 1.0.42
Provides:       bundled(crate(redox_syscall)) = 0.5.18
Provides:       bundled(crate(redox_syscall)) = 0.6.0
Provides:       bundled(crate(r-efi)) = 5.3.0
Provides:       bundled(crate(regex)) = 1.12.2
Provides:       bundled(crate(regex-automata)) = 0.4.13
Provides:       bundled(crate(regex-lite)) = 0.1.8
Provides:       bundled(crate(regex-syntax)) = 0.8.8
Provides:       bundled(crate(relm4)) = 0.10.0
Provides:       bundled(crate(relm4-components)) = 0.10.0
Provides:       bundled(crate(relm4-css)) = 0.10.0
Provides:       bundled(crate(relm4-macros)) = 0.10.0
Provides:       bundled(crate(ring)) = 0.17.14
Provides:       bundled(crate(rle-decode-fast)) = 1.0.3
Provides:       bundled(crate(rustc-hash)) = 2.1.1
Provides:       bundled(crate(rustc_version)) = 0.4.1
Provides:       bundled(crate(rust-embed)) = 8.9.0
Provides:       bundled(crate(rust-embed-impl)) = 8.9.0
Provides:       bundled(crate(rust-embed-utils)) = 8.9.0
Provides:       bundled(crate(rustix)) = 1.1.3
Provides:       bundled(crate(rustls)) = 0.23.35
Provides:       bundled(crate(rustls-pki-types)) = 1.13.2
Provides:       bundled(crate(rustls-webpki)) = 0.103.8
Provides:       bundled(crate(rustversion)) = 1.0.22
Provides:       bundled(crate(ryu)) = 1.0.21
Provides:       bundled(crate(same-file)) = 1.0.6
Provides:       bundled(crate(scopeguard)) = 1.2.0
Provides:       bundled(crate(self_cell)) = 1.2.1
Provides:       bundled(crate(semver)) = 1.0.27
Provides:       bundled(crate(serde)) = 1.0.228
Provides:       bundled(crate(serde_core)) = 1.0.228
Provides:       bundled(crate(serde_derive)) = 1.0.228
Provides:       bundled(crate(serde-error)) = 0.1.3
Provides:       bundled(crate(serde_json)) = 1.0.147
Provides:       bundled(crate(serde_norway)) = 0.9.42
Provides:       bundled(crate(serde_repr)) = 0.1.20
Provides:       bundled(crate(serde_spanned)) = 1.0.4
Provides:       bundled(crate(serde_with)) = 3.16.1
Provides:       bundled(crate(serde_with_macros)) = 3.16.1
Provides:       bundled(crate(sha2)) = 0.10.9
Provides:       bundled(crate(sharded-slab)) = 0.1.7
Provides:       bundled(crate(shlex)) = 1.3.0
Provides:       bundled(crate(signal-hook-registry)) = 1.4.8
Provides:       bundled(crate(simd-adler32)) = 0.3.8
Provides:       bundled(crate(similar)) = 2.7.0
Provides:       bundled(crate(slab)) = 0.4.11
Provides:       bundled(crate(smallvec)) = 1.15.1
Provides:       bundled(crate(socket2)) = 0.6.1
Provides:       bundled(crate(spin)) = 0.9.8
Provides:       bundled(crate(stable_deref_trait)) = 1.2.1
Provides:       bundled(crate(static_assertions)) = 1.1.0
Provides:       bundled(crate(strsim)) = 0.11.1
Provides:       bundled(crate(subtle)) = 2.6.1
Provides:       bundled(crate(syn)) = 2.0.111
Provides:       bundled(crate(synstructure)) = 0.13.2
Provides:       bundled(crate(sys-locale)) = 0.3.2
Provides:       bundled(crate(system-deps)) = 7.0.7
Provides:       bundled(crate(tar)) = 0.4.44
Provides:       bundled(crate(target-lexicon)) = 0.13.3
Provides:       bundled(crate(tempfile)) = 3.24.0
Provides:       bundled(crate(terminal_size)) = 0.4.3
Provides:       bundled(crate(thiserror)) = 1.0.69
Provides:       bundled(crate(thiserror)) = 2.0.17
Provides:       bundled(crate(thiserror-impl)) = 1.0.69
Provides:       bundled(crate(thiserror-impl)) = 2.0.17
Provides:       bundled(crate(thread_local)) = 1.1.9
Provides:       bundled(crate(threadpool)) = 1.8.1
Provides:       bundled(crate(thread-priority)) = 3.0.0
Provides:       bundled(crate(time)) = 0.3.44
Provides:       bundled(crate(time-core)) = 0.1.6
Provides:       bundled(crate(time-macros)) = 0.2.24
Provides:       bundled(crate(tinystr)) = 0.8.2
Provides:       bundled(crate(tokio)) = 1.48.0
Provides:       bundled(crate(tokio-macros)) = 2.6.0
Provides:       bundled(crate(toml)) = 0.5.11
Provides:       bundled(crate(toml-0.9.10+spec)) = 1.1.0
Provides:       bundled(crate(toml_datetime-0.7.5+spec)) = 1.1.0
Provides:       bundled(crate(toml_edit-0.23.10+spec)) = 1.0.0
Provides:       bundled(crate(toml_parser-1.0.6+spec)) = 1.1.0
Provides:       bundled(crate(toml_writer-1.0.6+spec)) = 1.1.0
Provides:       bundled(crate(tracing)) = 0.1.44
Provides:       bundled(crate(tracing-attributes)) = 0.1.31
Provides:       bundled(crate(tracing-core)) = 0.1.36
Provides:       bundled(crate(tracing-log)) = 0.2.0
Provides:       bundled(crate(tracing-subscriber)) = 0.3.22
Provides:       bundled(crate(tracker)) = 0.2.2
Provides:       bundled(crate(tracker-macros)) = 0.2.2
Provides:       bundled(crate(type-map)) = 0.5.1
Provides:       bundled(crate(typenum)) = 1.19.0
Provides:       bundled(crate(uds_windows)) = 1.1.0
Provides:       bundled(crate(unic-langid)) = 0.9.6
Provides:       bundled(crate(unic-langid-impl)) = 0.9.6
Provides:       bundled(crate(unicode-ident)) = 1.0.22
Provides:       bundled(crate(unsafe-libyaml-norway)) = 0.2.15
Provides:       bundled(crate(untrusted)) = 0.9.0
Provides:       bundled(crate(ureq)) = 3.1.4
Provides:       bundled(crate(ureq-proto)) = 0.5.3
Provides:       bundled(crate(url)) = 2.5.7
Provides:       bundled(crate(utf-8)) = 0.7.6
Provides:       bundled(crate(utf8_iter)) = 1.0.4
Provides:       bundled(crate(utf8parse)) = 0.2.2
Provides:       bundled(crate(uuid)) = 1.19.0
Provides:       bundled(crate(valuable)) = 0.1.1
Provides:       bundled(crate(vergen)) = 8.3.2
Provides:       bundled(crate(version_check)) = 0.9.5
Provides:       bundled(crate(version-compare)) = 0.2.1
Provides:       bundled(crate(walkdir)) = 2.5.0
Provides:       bundled(crate(wasi-0.11.1+wasi-snapshot)) = preview1
Provides:       bundled(crate(wasip2-1.0.1+wasi)) = 0.2.4
Provides:       bundled(crate(wasm-bindgen)) = 0.2.106
Provides:       bundled(crate(wasm-bindgen-macro)) = 0.2.106
Provides:       bundled(crate(wasm-bindgen-macro-support)) = 0.2.106
Provides:       bundled(crate(wasm-bindgen-shared)) = 0.2.106
Provides:       bundled(crate(webpki-roots)) = 1.0.4
Provides:       bundled(crate(web-sys)) = 0.3.83
Provides:       bundled(crate(winapi)) = 0.3.9
Provides:       bundled(crate(winapi-i686-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(winapi-util)) = 0.1.11
Provides:       bundled(crate(winapi-x86_64-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(windows)) = 0.61.3
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.53.1
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.52.6
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.53.1
Provides:       bundled(crate(windows-collections)) = 0.2.0
Provides:       bundled(crate(windows-core)) = 0.61.2
Provides:       bundled(crate(windows-core)) = 0.62.2
Provides:       bundled(crate(windows-future)) = 0.2.1
Provides:       bundled(crate(windows_i686_gnu)) = 0.52.6
Provides:       bundled(crate(windows_i686_gnu)) = 0.53.1
Provides:       bundled(crate(windows_i686_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_i686_gnullvm)) = 0.53.1
Provides:       bundled(crate(windows_i686_msvc)) = 0.52.6
Provides:       bundled(crate(windows_i686_msvc)) = 0.53.1
Provides:       bundled(crate(windows-implement)) = 0.60.2
Provides:       bundled(crate(windows-interface)) = 0.59.3
Provides:       bundled(crate(windows-link)) = 0.1.3
Provides:       bundled(crate(windows-link)) = 0.2.1
Provides:       bundled(crate(windows-numerics)) = 0.2.0
Provides:       bundled(crate(windows-result)) = 0.3.4
Provides:       bundled(crate(windows-result)) = 0.4.1
Provides:       bundled(crate(windows-strings)) = 0.4.2
Provides:       bundled(crate(windows-strings)) = 0.5.1
Provides:       bundled(crate(windows-sys)) = 0.52.0
Provides:       bundled(crate(windows-sys)) = 0.59.0
Provides:       bundled(crate(windows-sys)) = 0.60.2
Provides:       bundled(crate(windows-sys)) = 0.61.2
Provides:       bundled(crate(windows-targets)) = 0.52.6
Provides:       bundled(crate(windows-targets)) = 0.53.5
Provides:       bundled(crate(windows-threading)) = 0.1.0
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.53.1
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.53.1
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.53.1
Provides:       bundled(crate(winnow)) = 0.7.14
Provides:       bundled(crate(wit-bindgen)) = 0.46.0
Provides:       bundled(crate(wrapcenum-derive)) = 0.4.1
Provides:       bundled(crate(writeable)) = 0.6.2
Provides:       bundled(crate(xattr)) = 1.6.1
Provides:       bundled(crate(yansi)) = 1.0.1
Provides:       bundled(crate(yoke)) = 0.8.1
Provides:       bundled(crate(yoke-derive)) = 0.8.1
Provides:       bundled(crate(zbus)) = 5.12.0
Provides:       bundled(crate(zbus_macros)) = 5.12.0
Provides:       bundled(crate(zbus_names)) = 4.2.0
Provides:       bundled(crate(zerocopy)) = 0.8.31
Provides:       bundled(crate(zerocopy-derive)) = 0.8.31
Provides:       bundled(crate(zerofrom)) = 0.1.6
Provides:       bundled(crate(zerofrom-derive)) = 0.1.6
Provides:       bundled(crate(zeroize)) = 1.8.2
Provides:       bundled(crate(zerotrie)) = 0.2.3
Provides:       bundled(crate(zerovec)) = 0.11.5
Provides:       bundled(crate(zerovec-derive)) = 0.11.2
Provides:       bundled(crate(zmij)) = 0.1.9
Provides:       bundled(crate(zvariant)) = 5.8.0
Provides:       bundled(crate(zvariant_derive)) = 5.8.0
Provides:       bundled(crate(zvariant_utils)) = 3.2.1
%endif


%description
LACT is a GPU control utility.


%prep
%autosetup -p1 -n %{pkgname}-%{version} %{?with_vendor:-a1}

find -name '*.rs' -exec chmod -x {} ';'

sed -e '/^ExecStart=/s|=.*$|=%{_bindir}/lact daemon|' -i res/%{name}d.service

rm -f Cargo.lock

%if %{with vendor}
%cargo_prep -v vendor
%else
%generate_buildrequires
%cargo_generate_buildrequires
%endif


%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%if %{with vendor}
%{cargo_vendor_manifest}
%endif


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_unitdir}
install -pm0644 res/%{name}d.service %{buildroot}%{_unitdir}/%{name}d.service

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  res/%{appname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -pm0644 res/%{appname}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{appname}.svg

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
install -pm0644 res/%{appname}.png \
  %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{appname}.png

for res in 16 22 24 32 36 48 64 72 96 128 192 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  rsvg-convert res/%{appname}.svg -h ${res} -w ${res} \
    -o ${dir}/%{appname}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 res/%{appname}.metainfo.xml %{buildroot}%{_metainfodir}/


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%post
%systemd_post %{name}d.service

%preun
%systemd_preun %{name}d.service

%postun
%systemd_postun_with_restart %{name}d.service


%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc README.md
%{_bindir}/%{name}
%{_unitdir}/%{name}d.service
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/*/%{appname}*
%{_metainfodir}/%{appname}.metainfo.xml


%changelog
* Sun Jan 25 2026 Phantom X <megaphantomx at hotmail dot com> - 0.8.4-1
- 0.8.4

* Tue Nov 25 2025 Phantom X <megaphantomx at hotmail dot com> - 0.8.3-1
- Initial spec
