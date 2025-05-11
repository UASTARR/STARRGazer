import 'package:flutter/material.dart';
import 'sidebar.dart';

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Offline Map App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const SidebarLayout(),
      debugShowCheckedModeBanner: false,
    );
  }
}
