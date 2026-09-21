const cp = require('child_process');

console.log('====================================================');
console.log('Starting All 5 University Platform Microservices...');
console.log('====================================================');

const services = [
  { name: 'API-Gateway', cmd: 'node', args: ['APIGateway_Microservice/api-gateway.js'] },
  { name: 'Registration', cmd: 'node', args: ['Registration_Microservice/registration.js'] },
  { name: 'Authentication', cmd: 'node', args: ['Authentication_Microservice/authentication-service.js'] },
  { name: 'Admin', cmd: 'node', args: ['Admin_Microservice/index.js'] },
  { name: 'User', cmd: 'node', args: ['User_Microservice/index.js'] }
];

const processes = services.map(s => {
  const p = cp.spawn(s.cmd, s.args, { stdio: 'inherit', cwd: __dirname });
  p.on('exit', code => console.log(`[${s.name}] exited with code ${code}`));
  return p;
});

process.on('SIGINT', () => {
  console.log('\nShutting down all microservices...');
  processes.forEach(p => p.kill());
  process.exit(0);
});
