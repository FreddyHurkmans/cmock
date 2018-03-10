#ifndef MORE_ADVANCED_H
#define MORE_ADVANCED_H

struct MyType
{
    int number1;
    int number2;
};

int foo(struct MyType* ptr);
int foo(const struct MyType* ptr);

#endif
