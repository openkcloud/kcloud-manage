// src/utils/auth.js
const API_URL = window.ENV?.API_URL || import.meta.env.VITE_API_URL || '';

export async function fetchWithAuth(url, options = {}) {
  let accessToken = localStorage.getItem("access_token");
  const refreshToken = localStorage.getItem("refresh_token");

  if (!accessToken) {
    console.warn("❌ access token 없음. 로그인 필요");
    alert("로그인이 필요합니다.");
    window.location.href = "/";
    return;
  }

  let response = await fetch(`${API_URL}${url}`, {
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });


  if (response.status === 401 && refreshToken) {
    const refreshRes = await fetch(`${API_URL}/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (refreshRes.ok) {
      const data = await refreshRes.json();
      accessToken = data.token;
      localStorage.setItem("access_token", accessToken);

      // 재요청
      response = await fetch(`${API_URL}${url}`, {
        ...options,
        headers: {
          ...options.headers,
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
      });
    } else {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      alert("세션이 만료되었습니다. 다시 로그인해주세요.");
      window.location.href = "/";
      return;
    }
  }

  return response;
}

// 로그아웃 함수
export function logout() {
  // localStorage에서 토큰 제거
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  
  // 추가로 필요한 정리 작업이 있다면 여기에 추가
  
  // 로그인 페이지로 리다이렉트
  window.location.href = "/";
}

// 로그인 상태 확인
export function isLoggedIn() {
  const accessToken = localStorage.getItem("access_token");
  return !!accessToken;
}

// 현재 사용자 정보 가져오기 (토큰에서 디코드)
export function getCurrentUser() {
  const accessToken = localStorage.getItem("access_token");
  
  if (!accessToken) {
    return null;
  }
  
  try {
    // JWT 토큰 디코드 (간단한 방법)
    const payload = JSON.parse(atob(accessToken.split('.')[1]));
    return {
      username: payload.sub || payload.username || "사용자",
      role: payload.role || "user",
      exp: payload.exp
    };
  } catch (error) {
    console.error("토큰 디코드 실패:", error);
    return {
      username: "사용자",
      role: "user"
    };
  }
}