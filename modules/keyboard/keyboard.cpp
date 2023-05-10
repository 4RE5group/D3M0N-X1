extern "C" {
#include <keyboard.h>

// Here we implement the function using C++ code, but since it's
// declaration has to be compatible with C everything goes in extern "C" scope.
int cppfunc() {
    return 69;
}
}