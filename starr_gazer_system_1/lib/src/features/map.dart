import 'dart:async';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:flutter_map_mbtiles/flutter_map_mbtiles.dart';
import 'package:latlong2/latlong.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';

class OfflineMapScreen extends StatefulWidget {
  const OfflineMapScreen({
    super.key,
  });

  @override
  OfflineMapScreenState createState() => OfflineMapScreenState();
}

class OfflineMapScreenState extends State<OfflineMapScreen> {
  MbTilesTileProvider? _tileProvider;
  LatLngBounds? _mapBounds;
  Path path = Path<LatLng>();

  final MapController _mapController = MapController();
  double _minZoom = 12.0;
  double _maxZoom = 18.0;

  @override
  void initState() {
    super.initState();

    _initializeTileProvider();
    getBounds();
  }

  @override
  void dispose() {
    super.dispose();
  }

  Future<void> _initializeTileProvider() async {
    _tileProvider = MbTilesTileProvider.fromPath(
      path: 'assets/Edmonton.mbtiles',
    );
  }

  Future<void> getBounds() async {
    const mbtilesPath = "assets/Edmonton.mbtiles";
    databaseFactory = databaseFactoryFfi;
    var database = await openDatabase(mbtilesPath);

    List<Map<String, dynamic>> metadata =
        await database.rawQuery('SELECT * FROM metadata');

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

  void addCoordinate(LatLng coordinate) {
    try {
      if (_mapBounds != null && !_mapBounds!.contains(coordinate)) {
        print("Coordinate out of bounds: $coordinate");
        return;
      }

      if (path.coordinates.isEmpty || path.last != coordinate) {
        setState(() {
          path.add(coordinate);
        });
        _mapController.move(coordinate, _mapController.camera.zoom);
      }
    } catch (e) {
      print("Error Adding coordinate: $e");
    }
  }

  Future<void> loadCoordinatesFromFile(String _filepath) async {
    try {
      if (_filepath != '') {
        File file = File(_filepath);

        if (!file.existsSync()) {
          print("File not found: $_filepath");
          return;
        }

        String fileContent = file.readAsStringSync();

        List<String> lines = fileContent.trim().split('\n');

        for (String line in lines) {
          List<String> parts = line.split(',');
          if (parts.length == 2) {
            try {
              LatLng temp = LatLng(
                double.parse(parts[0].trim()),
                double.parse(parts[1].trim()),
              );
              addCoordinate(temp);
            } catch (e) {
              print("Invalid line skipped: $line");
            }
          }
        }
      }
    } catch (e) {
      print("Error loading coordinates: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: FlutterMap(
        mapController: _mapController,
        options: MapOptions(
          initialCenter: _mapBounds?.center ?? const LatLng(53.53, -113.50),
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
            TileLayer(tileProvider: _tileProvider!)
          else
            const Center(child: CircularProgressIndicator()),
          if (path.coordinates.isNotEmpty) ...[
            MarkerLayer(
              markers: [
                Marker(
                  point: path.first,
                  width: 30,
                  height: 30,
                  child: const Icon(Icons.location_pin,
                      color: Colors.green, size: 30),
                ),
                Marker(
                  point: path.last,
                  width: 30,
                  height: 30,
                  child: const Icon(Icons.location_pin,
                      color: Colors.red, size: 30),
                ),
              ],
            ),
            PolylineLayer(
              polylines: [
                Polyline(
                  points: path.coordinates,
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
