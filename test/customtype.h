#ifndef __CUSTOMTYPE_H
#define __CUSTOMTYPE_H

#include <stdint.h>

// no typedef
struct FOO
{
    int n;
    int m;
};

// with typedef
typedef struct
{
    int n;
    double m;
} BAR;

typedef int myInt;

struct FOO foo(struct foo f, struct foo *p1, const struct foo* p2);
BAR* bar(BAR* p1, const BAR *p2);
myInt bas(myInt i, myInt* p);

#endif
