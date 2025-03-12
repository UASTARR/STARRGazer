//import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:flutter_map_mbtiles/flutter_map_mbtiles.dart';
import 'package:flutter/services.dart' show rootBundle;

void main() {
  runApp(MaterialApp(
    home: OfflineMapScreen(),
  ));
}

class OfflineMapScreen extends StatefulWidget {
  const OfflineMapScreen({super.key});

  @override
  OfflineMapScreenState createState() => OfflineMapScreenState();
}

class OfflineMapScreenState extends State<OfflineMapScreen> {
  MbTilesTileProvider? _tileProvider;
  List<LatLng> coordinates = [];

  @override
  void initState() {
    super.initState();
    _initializeTileProvider();
    loadCoordinates();
  }

  Future<void> _initializeTileProvider() async {
    // add your own path
    _tileProvider = MbTilesTileProvider.fromPath(path: 'live_map_display/assets/Edmonton.mbtiles');
  }

  // will have to change based on how the gps cordniate system sends data
  Future<void> loadCoordinates() async {
    String filePath = "assets/fake_cord_data.txt"; 
    try {
      String fileContent = await rootBundle.loadString(filePath);
      List<String> lines = fileContent.split('\n');

      setState(() {
        coordinates = lines.map((line) {
          List<String> parts = line.split(',');
          if (parts.length == 2) {
            return LatLng(
              double.parse(parts[0].trim()), // Latitude
              double.parse(parts[1].trim()), // Longitude
            );
          }
          return null;
        }).whereType<LatLng>().toList();
      });
    } catch (e) {
      print("Error loading coordinates: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Offline Map with Coordinates")),
      body: FlutterMap(
        options: MapOptions(
          initialCenter: LatLng(53.53, -113.50),
          initialZoom: 12,
          maxZoom: 18,
        ),
        children: [
          // Wait until the tile provider is initialized before displaying the map
          if (_tileProvider != null)
            TileLayer(
              tileProvider: _tileProvider!,
            ),
          // If the provider is not initialized, show a loading indicator
          if (_tileProvider == null)
            Center(child: CircularProgressIndicator()),

          //Optional: Add Markers for each coordinate
          /*
          MarkerLayer(
            markers: coordinates.map((latLng) {
              return Marker(
                width: 30.0,
                height: 30.0,
                point: latLng,
                child: Icon(Icons.location_pin, color: Colors.red, size: 30),
              );
            }).toList(),
          ),
          */
          //Draw a Polyline between coordinates
          PolylineLayer(
            polylines: [
              Polyline(
                points: coordinates,
                strokeWidth: 3.0,
                color: Colors.blue,
              ),
            ],
          ),
        ],
      ),
    );
  }
}