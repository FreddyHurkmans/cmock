# cMock

## Introduction
Mock generator for C, version 0.4. cMock reads function prototypes from a headerfile and will automatically generate an 'expected call' function and 'mock' function for each function prototype.

Example: say your headerfile contains:

```c
int foo(double a);
```

Then the following functions will be generated:

```c
void foo_ExpectedCall(double a, int ReturnValue)
int foo(double a)
```
Details about these functions will be explained later on.

### Requires
cMock requires Python and ctags to run, the generated code requires the [Unity testing framework](https://github.com/ThrowTheSwitch/Unity).

### Tested on
I tested cMock on Ubuntu 14.04 with Python 2.7.6 and ctags 5.9, however since -as far as I know- I didn't use any special Python stuff it should work just fine on other versions.

ctags is called with parameters -x, -u and --c-kinds=fp, so as long as your version has these options you're good to go.

### Limitations
This version supports the following stuff very well, meaning they should work as parameter and return type of any function you know:

- all standard c types
- your own types
- structs
- single pointers

Function pointers work well with the following limitations:

- you cannot have a function pointer as return type (yet)
- you cannot typedef your function pointer parameter (see the chapter about function pointers)

Double pointers and arrays are not yet supported.

## How it works: the basics
You simply call `./cmock.py myfuncs.h` on the commandline. cMock will then generate both `myfuncs_mock.c` and `myfuncs_mock.h` for you.

For each function prototype in your headerfile, it will generate a mock function and a function to indicate an expected call. Let's assume this is our headerfile `myfuncs.h`:

```c
#ifndef MYFUNCS_H
#define MYFUNCS_H

struct MyType
{
    int number1;
    int number2;
};

int foo(char c);
void bar(void);
void bas(struct MyType m);

#endif
```

Now, let's take a look at each part of the generated header file:

```c
/*********************************************************************
 * generated code, please do not edit directly
 * cMock version 0.4 written by Freddy Hurkmans
 *
 * source file    : myfuncs.h
 * filename       : myfuncs_mock.h
 * generation date: 14 Jun 2015 - 22:40:15
 *
 ********************************************************************/

#ifndef __MYFUNCS_MOCK_H
#define __MYFUNCS_MOCK_H

#include <stdbool.h>
#include <stdint.h>

#include "myfuncs.h"
```

The generated file starts with a header that indicates this is a generated file; it will also tell you the name of the source file and the generation date. Then we see the obvious multiple include protection and some includes that can be required *(note: the script doesn't check if they actually are required, it just includes them)*. It also includes your original headerfile, which will guarantee you that the generated mock functions are 100% compatible with your prototypes.

```c
#define MAX_NR_FUNCTION_CALLS 25
```
Next part creates a define: one that is used to declare a number of expected function calls *(this can easily be modified by adding the option* `-n#` *to the commandline)*.

```c
typedef struct
{
    /* parameters */
    char c[MAX_NR_FUNCTION_CALLS];
    /* return value */
    int ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} fooStruct;

typedef struct
{
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} barStruct;

typedef struct
{
    /* parameters */
    struct MyType m[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} basStruct;
```

As our mock code needs to remember expected calls, their parameters and return values, we need some place to put all this information. In order to do this in a structured way, a struct is created for each function in your headerfile. This struct is called: `<your_function>Struct`. In here you will find an array for each parameter, an array for your return value, a counter for how often the generated function is called and a counter for how often it is expected to be called. *Please note that parameters and return types are only generated if the function in question has them!* The details about these variables are not really important for you, I just mention them so you understand how the mock works.

```c
void myfuncs_MockSetup(void);    /* call this before every test! */
void myfuncs_MockTeardown(void); /* call this after every test! */
```

`myfuncs_MockSetup` and `myfuncs_MockTeardown` can be considered constructor and destructor of your generated mock module. `myfuncs_MockSetup` will initialise all structs to 0 so your tests do not depend on the previous one. I will explain what `myfuncs_MockTeardown` does in a minute, however I hope it is obvious that you need to call these functions before and after each test. Luckily this is easy to do in [Unity](https://github.com/ThrowTheSwitch/Unity): just call them from your custom `setUp` and `tearDown` functions.

```c
/* call these for each call you expect for a given function */
void foo_ExpectedCall(char c, int ReturnValue);
void bar_ExpectedCall(void);
void bas_ExpectedCall(struct MyType m);

#endif  /* __MYFUNCS_MOCK_H */
```
The last part of the generated header defines prototypes for the `ExpectedCall` functions. Let's assume we expect our function under test to call `foo` with parameter 12, in that case we need to inform our mock. We also tell our mock what it is to return, so let's say we want to test if our function responds correctly if `foo` returns -1:

```c
foo_ExpectedCall(12, -1);
```

`foo_ExpectedCall` will remember the given values and it will increase the `ExpectedNrCalls` counter. When our function under test calls `foo`, it will test if the expected input parameter is given and it will return the given return value. `foo` will also test if it is not called too often.

Testing if all expected functions are called the specified amount of times cannot be done until the test is completely done. This is where `myfuncs_MockTeardown` comes in: it will test exactly that.

## More advanced
The previous chapter explains the basics of the generated mock. Without going into all details, there's a bit more you might need to know before you start using this mock generator. The 'bit more' part is mostly about pointers.

Let's say you have a function with the following prototype:

```c
int foo(struct MyType* ptr);
```
In real life c code, `ptr` can be both input and output, which makes it a bit hard when you want to generate code that's always correct. The obvious way for you to tell the generator whether `ptr` is input or output is by using the `const` keyword, which unfortunately is not used often in c. If you want to use cMock, you will have to use it though.

For the generated headerfile, adding `const` or not does not change anything. In both cases the generated `struct` and `ExpectedCall` parts look like:

```c
typedef struct
{
    /* parameters */
    struct MyType ptr[MAX_NR_FUNCTION_CALLS];
    /* return value */
    int ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} fooStruct;

void foo_ExpectedCall(const struct MyType* ptr, int ReturnValue);
```
This lack of difference is easily explained: for both versions the mock needs to remember the given data. When you look in the generated code, you will easily spot the difference:

```c
// ptr as output parameter
int foo(struct MyType* ptr)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, fooData.ExpectedNrCalls, fooData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(fooData.CallCounter < fooData.ExpectedNrCalls, errormsg);

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, fooData.CallCounter+1);
    *ptr = fooData.ptr[fooData.CallCounter];
    return fooData.ReturnValue[fooData.CallCounter++];
}
```
In the case where `ptr` is used as output parameter, you will note that the value you passed into the `ExpectedCall` function is copied into `*ptr`.

```c
int foo(const struct MyType* ptr)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, fooData.ExpectedNrCalls, fooData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(fooData.CallCounter < fooData.ExpectedNrCalls, errormsg);

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, fooData.CallCounter+1);
    TEST_ASSERT_EQUAL_MEMORY_MESSAGE(&(fooData.ptr[fooData.CallCounter]), ptr, sizeof(*ptr), errormsg);
    return fooData.ReturnValue[fooData.CallCounter++];
}
```
In the case where `ptr` is used as input parameter, you will note the function will check if the given data is the same as the expected data.

### Arrays
As noted in the 'limitations' paragraph, cMock currently does not support arrays. Most important reason is that c doesn't make it easy to detect the intention of a certain parameter. Is `int* bar` a pointer to a single integer, or is it in fact a pointer to the first value of an array? You cannot tell. In a **later version** I might decide that an array **must** be declared as: `int bar[]`. I am interested to your opinion on this, so if you have an idea that might help here, please let me know.

### Strings
Strings in c are, as you know, char arrays. Arrays are not supported, strings however are a bit supported. If you have a function that has a `const char*` parameter, this is considered to be an input type string, as normally it doesn't make sense to use a pointer type to feed a character into a function. If your function has a `char*` parameter however, it can mean both an output character and an output string. As I have no way of knowing which it is, the script considers this to be an output type character.

So with the following prototypes:

```c
int foo(char* character);
int bar(const char* text);
```
cMock will generate:

```c
// no big difference here:
void foo_ExpectedCall(const char* character, int ReturnValue);
void bar_ExpectedCall(const char* text, int ReturnValue);

// the difference is in the generated functions (only the important line shown here):
void foo_ExpectedCall(const char* character, int ReturnValue)
{
    ...
    fooData.character[fooData.ExpectedNrCalls] = *character;
    ...
}
int foo(char* character)
{
    ...
    *character = fooData.character[fooData.CallCounter];
    ...
}

void bar_ExpectedCall(const char* text, int ReturnValue)
{
    size_t length = 0;
    ...
    length = strlen(text);
    barData.text[barData.ExpectedNrCalls] = malloc(length+1);
    TEST_ASSERT_NOT_NULL_MESSAGE(barData.text[barData.ExpectedNrCalls], "could not allocate memory");
    strcpy(barData.text[barData.ExpectedNrCalls], text);
    ...
}
int bar(const char* text)
{
    ...
    TEST_ASSERT_EQUAL_STRING_MESSAGE(barData.text[barData.CallCounter], text, errormsg);
    free(barData.text[barData.CallCounter]);
    ...
}
```

### Function pointers
As from version 0.4 function pointers are supported. However, in `C` you basically have 2 ways of implementing a function that takes a function pointer as a parameter:

```c
int timer(int time, void (*callback)(int id));
```

and:

```c
typedef void (*callbackType)(int id);
int timer(int time, callbackType callback);
```

As cMock doesn't really parse `C` files, but rather uses ctags to extract prototypes, it cannot see what callbackType is. At this time, only the first option (without the typedef) is supported. If you however depend on the second version, I suggest running your header through any `C` preprocessor before feeding it to cMock. I have not yet tested this, I will do this in a later version.

Back to the first option. The generated `ExpectedCall` function looks like:

```c
void timer_ExpectedCall(int time, void (*callback)(int id), int ReturnValue); /* if you don't want to check function pointer(s), make it NULL */
```

The comment at the end of the line hints to 2 different ways of using your mock. As you might expect from what you've seen so far, the first way is like this:

```c
timer_ExpectedCall(10, my_callback_function);
```

This will tell the mock to expect 1 call to `timer()` with parameters `10` and `my_callback_function`. However, quite often you will find that callback functions given to functions are static functions, thus unavailable in your test file. In this case you can simply call the `ExpectedCall` with a `NULL` parameter:

```c
timer_ExpectedCall(10, NULL);
```

This will tell the mock timer function not to test the callback parameter.

## That be it :)
I wish you lots of coding fun, where the tedious old making of stub code is finally part of the past.

If you have great ideas for improvement, please send me a combination of function prototype and the suggested code that should be generated. If your idea matches the general concept of cMock I will try to change the generator.
