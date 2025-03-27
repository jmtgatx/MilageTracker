import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() {
  runApp(const MaterialApp(home: WebViewContainer()));
}

class WebViewContainer extends StatefulWidget {
  const WebViewContainer({super.key});

  @override
  WebViewContainerState createState() => WebViewContainerState();
}

class WebViewContainerState extends State<WebViewContainer> {
  late final WebViewController controller;

  @override
  void initState() {
    super.initState();

    // ✅ Correct WebView setup for Flutter 3.x
    controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted) // ✅ FIXED: Correct name
      ..loadRequest(Uri.parse("http://localhost:8501/")); // ✅ Replace with your actual Streamlit URL
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Mileage Tracker")),
      body: WebViewWidget(controller: controller), // ✅ FIXED: Correct WebView usage
    );
  }
}
