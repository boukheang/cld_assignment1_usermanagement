const cp = require('child_process');

async function runTests() {
  console.log('====================================================');
  console.log('Running End-to-End Verification Test Suite');
  console.log('====================================================\n');

  console.log('1. Starting All 5 Microservices...');
  const gw = cp.spawn('node', ['APIGateway_Microservice/api-gateway.js'], { cwd: __dirname });
  const reg = cp.spawn('node', ['Registration_Microservice/registration.js'], { cwd: __dirname });
  const auth = cp.spawn('node', ['Authentication_Microservice/authentication-service.js'], { cwd: __dirname });
  const adm = cp.spawn('node', ['Admin_Microservice/index.js'], { cwd: __dirname });
  const usr = cp.spawn('node', ['User_Microservice/index.js'], { cwd: __dirname });

  // Wait 6 seconds for boot & DB connections
  await new Promise(r => setTimeout(r, 6000));

  try {
    const testEmail = `test_e2e_${Date.now()}@university.edu`;

    // 1. Registration via Gateway
    console.log('\n--- 1. Testing Registration via Gateway (:4000/register/userregister) ---');
    const regRes = await fetch('http://localhost:4000/register/userregister', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'Goat Ronaldo',
        email: testEmail,
        password: 'Password@2026',
        role: 'user',
        phone: '+85512345678'
      })
    });
    const regData = await regRes.json();
    console.log('Register Status:', regRes.status, regData);
    if (regRes.status !== 201) throw new Error('Registration failed');

    // 2. Login via Gateway
    console.log('\n--- 2. Testing Login via Gateway (:4000/auth/login) ---');
    const loginRes = await fetch('http://localhost:4000/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: testEmail,
        password: 'Password@2026',
        role: 'user'
      })
    });
    const loginData = await loginRes.json();
    console.log('Login Status:', loginRes.status, 'Token received:', !!loginData.token);
    if (loginRes.status !== 200 || !loginData.token) throw new Error('Login failed');
    const userToken = loginData.token;

    // 3. Security: Direct microservice access without token (Two-Tier defense)
    console.log('\n--- 3. Testing Direct Microservice Port Access Without Token (:5003/viewalluser) ---');
    const directRes = await fetch('http://localhost:5003/viewalluser');
    const directData = await directRes.json();
    console.log('Direct Access Status (Expect 401):', directRes.status, directData);
    if (directRes.status !== 401) throw new Error('Direct microservice port was not protected!');

    // 4. Security: User token accessing Admin API
    console.log('\n--- 4. Testing User Token on Admin API (:4000/admin/viewalluser) ---');
    const forbidRes = await fetch('http://localhost:4000/admin/viewalluser', {
      headers: { 'Authorization': `Bearer ${userToken}` }
    });
    const forbidData = await forbidRes.json();
    console.log('User accessing Admin API (Expect 403):', forbidRes.status, forbidData);
    if (forbidRes.status !== 403) throw new Error('Mutual exclusion failed');

    // 5. User View Profile via Gateway
    console.log('\n--- 5. Testing View Profile via Gateway (:4000/user/viewprofile) ---');
    const profRes = await fetch('http://localhost:4000/user/viewprofile', {
      headers: { 'Authorization': `Bearer ${userToken}` }
    });
    const profData = await profRes.json();
    console.log('View Profile Status (Expect 200):', profRes.status, profData.user ? profData.user.name : profData);
    if (profRes.status !== 200) throw new Error('View profile failed');

    console.log('\n====================================================');
    console.log('SUCCESS: All End-to-End Tests Passed!');
    console.log('====================================================\n');
  } catch (err) {
    console.error('Test Suite Error:', err.message);
  } finally {
    gw.kill();
    reg.kill();
    auth.kill();
    adm.kill();
    usr.kill();
    process.exit(0);
  }
}

runTests();
