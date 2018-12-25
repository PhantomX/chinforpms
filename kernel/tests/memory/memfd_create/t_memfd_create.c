/*
 * Copyright (c) 2016 Red Hat, Inc.
 *
 * This program is free software: you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation, either version 2 of
 * the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be
 * useful, but WITHOUT ANY WARRANTY; without even the implied
 * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
 * PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see http://www.gnu.org/licenses/.
 *
 */

#include <linux/memfd.h>
#include <linux/fcntl.h>
#include <sys/syscall.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>

#define errExit(msg)    do { perror(msg); exit(EXIT_FAILURE); \
} while (0)

int main(int argc, char *argv[])
{
	int fd;
	unsigned int seals;
	char *addr;
	char *name, *seals_arg;
	ssize_t len;
	char* message = "this is a test message for memfd\n";

	if (argc < 3) {
		fprintf(stderr, "%s name size [seals]\n", argv[0]);
		fprintf(stderr, "\t'seals' can contain any of the "
				"following characters:\n");
		fprintf(stderr, "\t\tg - F_SEAL_GROW\n");
		fprintf(stderr, "\t\ts - F_SEAL_SHRINK\n");
		fprintf(stderr, "\t\tw - F_SEAL_WRITE\n");
		fprintf(stderr, "\t\tS - F_SEAL_SEAL\n");
		exit(EXIT_FAILURE);
	}

	name = argv[1];
	len = atoi(argv[2]);
	seals_arg = argv[3];

	/* Create an anonymous file in tmpfs; allow seals to be
	   placed on the file */

	fd = syscall(SYS_memfd_create, name, MFD_ALLOW_SEALING);
	if (fd == -1)
		errExit("memfd_create");

	/* Size the file as specified on the command line */

	if (ftruncate(fd, len) == -1)
		errExit("truncate");

	if (write(fd, message, strlen(message)) <= 0)
		errExit("write");

	//printf("PID: %ld; fd: %d; /proc/%ld/fd/%d\n",
	//        (long) getpid(), fd, (long) getpid(), fd);
	printf("/proc/%ld/fd/%d\n", (long) getpid(), fd);

	/* Code to map the file and populate the mapping with data
	   omitted */

	/* If a 'seals' command-line argument was supplied, set some
	   seals on the file */

	if (seals_arg != NULL) {
		seals = 0;

		if (strchr(seals_arg, 'g') != NULL)
			seals |= F_SEAL_GROW;
		if (strchr(seals_arg, 's') != NULL)
			seals |= F_SEAL_SHRINK;
		if (strchr(seals_arg, 'w') != NULL)
			seals |= F_SEAL_WRITE;
		if (strchr(seals_arg, 'S') != NULL)
			seals |= F_SEAL_SEAL;

		if (fcntl(fd, F_ADD_SEALS, seals) == -1)
			errExit("fcntl");
	}

	/* Keep running, so that the file created by memfd_create()
	   continues to exist */

	pause();

	exit(EXIT_SUCCESS);
}

