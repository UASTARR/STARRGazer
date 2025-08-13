import time

def main():
    time_pass = 0
    while True:
        time.sleep(1)
        with open("/home/uastarr/Desktop/STARRGazer/stream.txt", "w", encoding="utf-8") as f:
            f.write(f"{time_pass}")
        
        time_pass += 1
if __name__ == "__main__":
    main()