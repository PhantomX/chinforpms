#!/bin/sh

rm -f config.h
echo "Building for Linux"

set -e

ARCH="x86_64"

GENERAL="\
    --disable-shared \
    --enable-static"

MODULES="\
    --disable-avdevice \
    --disable-filters \
    --disable-programs \
    --disable-network \
    --disable-postproc \
    --disable-encoders \
    --disable-doc \
    --disable-ffplay \
    --disable-ffprobe \
    --disable-ffmpeg"

VIDEO_DECODERS="\
    --enable-decoder=h264 \
    --enable-decoder=mpeg4 \
    --enable-decoder=mpeg2video \
    --enable-decoder=mjpeg \
    --enable-decoder=mjpegb \
    --enable-decoder=mov"

AUDIO_DECODERS="\
    --enable-decoder=aac \
    --enable-decoder=aac_latm \
    --enable-decoder=atrac3 \
    --enable-decoder=atrac3p \
    --enable-decoder=atrac9 \
    --enable-decoder=mp3 \
    --enable-decoder=pcm_s16le \
    --enable-decoder=pcm_s8"

DEMUXERS="\
    --enable-demuxer=h264 \
    --enable-demuxer=m4v \
    --enable-demuxer=mjpeg \
    --enable-demuxer=mpegps \
    --enable-demuxer=mpegvideo \
    --enable-demuxer=avi \
    --enable-demuxer=mov \
    --enable-demuxer=mp3 \
    --enable-demuxer=aac \
    --enable-demuxer=pmp \
    --enable-demuxer=oma \
    --enable-demuxer=pcm_s16le \
    --enable-demuxer=pcm_s8 \
    --enable-demuxer=wav"

VIDEO_ENCODERS="\
    --enable-encoder=ffv1 \
    --enable-encoder=mjpeg \
    --enable-encoder=mpeg4 \
    --enable-encoder=h264"

AUDIO_ENCODERS="\
    --enable-encoder=pcm_s16le \
    --enable-encoder=mp3 \
    --enable-encoder=ac3 \
    --enable-encoder=aac"

MUXERS="\
    --enable-muxer=avi \
    --enable-muxer=h264 \
    --enable-muxer=mjpeg \
    --enable-muxer=mp4"

PARSERS="\
    --enable-parser=h264 \
    --enable-parser=mjpeg \
    --enable-parser=mpeg4video \
    --enable-parser=mpegvideo \
    --enable-parser=aac \
    --enable-parser=aac_latm \
    --enable-parser=mpegaudio"

PROTOCOLS="\
    --enable-protocol=file"

EXTRA="\
    --enable-indev=dshow"

./configure \
    --prefix=./linux/${ARCH} \
    ${GENERAL} \
    --cc="${CC:-gcc}" \
    --extra-cflags="-D__STDC_CONSTANT_MACROS -O3" \
    --enable-zlib \
    --enable-pic \
    --disable-x86asm \
    --disable-everything \
    --disable-debug \
    --disable-stripping \
    ${MODULES} \
    ${VIDEO_DECODERS} \
    ${AUDIO_DECODERS} \
    ${VIDEO_ENCODERS} \
    ${AUDIO_ENCODERS} \
    ${DEMUXERS} \
    ${MUXERS} \
    ${PARSERS} \
    ${PROTOCOLS} \
    ${EXTRA} \
    --arch=${ARCH}

make clean
make install
