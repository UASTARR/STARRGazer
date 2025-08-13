# Ground-Station

## Joystick Button functions (physical labels)
- Button 2 (Thumb) - exits program
- Button 8 - Toggles between joystick input and model control input

## Physical Steps
1. Connect all pins with 2 motor drivers
2. Turn on camera and change to video mode
3. Connect camera to Jetson with usb
4. Connect joystick
5. Mount camera on
6. Plug in motor driver power supply
7. Enable e-stop

## Terminal 1
8. `sh camera_init.sh`

## Terminal 2
9. `source ~/yolo_defualt/bin/activate`
10. `python main.py`