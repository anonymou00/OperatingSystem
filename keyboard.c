#include "keyboard.h"
#include <stdint.h>

// Port I/O işlemleri
static inline uint8_t inb(uint16_t port) {
    uint8_t result;
    asm volatile ("inb %1, %0" : "=a"(result) : "Nd"(port));
    return result;
}

// Ekrana yazmak için VGA belleği
uint16_t* vga_buffer = (uint16_t*)0xB8000;
int cursor_pos = 0;

// ASCII tablosu (sadece harfler ve rakamlar için örnek)
const char ascii_table[128] = {
    0,  27, '1','2','3','4','5','6','7','8','9','0','-','=','\b', // 0x0
    '\t','q','w','e','r','t','y','u','i','o','p','[',']','\n',   // 0x10
    0,'a','s','d','f','g','h','j','k','l',';','\'','`',          // 0x20
    0,'\\','z','x','c','v','b','n','m',',','.','/',0,            // 0x30
    '*',0,' ',                                                  // 0x39
};

void handle_keypress() {
    uint8_t scancode = inb(0x60);
    char ch = ascii_table[scancode];

    if (ch && cursor_pos < 80 * 25) {
        vga_buffer[cursor_pos++] = (0x0F << 8) | ch;  // Beyaz karakter
    }
}

void init_keyboard() {
    // Şimdilik gerçek interrupt yok, sadece örnek kullanım
}
