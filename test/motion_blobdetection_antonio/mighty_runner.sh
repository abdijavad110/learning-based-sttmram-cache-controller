#! /bin/bash
for ((a = 0; a < 100; a++)); do
  printf "\n>>>>>>>>>> iteration no. %d" $a
  python JH_runner.py
done
