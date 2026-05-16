# datatypes.py
# lookup table for all the sensors on the rocket
# each sensor has an address that gets stamped on every packet so we know who sent what
# update the addresses once firmware confirms them, everything else should still work
 
# value_type options:
# "uint32"  = 4 byte unsigned int
# "uint16"  = 2 byte unsigned int  
# "float32" = 4 byte float
 
SENSORS = {
    0x0001: {
        "name": "temperature",
        "fields": ["temperature"],
        "value_type": "uint32",
    },
    0x0002: {
        "name": "pressure",
        "fields": ["pressure"],
        "value_type": "uint32",
    },
    0x0003: {
        "name": "altitude",
        "fields": ["altitude"],
        "value_type": "uint32",
    },
    0x0004: {
        "name": "acceleration",
        "fields": ["accelerationx", "accelerationy", "accelerationz"],
        "value_type": "uint32",
    },
    0x0005: {
        "name": "gyroscope",
        "fields": ["gyroscopex", "gyroscopey", "gyroscopez"],
        "value_type": "uint32",
    },
    0x0006: {
        "name": "magnetometer",
        "fields": ["magnetometerx", "magnetometery", "magnetometerz"],
        "value_type": "uint32",
    },
    0x0007: {
        "name": "quaternion",
        "fields": ["quaternionw", "quaternionx", "quaterniony", "quaternionz"],
        "value_type": "uint32",
    },
    0x0008: {
        "name": "gps",
        "fields": ["lat", "lon", "alt"],
        "value_type": "uint32",
    },
    0x0009: {
        "name": "ground_speed",
        "fields": ["ground_speed"],
        "value_type": "uint32",
    },
    0x000A: {
        "name": "strain",
        "fields": ["strain"],
        "value_type": "uint32",
    },
}