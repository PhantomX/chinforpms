%bcond check 0

# Use vendor tarball
%bcond vendor 1

%global vendor_hash eef5d40a00f885d33c3cffc72291efaf
%global vendor_hash2 e45c78cec540e06edc2a9dd631cbdbb8

%global uniffi_bindgen_ver 0.9.0

%global soname_ver 0

Name:           wallet-engine
Version:        0.0.7
Release:        1%{?dist}
Summary:        Rust library for drawing Lottie animations

URL:            https://github.com/i582/%{name}
License:        MIT OR Apache-2.0

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%if %{with vendor}
# cargo vendor --versioned-dirs && tar --numeric-owner -cvJf ../%%{name}-%%{version}-vendor.tar.xz vendor/
Source1:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-%{version}-vendor.tar.xz/%{vendor_hash}/%{name}-%{version}-vendor.tar.xz
Source2:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/uniffi-bindgen-cpp-%{uniffi_bindgen_ver}-vendor.tar.xz/%{vendor_hash2}/uniffi-bindgen-cpp-%{uniffi_bindgen_ver}-vendor.tar.xz
%endif

Patch0:         %{url}/commit/e59e0d89d7ee90c388bf36e3334c5b276f396697.patch#/%{name}-gh-e59e0d8.patch
Patch1:         https://github.com/desktop-app/patches/raw/aec474953ff7ee9b6e4cd9b8658288ea86d124f3/wallet-engine.patch#/%{name}-gh-desktop-app-wallet-engine.patch

ExclusiveArch:  %{rust_arches}

BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  cmake
BuildRequires:  rust-packaging

