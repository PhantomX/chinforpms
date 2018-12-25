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

#include <linux/fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define errExit(msg)    do { perror(msg); exit(EXIT_FAILURE); \
} while (0)

int main(int argc, char *argv[])
{
	int fd;
	unsigned int seals;

	if (argc != 2) {
		fprintf(stderr, "%s /proc/PID/fd/FD\n", argv[0]);
		exit(EXIT_FAILURE);
	}

	fd = open(argv[1], O_RDWR);
	if (fd == -1)
		errExit("open");

	seals = fcntl(fd, F_GET_SEALS);
	if (seals == -1)
		errExit("fcntl");

	printf("Existing seals:");
	if (seals & F_SEAL_SEAL)
		printf(" SEAL");
	if (seals & F_SEAL_GROW)
		printf(" GROW");
	if (seals & F_SEAL_WRITE)
		printf(" WRITE");
	if (seals & F_SEAL_SHRINK)
		printf(" SHRINK");
	printf("\n");

	/* Code to map the file and access the contents of the
	   resulting mapping omitted */

	exit(EXIT_SUCCESS);
}

