WINESYNC_MINOR := 243

KERNELRELEASE ?= $(shell uname -r)
KDIR ?= /lib/modules/$(KERNELRELEASE)/build
PWD ?= $(shell pwd)

obj-m := winesync.o
ccflags-y := -include $(src)/defines.h -I$(src)/include -DWINESYNC_MINOR="$(WINESYNC_MINOR)" -Werror

default: modules
install: modules_install

modules modules_install clean:
	$(MAKE) -C $(KDIR) M=$(PWD) $@
