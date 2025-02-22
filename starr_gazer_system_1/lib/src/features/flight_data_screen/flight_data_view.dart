import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

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
    _baudRates.map<MenuEntry>((String name) => MenuEntry(value: name, label: name)),
  );
  String _selectedPort = _ports.first;
  String _selectedBaudRate = _baudRates.first;

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
          )
          // Row(children: [
          //   const Text("PORT",
          //       style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          //   const SizedBox(width: 20),
          //   DropdownButton(
          //     alignment: Alignment.center,
          //     value: _selectedPort,
          //     items: _ports.map<DropdownMenuItem<String>>((String value) {
          //       return DropdownMenuItem<String>(
          //           value: value, child: Text(value));
          //     }).toList(),
          //     onChanged: (String? value) {
          //       setState(() {
          //         _selectedPort = value!;
          //       });
          //     },
          //   ),
          //   const SizedBox(width: 20),
          //   const Text("BAUD RATE",
          //       style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          //   const SizedBox(width: 20),
          //   DropdownButton(
          //     alignment: Alignment.center,
          //     value: _selectedBaudRate,
          //     items: _baudRates.map<DropdownMenuItem<String>>((String value) {
          //       return DropdownMenuItem<String>(
          //           value: value, child: Text(value));
          //     }).toList(),
          //     onChanged: (String? value) {
          //       setState(() {
          //         _selectedBaudRate = value!;
          //       });
          //     },
          //   ),
          // ]),
        ],
      ),
    );
  }
}
