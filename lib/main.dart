import 'package:flutter/material.dart';
import 'api.dart';
import 'dart:convert';

void main() => runApp(MaterialApp(home: AuthPage()));

class AuthPage extends StatefulWidget {
  const AuthPage({super.key});
  @override
  State<AuthPage> createState() => _AuthPageState();
}

class _AuthPageState extends State<AuthPage> {
  final formKey = GlobalKey<FormState>();
  String email = '', password = '', confirm = '', message = '';
  bool dangNhap = true, loading = false;

  void submit() async {
    if (!formKey.currentState!.validate()) return;
    formKey.currentState!.save();
    if (!dangNhap && password != confirm) {
      setState(() => message = 'Mật khẩu không khớp');
      return;
    }
    setState(() {
      loading = true;
      message = '';
    });
    try {
      var data = {'email': email, 'password': password};
      var res = dangNhap
          ? await ApiService.login(data)
          : await ApiService.register(data);
      var body = jsonDecode(res.body);
      if (res.statusCode == 200) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => const HomePage()),
        );
      } else {
        setState(() => message = body['message'] ?? 'Lỗi');
      }
    } catch (_) {
      setState(() => message = 'Lỗi kết nối');
    }
    setState(() => loading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(dangNhap ? 'Đăng nhập' : 'Đăng ký')),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextFormField(
                decoration: const InputDecoration(labelText: 'Email'),
                onSaved: (v) => email = v ?? '',
                validator: (v) => v == null || v.isEmpty ? 'Nhập email' : null,
              ),
              TextFormField(
                decoration: const InputDecoration(labelText: 'Mật khẩu'),
                obscureText: true,
                onSaved: (v) => password = v ?? '',
                validator: (v) =>
                    v == null || v.isEmpty ? 'Nhập mật khẩu' : null,
              ),
              if (!dangNhap)
                TextFormField(
                  decoration: const InputDecoration(
                    labelText: 'Nhập lại mật khẩu',
                  ),
                  obscureText: true,
                  onSaved: (v) => confirm = v ?? '',
                  validator: (v) =>
                      v == null || v.isEmpty ? 'Nhập lại mật khẩu' : null,
                ),
              if (message.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.only(top: 12),
                  child: Text(
                    message,
                    style: const TextStyle(color: Colors.red),
                  ),
                ),
              if (loading)
                const Padding(
                  padding: EdgeInsets.all(12),
                  child: CircularProgressIndicator(),
                ),
              if (!loading)
                ElevatedButton(
                  onPressed: submit,
                  child: Text(dangNhap ? 'Đăng nhập' : 'Đăng ký'),
                ),
              TextButton(
                onPressed: () => setState(() {
                  dangNhap = !dangNhap;
                  message = '';
                }),
                child: Text(
                  dangNhap
                      ? 'Chưa có tài khoản? Đăng ký'
                      : 'Đã có tài khoản? Đăng nhập',
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});
  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Trang chủ')),
    body: const Center(child: Text('Đăng nhập thành công!')),
  );
}
