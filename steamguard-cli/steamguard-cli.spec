# prevent library files from being installed
%global cargo_install_lib 0

# Use vendor tarball
%bcond vendor 1

%global vendor_hash 63fe011c8eb9893d231bde129a31dc47

Name:           steamguard-cli
Version:        0.18.4
Release:        1%{?dist}
Summary:        Command line utility to generate Steam 2FA codes

License:        GPL-3.0-or-later
URL:            https://github.com/dyc3/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%if %{with vendor}
# cargo vendor --versioned-dirs && tar --numeric-owner -cvJf ../%%{name}-%%{version}-vendor.tar.xz vendor/
Source1:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-%{version}-vendor.tar.xz/%{vendor_hash}/%{name}-%{version}-vendor.tar.xz
%endif

ExclusiveArch:  %{rust_arches}

BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  rust-packaging
%if %{with vendor}
# for i in * ;do echo "Provides:       bundled(crate(${i%%-*})) = ${i##*-}";done
Provides:       bundled(crate(adler2)) = 2.0.1
Provides:       bundled(crate(aes)) = 0.8.4
Provides:       bundled(crate(aho-corasick)) = 1.1.4
Provides:       bundled(crate(aligned)) = 0.4.3
Provides:       bundled(crate(aligned-vec)) = 0.6.4
Provides:       bundled(crate(allocator-api2)) = 0.2.21
Provides:       bundled(crate(android_system_properties)) = 0.1.5
Provides:       bundled(crate(anstream)) = 1.0.0
Provides:       bundled(crate(anstyle)) = 1.0.14
Provides:       bundled(crate(anstyle-parse)) = 1.0.0
Provides:       bundled(crate(anstyle-query)) = 1.1.5
Provides:       bundled(crate(anstyle-wincon)) = 3.0.11
Provides:       bundled(crate(anyhow)) = 1.0.102
Provides:       bundled(crate(arbitrary)) = 1.4.2
Provides:       bundled(crate(arg_enum_proc_macro)) = 0.3.4
Provides:       bundled(crate(argon2)) = 0.5.3
Provides:       bundled(crate(arrayvec)) = 0.7.6
Provides:       bundled(crate(as-slice)) = 0.2.1
Provides:       bundled(crate(async-broadcast)) = 0.5.1
Provides:       bundled(crate(async-channel)) = 2.5.0
Provides:       bundled(crate(async-compression)) = 0.4.42
Provides:       bundled(crate(async-executor)) = 1.14.0
Provides:       bundled(crate(async-fs)) = 1.6.0
Provides:       bundled(crate(async-io)) = 1.13.0
Provides:       bundled(crate(async-io)) = 2.6.0
Provides:       bundled(crate(async-lock)) = 2.8.0
Provides:       bundled(crate(async-lock)) = 3.4.2
Provides:       bundled(crate(async-process)) = 1.8.1
Provides:       bundled(crate(async-recursion)) = 1.1.1
Provides:       bundled(crate(async-signal)) = 0.2.14
Provides:       bundled(crate(async-task)) = 4.7.1
Provides:       bundled(crate(async-trait)) = 0.1.89
Provides:       bundled(crate(atomic-polyfill)) = 1.0.3
Provides:       bundled(crate(atomic-waker)) = 1.1.2
Provides:       bundled(crate(autocfg)) = 1.5.1
Provides:       bundled(crate(av1-grain)) = 0.2.5
Provides:       bundled(crate(avif-serialize)) = 0.8.9
Provides:       bundled(crate(av-scenechange)) = 0.14.1
Provides:       bundled(crate(base64)) = 0.22.1
Provides:       bundled(crate(base64ct)) = 1.8.3
Provides:       bundled(crate(bit_field)) = 0.10.3
Provides:       bundled(crate(bitflags)) = 1.3.2
Provides:       bundled(crate(bitflags)) = 2.12.1
Provides:       bundled(crate(bit-set)) = 0.8.0
Provides:       bundled(crate(bitstream-io)) = 4.10.0
Provides:       bundled(crate(bit-vec)) = 0.8.0
Provides:       bundled(crate(blake2)) = 0.10.6
Provides:       bundled(crate(block-buffer)) = 0.10.4
Provides:       bundled(crate(blocking)) = 1.6.2
Provides:       bundled(crate(block-padding)) = 0.3.3
Provides:       bundled(crate(built)) = 0.8.1
Provides:       bundled(crate(bumpalo)) = 3.20.3
Provides:       bundled(crate(bytemuck)) = 1.25.0
Provides:       bundled(crate(byteorder)) = 1.5.0
Provides:       bundled(crate(byteorder-lite)) = 0.1.0
Provides:       bundled(crate(bytes)) = 1.11.1
Provides:       bundled(crate(cbc)) = 0.1.2
Provides:       bundled(crate(cc)) = 1.2.63
Provides:       bundled(crate(cfg_aliases)) = 0.2.1
Provides:       bundled(crate(cfg-if)) = 1.0.4
Provides:       bundled(crate(chacha20)) = 0.10.0
Provides:       bundled(crate(chrono)) = 0.4.45
Provides:       bundled(crate(cipher)) = 0.4.4
Provides:       bundled(crate(clap)) = 4.6.1
Provides:       bundled(crate(clap_builder)) = 4.6.0
Provides:       bundled(crate(clap_complete)) = 4.6.5
Provides:       bundled(crate(clap_derive)) = 4.6.1
Provides:       bundled(crate(clap_lex)) = 1.1.0
Provides:       bundled(crate(cobs)) = 0.3.0
Provides:       bundled(crate(colorchoice)) = 1.0.5
Provides:       bundled(crate(color_quant)) = 1.1.0
Provides:       bundled(crate(compression-codecs)) = 0.4.38
Provides:       bundled(crate(compression-core)) = 0.4.32
Provides:       bundled(crate(concurrent-queue)) = 2.5.0
Provides:       bundled(crate(const-oid)) = 0.9.6
Provides:       bundled(crate(cookie)) = 0.18.1
Provides:       bundled(crate(cookie_store)) = 0.22.1
Provides:       bundled(crate(core-foundation)) = 0.9.4
Provides:       bundled(crate(core-foundation-sys)) = 0.8.7
Provides:       bundled(crate(cpufeatures)) = 0.2.17
Provides:       bundled(crate(cpufeatures)) = 0.3.0
Provides:       bundled(crate(crc32fast)) = 1.5.0
Provides:       bundled(crate(critical-section)) = 1.2.0
Provides:       bundled(crate(crossbeam-deque)) = 0.8.6
Provides:       bundled(crate(crossbeam-epoch)) = 0.9.18
Provides:       bundled(crate(crossbeam-utils)) = 0.8.21
Provides:       bundled(crate(crossterm)) = 0.23.2
Provides:       bundled(crate(crossterm_winapi)) = 0.9.1
Provides:       bundled(crate(crunchy)) = 0.2.4
Provides:       bundled(crate(crypto-common)) = 0.1.7
Provides:       bundled(crate(der)) = 0.7.10
Provides:       bundled(crate(deranged)) = 0.5.8
Provides:       bundled(crate(derivative)) = 2.2.0
Provides:       bundled(crate(digest)) = 0.10.7
Provides:       bundled(crate(dirs)) = 5.0.1
Provides:       bundled(crate(dirs-sys)) = 0.4.1
Provides:       bundled(crate(displaydoc)) = 0.2.6
Provides:       bundled(crate(document-features)) = 0.2.12
Provides:       bundled(crate(either)) = 1.16.0
Provides:       bundled(crate(embedded-io)) = 0.4.0
Provides:       bundled(crate(embedded-io)) = 0.6.1
Provides:       bundled(crate(enumflags2)) = 0.7.12
Provides:       bundled(crate(enumflags2_derive)) = 0.7.12
Provides:       bundled(crate(equator)) = 0.4.2
Provides:       bundled(crate(equator-macro)) = 0.4.2
Provides:       bundled(crate(equivalent)) = 1.0.2
Provides:       bundled(crate(errno)) = 0.3.14
Provides:       bundled(crate(etcetera)) = 0.10.0
Provides:       bundled(crate(event-listener)) = 2.5.3
Provides:       bundled(crate(event-listener)) = 3.1.0
Provides:       bundled(crate(event-listener)) = 5.4.1
Provides:       bundled(crate(event-listener-strategy)) = 0.5.4
Provides:       bundled(crate(exr)) = 1.74.0
Provides:       bundled(crate(fastrand)) = 1.9.0
Provides:       bundled(crate(fastrand)) = 2.4.1
Provides:       bundled(crate(fax)) = 0.2.7
Provides:       bundled(crate(fdeflate)) = 0.3.7
Provides:       bundled(crate(find-msvc-tools)) = 0.1.9
Provides:       bundled(crate(flate2)) = 1.1.9
Provides:       bundled(crate(fnv)) = 1.0.7
Provides:       bundled(crate(foldhash)) = 0.1.5
Provides:       bundled(crate(form_urlencoded)) = 1.2.2
Provides:       bundled(crate(futures-channel)) = 0.3.32
Provides:       bundled(crate(futures-core)) = 0.3.32
Provides:       bundled(crate(futures-io)) = 0.3.32
Provides:       bundled(crate(futures-lite)) = 1.13.0
Provides:       bundled(crate(futures-lite)) = 2.6.1
Provides:       bundled(crate(futures-macro)) = 0.3.32
Provides:       bundled(crate(futures-sink)) = 0.3.32
Provides:       bundled(crate(futures-task)) = 0.3.32
Provides:       bundled(crate(futures-util)) = 0.3.32
Provides:       bundled(crate(g2gen)) = 1.2.2
Provides:       bundled(crate(g2p)) = 1.2.2
Provides:       bundled(crate(g2poly)) = 1.2.2
Provides:       bundled(crate(generic-array)) = 0.14.7
Provides:       bundled(crate(gethostname)) = 0.4.3
Provides:       bundled(crate(getrandom)) = 0.2.17
Provides:       bundled(crate(getrandom)) = 0.3.4
Provides:       bundled(crate(getrandom)) = 0.4.2
Provides:       bundled(crate(gif)) = 0.14.2
Provides:       bundled(crate(half)) = 2.7.1
Provides:       bundled(crate(hash32)) = 0.2.1
Provides:       bundled(crate(hashbrown)) = 0.15.5
Provides:       bundled(crate(hashbrown)) = 0.17.1
Provides:       bundled(crate(heapless)) = 0.7.17
Provides:       bundled(crate(heck)) = 0.5.0
Provides:       bundled(crate(hermit-abi)) = 0.3.9
Provides:       bundled(crate(hermit-abi)) = 0.5.2
Provides:       bundled(crate(hex)) = 0.4.3
Provides:       bundled(crate(hkdf)) = 0.12.4
Provides:       bundled(crate(hmac)) = 0.12.1
Provides:       bundled(crate(home)) = 0.5.12
Provides:       bundled(crate(http)) = 1.4.1
Provides:       bundled(crate(httparse)) = 1.10.1
Provides:       bundled(crate(http-body)) = 1.0.1
Provides:       bundled(crate(http-body-util)) = 0.1.3
Provides:       bundled(crate(hyper)) = 1.10.1
Provides:       bundled(crate(hyper-rustls)) = 0.27.9
Provides:       bundled(crate(hyper-util)) = 0.1.20
Provides:       bundled(crate(iana-time-zone)) = 0.1.65
Provides:       bundled(crate(iana-time-zone-haiku)) = 0.1.2
Provides:       bundled(crate(icu_collections)) = 2.2.0
Provides:       bundled(crate(icu_locale_core)) = 2.2.0
Provides:       bundled(crate(icu_normalizer)) = 2.2.0
Provides:       bundled(crate(icu_normalizer_data)) = 2.2.0
Provides:       bundled(crate(icu_properties)) = 2.2.0
Provides:       bundled(crate(icu_properties_data)) = 2.2.0
Provides:       bundled(crate(icu_provider)) = 2.2.0
Provides:       bundled(crate(id-arena)) = 2.3.0
Provides:       bundled(crate(idna)) = 1.1.0
Provides:       bundled(crate(idna_adapter)) = 1.2.2
Provides:       bundled(crate(image)) = 0.25.10
Provides:       bundled(crate(image-webp)) = 0.2.4
Provides:       bundled(crate(imgref)) = 1.12.1
Provides:       bundled(crate(indexmap)) = 2.14.0
Provides:       bundled(crate(inout)) = 0.1.4
Provides:       bundled(crate(instant)) = 0.1.13
Provides:       bundled(crate(interpolate_name)) = 0.2.4
Provides:       bundled(crate(io-lifetimes)) = 1.0.11
Provides:       bundled(crate(ipnet)) = 2.12.0
Provides:       bundled(crate(is-terminal)) = 0.4.17
Provides:       bundled(crate(is_terminal_polyfill)) = 1.70.2
Provides:       bundled(crate(itertools)) = 0.14.0
Provides:       bundled(crate(itoa)) = 1.0.18
Provides:       bundled(crate(jobserver)) = 0.1.34
Provides:       bundled(crate(js-sys)) = 0.3.99
Provides:       bundled(crate(keyring)) = 2.3.3
Provides:       bundled(crate(lazy_static)) = 1.5.0
Provides:       bundled(crate(leb128fmt)) = 0.1.0
Provides:       bundled(crate(lebe)) = 0.5.3
Provides:       bundled(crate(libc)) = 0.2.186
Provides:       bundled(crate(libfuzzer-sys)) = 0.4.12
Provides:       bundled(crate(libm)) = 0.2.16
Provides:       bundled(crate(libredox)) = 0.1.17
Provides:       bundled(crate(linked-hash-map)) = 0.5.6
Provides:       bundled(crate(linux-keyutils)) = 0.2.5
Provides:       bundled(crate(linux-raw-sys)) = 0.12.1
Provides:       bundled(crate(linux-raw-sys)) = 0.3.8
Provides:       bundled(crate(linux-raw-sys)) = 0.4.15
Provides:       bundled(crate(litemap)) = 0.8.2
Provides:       bundled(crate(litrs)) = 1.0.0
Provides:       bundled(crate(lock_api)) = 0.4.14
Provides:       bundled(crate(log)) = 0.4.32
Provides:       bundled(crate(loop9)) = 0.1.5
Provides:       bundled(crate(lru)) = 0.12.5
Provides:       bundled(crate(lru-cache)) = 0.1.2
Provides:       bundled(crate(lru-slab)) = 0.1.2
Provides:       bundled(crate(maplit)) = 1.0.2
Provides:       bundled(crate(maybe-rayon)) = 0.1.1
Provides:       bundled(crate(memchr)) = 2.8.1
Provides:       bundled(crate(memoffset)) = 0.7.1
Provides:       bundled(crate(memoffset)) = 0.9.1
Provides:       bundled(crate(mime)) = 0.3.17
Provides:       bundled(crate(mime_guess)) = 2.0.5
Provides:       bundled(crate(minimal-lexical)) = 0.2.1
Provides:       bundled(crate(miniz_oxide)) = 0.8.9
Provides:       bundled(crate(mio)) = 0.8.11
Provides:       bundled(crate(mio)) = 1.2.1
Provides:       bundled(crate(moxcms)) = 0.8.1
Provides:       bundled(crate(new_debug_unreachable)) = 1.0.6
Provides:       bundled(crate(nix)) = 0.26.4
Provides:       bundled(crate(nom)) = 7.1.3
Provides:       bundled(crate(nom)) = 8.0.0
Provides:       bundled(crate(noop_proc_macro)) = 0.3.0
Provides:       bundled(crate(no_std_io2)) = 0.9.4
Provides:       bundled(crate(num)) = 0.4.3
Provides:       bundled(crate(num-bigint)) = 0.4.6
Provides:       bundled(crate(num-bigint-dig)) = 0.8.6
Provides:       bundled(crate(num-complex)) = 0.4.6
Provides:       bundled(crate(num-conv)) = 0.2.2
Provides:       bundled(crate(num-derive)) = 0.4.2
Provides:       bundled(crate(num_enum)) = 0.7.6
Provides:       bundled(crate(num_enum_derive)) = 0.7.6
Provides:       bundled(crate(num-integer)) = 0.1.46
Provides:       bundled(crate(num-iter)) = 0.1.45
Provides:       bundled(crate(num-rational)) = 0.4.2
Provides:       bundled(crate(num-traits)) = 0.2.19
Provides:       bundled(crate(once_cell)) = 1.21.4
Provides:       bundled(crate(once_cell_polyfill)) = 1.70.2
Provides:       bundled(crate(oncemutex)) = 0.1.1
Provides:       bundled(crate(option-ext)) = 0.2.0
Provides:       bundled(crate(ordered-stream)) = 0.2.0
Provides:       bundled(crate(parking)) = 2.2.1
Provides:       bundled(crate(parking_lot)) = 0.12.5
Provides:       bundled(crate(parking_lot_core)) = 0.9.12
Provides:       bundled(crate(password-hash)) = 0.5.0
Provides:       bundled(crate(paste)) = 1.0.15
Provides:       bundled(crate(pastey)) = 0.1.1
Provides:       bundled(crate(pbkdf2)) = 0.12.2
Provides:       bundled(crate(pem-rfc7468)) = 0.7.0
Provides:       bundled(crate(percent-encoding)) = 2.3.2
Provides:       bundled(crate(phonenumber)) = 0.3.9+9.0.21
Provides:       bundled(crate(pin-project-lite)) = 0.2.17
Provides:       bundled(crate(piper)) = 0.2.5
Provides:       bundled(crate(pkcs1)) = 0.7.5
Provides:       bundled(crate(pkcs8)) = 0.10.2
Provides:       bundled(crate(png)) = 0.18.1
Provides:       bundled(crate(polling)) = 2.8.0
Provides:       bundled(crate(polling)) = 3.11.0
Provides:       bundled(crate(postcard)) = 1.1.3
Provides:       bundled(crate(potential_utf)) = 0.1.5
Provides:       bundled(crate(powerfmt)) = 0.2.0
Provides:       bundled(crate(ppv-lite86)) = 0.2.21
Provides:       bundled(crate(prettyplease)) = 0.2.37
Provides:       bundled(crate(proc-macro2)) = 1.0.106
Provides:       bundled(crate(proc-macro-crate)) = 1.3.1
Provides:       bundled(crate(proc-macro-crate)) = 3.5.0
Provides:       bundled(crate(profiling)) = 1.0.18
Provides:       bundled(crate(profiling-procmacros)) = 1.0.18
Provides:       bundled(crate(proptest)) = 1.11.0
Provides:       bundled(crate(protobuf)) = 3.7.2
Provides:       bundled(crate(protobuf-codegen)) = 3.7.2
Provides:       bundled(crate(protobuf-json-mapping)) = 3.7.2
Provides:       bundled(crate(protobuf-parse)) = 3.7.2
Provides:       bundled(crate(protobuf-support)) = 3.7.2
Provides:       bundled(crate(psl-types)) = 2.0.11
Provides:       bundled(crate(publicsuffix)) = 2.3.0
Provides:       bundled(crate(pxfm)) = 0.1.29
Provides:       bundled(crate(qoi)) = 0.4.1
Provides:       bundled(crate(qrcode)) = 0.14.1
Provides:       bundled(crate(quick-error)) = 1.2.3
Provides:       bundled(crate(quick-error)) = 2.0.1
Provides:       bundled(crate(quick-xml)) = 0.38.4
Provides:       bundled(crate(quinn)) = 0.11.9
Provides:       bundled(crate(quinn-proto)) = 0.11.14
Provides:       bundled(crate(quinn-udp)) = 0.5.14
Provides:       bundled(crate(quote)) = 1.0.45
Provides:       bundled(crate(rand)) = 0.10.1
Provides:       bundled(crate(rand)) = 0.8.6
Provides:       bundled(crate(rand)) = 0.9.4
Provides:       bundled(crate(rand_chacha)) = 0.3.1
Provides:       bundled(crate(rand_chacha)) = 0.9.0
Provides:       bundled(crate(rand_core)) = 0.10.1
Provides:       bundled(crate(rand_core)) = 0.6.4
Provides:       bundled(crate(rand_core)) = 0.9.5
Provides:       bundled(crate(rand_xorshift)) = 0.4.0
Provides:       bundled(crate(rav1e)) = 0.8.1
Provides:       bundled(crate(ravif)) = 0.13.0
Provides:       bundled(crate(rayon)) = 1.12.0
Provides:       bundled(crate(rayon-core)) = 1.13.0
Provides:       bundled(crate(redox_syscall)) = 0.5.18
Provides:       bundled(crate(redox_users)) = 0.4.6
Provides:       bundled(crate(r-efi)) = 5.3.0
Provides:       bundled(crate(r-efi)) = 6.0.0
Provides:       bundled(crate(regex)) = 1.12.3
Provides:       bundled(crate(regex-automata)) = 0.4.14
Provides:       bundled(crate(regex-cache)) = 0.2.1
Provides:       bundled(crate(regex-syntax)) = 0.6.29
Provides:       bundled(crate(regex-syntax)) = 0.8.10
Provides:       bundled(crate(reqwest)) = 0.12.28
Provides:       bundled(crate(rgb)) = 0.8.53
Provides:       bundled(crate(ring)) = 0.17.14
Provides:       bundled(crate(rpassword)) = 7.5.4
Provides:       bundled(crate(rqrr)) = 0.7.1
Provides:       bundled(crate(rsa)) = 0.9.10
Provides:       bundled(crate(rtoolbox)) = 0.0.5
Provides:       bundled(crate(rustc-hash)) = 2.1.2
Provides:       bundled(crate(rustc_version)) = 0.4.1
Provides:       bundled(crate(rustix)) = 0.37.28
Provides:       bundled(crate(rustix)) = 0.38.44
Provides:       bundled(crate(rustix)) = 1.1.4
Provides:       bundled(crate(rustls)) = 0.23.40
Provides:       bundled(crate(rustls-pki-types)) = 1.14.1
Provides:       bundled(crate(rustls-webpki)) = 0.103.13
Provides:       bundled(crate(rustversion)) = 1.0.22
Provides:       bundled(crate(rusty-fork)) = 0.3.1
Provides:       bundled(crate(ryu)) = 1.0.23
Provides:       bundled(crate(scopeguard)) = 1.2.0
Provides:       bundled(crate(secrecy)) = 0.8.0
Provides:       bundled(crate(secret-service)) = 3.1.0
Provides:       bundled(crate(security-framework)) = 2.11.1
Provides:       bundled(crate(security-framework-sys)) = 2.17.0
Provides:       bundled(crate(semver)) = 1.0.28
Provides:       bundled(crate(serde)) = 1.0.228
Provides:       bundled(crate(serde_core)) = 1.0.228
Provides:       bundled(crate(serde_derive)) = 1.0.228
Provides:       bundled(crate(serde_json)) = 1.0.150
Provides:       bundled(crate(serde_path_to_error)) = 0.1.20
Provides:       bundled(crate(serde_repr)) = 0.1.20
Provides:       bundled(crate(serde_urlencoded)) = 0.7.1
Provides:       bundled(crate(sha1)) = 0.10.6
Provides:       bundled(crate(sha2)) = 0.10.9
Provides:       bundled(crate(shlex)) = 2.0.1
Provides:       bundled(crate(signal-hook)) = 0.3.18
Provides:       bundled(crate(signal-hook-mio)) = 0.2.5
Provides:       bundled(crate(signal-hook-registry)) = 1.4.8
Provides:       bundled(crate(signature)) = 2.2.0
Provides:       bundled(crate(simd-adler32)) = 0.3.9
Provides:       bundled(crate(simd_helpers)) = 0.1.0
Provides:       bundled(crate(slab)) = 0.4.12
Provides:       bundled(crate(smallvec)) = 1.15.1
Provides:       bundled(crate(socket2)) = 0.4.10
Provides:       bundled(crate(socket2)) = 0.6.4
Provides:       bundled(crate(spin)) = 0.9.8
Provides:       bundled(crate(spki)) = 0.7.3
Provides:       bundled(crate(stable_deref_trait)) = 1.2.1
Provides:       bundled(crate(static_assertions)) = 1.1.0
Provides:       bundled(crate(stderrlog)) = 0.6.0
Provides:       bundled(crate(strsim)) = 0.11.1
Provides:       bundled(crate(strum)) = 0.27.2
Provides:       bundled(crate(strum_macros)) = 0.27.2
Provides:       bundled(crate(subtle)) = 2.6.1
Provides:       bundled(crate(syn)) = 1.0.109
Provides:       bundled(crate(syn)) = 2.0.117
Provides:       bundled(crate(sync_wrapper)) = 1.0.2
Provides:       bundled(crate(synstructure)) = 0.13.2
Provides:       bundled(crate(tempfile)) = 3.27.0
Provides:       bundled(crate(termcolor)) = 1.1.3
Provides:       bundled(crate(text_io)) = 0.1.13
Provides:       bundled(crate(thiserror)) = 1.0.69
Provides:       bundled(crate(thiserror)) = 2.0.18
Provides:       bundled(crate(thiserror-impl)) = 1.0.69
Provides:       bundled(crate(thiserror-impl)) = 2.0.18
Provides:       bundled(crate(thread_local)) = 1.1.9
Provides:       bundled(crate(tiff)) = 0.11.3
Provides:       bundled(crate(time)) = 0.3.47
Provides:       bundled(crate(time-core)) = 0.1.8
Provides:       bundled(crate(time-macros)) = 0.2.27
Provides:       bundled(crate(tinystr)) = 0.8.3
Provides:       bundled(crate(tinyvec)) = 1.11.0
Provides:       bundled(crate(tinyvec_macros)) = 0.1.1
Provides:       bundled(crate(tokio)) = 1.52.3
Provides:       bundled(crate(tokio-rustls)) = 0.26.4
Provides:       bundled(crate(tokio-util)) = 0.7.18
Provides:       bundled(crate(toml_datetime)) = 0.6.11
Provides:       bundled(crate(toml_datetime-1.1.1+spec)) = 1.1.0
Provides:       bundled(crate(toml_edit)) = 0.19.15
Provides:       bundled(crate(toml_edit-0.25.12+spec)) = 1.1.0
Provides:       bundled(crate(toml_parser-1.1.2+spec)) = 1.1.0
Provides:       bundled(crate(tower)) = 0.5.3
Provides:       bundled(crate(tower-http)) = 0.6.11
Provides:       bundled(crate(tower-layer)) = 0.3.3
Provides:       bundled(crate(tower-service)) = 0.3.3
Provides:       bundled(crate(tracing)) = 0.1.44
Provides:       bundled(crate(tracing-attributes)) = 0.1.31
Provides:       bundled(crate(tracing-core)) = 0.1.36
Provides:       bundled(crate(try-lock)) = 0.2.5
Provides:       bundled(crate(typenum)) = 1.20.1
Provides:       bundled(crate(uds_windows)) = 1.2.1
Provides:       bundled(crate(unarray)) = 0.1.4
Provides:       bundled(crate(unicase)) = 2.9.0
Provides:       bundled(crate(unicode-ident)) = 1.0.24
Provides:       bundled(crate(unicode-xid)) = 0.2.6
Provides:       bundled(crate(untrusted)) = 0.9.0
Provides:       bundled(crate(update-informer)) = 1.3.0
Provides:       bundled(crate(url)) = 2.5.8
Provides:       bundled(crate(utf8_iter)) = 1.0.4
Provides:       bundled(crate(utf8parse)) = 0.2.2
Provides:       bundled(crate(uuid)) = 1.23.2
Provides:       bundled(crate(version_check)) = 0.9.5
Provides:       bundled(crate(v_frame)) = 0.3.9
Provides:       bundled(crate(wait-timeout)) = 0.2.1
Provides:       bundled(crate(waker-fn)) = 1.2.0
Provides:       bundled(crate(want)) = 0.3.1
Provides:       bundled(crate(wasi-0.11.1+wasi-snapshot)) = preview1
Provides:       bundled(crate(wasip2-1.0.3+wasi)) = 0.2.9
Provides:       bundled(crate(wasip3-0.4.0+wasi-0.3.0-rc-2026-01)) = 06
Provides:       bundled(crate(wasm-bindgen)) = 0.2.122
Provides:       bundled(crate(wasm-bindgen-futures)) = 0.4.72
Provides:       bundled(crate(wasm-bindgen-macro)) = 0.2.122
Provides:       bundled(crate(wasm-bindgen-macro-support)) = 0.2.122
Provides:       bundled(crate(wasm-bindgen-shared)) = 0.2.122
Provides:       bundled(crate(wasm-encoder)) = 0.244.0
Provides:       bundled(crate(wasm-metadata)) = 0.244.0
Provides:       bundled(crate(wasmparser)) = 0.244.0
Provides:       bundled(crate(webpki-roots)) = 1.0.7
Provides:       bundled(crate(web-sys)) = 0.3.99
Provides:       bundled(crate(web-time)) = 1.1.0
Provides:       bundled(crate(weezl)) = 0.1.12
Provides:       bundled(crate(which)) = 4.4.2
Provides:       bundled(crate(winapi)) = 0.3.9
Provides:       bundled(crate(winapi-i686-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(winapi-util)) = 0.1.11
Provides:       bundled(crate(winapi-x86_64-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.48.5
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.53.1
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.48.5
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.52.6
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.53.1
Provides:       bundled(crate(windows-core)) = 0.62.2
Provides:       bundled(crate(windows_i686_gnu)) = 0.48.5
Provides:       bundled(crate(windows_i686_gnu)) = 0.52.6
Provides:       bundled(crate(windows_i686_gnu)) = 0.53.1
Provides:       bundled(crate(windows_i686_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_i686_gnullvm)) = 0.53.1
Provides:       bundled(crate(windows_i686_msvc)) = 0.48.5
Provides:       bundled(crate(windows_i686_msvc)) = 0.52.6
Provides:       bundled(crate(windows_i686_msvc)) = 0.53.1
Provides:       bundled(crate(windows-implement)) = 0.60.2
Provides:       bundled(crate(windows-interface)) = 0.59.3
Provides:       bundled(crate(windows-link)) = 0.2.1
Provides:       bundled(crate(windows-result)) = 0.4.1
Provides:       bundled(crate(windows-strings)) = 0.5.1
Provides:       bundled(crate(windows-sys)) = 0.48.0
Provides:       bundled(crate(windows-sys)) = 0.52.0
Provides:       bundled(crate(windows-sys)) = 0.59.0
Provides:       bundled(crate(windows-sys)) = 0.60.2
Provides:       bundled(crate(windows-sys)) = 0.61.2
Provides:       bundled(crate(windows-targets)) = 0.48.5
Provides:       bundled(crate(windows-targets)) = 0.52.6
Provides:       bundled(crate(windows-targets)) = 0.53.5
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.53.1
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.53.1
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.53.1
Provides:       bundled(crate(winnow)) = 0.5.40
Provides:       bundled(crate(winnow)) = 1.0.3
Provides:       bundled(crate(wit-bindgen)) = 0.51.0
Provides:       bundled(crate(wit-bindgen)) = 0.57.1
Provides:       bundled(crate(wit-bindgen-core)) = 0.51.0
Provides:       bundled(crate(wit-bindgen-rust)) = 0.51.0
Provides:       bundled(crate(wit-bindgen-rust-macro)) = 0.51.0
Provides:       bundled(crate(wit-component)) = 0.244.0
Provides:       bundled(crate(wit-parser)) = 0.244.0
Provides:       bundled(crate(writeable)) = 0.6.3
Provides:       bundled(crate(xdg-home)) = 1.3.0
Provides:       bundled(crate(y4m)) = 0.8.0
Provides:       bundled(crate(yoke)) = 0.8.3
Provides:       bundled(crate(yoke-derive)) = 0.8.2
Provides:       bundled(crate(zbus)) = 3.15.2
Provides:       bundled(crate(zbus_macros)) = 3.15.2
Provides:       bundled(crate(zbus_names)) = 2.6.1
Provides:       bundled(crate(zerocopy)) = 0.8.50
Provides:       bundled(crate(zerocopy-derive)) = 0.8.50
Provides:       bundled(crate(zerofrom)) = 0.1.8
Provides:       bundled(crate(zerofrom-derive)) = 0.1.7
Provides:       bundled(crate(zeroize)) = 1.8.2
Provides:       bundled(crate(zeroize_derive)) = 1.4.3
Provides:       bundled(crate(zerotrie)) = 0.2.4
Provides:       bundled(crate(zerovec)) = 0.11.6
Provides:       bundled(crate(zerovec-derive)) = 0.11.3
Provides:       bundled(crate(zmij)) = 1.0.21
Provides:       bundled(crate(zune-core)) = 0.5.1
Provides:       bundled(crate(zune-inflate)) = 0.2.54
Provides:       bundled(crate(zune-jpeg)) = 0.5.15
Provides:       bundled(crate(zvariant)) = 3.15.2
Provides:       bundled(crate(zvariant_derive)) = 3.15.2
Provides:       bundled(crate(zvariant_utils)) = 1.0.1
%endif


%description
%{name} is a command line utility to generate Steam 2FA codes and respond to
confirmations.


%prep
%autosetup -p1 %{?with_vendor:-a1}

%if %{with vendor}
sed \
  -e '/rustc_layout_scalar_valid_range_start/d' \
  -e '/rustc_layout_scalar_valid_range_end/d' \
  -i vendor/rustix-0.37*/src/backend/linux_raw/io/errno.rs

typedpath_hash="$(sha256sum vendor/rustix-0.37*/src/backend/linux_raw/io/errno.rs 2>&1 |cut -d" " -f1)"
sed \
  -e 's|"src/backend/linux_raw/io/errno.rs":"[^"]*"|"src/backend/linux_raw/io/errno.rs":"'${typedpath_hash}'"|' \
  -i vendor/rustix-0.37*/.cargo-checksum.json

%cargo_prep -v vendor
%else
%cargo_prep
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
%cargo_install


%files
%license LICENSE
%doc README.md
%license LICENSE.dependencies
%if %{with vendor}
%license cargo-vendor.txt
%endif
%doc README.md
%{_bindir}/steamguard


%changelog
* Wed Sep 16 2026 Phantom X <megaphantomx at hotmail dot com> - 0.18.4-1
- 0.18.4

* Fri Aug 01 2025 Phantom X <megaphantomx at hotmail dot com> - 0.17.1-1
- Initial spec

