# AI SOFTWARE IDE Frontend

Frontend application for the web dashboard for GPU cluster management. Built with React and Material Tailwind, providing features such as GPU server creation, monitoring, and storage management.

## 🚀 Key Features

- **GPU Server Creation**: Create servers by selecting CPU, Memory, and GPU resources
- **Real-time Monitoring**: Monitor GPU cluster status and running Pods
- **Storage Management**: Explore and manage PVC-based file systems
- **User Authentication**: JWT-based login/logout system
- **Responsive UI**: Optimized user experience across all devices

## 🛠 Tech Stack

- **Frontend Framework**: React 19.0.0
- **Build Tool**: Vite 6.1.0
- **UI Library**: Material Tailwind 2.1.10
- **Styling**: Tailwind CSS 3.4.17
- **Icons**: Heroicons 2.2.0
- **Routing**: React Router DOM 7.4.0
- **Authentication**: JWT Decode 4.0.0

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Secure/         # Authentication related components
│   ├── ExpendingRadioButton.jsx  # Server creation form
│   ├── RunningPodTable.jsx       # Running Pod table
│   ├── MyServerCard.jsx          # Server card component
│   ├── Navbar.jsx               # Navigation bar
│   ├── Sidebar.jsx              # Sidebar
│   ├── SignIn.jsx               # Login component
│   ├── GPUComponent.jsx         # GPU related component
│   ├── GPUNode.jsx              # GPU node display
│   ├── Loading.jsx              # Loading spinner
│   └── ...
├── layout/             # Layout components
│   ├── DashboardStatus.jsx      # Dashboard main screen
│   ├── CreatePod.jsx            # Server creation page
│   ├── MyServer.jsx             # My server management
│   ├── StorageManagement.jsx    # Storage management
│   └── Sidebar.jsx              # Layout sidebar
├── pages/              # Page components
│   ├── SignInPage.jsx           # Login page
│   ├── AdminDashboard.jsx       # Admin dashboard
│   └── UserDashboard.jsx        # User dashboard
├── utils/              # Utility functions
│   ├── auth.js                  # Authentication related functions
│   └── mockAuth.jsx             # Mock authentication
├── context/            # React Context configuration
├── assets/             # Static assets
├── public/             # Public files
├── App.jsx             # Main app component
├── main.jsx            # Entry point
└── index.css           # Global CSS
```

## 🔧 Installation and Execution

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation
```bash
# Install dependencies
npm install
```

### Development Server
```bash
# Run in development mode (port 4000)
npm run dev
```
Access via `http://localhost:4000` in your browser

### Build
```bash
# Production build
npm run build
```

### Lint Check
```bash
# Run ESLint
npm run lint
```

## 🌐 Environment Variables

Create a `.env` file and set the following environment variables:

```env
VITE_API_URL=http://localhost:8000  # Backend API URL
```

## 📝 Main Component Descriptions

### 1. Dashboard (DashboardStatus)
- Monitor overall GPU cluster status
- Display GPU, CPU, Memory usage per node
- Real-time updates (15-second interval)

### 2. Server Creation (ExpendingRadioButton)
- Step-by-step hardware selection (CPU → Memory → GPU)
- PVC selection (create new or use existing)
- Server name and description input

### 3. Storage Management (StorageManagement)
- Display PVC list
- File system exploration
- Folder/file information display

### 4. Running Server Table (RunningPodTable)
- Server classification by TAG (JUPYTER, LEGEND, DEV)
- Display user, resource usage, creation date
- Real-time updates (60-second interval)

## 🔐 Authentication System

- JWT-based token authentication
- Access Token + Refresh Token approach
- Automatic token refresh
- Token removal on logout

## 🎨 UI/UX Features

- **Material Design**: Consistent design based on Material Tailwind
- **Responsive**: Support for various screen sizes
- **Dark Mode**: Theme support based on user preference
- **Animations**: Smooth transitions using Framer Motion
- **Accessibility**: ARIA labels and keyboard navigation support

## 🔄 API Integration

Main endpoints for communication with backend API:

- `GET /server/list` - List running servers
- `POST /server/create-pod` - Create new server
- `GET /server/my-server` - List my servers
- `GET /server/my-pvcs` - List PVCs
- `GET /server/browse` - File system exploration
- `GET /metrics/gpu-resource` - GPU resource monitoring
- `GET /metrics/node-resource` - Node resource information

## 🐳 Docker Deployment

```bash
# Build Docker image
docker build -t ai-sw-ide-frontend .

# Run container
docker run -p 80:80 ai-sw-ide-frontend
```

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions, please create an issue.
