// src/components/ProtectedRoute.jsx
import React from "react";
import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode"; // Changed import statement

const isTokenValid = (token) => {
  try {
    const decoded = jwtDecode(token); // Remove .default
    // 가짜 토큰인 경우 exp가 없으면 true 처리
    if (!decoded.exp) return true;
    return decoded.exp * 1000 > Date.now(); // exp는 초 단위, Date.now()는 밀리초
  } catch (err) {
    console.error("JWT decode error:", err);
    return false;
  }
};

const ProtectedRoute = ({ children, requiredRole }) => {
  const token = localStorage.getItem("access_token");
  let user = null;
  
  try {
    const userStr = localStorage.getItem("user");
    if (userStr) {
      user = JSON.parse(userStr);
    }
  } catch (err) {
    console.error("Error parsing user:", err);
    return <Navigate to="/" replace />;
  }

  if (!token || !user || !isTokenValid(token)) {
    // console.log("Authentication failed - redirecting to login");
    return <Navigate to="/" replace />;
  }

  if (requiredRole && user.role !== requiredRole) {
    // console.log(`Role mismatch - required: ${requiredRole}, user has: ${user.role}`);
    return <Navigate to={`/${user.role}`} replace />;
  }

//   console.log("Authentication successful");
  return children;
};

export default ProtectedRoute;