if you tried a bit advanced approach to linking, i.e. use ld(1) instead of the cc wrapper with GCC on Linux, you have probably encountered a problem or two. Normally you do not need to do such thing and can happily stick with using cc to link however if you are interested in what happens under the hood then read on.

How to get there (link with ld instead of via cc) in the first place ? Start with tracing what the cc is doing when calling the link editor (-v would work equally well):

```
$ cc -### -o main main.o  -L ./ -lstat -Xlinker -rpath=/home/vkotal/MFF/Unix/Labs/unix-linux-prog-cvika.private/intro/libstat
Using built-in specs.
COLLECT_GCC=cc
COLLECT_LTO_WRAPPER=/usr/lib/gcc/x86_64-linux-gnu/7/lto-wrapper
OFFLOAD_TARGET_NAMES=nvptx-none
OFFLOAD_TARGET_DEFAULT=1
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Ubuntu 7.4.0-1ubuntu1~18.04.1' --with-bugurl=file:///usr/share/doc/gcc-7/README.Bugs --enable-languages=c,ada,c++,go,brig,d,fortran,objc,obj-c++ --prefix=/usr --with-gcc-major-version-only --program-suffix=-7 --program-prefix=x86_64-linux-gnu- --enable-shared --enable-linker-build-id --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --libdir=/usr/lib --enable-nls --with-sysroot=/ --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --with-default-libstdcxx-abi=new --enable-gnu-unique-object --disable-vtable-verify --enable-libmpx --enable-plugin --enable-default-pie --with-system-zlib --with-target-system-zlib --enable-objc-gc=auto --enable-multiarch --disable-werror --with-arch-32=i686 --with-abi=m64 --with-multilib-list=m32,m64,mx32 --enable-multilib --with-tune=generic --enable-offload-targets=nvptx-none --without-cuda-driver --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu
Thread model: posix
gcc version 7.4.0 (Ubuntu 7.4.0-1ubuntu1~18.04.1)
COMPILER_PATH=/usr/lib/gcc/x86_64-linux-gnu/7/:/usr/lib/gcc/x86_64-linux-gnu/7/:/usr/lib/gcc/x86_64-linux-gnu/:/usr/lib/gcc/x86_64-linux-gnu/7/:/usr/lib/gcc/x86_64-linux-gnu/
LIBRARY_PATH=/usr/lib/gcc/x86_64-linux-gnu/7/:/usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/:/usr/lib/gcc/x86_64-linux-gnu/7/../../../../lib/:/lib/x86_64-linux-gnu/:/lib/../lib/:/usr/lib/x86_64-linux-gnu/:/usr/lib/../lib/:/usr/lib/gcc/x86_64-linux-gnu/7/../../../:/lib/:/usr/lib/
COLLECT_GCC_OPTIONS='-o' 'main' '-L./' '-mtune=generic' '-march=x86-64'
 /usr/lib/gcc/x86_64-linux-gnu/7/collect2 -plugin /usr/lib/gcc/x86_64-linux-gnu/7/liblto_plugin.so "-plugin-opt=/usr/lib/gcc/x86_64-linux-gnu/7/lto-wrapper" "-plugin-opt=-fresolution=/tmp/ccV40P9D.res" "-plugin-opt=-pass-through=-lgcc" "-plugin-opt=-pass-through=-lgcc_s" "-plugin-opt=-pass-through=-lc" "-plugin-opt=-pass-through=-lgcc" "-plugin-opt=-pass-through=-lgcc_s" "--sysroot=/" --build-id --eh-frame-hdr -m elf_x86_64 "--hash-style=gnu" --as-needed -dynamic-linker /lib64/ld-linux-x86-64.so.2 -pie -z now -z relro -o main /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/Scrt1.o /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/crti.o /usr/lib/gcc/x86_64-linux-gnu/7/crtbeginS.o -L./ -L/usr/lib/gcc/x86_64-linux-gnu/7 -L/usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu -L/usr/lib/gcc/x86_64-linux-gnu/7/../../../../lib -L/lib/x86_64-linux-gnu -L/lib/../lib -L/usr/lib/x86_64-linux-gnu -L/usr/lib/../lib -L/usr/lib/gcc/x86_64-linux-gnu/7/../../.. main.o -lstat "-rpath=/home/vkotal/MFF/Unix/Labs/unix-linux-prog-cvika.private/intro/libstat" -lgcc --push-state --as-needed -lgcc_s --pop-state -lc -lgcc --push-state --as-needed -lgcc_s --pop-state /usr/lib/gcc/x86_64-linux-gnu/7/crtendS.o /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/crtn.o
COLLECT_GCC_OPTIONS='-o' 'main' '-L./' '-mtune=generic' '-march=x86-64'
```
Now let's try to link the program with selected options:
```
$ ld -o main main.o -lc /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/crtn.o -L ./ -lstat -rpath=/home/vkotal/MFF/Unix/Labs/unix-linux-prog-cvika.private/intro/libstat
ld: warning: cannot find entry symbol _start; defaulting to 00000000004004f0
```
Evidently, the binary needs a definition of _start symbol. On this system the main entry point of the program (i.e. first thing that is called when dynamic linker is done loading the program and its dependencies into memory) is the _start symbol which is included in C runtime object files. If you try to use any other symbol (e.g. with the -e linker option), it will fail in this setup.

