# prevent library files from being installed
%global cargo_install_lib 0

# Use vendor tarball
%bcond vendor 1

%global vendor_hash 70380cabf61cbd8bb19002062cf32dec

Name:           steamguard-cli
Version:        0.17.1
Release:        1%{?dist}
Summary:        Command line utility to generate Steam 2FA codes

License:        GPL-3.0-or-later
URL:            https://github.com/dyc3/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%if %{with vendor}
# rust2rpm -t fedora -V auto --no-rpmautospec --ignore-missing-license-files --path %%{name}-%%{version}
Source1:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-%{version}-vendor.tar.xz/%{vendor_hash}/%{name}-%{version}-vendor.tar.xz
%endif

ExclusiveArch:  %{rust_arches}

BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  rust-packaging
%if %{with vendor}
Provides:       bundled(crate(addr2line)) = 0.22.0
Provides:       bundled(crate(adler)) = 1.0.2
Provides:       bundled(crate(aes)) = 0.8.4
Provides:       bundled(crate(ahash)) = 0.8.11
Provides:       bundled(crate(aho)) = 1.1.3
Provides:       bundled(crate(aligned)) = 0.5.0
Provides:       bundled(crate(allocator)) = 0.2.18
Provides:       bundled(crate(android_system_properties)) = 0.1.5
Provides:       bundled(crate(android)) = 0.1.1
Provides:       bundled(crate(anstream)) = 0.6.15
Provides:       bundled(crate(anstyle)) = 1.0.8
Provides:       bundled(crate(anstyle)) = 0.2.5
Provides:       bundled(crate(anstyle)) = 1.1.1
Provides:       bundled(crate(anstyle)) = 3.0.4
Provides:       bundled(crate(anyhow)) = 1.0.86
Provides:       bundled(crate(arbitrary)) = 1.3.2
Provides:       bundled(crate(arg_enum_proc_macro)) = 0.3.4
Provides:       bundled(crate(argon2)) = 0.5.3
Provides:       bundled(crate(arrayvec)) = 0.7.4
Provides:       bundled(crate(async)) = 0.5.1
Provides:       bundled(crate(async)) = 2.3.1
Provides:       bundled(crate(async)) = 0.4.12
Provides:       bundled(crate(async)) = 1.13.0
Provides:       bundled(crate(async)) = 1.6.0
Provides:       bundled(crate(async)) = 1.13.0
Provides:       bundled(crate(async)) = 2.3.3
Provides:       bundled(crate(async)) = 2.8.0
Provides:       bundled(crate(async)) = 3.4.0
Provides:       bundled(crate(async)) = 1.8.1
Provides:       bundled(crate(async)) = 1.1.1
Provides:       bundled(crate(async)) = 0.2.9
Provides:       bundled(crate(async)) = 4.7.1
Provides:       bundled(crate(async)) = 0.1.81
Provides:       bundled(crate(atomic)) = 1.1.2
Provides:       bundled(crate(autocfg)) = 1.3.0
Provides:       bundled(crate(av1)) = 0.2.3
Provides:       bundled(crate(avif)) = 0.8.1
Provides:       bundled(crate(backtrace)) = 0.3.73
Provides:       bundled(crate(base64)) = 0.22.1
Provides:       bundled(crate(base64ct)) = 1.6.0
Provides:       bundled(crate(bincode)) = 1.3.3
Provides:       bundled(crate(bit_field)) = 0.10.2
Provides:       bundled(crate(bitflags)) = 1.3.2
Provides:       bundled(crate(bitflags)) = 2.6.0
Provides:       bundled(crate(bit)) = 0.5.3
Provides:       bundled(crate(bitstream)) = 2.5.0
Provides:       bundled(crate(bit)) = 0.6.3
Provides:       bundled(crate(blake2)) = 0.10.6
Provides:       bundled(crate(block)) = 0.10.4
Provides:       bundled(crate(blocking)) = 1.6.1
Provides:       bundled(crate(block)) = 0.3.3
Provides:       bundled(crate(built)) = 0.7.4
Provides:       bundled(crate(bumpalo)) = 3.16.0
Provides:       bundled(crate(bytemuck)) = 1.16.3
Provides:       bundled(crate(byteorder)) = 1.5.0
Provides:       bundled(crate(byteorder)) = 0.1.0
Provides:       bundled(crate(bytes)) = 1.7.1
Provides:       bundled(crate(cbc)) = 0.1.2
Provides:       bundled(crate(cc)) = 1.2.17
Provides:       bundled(crate(cfg)) = 0.15.8
Provides:       bundled(crate(cfg)) = 1.0.0
Provides:       bundled(crate(chrono)) = 0.4.38
Provides:       bundled(crate(cipher)) = 0.4.4
Provides:       bundled(crate(clap)) = 4.5.13
Provides:       bundled(crate(clap_builder)) = 4.5.13
Provides:       bundled(crate(clap_complete)) = 4.5.12
Provides:       bundled(crate(clap_derive)) = 4.5.13
Provides:       bundled(crate(clap_lex)) = 0.7.2
Provides:       bundled(crate(colorchoice)) = 1.0.2
Provides:       bundled(crate(color_quant)) = 1.1.0
Provides:       bundled(crate(concurrent)) = 2.5.0
Provides:       bundled(crate(const)) = 0.9.6
Provides:       bundled(crate(cookie)) = 0.18.1
Provides:       bundled(crate(cookie_store)) = 0.21.0
Provides:       bundled(crate(core)) = 0.9.4
Provides:       bundled(crate(core)) = 0.8.6
Provides:       bundled(crate(cpufeatures)) = 0.2.12
Provides:       bundled(crate(crc32fast)) = 1.4.2
Provides:       bundled(crate(crossbeam)) = 0.8.5
Provides:       bundled(crate(crossbeam)) = 0.9.18
Provides:       bundled(crate(crossbeam)) = 0.8.20
Provides:       bundled(crate(crossterm)) = 0.23.2
Provides:       bundled(crate(crossterm_winapi)) = 0.9.1
Provides:       bundled(crate(crunchy)) = 0.2.2
Provides:       bundled(crate(crypto)) = 0.1.6
Provides:       bundled(crate(der)) = 0.7.9
Provides:       bundled(crate(deranged)) = 0.3.11
Provides:       bundled(crate(derivative)) = 2.2.0
Provides:       bundled(crate(digest)) = 0.10.7
Provides:       bundled(crate(directories)) = 5.0.1
Provides:       bundled(crate(dirs)) = 5.0.1
Provides:       bundled(crate(dirs)) = 0.4.1
Provides:       bundled(crate(either)) = 1.13.0
Provides:       bundled(crate(enumflags2)) = 0.7.10
Provides:       bundled(crate(enumflags2_derive)) = 0.7.10
Provides:       bundled(crate(equivalent)) = 1.0.1
Provides:       bundled(crate(errno)) = 0.3.9
Provides:       bundled(crate(event)) = 2.5.3
Provides:       bundled(crate(event)) = 3.1.0
Provides:       bundled(crate(event)) = 5.3.1
Provides:       bundled(crate(event)) = 0.5.2
Provides:       bundled(crate(exr)) = 1.72.0
Provides:       bundled(crate(fastrand)) = 1.9.0
Provides:       bundled(crate(fastrand)) = 2.1.0
Provides:       bundled(crate(fdeflate)) = 0.3.4
Provides:       bundled(crate(flate2)) = 1.0.30
Provides:       bundled(crate(flume)) = 0.11.0
Provides:       bundled(crate(fnv)) = 1.0.7
Provides:       bundled(crate(form_urlencoded)) = 1.2.1
Provides:       bundled(crate(futures)) = 0.3.30
Provides:       bundled(crate(futures)) = 0.3.30
Provides:       bundled(crate(futures)) = 0.3.30
Provides:       bundled(crate(futures)) = 1.13.0
Provides:       bundled(crate(futures)) = 2.3.0
Provides:       bundled(crate(futures)) = 0.3.30
Provides:       bundled(crate(futures)) = 0.3.30
Provides:       bundled(crate(futures)) = 0.3.30
Provides:       bundled(crate(futures)) = 0.3.30
Provides:       bundled(crate(g2gen)) = 1.0.1
Provides:       bundled(crate(g2p)) = 1.0.1
Provides:       bundled(crate(g2poly)) = 1.0.1
Provides:       bundled(crate(generic)) = 0.14.7
Provides:       bundled(crate(gethostname)) = 0.4.3
Provides:       bundled(crate(getrandom)) = 0.2.15
Provides:       bundled(crate(gif)) = 0.13.1
Provides:       bundled(crate(gimli)) = 0.29.0
Provides:       bundled(crate(half)) = 2.4.1
Provides:       bundled(crate(hashbrown)) = 0.14.5
Provides:       bundled(crate(heck)) = 0.5.0
Provides:       bundled(crate(hermit)) = 0.3.9
Provides:       bundled(crate(hermit)) = 0.4.0
Provides:       bundled(crate(hex)) = 0.4.3
Provides:       bundled(crate(hkdf)) = 0.12.4
Provides:       bundled(crate(hmac)) = 0.12.1
Provides:       bundled(crate(home)) = 0.5.9
Provides:       bundled(crate(http)) = 1.1.0
Provides:       bundled(crate(httparse)) = 1.9.4
Provides:       bundled(crate(http)) = 1.0.1
Provides:       bundled(crate(http)) = 0.1.2
Provides:       bundled(crate(hyper)) = 1.4.1
Provides:       bundled(crate(hyper)) = 0.27.2
Provides:       bundled(crate(hyper)) = 0.1.6
Provides:       bundled(crate(iana)) = 0.1.60
Provides:       bundled(crate(iana)) = 0.1.2
Provides:       bundled(crate(idna)) = 0.3.0
Provides:       bundled(crate(idna)) = 0.5.0
Provides:       bundled(crate(image)) = 0.25.2
Provides:       bundled(crate(image)) = 0.1.3
Provides:       bundled(crate(imgref)) = 1.10.1
Provides:       bundled(crate(indexmap)) = 2.3.0
Provides:       bundled(crate(inout)) = 0.1.3
Provides:       bundled(crate(instant)) = 0.1.13
Provides:       bundled(crate(interpolate_name)) = 0.2.4
Provides:       bundled(crate(io)) = 1.0.11
Provides:       bundled(crate(ipnet)) = 2.9.0
Provides:       bundled(crate(is)) = 0.4.12
Provides:       bundled(crate(is_terminal_polyfill)) = 1.70.1
Provides:       bundled(crate(itertools)) = 0.12.1
Provides:       bundled(crate(itoa)) = 1.0.11
Provides:       bundled(crate(jobserver)) = 0.1.32
Provides:       bundled(crate(jpeg)) = 0.3.1
Provides:       bundled(crate(js)) = 0.3.69
Provides:       bundled(crate(keyring)) = 2.3.3
Provides:       bundled(crate(lazy_static)) = 1.5.0
Provides:       bundled(crate(lebe)) = 0.5.2
Provides:       bundled(crate(libc)) = 0.2.155
Provides:       bundled(crate(libfuzzer)) = 0.4.7
Provides:       bundled(crate(libm)) = 0.2.8
Provides:       bundled(crate(libredox)) = 0.1.3
Provides:       bundled(crate(linked)) = 0.5.6
Provides:       bundled(crate(linux)) = 0.2.4
Provides:       bundled(crate(linux)) = 0.3.8
Provides:       bundled(crate(linux)) = 0.4.14
Provides:       bundled(crate(lock_api)) = 0.4.12
Provides:       bundled(crate(log)) = 0.4.22
Provides:       bundled(crate(loop9)) = 0.1.5
Provides:       bundled(crate(lru)) = 0.12.4
Provides:       bundled(crate(lru)) = 0.1.2
Provides:       bundled(crate(maplit)) = 1.0.2
Provides:       bundled(crate(maybe)) = 0.1.1
Provides:       bundled(crate(memchr)) = 2.7.4
Provides:       bundled(crate(memoffset)) = 0.7.1
Provides:       bundled(crate(memoffset)) = 0.9.1
Provides:       bundled(crate(mime)) = 0.3.17
Provides:       bundled(crate(mime_guess)) = 2.0.5
Provides:       bundled(crate(minimal)) = 0.2.1
Provides:       bundled(crate(miniz_oxide)) = 0.7.4
Provides:       bundled(crate(mio)) = 0.8.11
Provides:       bundled(crate(mio)) = 1.0.1
Provides:       bundled(crate(new_debug_unreachable)) = 1.0.6
Provides:       bundled(crate(nix)) = 0.26.4
Provides:       bundled(crate(nom)) = 7.1.3
Provides:       bundled(crate(noop_proc_macro)) = 0.3.0
Provides:       bundled(crate(num)) = 0.4.3
Provides:       bundled(crate(num)) = 0.4.6
Provides:       bundled(crate(num)) = 0.8.4
Provides:       bundled(crate(num)) = 0.4.6
Provides:       bundled(crate(num)) = 0.1.0
Provides:       bundled(crate(num)) = 0.4.2
Provides:       bundled(crate(num_enum)) = 0.7.3
Provides:       bundled(crate(num_enum_derive)) = 0.7.3
Provides:       bundled(crate(num)) = 0.1.46
Provides:       bundled(crate(num)) = 0.1.45
Provides:       bundled(crate(num)) = 0.4.2
Provides:       bundled(crate(num)) = 0.2.19
Provides:       bundled(crate(object)) = 0.36.2
Provides:       bundled(crate(once_cell)) = 1.19.0
Provides:       bundled(crate(oncemutex)) = 0.1.1
Provides:       bundled(crate(option)) = 0.2.0
Provides:       bundled(crate(ordered)) = 0.2.0
Provides:       bundled(crate(parking)) = 2.2.0
Provides:       bundled(crate(parking_lot)) = 0.12.3
Provides:       bundled(crate(parking_lot_core)) = 0.9.10
Provides:       bundled(crate(password)) = 0.5.0
Provides:       bundled(crate(paste)) = 1.0.15
Provides:       bundled(crate(pbkdf2)) = 0.12.2
Provides:       bundled(crate(pem)) = 0.7.0
Provides:       bundled(crate(percent)) = 2.3.1
Provides:       bundled(crate(phonenumber)) = 0.3.6+8.13.36
Provides:       bundled(crate(pin)) = 1.1.5
Provides:       bundled(crate(pin)) = 1.1.5
Provides:       bundled(crate(pin)) = 0.2.14
Provides:       bundled(crate(pin)) = 0.1.0
Provides:       bundled(crate(piper)) = 0.2.3
Provides:       bundled(crate(pkcs1)) = 0.7.5
Provides:       bundled(crate(pkcs8)) = 0.10.2
Provides:       bundled(crate(pkg)) = 0.3.30
Provides:       bundled(crate(png)) = 0.17.13
Provides:       bundled(crate(polling)) = 2.8.0
Provides:       bundled(crate(polling)) = 3.7.2
Provides:       bundled(crate(powerfmt)) = 0.2.0
Provides:       bundled(crate(ppv)) = 0.2.18
Provides:       bundled(crate(proc)) = 1.0.86
Provides:       bundled(crate(proc)) = 1.3.1
Provides:       bundled(crate(proc)) = 3.1.0
Provides:       bundled(crate(profiling)) = 1.0.15
Provides:       bundled(crate(profiling)) = 1.0.15
Provides:       bundled(crate(proptest)) = 1.5.0
Provides:       bundled(crate(protobuf)) = 3.7.1
Provides:       bundled(crate(protobuf)) = 3.7.1
Provides:       bundled(crate(protobuf)) = 3.7.1
Provides:       bundled(crate(protobuf)) = 3.7.1
Provides:       bundled(crate(protobuf)) = 3.7.1
Provides:       bundled(crate(psl)) = 2.0.11
Provides:       bundled(crate(publicsuffix)) = 2.2.3
Provides:       bundled(crate(qoi)) = 0.4.1
Provides:       bundled(crate(qrcode)) = 0.14.1
Provides:       bundled(crate(quick)) = 1.2.3
Provides:       bundled(crate(quick)) = 2.0.1
Provides:       bundled(crate(quick)) = 0.31.0
Provides:       bundled(crate(quinn)) = 0.11.2
Provides:       bundled(crate(quinn)) = 0.11.8
Provides:       bundled(crate(quinn)) = 0.5.4
Provides:       bundled(crate(quote)) = 1.0.36
Provides:       bundled(crate(rand)) = 0.8.5
Provides:       bundled(crate(rand_chacha)) = 0.3.1
Provides:       bundled(crate(rand_core)) = 0.6.4
Provides:       bundled(crate(rand_xorshift)) = 0.3.0
Provides:       bundled(crate(rav1e)) = 0.7.1
Provides:       bundled(crate(ravif)) = 0.11.9
Provides:       bundled(crate(rayon)) = 1.10.0
Provides:       bundled(crate(rayon)) = 1.12.1
Provides:       bundled(crate(redox_syscall)) = 0.5.3
Provides:       bundled(crate(redox_users)) = 0.4.5
Provides:       bundled(crate(regex)) = 1.10.5
Provides:       bundled(crate(regex)) = 0.4.7
Provides:       bundled(crate(regex)) = 0.2.1
Provides:       bundled(crate(regex)) = 0.6.29
Provides:       bundled(crate(regex)) = 0.8.4
Provides:       bundled(crate(reqwest)) = 0.12.5
Provides:       bundled(crate(rgb)) = 0.8.45
Provides:       bundled(crate(ring)) = 0.17.14
Provides:       bundled(crate(rpassword)) = 7.3.1
Provides:       bundled(crate(rqrr)) = 0.7.1
Provides:       bundled(crate(rsa)) = 0.9.6
Provides:       bundled(crate(rtoolbox)) = 0.0.2
Provides:       bundled(crate(rustc)) = 0.1.24
Provides:       bundled(crate(rustc)) = 1.1.0
Provides:       bundled(crate(rustc)) = 2.0.0
Provides:       bundled(crate(rustix)) = 0.37.27
Provides:       bundled(crate(rustix)) = 0.38.34
Provides:       bundled(crate(rustls)) = 0.23.12
Provides:       bundled(crate(rustls)) = 2.1.2
Provides:       bundled(crate(rustls)) = 1.7.0
Provides:       bundled(crate(rustls)) = 0.102.6
Provides:       bundled(crate(rustversion)) = 1.0.17
Provides:       bundled(crate(rusty)) = 0.3.0
Provides:       bundled(crate(ryu)) = 1.0.18
Provides:       bundled(crate(scopeguard)) = 1.2.0
Provides:       bundled(crate(secrecy)) = 0.8.0
Provides:       bundled(crate(secret)) = 3.1.0
Provides:       bundled(crate(security)) = 2.11.1
Provides:       bundled(crate(security)) = 2.11.1
Provides:       bundled(crate(semver)) = 1.0.23
Provides:       bundled(crate(serde)) = 1.0.204
Provides:       bundled(crate(serde_derive)) = 1.0.204
Provides:       bundled(crate(serde_json)) = 1.0.122
Provides:       bundled(crate(serde_path_to_error)) = 0.1.16
Provides:       bundled(crate(serde_repr)) = 0.1.19
Provides:       bundled(crate(serde_spanned)) = 0.6.7
Provides:       bundled(crate(serde_urlencoded)) = 0.7.1
Provides:       bundled(crate(sha1)) = 0.10.6
Provides:       bundled(crate(sha2)) = 0.10.8
Provides:       bundled(crate(shlex)) = 1.3.0
Provides:       bundled(crate(signal)) = 0.3.17
Provides:       bundled(crate(signal)) = 0.2.4
Provides:       bundled(crate(signal)) = 1.4.2
Provides:       bundled(crate(signature)) = 2.2.0
Provides:       bundled(crate(simd)) = 0.3.7
Provides:       bundled(crate(simd_helpers)) = 0.1.0
Provides:       bundled(crate(slab)) = 0.4.9
Provides:       bundled(crate(smallvec)) = 1.13.2
Provides:       bundled(crate(socket2)) = 0.4.10
Provides:       bundled(crate(socket2)) = 0.5.7
Provides:       bundled(crate(spin)) = 0.9.8
Provides:       bundled(crate(spki)) = 0.7.3
Provides:       bundled(crate(static_assertions)) = 1.1.0
Provides:       bundled(crate(stderrlog)) = 0.6.0
Provides:       bundled(crate(strsim)) = 0.11.1
Provides:       bundled(crate(strum)) = 0.26.3
Provides:       bundled(crate(strum_macros)) = 0.26.4
Provides:       bundled(crate(subtle)) = 2.6.1
Provides:       bundled(crate(syn)) = 1.0.109
Provides:       bundled(crate(syn)) = 2.0.72
Provides:       bundled(crate(sync_wrapper)) = 1.0.1
Provides:       bundled(crate(system)) = 6.2.2
Provides:       bundled(crate(target)) = 0.12.16
Provides:       bundled(crate(tempfile)) = 3.10.1
Provides:       bundled(crate(termcolor)) = 1.1.3
Provides:       bundled(crate(text_io)) = 0.1.12
Provides:       bundled(crate(thiserror)) = 1.0.63
Provides:       bundled(crate(thiserror)) = 1.0.63
Provides:       bundled(crate(thread_local)) = 1.1.8
Provides:       bundled(crate(tiff)) = 0.9.1
Provides:       bundled(crate(time)) = 0.3.36
Provides:       bundled(crate(time)) = 0.1.2
Provides:       bundled(crate(time)) = 0.2.18
Provides:       bundled(crate(tinyvec)) = 1.8.0
Provides:       bundled(crate(tinyvec_macros)) = 0.1.1
Provides:       bundled(crate(tokio)) = 1.39.2
Provides:       bundled(crate(tokio)) = 0.26.0
Provides:       bundled(crate(tokio)) = 0.7.11
Provides:       bundled(crate(toml)) = 0.8.19
Provides:       bundled(crate(toml_datetime)) = 0.6.8
Provides:       bundled(crate(toml_edit)) = 0.19.15
Provides:       bundled(crate(toml_edit)) = 0.21.1
Provides:       bundled(crate(toml_edit)) = 0.22.20
Provides:       bundled(crate(tower)) = 0.4.13
Provides:       bundled(crate(tower)) = 0.3.2
Provides:       bundled(crate(tower)) = 0.3.2
Provides:       bundled(crate(tracing)) = 0.1.40
Provides:       bundled(crate(tracing)) = 0.1.27
Provides:       bundled(crate(tracing)) = 0.1.32
Provides:       bundled(crate(try)) = 0.2.5
Provides:       bundled(crate(typenum)) = 1.17.0
Provides:       bundled(crate(uds_windows)) = 1.1.0
Provides:       bundled(crate(unarray)) = 0.1.4
Provides:       bundled(crate(unicase)) = 2.7.0
Provides:       bundled(crate(unicode)) = 0.3.15
Provides:       bundled(crate(unicode)) = 1.0.12
Provides:       bundled(crate(unicode)) = 0.1.23
Provides:       bundled(crate(untrusted)) = 0.9.0
Provides:       bundled(crate(update)) = 1.1.0
Provides:       bundled(crate(url)) = 2.5.2
Provides:       bundled(crate(utf8parse)) = 0.2.2
Provides:       bundled(crate(uuid)) = 1.10.0
Provides:       bundled(crate(version_check)) = 0.9.5
Provides:       bundled(crate(version)) = 0.2.0
Provides:       bundled(crate(v_frame)) = 0.3.8
Provides:       bundled(crate(wait)) = 0.2.0
Provides:       bundled(crate(waker)) = 1.2.0
Provides:       bundled(crate(want)) = 0.3.1
Provides:       bundled(crate(wasi)) = preview1
Provides:       bundled(crate(wasm)) = 0.2.92
Provides:       bundled(crate(wasm)) = 0.2.92
Provides:       bundled(crate(wasm)) = 0.4.42
Provides:       bundled(crate(wasm)) = 0.2.92
Provides:       bundled(crate(wasm)) = 0.2.92
Provides:       bundled(crate(wasm)) = 0.2.92
Provides:       bundled(crate(webpki)) = 0.26.3
Provides:       bundled(crate(web)) = 0.3.69
Provides:       bundled(crate(weezl)) = 0.1.8
Provides:       bundled(crate(which)) = 4.4.2
Provides:       bundled(crate(winapi)) = 0.3.9
Provides:       bundled(crate(winapi)) = 0.4.0
Provides:       bundled(crate(winapi)) = 0.1.8
Provides:       bundled(crate(winapi)) = 0.4.0
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.48.5
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.48.5
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.52.6
Provides:       bundled(crate(windows)) = 0.52.0
Provides:       bundled(crate(windows_i686_gnu)) = 0.48.5
Provides:       bundled(crate(windows_i686_gnu)) = 0.52.6
Provides:       bundled(crate(windows_i686_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_i686_msvc)) = 0.48.5
Provides:       bundled(crate(windows_i686_msvc)) = 0.52.6
Provides:       bundled(crate(windows)) = 0.48.0
Provides:       bundled(crate(windows)) = 0.52.0
Provides:       bundled(crate(windows)) = 0.48.5
Provides:       bundled(crate(windows)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.52.6
Provides:       bundled(crate(winnow)) = 0.5.40
Provides:       bundled(crate(winnow)) = 0.6.18
Provides:       bundled(crate(winreg)) = 0.52.0
Provides:       bundled(crate(xdg)) = 1.2.0
Provides:       bundled(crate(zbus)) = 3.15.2
Provides:       bundled(crate(zbus_macros)) = 3.15.2
Provides:       bundled(crate(zbus_names)) = 2.6.1
Provides:       bundled(crate(zerocopy)) = 0.6.6
Provides:       bundled(crate(zerocopy)) = 0.7.35
Provides:       bundled(crate(zerocopy)) = 0.6.6
Provides:       bundled(crate(zerocopy)) = 0.7.35
Provides:       bundled(crate(zeroize)) = 1.8.1
Provides:       bundled(crate(zeroize_derive)) = 1.4.2
Provides:       bundled(crate(zune)) = 0.4.12
Provides:       bundled(crate(zune)) = 0.2.54
Provides:       bundled(crate(zune)) = 0.4.13
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
%cargo_install


%files
%license LICENSE
%doc README.md
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc README.md
%{_bindir}/steamguard


%changelog
* Fri Aug 01 2025 Phantom X <megaphantomx at hotmail dot com> - 0.17.1-1
- Initial spec

