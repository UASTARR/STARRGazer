import 'dart:convert';
import 'package:flutter_libserialport/flutter_libserialport.dart';
import 'package:latlong2/latlong.dart';
import 'package:signals_slots/signals_slots.dart';

class Serial {
  SerialPort? _port;
  SerialPortReader? _reader;
  Signal1<LatLng> onDataReceived = Signal1<LatLng>();

  List<String> get availablePorts => SerialPort.availablePorts;

  bool connect(String portName) {
    try {
      _port = SerialPort(portName);
      if (!_port!.openReadWrite()) {
        print('Failed to open port');
        return false;
      }

      _reader = SerialPortReader(_port!);
      _reader!.stream.listen((data) {
        try {
          final line = utf8.decode(data);
          // Expecting "lat,lon\n"
          List<String> parts = line.trim().split(',');
          if (parts.length == 2) {
            final lat = double.tryParse(parts[0]);
            final lon = double.tryParse(parts[1]);
            if (lat != null && lon != null) {
              LatLng temp = LatLng(lat, lon);
              onDataReceived.emit(temp);
            }
          }
        } catch (e) {
          print("Serial data parsing error: $e");
        }
      });

      return true;
    } catch (e) {
      print('Connection error: $e');
      return false;
    }
  }

  void disconnect() {
    _reader?.close();
    _port?.close();
    _port = null;
    _reader = null;
  }
}
