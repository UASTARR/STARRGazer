import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_gauges/gauges.dart';

// Reference: https://www.youtube.com/watch?v=33z9M_XT1AE
class Speedometer extends StatelessWidget {
  final double minSpeed;
  final double maxSpeed;
  final double speed;
  final double verticalSpeed;
  final double horizontalSpeed;
  const Speedometer({
    super.key,
    required this.minSpeed,
    required this.maxSpeed,
    required this.speed,
    required this.verticalSpeed,
    required this.horizontalSpeed,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 250,
      child: Row(
        children: [
          Expanded(
            child: SfRadialGauge(
              title: const GaugeTitle(
                text: 'Speed',
                textStyle: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              axes: <RadialAxis>[
                RadialAxis(
                  startAngle: 150,
                  endAngle: 30,
                  minimum: minSpeed,
                  maximum: maxSpeed,
                  showLastLabel: true,
                  pointers: <GaugePointer>[
                    NeedlePointer(value: speed),
                  ],
                  majorTickStyle: const MajorTickStyle(
                    thickness: 2,
                    color: Colors.white,
                  ),
                  minorTickStyle: const MinorTickStyle(
                    thickness: 1,
                    color: Colors.white,
                  ),
                  axisLineStyle: const AxisLineStyle(
                      gradient: SweepGradient(colors: [
                    Colors.green,
                    Colors.yellow,
                    Colors.orange,
                    Colors.red,
                  ])),
                  axisLabelStyle:
                      const GaugeTextStyle(fontSize: 12, color: Colors.white),
                )
              ],
            ),
          ),
          Expanded(
            child: SfRadialGauge(
              title: const GaugeTitle(
                text: 'Vertical',
                textStyle: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              axes: <RadialAxis>[
                RadialAxis(
                  startAngle: 150,
                  endAngle: 30,
                  minimum: minSpeed,
                  maximum: maxSpeed,
                  showLastLabel: true,
                  pointers: <GaugePointer>[
                    NeedlePointer(value: verticalSpeed),
                  ],
                  majorTickStyle: const MajorTickStyle(
                    thickness: 2,
                    color: Colors.white,
                  ),
                  minorTickStyle: const MinorTickStyle(
                    thickness: 1,
                    color: Colors.white,
                  ),
                  axisLineStyle: const AxisLineStyle(
                      gradient: SweepGradient(colors: [
                    Colors.green,
                    Colors.yellow,
                    Colors.orange,
                    Colors.red,
                  ])),
                  axisLabelStyle:
                      const GaugeTextStyle(fontSize: 12, color: Colors.white),
                )
              ],
            ),
          ),
          Expanded(
            child: SfRadialGauge(
              title: const GaugeTitle(
                text: 'Horizontal',
                textStyle: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              axes: <RadialAxis>[
                RadialAxis(
                  startAngle: 150,
                  endAngle: 30,
                  minimum: minSpeed,
                  maximum: maxSpeed,
                  showLastLabel: true,
                  pointers: <GaugePointer>[
                    NeedlePointer(value: horizontalSpeed),
                  ],
                  majorTickStyle: const MajorTickStyle(
                    thickness: 2,
                    color: Colors.white,
                  ),
                  minorTickStyle: const MinorTickStyle(
                    thickness: 1,
                    color: Colors.white,
                  ),
                  axisLineStyle: const AxisLineStyle(
                      gradient: SweepGradient(colors: [
                    Colors.green,
                    Colors.yellow,
                    Colors.orange,
                    Colors.red,
                  ])),
                  axisLabelStyle:
                      const GaugeTextStyle(fontSize: 12, color: Colors.white),
                )
              ],
            ),
          ),
        ],
      ),
    );
  }
}
