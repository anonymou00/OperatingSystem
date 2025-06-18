#include <stdint.h>
#include "logo.h"
#include "keyboard.h"

#define VGA_WIDTH 320
#define VGA_HEIGHT 200
#define VGA_MEMORY (uint8_t*)0xA0000

void set_video_mode() {
    asm volatile (
        "mov $0x13, %%ax\n"
        "int $0x10\n"
        : : : "ax"
    );
}

void draw_logo() {
    uint8_t* video_memory = VGA_MEMORY;
    for (int i = 0; i < VGA_WIDTH * VGA_HEIGHT; i++) {
        video_memory[i] = logo_data[i];
    }
}

void main() {
    set_video_mode();
    draw_logo();

    // VGA moddan çıkmak için bir tuşa basılmasını bekle
    for (volatile int i = 0; i < 10000000; i++);

    // Text moda geç
    asm volatile (
        "mov $0x03, %%ax\n"
        "int $0x10\n"
        : : : "ax"
    );

    // Keyboard simülasyonu başlasın
    while (1) {
        handle_keypress();
    }
}
