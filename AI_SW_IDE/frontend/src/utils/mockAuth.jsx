const MOCK_USERS = [
  {
    email: 'admin@okestro.com',
    password: '123',
    role: 'admin',
    name: 'Admin User',
    department: 'AI Research Lab'
  },
  {
    email: 'user@okestro.com', 
    password: 'user123',
    role: 'user',
    name: 'Regular User',
    department: 'AI Applications Team'
  }
];

export const loginUser = (email, password) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const user = MOCK_USERS.find(
        u => u.email === email && u.password === password
      );
      if (user) {
        resolve({
          success: true,
          user: {
            email: user.email,
            name: user.name,
            role: user.role,
            department: user.department
          }
        });
      } else {
        reject({ success: false, message: "Invalid email or password" });
      }
    }, 1000);
  });
};