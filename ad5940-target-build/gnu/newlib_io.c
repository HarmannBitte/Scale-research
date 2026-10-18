/* NEW 2026-10-17: experimental ADuCM3029 GNU/newlib integration.
 * No semihosting. No receive protocol. Not hardware-qualified firmware.
 * This file does not relicense any ADI or third-party source.
 */
#include <errno.h>
#include <limits.h>
#include <string.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include "ADuCM3029.h"
#include "ad5940.h"

extern unsigned char __HeapBase[], __HeapLimit[];
static ptrdiff_t heap_used;

/* The selected vendor linker script reserves heap and stack in DSRAM_A. */
void *_sbrk(ptrdiff_t increment)
{
    ptrdiff_t capacity = (ptrdiff_t)((uintptr_t)__HeapLimit - (uintptr_t)__HeapBase);
    unsigned char *previous = __HeapBase + heap_used;
    if (increment > capacity - heap_used || increment < -heap_used) {
        errno = ENOMEM;
        return (void *)-1;
    }
    heap_used += increment;
    return previous;
}

/* Route newlib's actual write backend to the bounded vendor-port transmitter.
 * Merely overriding fputc is insufficient to retarget newlib fwrite/printf. */
int _write(int fd, const void *buffer, size_t length)
{
    const unsigned char *p = buffer;
    size_t i;
    if (fd != 1 && fd != 2) { errno = EBADF; return -1; }
    if (length > INT_MAX) { errno = EINVAL; return -1; }
    if (length && !buffer) { errno = EFAULT; return -1; }
    for (i = 0; i < length; ++i) {
        if (fputc(p[i], stdout) == EOF) { errno = EIO; return -1; }
    }
    return (int)length;
}
int _read(int fd, void *p, size_t n)
{ (void)fd; (void)p; (void)n; errno = ENOSYS; return -1; }
int _close(int fd) { (void)fd; errno = EBADF; return -1; }
int _isatty(int fd) { return fd == 1 || fd == 2; }
int _fstat(int fd, struct stat *st)
{
    if ((fd != 1 && fd != 2) || !st) { errno = EBADF; return -1; }
    memset(st, 0, sizeof(*st));
    st->st_mode = S_IFCHR;
    return 0;
}
int _lseek(int fd, int position, int whence)
{ (void)fd; (void)position; (void)whence; errno = ESPIPE; return -1; }
int _getpid(void) { return 1; }
int _kill(int pid, int signal)
{ (void)pid; (void)signal; errno = ENOSYS; return -1; }
void _exit(int status) __attribute__((noreturn));
void _exit(int status)
{
    (void)status;
    /* Best-effort latch clear; not proof of electrical shutdown. */
    AD5940_RstClr();
    __disable_irq();
    for (;;) { __WFI(); }
}
