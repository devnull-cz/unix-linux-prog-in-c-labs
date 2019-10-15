
Makefiles:
  - let's assume GNU make for now

  0) implement a program and dynamic library
     - start without makefiles
     - the dynamic library will be called libmin.so
       - it will implement one function:

         int min(int a[], ssize_t len); // return minimum value

       - the library source will be comprised of 2 files:
 	 - libmin.h
         - libmin.c // will include libmin.h

     - the program will be in main.c, compiled into 'main' binary
       and will be linked against the libmin.so
       - main.c will create array of the size of program arguments,
         fill it with the numbers, call min() and print the result to stdout
       - use file(1), nm, ldd, readelf to inspect libmin.o, libmin.so, main.o,
	 main
       - run the program with various LD_DEBUG values to see dynamic linker
         processing (e.g. 'libs', 'symbols')

  1) construct set of Makefiles
     - basic targets: all, clean
     - use automatic gmake variables (preceded with the '@' char)
     - use wildcard rule for *.c => *.o files
     - header files => C files dependencies
     - use phony targets (clean) if using GNU make

    Q: - what if -shared is used for building .o files as well ?
       - what if -fpic is used for building .so files ?

  2) implement

        int max(int a[], ssize_t len); // return maximum value

     similarly to libmin, i.e. libmax.[ch], libmax.so, ...

     - and link main with both libraries
       - 1st argument will be now "min" or "max" and based on that
         given function (and therefore library will be used)

     - use hierarchical build:
       Makefile
       main.c
       libmin/
         Makefile
	 libmin.c
       libmax/
         Makefile
	 libmax.c

     - hint: subdirs + shell snippet that will run 'make' (or better $(MAKE))
             inside these directories
	     - or use 'make -C' with target specification of multiple elements

     [bonus]: use Makefile includes to minimize sharing/copying
              (hint: use top-level makefile and include it in subdirs)

  3) [optional] build with various compilers in CI environment
     - use Travis / Github Actions

  4) [optional] write simple test script
     - run it in the CI environment above

------------------------------------------------------------------------------

histogram:
  - command line arguments are positive integers
    - exit on non-number argument
    - if less arguments than default number of columns (75), use some heuristics
      for the number of columns (e.g. argc/2)
  - draw a histogram of the input integers
    - determine minimum/maximum of values
    - determine range for buckets
    - assign the values to buckets
  - optional: log scale (see math.h and log(3))

- sample output:

