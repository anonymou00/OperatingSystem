CC=i686-elf-gcc
LD=i686-elf-ld
CFLAGS=-ffreestanding -O2 -m32 -nostdlib

OBJS = main.o logo.o keyboard.o

all: kernel.bin

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

kernel.bin: $(OBJS)
	$(LD) -Ttext 0x1000 -o kernel.bin $(OBJS) --oformat binary

clean:
	rm -f *.o kernel.bin
