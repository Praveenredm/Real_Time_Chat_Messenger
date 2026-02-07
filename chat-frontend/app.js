const API = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost"
  ? "http://127.0.0.1:8000"
  : ""; // Empty string means use current origin (relative path)

let token = localStorage.getItem("chat_token") || "";
let username = localStorage.getItem("chat_username") || "";
let socket = null;

// Auto-login if token exists
if (token) {
  showChat();
} else {
  showTab('login');
}

function showTab(tab) {
  document.querySelectorAll('.tabs button').forEach(b => b.classList.remove('active'));
  document.getElementById(`tab-${tab}`).classList.add('active');

  if (tab === 'login') {
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('register-form').style.display = 'none';
  } else {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'block';
  }
}

async function handleRegister(e) {
  e.preventDefault();
  const usernameInput = document.getElementById("reg-username").value;
  const email = document.getElementById("reg-email").value;
  const password = document.getElementById("reg-password").value;

  try {
    const res = await fetch(API + "/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: usernameInput, email, password })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Registration failed");

    loginSuccess(data);
  } catch (err) {
    alert(err.message);
  }
}

async function handleLogin(e) {
  e.preventDefault();
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  try {
    const res = await fetch(API + "/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Login failed");

    loginSuccess(data);
  } catch (err) {
    alert(err.message);
  }
}

function loginSuccess(data) {
  token = data.token;
  username = data.username;
  localStorage.setItem("chat_token", token);
  localStorage.setItem("chat_username", username);

  // Clear forms
  document.getElementById("login-form").reset();
  document.getElementById("register-form").reset();

  showChat();
}

function logout() {
  token = "";
  username = "";
  localStorage.removeItem("chat_token");
  localStorage.removeItem("chat_username");

  if (socket) {
    socket.close();
    socket = null;
  }

  document.getElementById("auth-section").classList.remove("hidden");
  document.getElementById("chat-section").classList.add("hidden");
  document.getElementById("messages-container").innerHTML = "";
  showTab('login');
}

function showChat() {
  document.getElementById("auth-section").classList.add("hidden");
  document.getElementById("chat-section").classList.remove("hidden");
  document.getElementById("chat-title").innerText = `Chatting as ${username}`;
  startChat();
}

function startChat() {
  if (socket) return;

  socket = new WebSocket(`ws://127.0.0.1:8000/ws/chat?token=${token}`);

  socket.onopen = () => {
    console.log("Connected to chat");
    appendMessage("System", "Connected to chat server");
  };

  socket.onmessage = (e) => {
    // Format is "username:message"
    const msg = e.data;
    const firstColon = msg.indexOf(':');

    if (firstColon === -1) {
      appendMessage("System", msg, false);
      return;
    }

    let senderName = msg.substring(0, firstColon);
    const text = msg.substring(firstColon + 1);

    // START DEBUG
    console.log(`Received: ${senderName}, My Username: ${username}`);
    // END DEBUG

    // If the server sends "User Praveen P", strip "User " to just get "Praveen P" if that's what we have locally
    // Or just check if senderName ENDS with our username? 
    // Let's try to normalize. 

    // Basic check
    if (senderName === username) {
      return;
    }

    // Fuzzy check for the "User " prefix issue
    if (senderName === `User ${username}`) {
      return;
    }

    // If we are "User 1" locally (old token) and server sends "User 1", it matches above.
    // If we are "Praveen" locally and server sends "User Praveen" (unexpected but possible if logic mixed), the 2nd check handles it.

    appendMessage(senderName, text, false);
  };

  socket.onclose = () => {
    console.log("Disconnected");
    socket = null;
  };

  socket.onerror = (e) => console.log("WS error", e);
}

function handleKey(e) {
  if (e.key === 'Enter') sendMessage();
}

function sendMessage() {
  if (!socket) return;
  const input = document.getElementById("message-input");
  const text = input.value.trim();
  if (!text) return;

  socket.send(text);
  appendMessage("You", text, true); // Optimistic UI
  input.value = "";
}

function appendMessage(sender, text, isSelf = false) {
  const container = document.getElementById("messages-container");
  const div = document.createElement("div");
  div.className = `msg ${isSelf ? 'self' : ''}`;

  if (sender === "System") {
    div.style.background = "#fff3cd";
    div.style.alignSelf = "center";
    div.innerText = text;
  } else {
    // If it's from server, it might be "user123". "You" is distinct.
    div.innerText = isSelf ? text : `${sender}: ${text}`;
  }

  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}
