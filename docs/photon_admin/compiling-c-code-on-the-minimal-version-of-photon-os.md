# Compiling C++ Code on the Minimal Version of Photon OS

As a minimalist Linux run-time environment, the minimal version of Photon OS lacks the packages that you need to compile the code for a C++ program. For example, without the requisite packages, trying to compile the file containing the following code with the `gcc` command will generate errors: 

    #include <stdio.h>
    int main()
    {
    return 0;
    }

The errors appear as follows: 

    gcc test.c
    -bash: gcc: command not found
    tdnf install gcc -y
    gcc test.c
    test.c:1:19: fatal error: stdio.h: No such file or directory
    compilation terminated.

To enable the minimal version of Photon OS to preprocess, compile, assemble, and link C++ code, you must install the following packages as root with tdnf:

* `gcc`
* `glibc-devel`
* `binutils`

To install the packages, use the following the `tdnf` command: 

    tdnf install gcc glibc-devel binutils