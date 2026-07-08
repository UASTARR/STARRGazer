# testing the parser without needing actual hardware
# run generate_test_data.py first
 
import sys
import os
 
sys.path.insert(0, os.path.dirname(__file__))
 
from backend import SerialBackend
 
backend = SerialBackend(port=None)
 
def run_file(filepath, max_print=5):
    print(f"\ntesting: {filepath}")
    print("=" * 40)
 
    if not os.path.exists(filepath):
        print("file not found, run generate_test_data.py first")
        return
 
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
 
    print(f"{len(lines)} packets found")
 
    ok = 0
    errors = 0
 
    for i, hex_line in enumerate(lines):
        packet = bytes.fromhex(hex_line)
 
        if len(packet) != 128:
            print(f"packet {i+1} wrong size")
            errors += 1
            continue
 
        result = backend._parse_packet(packet)
 
        if i < max_print:
            print(f"packet {i+1}: {result}")
        elif i == max_print:
            print(f"... only showing first {max_print}")
 
        ok += 1
 
    print(f"\n{ok} worked, {errors} didnt")
 
 
run_file("records/test_single.txt", max_print=10)
run_file("records/test_flight.txt", max_print=5)
run_file("records/test_bad.txt", max_print=10)
 
print("\nif test_single has 10 dicts and test_bad printed warnings without crashing its working")