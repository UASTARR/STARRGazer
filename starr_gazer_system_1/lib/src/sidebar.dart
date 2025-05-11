import 'package:flutter/material.dart';
import 'features/map.dart';
import 'features/serial.dart';
import 'package:signals_slots/signals_slots.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter_libserialport/flutter_libserialport.dart';

class SidebarLayout extends StatefulWidget {
  const SidebarLayout({super.key});

  @override
  State<SidebarLayout> createState() => _SidebarLayoutState();
}

class _SidebarLayoutState extends State<SidebarLayout> {
  String? selectedFilePath;
  late Serial serialManager;
  Connection? _serialSubscription;
  final GlobalKey<OfflineMapScreenState> mapKey = GlobalKey();

  @override
  void initState() {
    super.initState();
    serialManager = Serial();

    _serialSubscription = serialManager.onDataReceived.connect((data) {
      mapKey.currentState?.addCoordinate(data);
    });
  }

  @override
  void dispose() {
    _serialSubscription?.disconnect();
    serialManager.disconnect();
    super.dispose();
  }

  void _pickFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles();

    if (result != null && result.files.single.path != null) {
      setState(() {
        selectedFilePath = result.files.single.path!;
      });
      mapKey.currentState?.loadCoordinatesFromFile(selectedFilePath!);
    }
  }

  void _connectToPort(String portName) {
    serialManager.connect(portName);
  }

  @override
  Widget build(BuildContext context) {
    final ports = SerialPort.availablePorts;

    return Scaffold(
      appBar: AppBar(title: const Text('Offline Map with Sidebar')),
      body: Row(
        children: [
          Expanded(
            child: OfflineMapScreen(
              key: mapKey,
            ),
          ),
          Container(
            width: 300,
            color: Colors.grey[200],
            child: Column(
              children: [
                ElevatedButton(
                  onPressed: _pickFile,
                  child: const Text('Load File'),
                ),
                const Divider(),
                const Text('Serial Ports',
                    style: TextStyle(fontWeight: FontWeight.bold)),
                Expanded(
                  child: ListView.builder(
                    itemCount: ports.length,
                    itemBuilder: (context, index) {
                      final portName = ports[index];
                      return ListTile(
                        title: Text(portName),
                        onTap: () => _connectToPort(portName),
                      );
                    },
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
