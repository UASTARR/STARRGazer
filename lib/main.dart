import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:flutter_map_mbtiles/flutter_map_mbtiles.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';

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
  LatLngBounds? _mapBounds;
  final MapController _mapController = MapController();
  double _minZoom = 12.0;
  double _maxZoom = 18.0;
  Timer? _fileMonitorTimer;

  String filePath = "C:/Users/School/VS_Code_Projects/live_map_display/assets/fake_cord_data.txt";
  String? _lastFileContent; // Stores last read file content

  @override
  void initState() {
    super.initState();
    _initializeTileProvider();
    getBounds();
    loadCoordinates();

    // Start monitoring the file every 2 seconds
    _fileMonitorTimer = Timer.periodic(Duration(seconds: 2), (timer) {
      loadCoordinates();
    });
  }

  @override
  void dispose() {
    _fileMonitorTimer?.cancel(); // Stop monitoring when widget is disposed
    super.dispose();
  }

  Future<void> _initializeTileProvider() async {
    _tileProvider = MbTilesTileProvider.fromPath(
        path: 'C:/Users/School/VS_Code_Projects/live_map_display/assets/Edmonton.mbtiles');
  }

  Future<void> getBounds() async {
    String mbtilesPath = "C:/Users/School/VS_Code_Projects/live_map_display/assets/Edmonton.mbtiles";
    databaseFactory = databaseFactoryFfi;
    var database = await openDatabase(mbtilesPath);

    List<Map<String, dynamic>> metadata = await database.rawQuery('SELECT * FROM metadata');

    double? minLatitude, minLongitude, maxLatitude, maxLongitude;

    var boundsEntry = metadata.firstWhere(
      (entry) => entry['name'] == 'bounds',
      orElse: () => {},
    );

    if (boundsEntry.isNotEmpty) {
      List<String> coordinatesBounds = boundsEntry['value'].split(',');
      if (coordinatesBounds.length == 4) {
        minLongitude = double.tryParse(coordinatesBounds[0]);
        minLatitude = double.tryParse(coordinatesBounds[1]);
        maxLongitude = double.tryParse(coordinatesBounds[2]);
        maxLatitude = double.tryParse(coordinatesBounds[3]);

        if (minLatitude != null &&
            minLongitude != null &&
            maxLatitude != null &&
            maxLongitude != null) {
          _mapBounds = LatLngBounds(
            LatLng(minLatitude, minLongitude),
            LatLng(maxLatitude, maxLongitude),
          );
        }
      }
    }

    double maxZoom = double.tryParse(
          metadata.firstWhere((item) => item["name"] == "maxzoom",
              orElse: () => {"value": "18"})["value"]!,
        ) ??
        18.0;
    double minZoom = double.tryParse(
          metadata.firstWhere((item) => item["name"] == "minzoom",
              orElse: () => {"value": "12"})["value"]!,
        ) ??
        12.0;

    setState(() {
      _minZoom = minZoom;
      _maxZoom = maxZoom;
    });

    await database.close();
  }

  Future<void> loadCoordinates() async {
    try {
      File file = File(filePath);

      if (!file.existsSync()) {
        print("File not found: $filePath");
        return;
      }

      String fileContent = file.readAsStringSync();

      // Check if the file has changed
      if (_lastFileContent == fileContent) return;
      _lastFileContent = fileContent;

      List<String> lines = fileContent.trim().split('\n');

      List<LatLng> newCoordinates = lines.map((line) {
        List<String> parts = line.split(',');
        if (parts.length == 2) {
          return LatLng(
            double.parse(parts[0].trim()),
            double.parse(parts[1].trim()),
          );
        }
        return null;
      }).whereType<LatLng>().toList();

      if (newCoordinates.isNotEmpty) {
        LatLng newLastCoord = newCoordinates.last;
        LatLng? currentLastCoord = coordinates.isNotEmpty ? coordinates.last : null;

        // Only update if the new data is different
        if (currentLastCoord == null || newLastCoord != currentLastCoord) {
          setState(() {
            coordinates = newCoordinates;
          });

          // Move map only if new coordinate is different
          _mapController.move(newLastCoord, _mapController.camera.zoom);
        }
      }
    } catch (e) {
      print("Error loading coordinates: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Offline Map with Coordinates")),
      body: FlutterMap(
        mapController: _mapController,
        options: MapOptions(
          initialCenter: _mapBounds?.center ?? LatLng(53.53, -113.50),
          initialZoom: _minZoom,
          maxZoom: _maxZoom,
          minZoom: _minZoom,
          
          onPositionChanged: (position, hasGesture) {
            if (_mapBounds != null) {
              LatLng center = position.center;
              double lat = center.latitude.clamp(
                _mapBounds!.southWest.latitude,
                _mapBounds!.northEast.latitude,
              );
              double lon = center.longitude.clamp(
                _mapBounds!.southWest.longitude,
                _mapBounds!.northEast.longitude,
              );

              if (lat != center.latitude || lon != center.longitude) {
                _mapController.move(LatLng(lat, lon), position.zoom);
              }
            }
          },
        
        ),
        children: [
          if (_tileProvider != null)
            TileLayer(
              tileProvider: _tileProvider!,
            ),
          if (_tileProvider == null)
            Center(child: CircularProgressIndicator()),

          if (coordinates.isNotEmpty) ...[
            MarkerLayer(
              markers: [
                Marker(
                  point: coordinates.first,
                  width: 30,
                  height: 30,
                  child: Icon(Icons.location_pin, color: Colors.green, size: 30),
                ),
                Marker(
                  point: coordinates.last,
                  width: 30,
                  height: 30,
                  child: Icon(Icons.location_pin, color: Colors.red, size: 30),
                ),
              ],
            ),
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
        ],
      ),
    );
  }
}