So let's add some of the C runtime object files:
```
$ ld -o main /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/Scrt1.o /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/crti.o main.o -lc /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/crtn.o -L ./ -lstat -rpath=/home/vkotal/MFF/Unix/Labs/unix-linux-prog-cvika.private/intro/libstat
```
The crt1.o, crti.o and crtn.o files(supplied by the compiler) are important as they provide glue for running and exiting the program. Especially the crt1 (C runtime) prepares the arguments to main(). crti runs the .init code, crtn runs the .fini code.

These files are described nicely on https://wiki.osdev.org/Creating_a_C_Library

You will then run into like this:
```
$ ./main
bash: ./main: No such file or directory
```
Now, the 'main' file is present (otherwise the shell would not be able to execute it) so what is going on ? Let's see the system calls:
```
$ strace ./main
execve("./main", ["./main"], 0x7ffcf5d10140 /* 74 vars */) = -1 ENOENT (No such file or directory)
fstat(2, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 10), ...}) = 0
write(2, "strace: exec: No such file or di"..., 40strace: exec: No such file or directory
) = 40
getpid()                                = 31486
exit_group(1)                           = ?
+++ exited with 1 +++
```
surely, something failed when handling the exec syscall within kernel. Most probably related to the contents of the file itself. What could be wrong ? The basic ELF data look good:
```
$ ldd ./main
linux-vdso.so.1 (0x00007fff04ba9000)
libstat.so => /home/vkotal/MFF/Unix/Labs/unix-linux-prog-cvika.private/intro/libstat/libstat.so (0x00007fee25ba7000)
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fee257b6000)
/lib/ld64.so.1 => /lib64/ld-linux-x86-64.so.2 (0x00007fee25da9000)
```
```
$ readelf -d ./main

Dynamic section at offset 0xe48 contains 22 entries:
  Tag        Type                         Name/Value
 0x0000000000000001 (NEEDED)             Shared library: [libstat.so]
 0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]
 0x000000000000001d (RUNPATH)            Library runpath: [/home/vkotal/MFF/Unix/Labs/unix-linux-prog-cvika.private/intro/libstat]
 0x000000000000000c (INIT)               0x4005c0
 0x0000000000000004 (HASH)               0x400230
 0x000000006ffffef5 (GNU_HASH)           0x400270
 0x0000000000000005 (STRTAB)             0x4003a8
 0x0000000000000006 (SYMTAB)             0x4002a0
 0x000000000000000a (STRSZ)              201 (bytes)
 0x000000000000000b (SYMENT)             24 (bytes)
 0x0000000000000015 (DEBUG)              0x0
 0x0000000000000003 (PLTGOT)             0x601000
 0x0000000000000002 (PLTRELSZ)           144 (bytes)
 0x0000000000000014 (PLTREL)             RELA
 0x0000000000000017 (JMPREL)             0x4004d0
 0x0000000000000007 (RELA)               0x4004b8
 0x0000000000000008 (RELASZ)             24 (bytes)
 0x0000000000000009 (RELAENT)            24 (bytes)
 0x000000006ffffffe (VERNEED)            0x400488
 0x000000006fffffff (VERNEEDNUM)         1
 0x000000006ffffff0 (VERSYM)             0x400472
 0x0000000000000000 (NULL)               0x0
```
Well, it turns out the interpreter (i.e. the dynamic linker) embedded in the binary has bad path:
```
$ readelf -l ./main

Elf file type is EXEC (Executable file)
Entry point 0x400630
There are 8 program headers, starting at offset 64

Program Headers:
  Type           Offset             VirtAddr           PhysAddr
                 FileSiz            MemSiz              Flags  Align
  PHDR           0x0000000000000040 0x0000000000400040 0x0000000000400040
                 0x00000000000001c0 0x00000000000001c0  R      0x8
  INTERP         0x0000000000000200 0x0000000000400200 0x0000000000400200
                 0x000000000000000f 0x000000000000000f  R      0x1
      [Requesting program interpreter: /lib/ld64.so.1]
  LOAD           0x0000000000000000 0x0000000000400000 0x0000000000400000
                 0x0000000000000934 0x0000000000000934  R E    0x200000
  LOAD           0x0000000000000e30 0x0000000000600e30 0x0000000000600e30
                 0x0000000000000214 0x0000000000000214  RW     0x200000
  DYNAMIC        0x0000000000000e30 0x0000000000600e30 0x0000000000600e30
                 0x00000000000001c0 0x00000000000001c0  RW     0x8
  NOTE           0x0000000000000210 0x0000000000400210 0x0000000000400210
                 0x0000000000000020 0x0000000000000020  R      0x4
  GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000000 0x0000000000000000  RW     0x10
  GNU_RELRO      0x0000000000000e30 0x0000000000600e30 0x0000000000600e30
                 0x00000000000001d0 0x00000000000001d0  R      0x1
...
```

because /lib/ld64.so.1 does not exist on the file system (hence the 'no such file or directory' error message). This is bad because when kernel is handling that execve() syscall, it runs the dynamic linker first which then hands the control over to main(). So, let's copy one more argument from how cc runs ld to tell where the dynamic linker is (here the binary is 64-bit so 64-bit dynamic linker is used):
```
$ ld -o main -dynamic-linker /lib64/ld-linux-x86-64.so.2 /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/Scrt1.o /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/crti.o main.o -lc /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/crtn.o -L ./ -lstat -rpath=/home/vkotal/MFF/Unix/Labs/unix-linux-prog-cvika.private/intro/libstat
```
and then all is well:
```
$ ./main
main: usage: ./main num1 num2..
```
Note that with other link editor implementations the behavior will differ and the linker might as well supply the C runtime objects for you. Also note that while normally it does not matter much which linker implementation you use however there might be some cases when it is important (like linking huge executables).
