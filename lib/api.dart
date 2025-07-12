import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://localhost:5001';

  static Future<http.Response> login(Map<String, dynamic> data) async {
    final url = Uri.parse('$baseUrl/auth/login');
    return await http.post(
      url,
      body: jsonEncode(data),
      headers: {'Content-Type': 'application/json'},
    );
  }

  static Future<http.Response> register(Map<String, dynamic> data) async {
    final url = Uri.parse('$baseUrl/auth/register');
    return await http.post(
      url,
      body: jsonEncode(data),
      headers: {'Content-Type': 'application/json'},
    );
  }
}
