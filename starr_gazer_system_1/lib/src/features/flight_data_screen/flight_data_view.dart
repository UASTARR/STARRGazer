import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'speedometer.dart';
import 'status_bar.dart';

// TODO: Change ports
const List<String> _ports = [
  'COM1',
  'COM2',
  'COM3',
  'COM4',
  'COM5',
  'COM6',
  'COM7',
  'COM8',
  'COM9',
  'COM10',
];

const List<String> _baudRates = [
  '9600',
  '19200',
  '38400',
  '57600',
  '115200',
];

class FlightDataView extends StatefulWidget {
  const FlightDataView({super.key});

  @override
  State<FlightDataView> createState() => _FlightDataViewState();
}

typedef MenuEntry = DropdownMenuEntry<String>;

class _FlightDataViewState extends State<FlightDataView> {
  static final List<MenuEntry> _portEntries = UnmodifiableListView<MenuEntry>(
    _ports.map<MenuEntry>((String name) => MenuEntry(value: name, label: name)),
  );
  static final List<MenuEntry> _baudRateEntries =
      UnmodifiableListView<MenuEntry>(
    _baudRates
        .map<MenuEntry>((String name) => MenuEntry(value: name, label: name)),
  );
  String _selectedPort = _ports.first;
  String _selectedBaudRate = _baudRates.first;
  bool saveData = true;
  double _signalStrength = -2;
  double _speed = 0;
  double _verticalSpeed = 0;
  double _horizontalSpeed = 0;
  List<double> gpsData = [
    0,
    1,
    2,
    3,
    4,
    5,
  ];

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.all(20),
      padding: const EdgeInsets.all(20),
      width: MediaQuery.of(context).size.width,
      height: MediaQuery.of(context).size.height,
      decoration: BoxDecoration(
        color: const Color(0x9A1C5500),
        border: Border.all(
          color: Colors.black,
        ),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Row(children: [
            const Text("Serial Connection",
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(width: 20),
            // TODO: Implement a switch widget
            // TODO: Change button style
            ElevatedButton(onPressed: () {}, child: const Text('Change Mode'))
          ]),
          const SizedBox(height: 20),
          Row(
            children: [
              const Text("PORT",
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(width: 20),
              DropdownMenu<String>(
                initialSelection: _selectedPort,
                dropdownMenuEntries: _portEntries,
                onSelected: (String? value) {
                  setState(() {
                    _selectedPort = value!;
                  });
                },
              ),
              const SizedBox(width: 20),
              const Text("BAUD RATE",
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(width: 20),
              DropdownMenu<String>(
                initialSelection: _selectedBaudRate,
                dropdownMenuEntries: _baudRateEntries,
                onSelected: (String? value) {
                  setState(() {
                    _selectedPort = value!;
                  });
                },
              ),
            ],
          ),
          const SizedBox(height: 20),
          Row(
            children: [
              // TODO: Implement functionalities for this row
              Checkbox(
                  value: saveData,
                  onChanged: (bool? value) {
                    setState(() {
                      saveData = value!;
                    });
                  }),
              const Text("Save Data",
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(width: 20),
              ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _signalStrength = 0;
                    });
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                  ),
                  child: const Text('Start',
                      style: TextStyle(color: Colors.white))),
              const SizedBox(width: 20),
              ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _signalStrength = -2;
                    });
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.red,
                  ),
                  child: const Text('Stop',
                      style: TextStyle(color: Colors.white))),
            ],
          ),
          const SizedBox(height: 20),
          StatusBar(
              signalStrength: _signalStrength, textLength: 120, barLength: 150),
          const SizedBox(height: 20),
          const Text("GPS Data",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 20),
          Speedometer(
              minSpeed: 0,
              maxSpeed: 2000,
              speed: _speed,
              verticalSpeed: _verticalSpeed,
              horizontalSpeed: _horizontalSpeed),
          Row(
            children: [
              const SizedBox(
                width: 150,
                child: Text("Latitude", style: TextStyle(fontSize: 20)),
              ),
              SizedBox(
                width: 150,
                child: Text(gpsData[0].toString(), style: const TextStyle(fontSize: 20)),
              )
            ],
          ),
          const SizedBox(height: 20),
          Row(
            children: [
              const SizedBox(
                width: 150,
                child: Text("Longitude", style: TextStyle(fontSize: 20)),
              ),
              SizedBox(
                width: 150,
                child: Text(gpsData[1].toString(), style: const TextStyle(fontSize: 20)),
              )
            ],
          ),
          const SizedBox(height: 20),
          Row(
            children: [
              const SizedBox(
                width: 150,
                child: Text("Altitude (m)", style: TextStyle(fontSize: 20)),
              ),
              SizedBox(
                width: 150,
                child: Text(gpsData[2].toString(), style: const TextStyle(fontSize: 20)),
              )
            ],
          ),
          const SizedBox(height: 20),
          Row(
            children: [
              const SizedBox(
                width: 150,
                child: Text("AGL (m)", style: TextStyle(fontSize: 20)),
              ),
              SizedBox(
                width: 150,
                child: Text(gpsData[3].toString(), style: const TextStyle(fontSize: 20)),
              )
            ],
          ),
          const SizedBox(height: 20),
          Row(
            children: [
              const SizedBox(
                width: 150,
                child: Text("RSSI", style: TextStyle(fontSize: 20)),
              ),
              SizedBox(
                width: 150,
                child: Text(gpsData[4].toString(), style: const TextStyle(fontSize: 20)),
              )
            ],
          ),
          const SizedBox(height: 20),
          Row(
            children: [
              const SizedBox(
                width: 150,
                child: Text("Number of Sat.", style: TextStyle(fontSize: 20)),
              ),
              SizedBox(
                width: 150,
                child: Text(gpsData[5].toString(), style: const TextStyle(fontSize: 20)),
              )
            ],
          ),
        ],
      ),
    );
  }
}
