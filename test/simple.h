#ifndef __SIMPLE_H
#define __SIMPLE_H

#include <stdint.h>

// the keyword extern should not make a difference!
extern double pi(void);
int foo(int nr);
int bar(void);
uint_16_t bas(uint8_t v1, int16_t v2, int32_t* p1);
int constPtrs(const int* p1, const int *p2, int const* p3, int const *p4);

#endif
