# Approxilyzer

Approxilyzer is an open-source framework for instruction level approximation 
and resiliency software. Approxilyzer provides a systematic way to identify 
instructions that exhibit first-order approximation potential. It can also identify 
silent data corruption (SDC) causing instructions in the presence of single-bit errors. 
Approxilyzer employs static and dynamic analysis, in addition to heuristics, to reduce 
the run-time of finding Approximate instructions and SDC-causing instructions by 3-6x 
orders of magnitude.

Project overview can be viewed at: https://cs.illinois.edu/approxilyzer



## Approxilyzer Setup Instructions
1. all dependencies for gem5 are required (see gem5 documentation) This includes the following:

  * gcc 4.8 or greater
  * python 2.7 or greater
  * SCons
  * SWIG 2.0.4 or greater
  * protobuf 2.1 or greater
  * M4

   On Ubuntu, the following commands should cover all of the requirements:
   
```
sudo apt-get update
sudo apt-get install build-essential
sudo apt-get install scons
sudo apt-get install python-dev
sudo apt-get install swig
sudo apt-get install libprotobuf-dev python-protobuf protobuf-compiler libgoogle-perftools-dev
sudo apt-get install m4
```
2. To build from the source code run the following:
```
cd gem5
scons build/X86/gem5.fast -jX
scons build/X86/gem5.opt -jX
```

   Where **X** is the number of available CPU cores plus 1.  

## Downloading Disk Images
1. Download sample gem5 disk images [here](https://uofi.box.com/s/6h0ep96pbi5sexygmyobt778wyqfl3r6)
Create the following directory structure, or modify the paths in
gem5/configs/common/SysPaths.py: /dist/m5/system/disks
                            /dist/m5/system/binaries


## How to use Approxilyzer
1. In progress
