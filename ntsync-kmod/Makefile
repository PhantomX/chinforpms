NTSYNC_MINOR := 243

KERNELRELEASE ?= $(shell uname -r)
KDIR ?= /lib/modules/$(KERNELRELEASE)/build
PWD ?= $(shell pwd)

obj-m := ntsync.o
ccflags-y := -I$(src)/include -DNTSYNC_MINOR="$(NTSYNC_MINOR)" -Werror

default: modules
install: modules_install

modules modules_install clean:
	$(MAKE) -C $(KDIR) M=$(PWD) $@