%if %{with vendor}
# for i in * ;do echo "Provides:       bundled(crate(${i%%-*})) = ${i##*-}";done
Provides:       bundled(crate(aead)) = 0.5.2
Provides:       bundled(crate(aes)) = 0.8.4
Provides:       bundled(crate(android_system_properties)) = 0.1.6
Provides:       bundled(crate(anyhow)) = 1.0.102
Provides:       bundled(crate(arrayvec)) = 0.7.8
Provides:       bundled(crate(askama)) = 0.16.0
Provides:       bundled(crate(askama_derive)) = 0.16.0
Provides:       bundled(crate(askama_macros)) = 0.16.0
Provides:       bundled(crate(askama_parser)) = 0.16.0
Provides:       bundled(crate(async-trait)) = 0.1.89
Provides:       bundled(crate(atomic-waker)) = 1.1.2
Provides:       bundled(crate(autocfg)) = 1.5.1
Provides:       bundled(crate(base64)) = 0.22.1
Provides:       bundled(crate(base64ct)) = 1.8.3
Provides:       bundled(crate(basic-toml)) = 0.1.10
Provides:       bundled(crate(bip39)) = 2.2.2
Provides:       bundled(crate(bitcoin_hashes)) = 0.14.101
Provides:       bundled(crate(bitflags)) = 2.13.1
Provides:       bundled(crate(bit-set)) = 0.8.0
Provides:       bundled(crate(bitstream-io)) = 4.10.0
Provides:       bundled(crate(bit-vec)) = 0.8.0
Provides:       bundled(crate(bitvec)) = 1.1.1
Provides:       bundled(crate(block-buffer)) = 0.10.4
Provides:       bundled(crate(bnum)) = 0.12.1
Provides:       bundled(crate(bumpalo)) = 3.20.3
Provides:       bundled(crate(bytes)) = 1.12.1
Provides:       bundled(crate(camino)) = 1.2.5
Provides:       bundled(crate(cargo_metadata)) = 0.23.1
Provides:       bundled(crate(cargo-platform)) = 0.3.2
Provides:       bundled(crate(cc)) = 1.4.2
Provides:       bundled(crate(cfg_aliases)) = 0.2.2
Provides:       bundled(crate(cfg-if)) = 1.0.4
Provides:       bundled(crate(chacha20)) = 0.10.1
Provides:       bundled(crate(chrono)) = 0.4.45
Provides:       bundled(crate(cipher)) = 0.4.4
Provides:       bundled(crate(const-oid)) = 0.9.6
Provides:       bundled(crate(convert_case)) = 0.11.0
Provides:       bundled(crate(core-foundation-sys)) = 0.8.7
Provides:       bundled(crate(cpufeatures)) = 0.2.17
Provides:       bundled(crate(cpufeatures)) = 0.3.0
Provides:       bundled(crate(crc)) = 3.4.0
Provides:       bundled(crate(crc-catalog)) = 2.5.0
Provides:       bundled(crate(crypto_box)) = 0.9.1
Provides:       bundled(crate(crypto-common)) = 0.1.7
Provides:       bundled(crate(crypto_secretbox)) = 0.1.1
Provides:       bundled(crate(curve25519-dalek)) = 4.1.3
Provides:       bundled(crate(curve25519-dalek-derive)) = 0.1.1
Provides:       bundled(crate(deluxe)) = 0.5.0
Provides:       bundled(crate(deluxe-core)) = 0.5.0
Provides:       bundled(crate(deluxe-macros)) = 0.5.0
Provides:       bundled(crate(der)) = 0.7.10
Provides:       bundled(crate(digest)) = 0.10.7
Provides:       bundled(crate(displaydoc)) = 0.2.7
Provides:       bundled(crate(ed25519)) = 2.2.3
Provides:       bundled(crate(ed25519-dalek)) = 2.2.0
Provides:       bundled(crate(equivalent)) = 1.0.2
Provides:       bundled(crate(errno)) = 0.3.14
Provides:       bundled(crate(fastnum)) = 0.7.4
Provides:       bundled(crate(fastrand)) = 2.5.0
Provides:       bundled(crate(fiat-crypto)) = 0.2.9
Provides:       bundled(crate(find-msvc-tools)) = 0.1.10
Provides:       bundled(crate(fnv)) = 1.0.7
Provides:       bundled(crate(form_urlencoded)) = 1.2.2
Provides:       bundled(crate(fs-err)) = 3.3.1
Provides:       bundled(crate(funty)) = 2.0.0
Provides:       bundled(crate(futures)) = 0.3.31
Provides:       bundled(crate(futures-channel)) = 0.3.34
Provides:       bundled(crate(futures-core)) = 0.3.34
Provides:       bundled(crate(futures-executor)) = 0.3.34
Provides:       bundled(crate(futures-io)) = 0.3.34
Provides:       bundled(crate(futures-macro)) = 0.3.34
Provides:       bundled(crate(futures-sink)) = 0.3.34
Provides:       bundled(crate(futures-task)) = 0.3.34
Provides:       bundled(crate(futures-util)) = 0.3.34
Provides:       bundled(crate(generic-array)) = 0.14.7
Provides:       bundled(crate(getrandom)) = 0.2.17
Provides:       bundled(crate(getrandom)) = 0.3.4
Provides:       bundled(crate(getrandom)) = 0.4.3
Provides:       bundled(crate(glob)) = 0.3.4
Provides:       bundled(crate(goblin)) = 0.8.2
Provides:       bundled(crate(hashbrown)) = 0.17.1
Provides:       bundled(crate(heck)) = 0.4.1
Provides:       bundled(crate(heck)) = 0.5.0
Provides:       bundled(crate(hex)) = 0.4.3
Provides:       bundled(crate(hex-conservative)) = 0.2.2
Provides:       bundled(crate(hmac)) = 0.12.1
Provides:       bundled(crate(http)) = 1.5.0
Provides:       bundled(crate(httparse)) = 1.10.1
Provides:       bundled(crate(http-body)) = 1.1.0
Provides:       bundled(crate(http-body-util)) = 0.1.5
Provides:       bundled(crate(hyper)) = 1.11.0
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
Provides:       bundled(crate(idna)) = 1.1.0
Provides:       bundled(crate(idna_adapter)) = 1.2.2
Provides:       bundled(crate(if_chain)) = 1.0.3
Provides:       bundled(crate(indexmap)) = 2.14.0
Provides:       bundled(crate(inout)) = 0.1.4
Provides:       bundled(crate(ipnet)) = 2.12.1
Provides:       bundled(crate(itoa)) = 1.0.18
Provides:       bundled(crate(js-sys)) = 0.3.104
Provides:       bundled(crate(libc)) = 0.2.189
Provides:       bundled(crate(libm)) = 0.2.16
Provides:       bundled(crate(linux-raw-sys)) = 0.12.1
Provides:       bundled(crate(litemap)) = 0.8.2
Provides:       bundled(crate(lock_api)) = 0.4.14
Provides:       bundled(crate(log)) = 0.4.33
Provides:       bundled(crate(lru-slab)) = 0.1.2
Provides:       bundled(crate(memchr)) = 2.8.3
Provides:       bundled(crate(minimal-lexical)) = 0.2.1
Provides:       bundled(crate(mio)) = 1.2.2
Provides:       bundled(crate(nom)) = 7.1.3
Provides:       bundled(crate(no_std_io2)) = 0.9.4
Provides:       bundled(crate(num-bigint)) = 0.4.8
Provides:       bundled(crate(num-integer)) = 0.1.47
Provides:       bundled(crate(num-traits)) = 0.2.19
Provides:       bundled(crate(once_cell)) = 1.21.4
Provides:       bundled(crate(opaque-debug)) = 0.3.1
Provides:       bundled(crate(ordered-float)) = 2.10.1
Provides:       bundled(crate(parking_lot)) = 0.12.5
Provides:       bundled(crate(parking_lot_core)) = 0.9.12
Provides:       bundled(crate(password-hash)) = 0.5.0
Provides:       bundled(crate(pbkdf2)) = 0.12.2
Provides:       bundled(crate(percent-encoding)) = 2.3.2
Provides:       bundled(crate(pin-project-lite)) = 0.2.17
Provides:       bundled(crate(pkcs8)) = 0.10.2
Provides:       bundled(crate(plain)) = 0.2.3
Provides:       bundled(crate(poly1305)) = 0.8.0
Provides:       bundled(crate(potential_utf)) = 0.1.5
Provides:       bundled(crate(ppv-lite86)) = 0.2.21
Provides:       bundled(crate(proc-macro2)) = 1.0.107
Provides:       bundled(crate(proc-macro-crate)) = 1.3.1
Provides:       bundled(crate(proc-macro-crate)) = 3.5.0
Provides:       bundled(crate(proptest)) = 1.11.0
Provides:       bundled(crate(quick-error)) = 1.2.3
Provides:       bundled(crate(quinn)) = 0.11.11
Provides:       bundled(crate(quinn-proto)) = 0.11.16
Provides:       bundled(crate(quinn-udp)) = 0.5.15
Provides:       bundled(crate(quote)) = 1.0.47
Provides:       bundled(crate(radium)) = 0.7.0
Provides:       bundled(crate(rand)) = 0.10.2
Provides:       bundled(crate(rand)) = 0.9.5
Provides:       bundled(crate(rand_chacha)) = 0.9.0
Provides:       bundled(crate(rand_core)) = 0.10.1
Provides:       bundled(crate(rand_core)) = 0.6.4
Provides:       bundled(crate(rand_core)) = 0.9.5
Provides:       bundled(crate(rand_pcg)) = 0.10.2
Provides:       bundled(crate(rand_xorshift)) = 0.4.0
Provides:       bundled(crate(redox_syscall)) = 0.5.18
Provides:       bundled(crate(r-efi)) = 5.3.0
Provides:       bundled(crate(r-efi)) = 6.0.0
Provides:       bundled(crate(regex-syntax)) = 0.8.11
Provides:       bundled(crate(reqwest)) = 0.12.28
Provides:       bundled(crate(ring)) = 0.17.14
Provides:       bundled(crate(rustc-hash)) = 2.1.3
Provides:       bundled(crate(rustc_version)) = 0.4.1
Provides:       bundled(crate(rustix)) = 1.1.4
Provides:       bundled(crate(rustls)) = 0.23.45
Provides:       bundled(crate(rustls-pki-types)) = 1.15.1
Provides:       bundled(crate(rustls-webpki)) = 0.103.14
Provides:       bundled(crate(rustversion)) = 1.0.23
Provides:       bundled(crate(rusty-fork)) = 0.3.1
Provides:       bundled(crate(ryu)) = 1.0.23
Provides:       bundled(crate(salsa20)) = 0.10.2
Provides:       bundled(crate(scopeguard)) = 1.2.0
Provides:       bundled(crate(scroll)) = 0.12.0
Provides:       bundled(crate(scroll_derive)) = 0.12.1
Provides:       bundled(crate(semver)) = 1.0.28
Provides:       bundled(crate(serde)) = 1.0.229
Provides:       bundled(crate(serde-aux)) = 4.7.0
Provides:       bundled(crate(serde_core)) = 1.0.229
Provides:       bundled(crate(serde_derive)) = 1.0.229
Provides:       bundled(crate(serde_json)) = 1.0.151
Provides:       bundled(crate(serde_spanned)) = 1.1.1
Provides:       bundled(crate(serde_urlencoded)) = 0.7.1
Provides:       bundled(crate(serde-value)) = 0.7.0
Provides:       bundled(crate(sha2)) = 0.10.9
Provides:       bundled(crate(shlex)) = 2.0.1
Provides:       bundled(crate(signature)) = 2.2.0
Provides:       bundled(crate(similar)) = 2.7.0
Provides:       bundled(crate(siphasher)) = 1.0.3
Provides:       bundled(crate(slab)) = 0.4.12
Provides:       bundled(crate(smallvec)) = 1.15.2
Provides:       bundled(crate(smawk)) = 0.3.3
Provides:       bundled(crate(socket2)) = 0.6.5
Provides:       bundled(crate(spki)) = 0.7.3
Provides:       bundled(crate(stable_deref_trait)) = 1.2.1
Provides:       bundled(crate(static_assertions)) = 1.1.0
Provides:       bundled(crate(strsim)) = 0.10.0
Provides:       bundled(crate(subtle)) = 2.6.1
Provides:       bundled(crate(syn)) = 2.0.119
Provides:       bundled(crate(syn)) = 3.0.3
Provides:       bundled(crate(sync_wrapper)) = 1.0.2
Provides:       bundled(crate(synstructure)) = 0.13.2
Provides:       bundled(crate(tap)) = 1.0.1
Provides:       bundled(crate(tempfile)) = 3.27.0
Provides:       bundled(crate(textwrap)) = 0.16.2
Provides:       bundled(crate(thiserror)) = 2.0.17
Provides:       bundled(crate(thiserror-impl)) = 2.0.17
Provides:       bundled(crate(tinystr)) = 0.8.3
Provides:       bundled(crate(tinyvec)) = 1.12.0
Provides:       bundled(crate(tinyvec_macros)) = 0.1.1
Provides:       bundled(crate(tokio)) = 1.53.1
Provides:       bundled(crate(tokio-rustls)) = 0.26.4
Provides:       bundled(crate(toml-1.1.4+spec)) = 1.1.0
Provides:       bundled(crate(toml_datetime)) = 0.6.11
Provides:       bundled(crate(toml_datetime-1.1.1+spec)) = 1.1.0
Provides:       bundled(crate(toml_edit)) = 0.19.15
Provides:       bundled(crate(toml_edit-0.25.13+spec)) = 1.1.0
Provides:       bundled(crate(toml_parser-1.1.3+spec)) = 1.1.0
Provides:       bundled(crate(toml_writer-1.1.2+spec)) = 1.1.0
Provides:       bundled(crate(ton)) = ton
Provides:       bundled(crate(ton_core)) = 0.1.4
Provides:       bundled(crate(ton_macros)) = 0.1.2
Provides:       bundled(crate(tower)) = 0.5.3
Provides:       bundled(crate(tower-http)) = 0.6.11
Provides:       bundled(crate(tower-layer)) = 0.3.3
Provides:       bundled(crate(tower-service)) = 0.3.3
Provides:       bundled(crate(tracing)) = 0.1.44
Provides:       bundled(crate(tracing-core)) = 0.1.36
Provides:       bundled(crate(try-lock)) = 0.2.5
Provides:       bundled(crate(typenum)) = 1.20.1
Provides:       bundled(crate(unarray)) = 0.1.4
Provides:       bundled(crate(unicode-ident)) = 1.0.24
Provides:       bundled(crate(unicode-normalization)) = 0.1.25
Provides:       bundled(crate(unicode-segmentation)) = 1.13.3
Provides:       bundled(crate(uniffi)) = 0.32.0
Provides:       bundled(crate(uniffi_bindgen)) = 0.32.0
Provides:       bundled(crate(uniffi_core)) = 0.32.0
Provides:       bundled(crate(uniffi_internal_macros)) = 0.32.0
Provides:       bundled(crate(uniffi_macros)) = 0.32.0
Provides:       bundled(crate(uniffi_meta)) = 0.32.0
Provides:       bundled(crate(uniffi_pipeline)) = 0.32.0
Provides:       bundled(crate(uniffi_udl)) = 0.32.0
Provides:       bundled(crate(universal-hash)) = 0.5.1
Provides:       bundled(crate(untrusted)) = 0.9.0
Provides:       bundled(crate(url)) = 2.5.7
Provides:       bundled(crate(utf8_iter)) = 1.0.4
Provides:       bundled(crate(version_check)) = 0.9.5
Provides:       bundled(crate(wait-timeout)) = 0.2.1
Provides:       bundled(crate(want)) = 0.3.1
Provides:       bundled(crate(wasi-0.11.1+wasi-snapshot)) = preview1
Provides:       bundled(crate(wasip2-1.0.4+wasi)) = 0.2.12
Provides:       bundled(crate(wasm-bindgen)) = 0.2.127
Provides:       bundled(crate(wasm-bindgen-futures)) = 0.4.77
Provides:       bundled(crate(wasm-bindgen-macro)) = 0.2.127
Provides:       bundled(crate(wasm-bindgen-macro-support)) = 0.2.127
Provides:       bundled(crate(wasm-bindgen-shared)) = 0.2.127
Provides:       bundled(crate(webpki-roots)) = 1.0.9
Provides:       bundled(crate(web-sys)) = 0.3.104
Provides:       bundled(crate(web-time)) = 1.1.0
Provides:       bundled(crate(weedle2)) = 5.0.0
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.52.6
Provides:       bundled(crate(windows-core)) = 0.62.2
Provides:       bundled(crate(windows_i686_gnu)) = 0.52.6
Provides:       bundled(crate(windows_i686_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_i686_msvc)) = 0.52.6
Provides:       bundled(crate(windows-implement)) = 0.60.2
Provides:       bundled(crate(windows-interface)) = 0.59.3
Provides:       bundled(crate(windows-link)) = 0.2.1
Provides:       bundled(crate(windows-result)) = 0.4.1
Provides:       bundled(crate(windows-strings)) = 0.5.1
Provides:       bundled(crate(windows-sys)) = 0.52.0
Provides:       bundled(crate(windows-sys)) = 0.61.2
Provides:       bundled(crate(windows-targets)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.52.6
Provides:       bundled(crate(winnow)) = 0.5.40
Provides:       bundled(crate(winnow)) = 1.0.4
Provides:       bundled(crate(wit-bindgen)) = 0.57.1
Provides:       bundled(crate(writeable)) = 0.6.3
Provides:       bundled(crate(wyz)) = 0.5.1
Provides:       bundled(crate(yoke)) = 0.8.3
Provides:       bundled(crate(yoke-derive)) = 0.8.2
Provides:       bundled(crate(zerocopy)) = 0.8.56
Provides:       bundled(crate(zerocopy-derive)) = 0.8.56
Provides:       bundled(crate(zerofrom)) = 0.1.8
Provides:       bundled(crate(zerofrom-derive)) = 0.1.7
Provides:       bundled(crate(zeroize)) = 1.9.0
Provides:       bundled(crate(zeroize_derive)) = 1.5.0
Provides:       bundled(crate(zerotrie)) = 0.2.4
Provides:       bundled(crate(zerovec)) = 0.11.6
Provides:       bundled(crate(zerovec-derive)) = 0.11.3
Provides:       bundled(crate(zmij)) = 1.0.23
%endif

%description
%{name} is Rust library for drawing Lottie animations.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 %{?with_vendor:-a1}

cat > build.rs <<'EOF'
pub fn main() {
    println!("cargo:rustc-cdylib-link-arg=-Wl,-soname,libwallet_engine.so.%{soname_ver}");
}
EOF

%if %{with vendor}
pushd bindgen/cpp
tar xf %{S:2}
%cargo_prep -v vendor
popd
mv vendor/ton vendor_ton
sed -e 's|vendor/ton|vendor_ton|g' -i Cargo.toml
%cargo_prep -v vendor
%else
%cargo_prep
%generate_buildrequires
%cargo_generate_buildrequires
%endif

%build
pushd bindgen/cpp
%cargo_build
popd
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%if %{with vendor}
%{cargo_vendor_manifest}
%endif

./bindgen/cpp/target/rpm/uniffi-bindgen-cpp --library --out-dir bindings/cpp-experimental target/rpm/libwallet_engine.so


%install
mkdir -p %{buildroot}/%{_libdir}
install -m 0755 target/rpm/libwallet_engine.so \
  %{buildroot}%{_libdir}/libwallet_engine.so.%{version}
ln -s libwallet_engine.so.%{version} %{buildroot}%{_libdir}/libwallet_engine.so.%{soname_ver}
ln -s libwallet_engine.so.%{soname_ver} %{buildroot}%{_libdir}/libwallet_engine.so

mkdir -p %{buildroot}%{_includedir}/wallet_engine
install -pm0644 bindings/cpp-experimental/wallet_engine*.{c,h}pp %{buildroot}%{_includedir}/wallet_engine


%if %{with check}
%check
%cargo_test
%endif


%files
%doc README.md
%license LICENSE-APACHE LICENSE-MIT
%{_libdir}/libwallet_engine.so.*

%files devel
%{_includedir}/wallet_engine/wallet_engine*.{c,h}pp
%{_libdir}/libwallet_engine.so


%changelog
* Sun Oct 11 2026 Phantom X <megaphantomx at hotmail dot com> - 0.0.7-1
- Initial spec

