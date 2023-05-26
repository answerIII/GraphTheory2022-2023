#!/usr/bin/env python3

import os

for name in os.listdir("testsrc"):
    lines = []

    with open(f"testsrc/{name}") as file:
        lines = [line.rstrip() for line in file]

    with open(f"test/{name}", "w") as file:
        for line in lines:
            file.write(f"{line} 1 1\n")
