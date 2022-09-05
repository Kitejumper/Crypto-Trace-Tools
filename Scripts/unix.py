import time

rawtime = str(raw_input("Whats the value from the hex?"))

flip = rawtime[::-1]

u_time = int(flip, 16)

final = time.ctime(int(u_time))

print final