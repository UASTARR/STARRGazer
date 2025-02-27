import 'package:flutter/material.dart';

class StatusBar extends StatelessWidget {
  final double signalStrength;
  final double barLength;
  final double textLength;
  const StatusBar({super.key, required this.signalStrength, required this.textLength, required this.barLength, });

  @override
  Widget build(BuildContext context) {
    switch (signalStrength) {
      case -2:
        return Row(
          children: [
            SizedBox(
              width: textLength,
              child: const Text('Disconnected',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            ),
            const SizedBox(width: 20),
            SizedBox(
                width: barLength,
                child: const LinearProgressIndicator(
                    value: 0, backgroundColor: Colors.grey, minHeight: 10)),
          ],
        );
      case -1:
        return Row(
          children: [
            SizedBox(
              width: textLength,
              child: const Text('Lost',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            ),
            const SizedBox(width: 20),
            SizedBox(
                width: barLength,
                child: const LinearProgressIndicator(
                    value: 0, backgroundColor: Colors.red, minHeight: 10)),
          ],
        );
      case 0:
        return Row(
          children: [
            SizedBox(
              width: textLength,
              child: const Text('Idle',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            ),
            const SizedBox(width: 20),
            SizedBox(
                width: barLength,
                child: const LinearProgressIndicator(
                    value: 0, backgroundColor: Colors.blue, minHeight: 10)),
          ],
        );
      case > 0 && < 0.5:
        return Row(
          children: [
            SizedBox(
              width: textLength,
              child: const Text('Weak',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            ),
            const SizedBox(width: 20),
            SizedBox(
                width: barLength,
                child: LinearProgressIndicator(
                    value: signalStrength, color: Colors.green, backgroundColor: Colors.grey, minHeight: 10)),
          ],
        );
      case > 0.5 && < 0.75:
        return Row(
          children: [
            SizedBox(
              width: textLength,
              child: const Text('Moderate',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            ),
            const SizedBox(width: 20),
            SizedBox(
                width: barLength,
                child: LinearProgressIndicator(
                    value: signalStrength, color: Colors.green, backgroundColor: Colors.grey, minHeight: 10)),
          ],
        );
      case > 0.75:
        return Row(
          children: [
            SizedBox(
              width: textLength,
              child: const Text('Strong',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            ),
            const SizedBox(width: 20),
            SizedBox(
                width: barLength,
                child: LinearProgressIndicator(
                    value: signalStrength, color: Colors.green, backgroundColor: Colors.grey, minHeight: 10)),
          ],
        );
    }
    return const Placeholder();
  }
}
