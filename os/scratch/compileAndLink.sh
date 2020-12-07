#!/bin/bash
if [ -z $1 ] 
then 
    echo "INVALID PARAMETER ERROR"
    exit 1
fi

echo "Compile and Link $1 in x32..."

nasm -f elf32 $1 -o out.o
ld -m elf_i386 out.o -o out

echo "finished..."
