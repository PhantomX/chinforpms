# prevent library files from being installed
%global cargo_install_lib 0

# Use vendor tarball
%bcond vendor 1

%global vendor_hash ba3c836987d521e92b4b6b92c2cabbc3

%global appname io.github.doukutsu_rs.%{name}

Name:           doukutsu-rs
Version:        1.0.0
Release:        1%{?dist}
Summary:        A faithful and open-source remake of Cave Story's engine written in Rust 

License:        MIT
URL:            https://github.com/%{name}/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%if %{with vendor}
# cargo vendor-filterer --versioned-dirs --platform=x86_64-unknown-linux-gnu && tar --numeric-owner -cvJf ../%%{name}-%%{version}-vendor.tar.xz vendor/
Source1:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-%{version}-vendor.tar.xz/%{vendor_hash}/%{name}-%{version}-vendor.tar.xz
%endif
Source10:       %{name}-%{version}-vendor-config.toml
Source11:       README.Fedora

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  rust-packaging
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(xext)
BuildRequires:  sdl_gamecontrollerdb
Requires:       hicolor-icon-theme

%if %{with vendor}
# for i in * ;do echo "Provides:       bundled(crate(${i%%-*})) = ${i##*-}";done
Provides:       bundled(crate(adler2)) = 2.0.1
Provides:       bundled(crate(aho-corasick)) = 1.1.4
Provides:       bundled(crate(alsa)) = 0.9.1
Provides:       bundled(crate(alsa-sys)) = 0.3.1
Provides:       bundled(crate(android_system_properties)) = 0.1.5
Provides:       bundled(crate(anstyle)) = 1.0.14
Provides:       bundled(crate(autocfg)) = 1.5.1
Provides:       bundled(crate(bindgen)) = 0.62.0
Provides:       bundled(crate(bindgen)) = 0.72.1
Provides:       bundled(crate(bitfield)) = 0.16.1
Provides:       bundled(crate(bitflags)) = 1.3.2
Provides:       bundled(crate(bitflags)) = 2.12.1
Provides:       bundled(crate(block)) = 0.1.6
Provides:       bundled(crate(bumpalo)) = 3.20.3
Provides:       bundled(crate(bytemuck)) = 1.25.0
Provides:       bundled(crate(byteorder)) = 1.5.0
Provides:       bundled(crate(bytes)) = 1.11.1
Provides:       bundled(crate(case_insensitive_hashmap)) = 1.0.1
Provides:       bundled(crate(cc)) = 1.2.63
Provides:       bundled(crate(cesu8)) = 1.1.0
Provides:       bundled(crate(cexpr)) = 0.6.0
Provides:       bundled(crate(cfg-if)) = 0.1.10
Provides:       bundled(crate(cfg-if)) = 1.0.4
Provides:       bundled(crate(cgl)) = 0.3.2
Provides:       bundled(crate(chlorine)) = 1.0.13
Provides:       bundled(crate(chrono)) = 0.4.44
Provides:       bundled(crate(clang-sys)) = 1.8.1
Provides:       bundled(crate(clap)) = 4.6.1
Provides:       bundled(crate(clap_builder)) = 4.6.0
Provides:       bundled(crate(clap_derive)) = 4.6.1
Provides:       bundled(crate(clap_lex)) = 1.1.0
Provides:       bundled(crate(cmake)) = 0.1.58
Provides:       bundled(crate(cocoa)) = 0.23.0
Provides:       bundled(crate(cocoa)) = 0.24.1
Provides:       bundled(crate(cocoa-foundation)) = 0.1.2
Provides:       bundled(crate(color_quant)) = 1.1.0
Provides:       bundled(crate(combine)) = 4.6.7
Provides:       bundled(crate(coreaudio-rs)) = 0.11.3
Provides:       bundled(crate(coreaudio-sys)) = 0.2.17
Provides:       bundled(crate(core-foundation)) = 0.7.0
Provides:       bundled(crate(core-foundation)) = 0.9.4
Provides:       bundled(crate(core-foundation-sys)) = 0.7.0
Provides:       bundled(crate(core-foundation-sys)) = 0.8.7
Provides:       bundled(crate(core-graphics)) = 0.19.2
Provides:       bundled(crate(core-graphics)) = 0.22.3
Provides:       bundled(crate(core-graphics-types)) = 0.1.3
Provides:       bundled(crate(core-video-sys)) = 0.1.4
Provides:       bundled(crate(cpal)) = 0.15.3
Provides:       bundled(crate(crc32fast)) = 1.5.0
Provides:       bundled(crate(crossbeam)) = 0.8.4
Provides:       bundled(crate(crossbeam-channel)) = 0.5.15
Provides:       bundled(crate(crossbeam-deque)) = 0.8.6
Provides:       bundled(crate(crossbeam-epoch)) = 0.9.18
Provides:       bundled(crate(crossbeam-queue)) = 0.3.12
Provides:       bundled(crate(crossbeam-utils)) = 0.8.21
Provides:       bundled(crate(cty)) = 0.2.2
Provides:       bundled(crate(darling)) = 0.13.4
Provides:       bundled(crate(darling_core)) = 0.13.4
Provides:       bundled(crate(darling_macro)) = 0.13.4
Provides:       bundled(crate(dasp_sample)) = 0.11.0
Provides:       bundled(crate(dataview)) = 1.0.2
Provides:       bundled(crate(deko3d)) = 0.1.0
Provides:       bundled(crate(deko3d-sys)) = 0.1.0
Provides:       bundled(crate(directories)) = 3.0.2
Provides:       bundled(crate(dirs-sys)) = 0.3.7
Provides:       bundled(crate(discord-rich-presence)) = 1.1.0
Provides:       bundled(crate(dispatch)) = 0.2.0
Provides:       bundled(crate(displaydoc)) = 0.2.6
Provides:       bundled(crate(downcast)) = 0.11.0
Provides:       bundled(crate(either)) = 1.16.0
Provides:       bundled(crate(encoding_rs)) = 0.8.35
Provides:       bundled(crate(equivalent)) = 1.0.2
Provides:       bundled(crate(erasable)) = 1.3.0
Provides:       bundled(crate(errno)) = 0.3.14
Provides:       bundled(crate(fdeflate)) = 0.3.7
Provides:       bundled(crate(fern)) = 0.6.2
Provides:       bundled(crate(find-msvc-tools)) = 0.1.9
Provides:       bundled(crate(flate2)) = 1.1.9
Provides:       bundled(crate(fnv)) = 1.0.7
Provides:       bundled(crate(foreign-types)) = 0.3.2
Provides:       bundled(crate(foreign-types-shared)) = 0.1.1
Provides:       bundled(crate(form_urlencoded)) = 1.2.2
Provides:       bundled(crate(futures-core)) = 0.3.32
Provides:       bundled(crate(futures-task)) = 0.3.32
Provides:       bundled(crate(futures-util)) = 0.3.32
Provides:       bundled(crate(getrandom)) = 0.2.17
Provides:       bundled(crate(getrandom)) = 0.3.4
Provides:       bundled(crate(gl_generator)) = 0.14.0
Provides:       bundled(crate(glob)) = 0.3.3
Provides:       bundled(crate(glutin)) = 0.26.0
Provides:       bundled(crate(glutin_egl_sys)) = 0.1.5
Provides:       bundled(crate(glutin_emscripten_sys)) = 0.1.1
Provides:       bundled(crate(glutin_gles2_sys)) = 0.1.5
Provides:       bundled(crate(glutin_glx_sys)) = 0.1.7
Provides:       bundled(crate(glutin_wgl_sys)) = 0.1.5
Provides:       bundled(crate(half)) = 1.8.3
Provides:       bundled(crate(hashbrown)) = 0.17.1
Provides:       bundled(crate(heck)) = 0.4.1
Provides:       bundled(crate(heck)) = 0.5.0
Provides:       bundled(crate(home)) = 0.5.12
Provides:       bundled(crate(iana-time-zone)) = 0.1.65
Provides:       bundled(crate(iana-time-zone-haiku)) = 0.1.2
Provides:       bundled(crate(icu_collections)) = 2.2.0
Provides:       bundled(crate(icu_locale_core)) = 2.2.0
Provides:       bundled(crate(icu_normalizer)) = 2.2.0
Provides:       bundled(crate(icu_normalizer_data)) = 2.2.0
Provides:       bundled(crate(icu_properties)) = 2.2.0
Provides:       bundled(crate(icu_properties_data)) = 2.2.0
Provides:       bundled(crate(icu_provider)) = 2.2.0
Provides:       bundled(crate(ident_case)) = 1.0.1
Provides:       bundled(crate(idna)) = 1.1.0
Provides:       bundled(crate(idna_adapter)) = 1.2.2
Provides:       bundled(crate(image)) = 0.24.9
Provides:       bundled(crate(imgui)) = 0.12.0
Provides:       bundled(crate(imgui-sys)) = 0.12.0
Provides:       bundled(crate(indexmap)) = 2.14.0
Provides:       bundled(crate(instant)) = 0.1.13
Provides:       bundled(crate(itertools)) = 0.10.5
Provides:       bundled(crate(itertools)) = 0.13.0
Provides:       bundled(crate(itoa)) = 1.0.18
Provides:       bundled(crate(jni)) = 0.20.0
Provides:       bundled(crate(jni)) = 0.21.1
Provides:       bundled(crate(jni-sys)) = 0.3.1
Provides:       bundled(crate(jni-sys)) = 0.4.1
Provides:       bundled(crate(jni-sys-macros)) = 0.4.1
Provides:       bundled(crate(jobserver)) = 0.1.34
Provides:       bundled(crate(js-sys)) = 0.3.99
Provides:       bundled(crate(khronos_api)) = 3.1.0
Provides:       bundled(crate(lazycell)) = 1.3.0
Provides:       bundled(crate(lazy_static)) = 1.5.0
Provides:       bundled(crate(lewton)) = 0.10.2
Provides:       bundled(crate(libc)) = 0.2.186
Provides:       bundled(crate(libloading)) = 0.6.7
Provides:       bundled(crate(libloading)) = 0.8.9
Provides:       bundled(crate(libredox)) = 0.1.17
Provides:       bundled(crate(linux-raw-sys)) = 0.4.15
Provides:       bundled(crate(litemap)) = 0.8.2
Provides:       bundled(crate(lock_api)) = 0.4.14
Provides:       bundled(crate(log)) = 0.4.31
Provides:       bundled(crate(mach2)) = 0.4.3
Provides:       bundled(crate(malloc_buf)) = 0.0.6
Provides:       bundled(crate(memchr)) = 2.8.1
Provides:       bundled(crate(minimal-lexical)) = 0.2.1
Provides:       bundled(crate(miniz_oxide)) = 0.8.9
Provides:       bundled(crate(mint)) = 0.5.9
Provides:       bundled(crate(mio)) = 0.7.14
Provides:       bundled(crate(mio-misc)) = 1.2.2
Provides:       bundled(crate(miow)) = 0.3.7
Provides:       bundled(crate(ndk)) = 0.7.0
Provides:       bundled(crate(ndk)) = 0.8.0
Provides:       bundled(crate(ndk-context)) = 0.1.1
Provides:       bundled(crate(ndk-glue)) = 0.7.0
Provides:       bundled(crate(ndk-macro)) = 0.3.0
Provides:       bundled(crate(ndk-sys)) = 0.4.1+23.1.7779620
Provides:       bundled(crate(ndk-sys)) = 0.5.0+25.2.9519653
Provides:       bundled(crate(nom)) = 7.1.3
Provides:       bundled(crate(no-std-compat)) = 0.4.1
Provides:       bundled(crate(ntapi)) = 0.3.7
Provides:       bundled(crate(num-derive)) = 0.3.3
Provides:       bundled(crate(num-derive)) = 0.4.2
Provides:       bundled(crate(num_enum)) = 0.5.11
Provides:       bundled(crate(num_enum)) = 0.7.6
Provides:       bundled(crate(num_enum_derive)) = 0.5.11
Provides:       bundled(crate(num_enum_derive)) = 0.7.6
Provides:       bundled(crate(num-traits)) = 0.2.19
Provides:       bundled(crate(objc)) = 0.2.7
Provides:       bundled(crate(oboe)) = 0.6.1
Provides:       bundled(crate(oboe-sys)) = 0.6.1
Provides:       bundled(crate(ogg)) = 0.8.0
Provides:       bundled(crate(once_cell)) = 1.21.4
Provides:       bundled(crate(open)) = 3.2.0
Provides:       bundled(crate(osmesa-sys)) = 0.1.2
Provides:       bundled(crate(parking_lot)) = 0.11.2
Provides:       bundled(crate(parking_lot)) = 0.12.5
Provides:       bundled(crate(parking_lot_core)) = 0.8.6
Provides:       bundled(crate(parking_lot_core)) = 0.9.12
Provides:       bundled(crate(paste)) = 1.0.15
Provides:       bundled(crate(pathdiff)) = 0.2.3
Provides:       bundled(crate(peeking_take_while)) = 0.1.2
Provides:       bundled(crate(pelite)) = 0.10.0
Provides:       bundled(crate(pelite-macros)) = 0.1.1
Provides:       bundled(crate(percent-encoding)) = 2.3.2
Provides:       bundled(crate(pin-project-lite)) = 0.2.17
Provides:       bundled(crate(pkg-config)) = 0.3.33
Provides:       bundled(crate(png)) = 0.17.16
Provides:       bundled(crate(potential_utf)) = 0.1.5
Provides:       bundled(crate(proc-macro2)) = 1.0.106
Provides:       bundled(crate(proc-macro-crate)) = 1.3.1
Provides:       bundled(crate(proc-macro-crate)) = 3.5.0
Provides:       bundled(crate(quote)) = 1.0.45
Provides:       bundled(crate(raw-window-handle)) = 0.3.4
Provides:       bundled(crate(raw-window-handle)) = 0.4.3
Provides:       bundled(crate(raw-window-handle)) = 0.5.2
Provides:       bundled(crate(rc-box)) = 1.3.0
Provides:       bundled(crate(redox_syscall)) = 0.2.16
Provides:       bundled(crate(redox_syscall)) = 0.5.18
Provides:       bundled(crate(redox_users)) = 0.4.6
Provides:       bundled(crate(r-efi)) = 5.3.0
Provides:       bundled(crate(regex)) = 1.12.3
Provides:       bundled(crate(regex-automata)) = 0.4.14
Provides:       bundled(crate(regex-syntax)) = 0.8.10
Provides:       bundled(crate(rustc-hash)) = 1.1.0
Provides:       bundled(crate(rustc-hash)) = 2.1.2
Provides:       bundled(crate(rustix)) = 0.38.44
Provides:       bundled(crate(rustversion)) = 1.0.22
Provides:       bundled(crate(same-file)) = 1.0.6
Provides:       bundled(crate(scopeguard)) = 1.2.0
Provides:       bundled(crate(sdl2)) = 0.37.0
Provides:       bundled(crate(sdl2-sys)) = 0.37.0
Provides:       bundled(crate(serde)) = 1.0.228
Provides:       bundled(crate(serde_cbor)) = 0.11.2
Provides:       bundled(crate(serde_core)) = 1.0.228
Provides:       bundled(crate(serde_derive)) = 1.0.228
Provides:       bundled(crate(serde_json)) = 1.0.150
Provides:       bundled(crate(serde_repr)) = 0.1.20
Provides:       bundled(crate(shared_library)) = 0.1.9
Provides:       bundled(crate(shlex)) = 1.3.0
Provides:       bundled(crate(shlex)) = 2.0.1
Provides:       bundled(crate(simd-adler32)) = 0.3.9
Provides:       bundled(crate(slab)) = 0.4.12
Provides:       bundled(crate(smallvec)) = 1.15.1
Provides:       bundled(crate(stable_deref_trait)) = 1.2.1
Provides:       bundled(crate(strsim)) = 0.10.0
Provides:       bundled(crate(strum)) = 0.24.1
Provides:       bundled(crate(strum_macros)) = 0.24.3
Provides:       bundled(crate(syn)) = 1.0.109
Provides:       bundled(crate(syn)) = 2.0.117
Provides:       bundled(crate(synstructure)) = 0.13.2
Provides:       bundled(crate(thiserror)) = 1.0.69
Provides:       bundled(crate(thiserror)) = 2.0.18
Provides:       bundled(crate(thiserror-impl)) = 1.0.69
Provides:       bundled(crate(thiserror-impl)) = 2.0.18
Provides:       bundled(crate(tinystr)) = 0.8.3
Provides:       bundled(crate(tinyvec)) = 1.11.0
Provides:       bundled(crate(tinyvec_macros)) = 0.1.1
Provides:       bundled(crate(toml)) = 0.5.11
Provides:       bundled(crate(toml_datetime)) = 0.6.11
Provides:       bundled(crate(toml_datetime-1.1.1+spec)) = 1.1.0
Provides:       bundled(crate(toml_edit)) = 0.19.15
Provides:       bundled(crate(toml_edit-0.25.12+spec)) = 1.1.0
Provides:       bundled(crate(toml_parser-1.1.2+spec)) = 1.1.0
Provides:       bundled(crate(unicase)) = 2.9.0
Provides:       bundled(crate(unicode-ident)) = 1.0.24
Provides:       bundled(crate(url)) = 2.5.8
Provides:       bundled(crate(utf8_iter)) = 1.0.4
Provides:       bundled(crate(uuid)) = 0.8.2
Provides:       bundled(crate(vec_mut_scan)) = 0.4.0
Provides:       bundled(crate(version-compare)) = 0.1.1
Provides:       bundled(crate(walkdir)) = 2.5.0
Provides:       bundled(crate(wasi-0.11.1+wasi-snapshot)) = preview1
Provides:       bundled(crate(wasip2-1.0.3+wasi)) = 0.2.9
Provides:       bundled(crate(wasm-bindgen)) = 0.2.122
Provides:       bundled(crate(wasm-bindgen-futures)) = 0.4.72
Provides:       bundled(crate(wasm-bindgen-macro)) = 0.2.122
Provides:       bundled(crate(wasm-bindgen-macro-support)) = 0.2.122
Provides:       bundled(crate(wasm-bindgen-shared)) = 0.2.122
Provides:       bundled(crate(webbrowser)) = 0.8.15
Provides:       bundled(crate(web-sys)) = 0.3.99
Provides:       bundled(crate(which)) = 4.4.2
Provides:       bundled(crate(winapi)) = 0.3.9
Provides:       bundled(crate(winapi-i686-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(winapi-util)) = 0.1.11
Provides:       bundled(crate(winapi-x86_64-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(windows)) = 0.54.0
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.42.2
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.42.2
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.52.6
Provides:       bundled(crate(windows-core)) = 0.54.0
Provides:       bundled(crate(windows-core)) = 0.62.2
Provides:       bundled(crate(windows_i686_gnu)) = 0.42.2
Provides:       bundled(crate(windows_i686_gnu)) = 0.52.6
Provides:       bundled(crate(windows_i686_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_i686_msvc)) = 0.42.2
Provides:       bundled(crate(windows_i686_msvc)) = 0.52.6
Provides:       bundled(crate(windows-implement)) = 0.60.2
Provides:       bundled(crate(windows-interface)) = 0.59.3
Provides:       bundled(crate(windows-link)) = 0.2.1
Provides:       bundled(crate(windows-result)) = 0.1.2
Provides:       bundled(crate(windows-result)) = 0.4.1
Provides:       bundled(crate(windows-strings)) = 0.5.1
Provides:       bundled(crate(windows-sys)) = 0.42.0
Provides:       bundled(crate(windows-sys)) = 0.45.0
Provides:       bundled(crate(windows-sys)) = 0.59.0
Provides:       bundled(crate(windows-sys)) = 0.61.2
Provides:       bundled(crate(windows-targets)) = 0.42.2
Provides:       bundled(crate(windows-targets)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.42.2
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.42.2
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.42.2
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.52.6
Provides:       bundled(crate(winit)) = 0.24.0
Provides:       bundled(crate(winnow)) = 0.5.40
Provides:       bundled(crate(winnow)) = 1.0.3
Provides:       bundled(crate(winres)) = 0.1.12
Provides:       bundled(crate(wit-bindgen)) = 0.57.1
Provides:       bundled(crate(writeable)) = 0.6.3
Provides:       bundled(crate(x11-dl)) = 2.21.0
Provides:       bundled(crate(xml-rs)) = 0.8.28
Provides:       bundled(crate(xmltree)) = 0.10.3
Provides:       bundled(crate(yoke)) = 0.8.3
Provides:       bundled(crate(yoke-derive)) = 0.8.2
Provides:       bundled(crate(zerofrom)) = 0.1.8
Provides:       bundled(crate(zerofrom-derive)) = 0.1.7
Provides:       bundled(crate(zerotrie)) = 0.2.4
Provides:       bundled(crate(zerovec)) = 0.11.6
Provides:       bundled(crate(zerovec-derive)) = 0.11.3
Provides:       bundled(crate(zmij)) = 1.0.21
%endif


%description
A reimplementation of the Cave Story (Doukutsu Monogatari) engine with many
quality-of-life improvements. It lets you enjoy the 2004 indie classic like a
modern game, with support for the original freeware, Cave Story+, and NX data
files.

%prep
%autosetup -p1 %{?with_vendor:-a1}

sed -e '/sdl2/s|, "static-link"||g' -i Cargo.toml

%if %{with vendor}
%cargo_prep -v vendor
cat %{S:10} >> .cargo/config.toml
%else
%generate_buildrequires
%cargo_generate_buildrequires
%endif

install -m644 -p %{S:11} .

cat > %{name}.sh <<'EOF'
#!/usr/bin/bash
set -e
DRSBIN="%{_libexecdir}/%{name}"

if [[ "${XDG_DATA_HOME}" ]] ;then
  DRSSHOME="${XDG_DATA_HOME}/%{name}"
else
  DRSHOME="${HOME}/.local/share/%{name}"
fi

shopt -s nullglob

CAVESTORY_DATA_DIR="${CAVESTORY_DATA_DIR:-${DRSHOME}/data}"
export CAVESTORY_DATA_DIR

exec "${DRSBIN}" "$@"
EOF

cp -pf %{_datadir}/SDL_GameControllerDB/gamecontrollerdb.txt src/data/builtin/gamecontrollerdb.txt


%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%if %{with vendor}
%{cargo_vendor_manifest}
%endif


%install
mkdir -p %{buildroot}%{_libexecdir}
install -pm0755 target/release/%{name} %{buildroot}%{_libexecdir}/%{name}

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}.sh %{buildroot}%{_bindir}/%{name}


mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  res/flatpak/%{appname}.desktop

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 res/flatpak/%{appname}.metainfo.xml %{buildroot}%{_metainfodir}/


mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
install -pm0644 res/flatpak/%{appname}.png \
  %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{appname}.png

for res in 16 22 24 32 36 48 64 72 96 128 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick res/flatpak/%{appname}.png \
    -filter Lanczos -resize ${res}x${res} ${dir}/%{appname}.png
done


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%files
%license LICENSE
%license %license LICENSE.dependencies
%doc README.md
%doc README.Fedora
%{_bindir}/%{name}
%{_libexecdir}/%{name}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appname}.png
%{_metainfodir}/%{appname}.metainfo.xml


%changelog
* Thu Jun 11 2026 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-1
- Initial spec