$ for i in `seq 100`; do args="$args $RANDOM"; done
$ ./a.out $args
min = 6, max = 32574
buckets = 75, diff = 32568, range = 434.239990
boundary[0]: 6.000000, 440.239990
boundary[1]: 440.239990, 874.479980
boundary[2]: 874.479980, 1308.719971
boundary[3]: 1308.719971, 1742.959961
boundary[4]: 1742.959961, 2177.199951
boundary[5]: 2177.199951, 2611.439941
boundary[6]: 2611.439941, 3045.679932
boundary[7]: 3045.679932, 3479.919922
boundary[8]: 3479.919922, 3914.159912
boundary[9]: 3914.159912, 4348.399902
boundary[10]: 4348.399902, 4782.639648
boundary[11]: 4782.639648, 5216.879883
boundary[12]: 5216.879883, 5651.120117
boundary[13]: 5651.120117, 6085.360352
boundary[14]: 6085.360352, 6519.600586
boundary[15]: 6519.600586, 6953.840820
boundary[16]: 6953.840820, 7388.081055
boundary[17]: 7388.081055, 7822.321289
boundary[18]: 7822.321289, 8256.561523
boundary[19]: 8256.561523, 8690.801758
boundary[20]: 8690.801758, 9125.041992
boundary[21]: 9125.041992, 9559.282227
boundary[22]: 9559.282227, 9993.522461
boundary[23]: 9993.522461, 10427.762695
boundary[24]: 10427.762695, 10862.002930
boundary[25]: 10862.002930, 11296.243164
boundary[26]: 11296.243164, 11730.483398
boundary[27]: 11730.483398, 12164.723633
boundary[28]: 12164.723633, 12598.963867
boundary[29]: 12598.963867, 13033.204102
boundary[30]: 13033.204102, 13467.444336
boundary[31]: 13467.444336, 13901.684570
boundary[32]: 13901.684570, 14335.924805
boundary[33]: 14335.924805, 14770.165039
boundary[34]: 14770.165039, 15204.405273
boundary[35]: 15204.405273, 15638.645508
boundary[36]: 15638.645508, 16072.885742
boundary[37]: 16072.885742, 16507.125000
boundary[38]: 16507.125000, 16941.365234
boundary[39]: 16941.365234, 17375.605469
boundary[40]: 17375.605469, 17809.845703
boundary[41]: 17809.845703, 18244.085938
boundary[42]: 18244.085938, 18678.326172
boundary[43]: 18678.326172, 19112.566406
boundary[44]: 19112.566406, 19546.806641
boundary[45]: 19546.806641, 19981.046875
boundary[46]: 19981.046875, 20415.287109
boundary[47]: 20415.287109, 20849.527344
boundary[48]: 20849.527344, 21283.767578
boundary[49]: 21283.767578, 21718.007812
boundary[50]: 21718.007812, 22152.248047
boundary[51]: 22152.248047, 22586.488281
boundary[52]: 22586.488281, 23020.728516
boundary[53]: 23020.728516, 23454.968750
boundary[54]: 23454.968750, 23889.208984
boundary[55]: 23889.208984, 24323.449219
boundary[56]: 24323.449219, 24757.689453
boundary[57]: 24757.689453, 25191.929688
boundary[58]: 25191.929688, 25626.169922
boundary[59]: 25626.169922, 26060.410156
boundary[60]: 26060.410156, 26494.650391
boundary[61]: 26494.650391, 26928.890625
boundary[62]: 26928.890625, 27363.130859
boundary[63]: 27363.130859, 27797.371094
boundary[64]: 27797.371094, 28231.611328
boundary[65]: 28231.611328, 28665.851562
boundary[66]: 28665.851562, 29100.091797
boundary[67]: 29100.091797, 29534.332031
boundary[68]: 29534.332031, 29968.572266
boundary[69]: 29968.572266, 30402.812500
boundary[70]: 30402.812500, 30837.052734
boundary[71]: 30837.052734, 31271.292969
boundary[72]: 31271.292969, 31705.533203
boundary[73]: 31705.533203, 32139.773438
boundary[74]: 32139.773438, 32574.013672
histogram: 15 3 8 5 8 1 6 9 8 6 10 9 12 9 11 11 8 3 10 1 11 9 7 12 6 10 6 7 6 9 11 6 8 10 4 10 8 10 13 7 3 8 6 10 14 10 8 11 8 7 10 11 7 3 7 9 7 4 13 4 12 5 9 2 6 6 6 7 6 14 7 8 14 6 9
histogram max = 15
#
#                                           #                        #  #
#                                     #     #             #          #  #
#           #          #              #     #             # #        #  #
#           # ##    #  #      #       #     #  #   #      # #        #  #
#         # # ##  # #  # #    #  # # ##    ### #  ##      # #        #  #
#      #  ######  # ## # #   ##  # # ##    ### #  ##   #  # # #      #  # #
# # #  ## ####### # ## # #   ## ## ####  # ###### ##   #  # # #      # ## #
# # #  ## ####### # #### # # ## ## ##### # ########## ### # # #    # #### #
# # # ########### # ############## ##### ############ ### # # # ###########
# ### ########### # ############## ##### ############ ### # ### ###########
# ### ########### # #################### ############ ######### ###########
##### ############# ########################################### ###########
##### ############# #######################################################
###########################################################################
