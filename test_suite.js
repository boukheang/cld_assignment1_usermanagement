const http = require('http');

function makeRequest(options, postData = null) {
  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve({ status: res.statusCode, headers: res.headers, body: parsed, raw: data });
        } catch (e) {
          resolve({ status: res.statusCode, headers: res.headers, body: data, raw: data });
        }
      });
    });

    req.on('error', (err) => reject(err));

    if (postData) {
      req.write(typeof postData === 'string' ? postData : JSON.stringify(postData));
    }
    req.end();
  });
}

async function runTests() {
  console.log('================================================================');
  console.log('UNIVERSITY MICROSERVICES END-TO-END VERIFICATION TEST SUITE');
  console.log('================================================================\n');

  const results = [];

  async function step(title, description, reqOpts, reqBody) {
    console.log(`>>> TEST: ${title}`);
    console.log(`    ${reqOpts.method} http://localhost:${reqOpts.port || 4000}${reqOpts.path}`);
    if (reqBody) console.log(`    Body: ${JSON.stringify(reqBody)}`);
    try {
      const res = await makeRequest(reqOpts, reqBody);
      console.log(`    Status: ${res.status}`);
      console.log(`    Response: ${JSON.stringify(res.body, null, 2)}\n`);
      results.push({ title, description, reqOpts, reqBody, res });
      return res;
    } catch (err) {
      console.error(`    ERROR: ${err.message}\n`);
      results.push({ title, description, reqOpts, reqBody, error: err.message });
      throw err;
    }
  }

  // --- TASK 5: REGISTRATION ---
  // 1. Register normal user
  const regUserRes = await step(
    'Task 5.1: Register User Account (Student)',
    'Register student user with password hashing and unique email',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/register/userregister',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    },
    {
      name: 'Try Boukheang',
      email: 'student_boukheang@university.edu',
      password: 'StudentSecurePass123!',
      role: 'user',
      phone: '+85512345678'
    }
  );

  // 2. Register admin user
  const regAdminRes = await step(
    'Task 5.2: Register Admin Account',
    'Register administrative user with role admin',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/register/userregister',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    },
    {
      name: 'University Registrar Admin',
      email: 'admin_office@university.edu',
      password: 'AdminMasterPass123!',
      role: 'admin',
      phone: '+85598765432'
    }
  );

  // 3. Register duplicate email (Should fail)
  await step(
    'Task 5.3: Duplicate Email Prevention Test',
    'Attempt duplicate registration with same student email (Expect 400 Bad Request)',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/register/userregister',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    },
    {
      name: 'Duplicate Account',
      email: 'student_boukheang@university.edu',
      password: 'AnotherPassword',
      role: 'user',
      phone: '+85500000000'
    }
  );

  // --- TASK 6: LOGIN & JWT GENERATION ---
  // 1. Matched User Login
  const userLogin = await step(
    'Task 6.1: Valid User Login',
    'Login with valid student credentials and role user (Returns JWT)',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/auth/login',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    },
    {
      email: 'student_boukheang@university.edu',
      password: 'StudentSecurePass123!',
      role: 'user'
    }
  );
  const userToken = userLogin.body.token;

  // 2. Matched Admin Login
  const adminLogin = await step(
    'Task 6.2: Valid Admin Login',
    'Login with valid admin credentials and role admin (Returns JWT)',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/auth/login',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    },
    {
      email: 'admin_office@university.edu',
      password: 'AdminMasterPass123!',
      role: 'admin'
    }
  );
  const adminToken = adminLogin.body.token;

  // 3. Invalid Password
  await step(
    'Task 6.3: Invalid Password Login Attempt',
    'Attempt login with incorrect password (Expect 401 Unauthorized)',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/auth/login',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    },
    {
      email: 'student_boukheang@university.edu',
      password: 'WrongPassword456',
      role: 'user'
    }
  );

  // 4. Invalid Role
  await step(
    'Task 6.4: Invalid Role Login Attempt',
    'Attempt student account login claiming role admin (Expect 403 Forbidden)',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/auth/login',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    },
    {
      email: 'student_boukheang@university.edu',
      password: 'StudentSecurePass123!',
      role: 'admin'
    }
  );

  // --- TASK 10 & 7: SECURITY & ROLE GUARDS ---
  // 10.a: Without token try to access any API for admin or user
  await step(
    'Task 10.a: Access Admin API Without Token',
    'Access /admin/viewalluser without Authorization header (Expect 401 Unauthorized)',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/admin/viewalluser',
      method: 'GET'
    }
  );

  await step(
    'Task 10.a (User): Access User API Without Token',
    'Access /user/viewprofile without Authorization header (Expect 401 Unauthorized)',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/user/viewprofile',
      method: 'GET'
    }
  );

  // 10.b: With wrong token try to access any API for admin or user
  await step(
    'Task 10.b: Access Admin API With Wrong Token',
    'Access /admin/viewalluser with malformed/invalid token (Expect 403 Forbidden)',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/admin/viewalluser',
      method: 'GET',
      headers: { 'Authorization': 'Bearer this.is.an.invalid.token.12345' }
    }
  );

  // 10.c: Using admin token try to access any User API (Forbidden)
  await step(
    'Task 10.c: Using Admin Token to Access User API',
    'Administrator attempts to access /user/viewprofile (Expect 403 Forbidden: Admin cannot access User APIs)',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/user/viewprofile',
      method: 'GET',
      headers: { 'Authorization': `Bearer ${adminToken}` }
    }
  );

  // 10.d: Using user token try to access any Admin API (Forbidden)
  await step(
    'Task 10.d: Using User Token to Access Admin API',
    'Ordinary user attempts to access /admin/viewalluser (Expect 403 Forbidden: User cannot access Admin APIs)',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/admin/viewalluser',
      method: 'GET',
      headers: { 'Authorization': `Bearer ${userToken}` }
    }
  );

  // --- TASK 8: ADMIN MICROSERVICE ---
  // 1. View all users
  await step(
    'Task 8.1: Admin View All Users',
    'Admin views all registered users information with Admin Token',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/admin/viewalluser',
      method: 'GET',
      headers: { 'Authorization': `Bearer ${adminToken}` }
    }
  );

  // 2. Search user (Found)
  await step(
    'Task 8.2a: Admin Search User (Found by Email)',
    'Admin searches for student user by email query parameter',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/admin/searchuser?email=student_boukheang@university.edu',
      method: 'GET',
      headers: { 'Authorization': `Bearer ${adminToken}` }
    }
  );

  // 3. Search user (Found by Name)
  await step(
    'Task 8.2b: Admin Search User (Found by Name)',
    'Admin searches for user by name query parameter',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/admin/searchuser?name=Boukheang',
      method: 'GET',
      headers: { 'Authorization': `Bearer ${adminToken}` }
    }
  );

  // 4. Search user (Not Found)
  await step(
    'Task 8.2c: Admin Search User (Not Found)',
    'Admin searches for non-existent user (Expect 404 Not Found)',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/admin/searchuser?email=ghost_nonexistent@university.edu',
      method: 'GET',
      headers: { 'Authorization': `Bearer ${adminToken}` }
    }
  );

  // 5. Delete user: First create a disposable user to delete
  await step(
    'Task 8.3-Prep: Register Temporary User for Deletion',
    'Create temporary user to test delete functionality',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/register/userregister',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    },
    {
      name: 'Temp Delete User',
      email: 'temp_to_delete@university.edu',
      password: 'TempPassword123!',
      role: 'user',
      phone: '+85511223344'
    }
  );

  // Now delete the disposable user
  await step(
    'Task 8.3: Admin Delete User by Email',
    'Admin deletes temporary user by email with Admin Token',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/admin/deluser?email=temp_to_delete@university.edu',
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${adminToken}` }
    }
  );

  // --- TASK 9: USER MICROSERVICE ---
  // 1. View own profile (Before update)
  await step(
    'Task 9.1: User View Own Profile (Before Update)',
    'Student views own profile using User Token',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/user/viewprofile',
      method: 'GET',
      headers: { 'Authorization': `Bearer ${userToken}` }
    }
  );

  // 2. Update profile
  await step(
    'Task 9.2: User Update Own Profile',
    'Student updates name and phone number using User Token',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/user/updateprofile',
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${userToken}`,
        'Content-Type': 'application/json'
      }
    },
    {
      name: 'Try Boukheang (Updated Profile)',
      phone: '+85599887766'
    }
  );

  // 3. View own profile (After update)
  await step(
    'Task 9.3: User View Own Profile (After Update)',
    'Student verifies updated profile using User Token',
    {
      hostname: 'localhost',
      port: 4000,
      path: '/user/viewprofile',
      method: 'GET',
      headers: { 'Authorization': `Bearer ${userToken}` }
    }
  );

  console.log('================================================================');
  console.log('ALL TEST CASES EXECUTED SUCCESSFULLY!');
  console.log('================================================================');

  const fs = require('fs');
  fs.writeFileSync('test_results.json', JSON.stringify(results, null, 2));
  console.log('Saved test results to test_results.json');
}

runTests().catch((e) => {
  console.error('Test suite failed:', e);
  process.exit(1);
});
