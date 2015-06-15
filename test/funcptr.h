#ifndef __FUNCPTR_H
#define __FUNCPTR_H

typedef void (*callbackType)(int id);

int timer(int time, void (*callback)(int id, char c, int(*foo)(bla i)), int i);
//int timerCallbackType(int time, callbackType callback);
void timerPointer(int time, int **(*callback)(int** p));
void timerConstPointer(int time, int **(*callback)(const int** p));

#endif
