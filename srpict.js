function showSignup() {
  document.getElementById("loginForm").style.display = "none";
  document.getElementById("signupForm").style.display = "block";
  document.getElementById("title").innerText = "Đăng ký";
}

function showLogin() {
  document.getElementById("signupForm").style.display = "none";
  document.getElementById("loginForm").style.display = "block";
  document.getElementById("title").innerText = "Đăng nhập";
}

// Đăng ký
document.getElementById("signupForm").addEventListener("submit", function(e){
  e.preventDefault();

  let user = signupUser.value;
  let pass = signupPass.value;
  let rePass = signupRePass.value;

  if(pass !== rePass){
    alert("Mật khẩu không khớp!");
    return;
  }

  localStorage.setItem(user, pass);
  alert("Đăng ký thành công!");
  showLogin();
});

// Đăng nhập
document.getElementById("loginForm").addEventListener("submit", function(e){
  e.preventDefault();

  let user = loginUser.value;
  let pass = loginPass.value;
  let savedPass = localStorage.getItem(user);

  if(savedPass === pass){
    alert("Đăng nhập thành công!");
  } else {
    alert("Sai tài khoản hoặc mật khẩu!");
  }
});
