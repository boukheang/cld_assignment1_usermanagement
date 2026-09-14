const { spawn } = require('child_process');
const path = require('path');

const services = [
  { name: 'API-Gateway', dir: 'APIGateway_Microservice', file: 'api-gateway.js', port: 4000 },
  { name: 'Registration', dir: 'Registration_Microservice', file: 'index.js', port: 5001 },
  { name: 'Login', dir: 'Login_Microservice', file: 'index.js', port: 5002 },
  { name: 'Admin', dir: 'Admin_Microservice', file: 'index.js', port: 5003 },
  { name: 'User', dir: 'User_Microservice', file: 'index.js', port: 5004 },
];

console.log('====================================================');
console.log('Starting All 5 University Platform Microservices...');
console.log('====================================================');

const processes = [];

services.forEach(s => {
  const p = spawn('node', [path.join(__dirname, s.dir, s.file)], {
    stdio: ['inherit', 'pipe', 'pipe'],
    cwd: path.join(__dirname, s.dir)
  });

  p.stdout.on('data', data => {
    const lines = data.toString().trim().split('\n');
    lines.forEach(line => console.log(`[${s.name}] ${line.trim()}`));
  });

  p.stderr.on('data', data => {
    const lines = data.toString().trim().split('\n');
    lines.forEach(line => console.error(`[${s.name} ERR] ${line.trim()}`));
  });

  p.on('exit', code => {
    console.log(`[${s.name}] Process exited with code ${code}`);
  });

  processes.push(p);
});

process.on('SIGINT', () => {
  console.log('\nStopping all microservices...');
  processes.forEach(p => p.kill());
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\nStopping all microservices...');
  processes.forEach(p => p.kill());
  process.exit(0);
});
