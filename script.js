
const loginForm = document.getElementById("loginForm");
const passwordInput = document.getElementById("password");
const togglePassword = document.getElementById("togglePassword");
const message = document.getElementById("message");

// Mostrar ou ocultar senha
togglePassword.addEventListener("click", () => {

    const isPassword = passwordInput.type === "password";

    passwordInput.type = isPassword ? "text" : "password";

    togglePassword.textContent = isPassword ? "Ocultar" : "Mostrar";
});

// Evento de login
loginForm.addEventListener("submit", (event) => {

    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = passwordInput.value;

    if (!username || !password) {
        message.textContent = "Preencha todos os campos.";
        message.style.color = "#f87171";
        return;
    }

    message.textContent = "Interface pronta. Autenticação ainda não configurada.";
    message.style.color = "#fbbf24";

    console.log("Usuário informado:", username);

});
