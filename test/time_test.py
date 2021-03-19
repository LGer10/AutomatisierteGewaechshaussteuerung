import time

running = True
timeout_start = time.time()
time_to_shine = 2

while time.time() < timeout_start + time_to_shine:
    print("test")