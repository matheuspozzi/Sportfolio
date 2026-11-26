document.addEventListener("DOMContentLoaded", () => {
    const app = document.querySelector(".app");
    if (!app) return;

    const authView = document.createElement("main");
    authView.id = "authView";

    authView.innerHTML = `
        <div class="auth-layout">
            <section class="auth-showcase">
                <div class="showcase-top">
                    <span class="showcase-logo">SPORTFOLIO</span>
                    <span class="showcase-version">ATHLETE PLATFORM / 01</span>
                </div>

                <div class="showcase-content">
                    <span class="showcase-tag">
                        <span class="status-dot"></span>
                        SUA JORNADA COMEÇA AQUI
                    </span>
                    <h1>Mais que números.<br><span>Sua evolução.</span></h1>
                    <p>
                        Acompanhe sua trajetória esportiva,
                        organize seus resultados e transforme
                        dedicação em evolução.
                    </p>
                    <div class="showcase-stats">
                        <div><strong>01</strong><span>PERFIL</span></div>
                        <div><strong>02</strong><span>DESEMPENHO</span></div>
                        <div><strong>03</strong><span>EVOLUÇÃO</span></div>
                    </div>
                </div>

                <div class="showcase-decoration">
                    <div class="decoration-circle"></div>
                    <div class="decoration-line"></div>
                    <span>PERFORMANCE IS A JOURNEY.</span>
                </div>

                <div class="showcase-bottom">
                    <span>SPORTFOLIO © 2026</span>
                    <span>FEITO PARA QUEM VIVE O ESPORTE.</span>
                </div>
            </section>

            <section class="auth-panel">
                <div class="auth-card">
                    <div class="auth-mobile-logo">SPORTFOLIO</div>

                    <div class="auth-heading">
                        <span class="auth-eyebrow">ÁREA DO ATLETA</span>
                        <h2 id="authTitle">Bem-vindo de volta.</h2>
                        <p id="authSubtitle">
                            Entre para acompanhar sua trajetória.
                        </p>
                    </div>

                    <div class="auth-tabs">
                        <button type="button" class="active" data-mode="login">Entrar</button>
                        <button type="button" data-mode="register">Criar conta</button>
                    </div>

                    <form id="authForm">
                        <div id="nameField" class="auth-field" hidden>
                            <label for="authName">Nome completo</label>
                            <input id="authName" type="text"
                                placeholder="Como podemos te chamar?"
                                minlength="2" maxlength="120">
                        </div>

                        <div class="auth-field">
                            <label for="authEmail">E-mail</label>
                            <input id="authEmail" type="email"
                                placeholder="seu@email.com" required>
                        </div>

                        <div class="auth-field">
                            <label for="authPassword">Senha</label>
                            <div class="auth-password-wrap">
                                <input id="authPassword" type="password"
                                    placeholder="Digite sua senha" required>
                                <button type="button" class="auth-password-toggle"
                                    data-toggle="authPassword"
                                    aria-label="Mostrar senha">Mostrar</button>
                            </div>
                        </div>

                        <div id="confirmField" class="auth-field" hidden>
                            <label for="authConfirmPassword">Confirmar senha</label>
                            <div class="auth-password-wrap">
                                <input id="authConfirmPassword" type="password"
                                    placeholder="Digite a senha novamente">
                                <button type="button" class="auth-password-toggle"
                                    data-toggle="authConfirmPassword"
                                    aria-label="Mostrar confirmação de senha">Mostrar</button>
                            </div>
                        </div>

                        <button class="auth-submit" type="submit">
                            Entrar na plataforma <span>→</span>
                        </button>

                        <p id="authMessage" role="status" aria-live="polite"></p>
                    </form>

                    <div class="auth-footer">
                        <span>SPORTFOLIO</span>
                        <span>Desenvolvido para atletas.</span>
                    </div>
                </div>
            </section>
        </div>
    `;

    document.body.insertBefore(authView, app);

    const tabs = authView.querySelectorAll("[data-mode]");
    const form = document.getElementById("authForm");
    const nameField = document.getElementById("nameField");
    const nameInput = document.getElementById("authName");
    const confirmField = document.getElementById("confirmField");
    const password = document.getElementById("authPassword");
    const confirmPassword = document.getElementById("authConfirmPassword");
    const submit = authView.querySelector(".auth-submit");
    const message = document.getElementById("authMessage");
    const title = document.getElementById("authTitle");
    const subtitle = document.getElementById("authSubtitle");

    let mode = "login";

    function showMessage(text, success = false) {
        message.textContent = text;
        message.style.color = success ? "#b8f36b" : "#ff8585";
    }

    function changeMode(newMode) {
        mode = newMode;
        const registering = mode === "register";

        tabs.forEach(tab => {
            tab.classList.toggle("active", tab.dataset.mode === mode);
        });

        nameField.hidden = !registering;
        confirmField.hidden = !registering;

        nameInput.required = registering;
        confirmPassword.required = registering;

        password.minLength = registering ? 12 : 0;

        title.textContent = registering
            ? "Comece sua jornada."
            : "Bem-vindo de volta.";

        subtitle.textContent = registering
            ? "Crie seu perfil de atleta."
            : "Entre para acompanhar sua trajetória.";

        submit.innerHTML = registering
            ? 'Criar minha conta <span>→</span>'
            : 'Entrar na plataforma <span>→</span>';

        form.reset();

        authView.querySelectorAll(".auth-password-toggle").forEach(button => {
            const input = document.getElementById(button.dataset.toggle);
            input.type = "password";
            button.textContent = "Mostrar";
        });

        showMessage("");
    }

    tabs.forEach(tab => {
        tab.addEventListener("click", () => changeMode(tab.dataset.mode));
    });

    authView.querySelectorAll(".auth-password-toggle").forEach(button => {
        button.addEventListener("click", () => {
            const input = document.getElementById(button.dataset.toggle);
            const visible = input.type === "text";

            input.type = visible ? "password" : "text";
            button.textContent = visible ? "Mostrar" : "Ocultar";
            button.setAttribute(
                "aria-label",
                visible ? "Mostrar senha" : "Ocultar senha"
            );
        });
    });

    form.addEventListener("submit", event => {
        event.preventDefault();

        if (!form.reportValidity()) return;

        if (mode === "register") {
            if (nameInput.value.trim().length < 2) {
                showMessage("Informe seu nome completo.");
                nameInput.focus();
                return;
            }

            if (password.value.length < 12) {
                showMessage("A senha precisa ter pelo menos 12 caracteres.");
                password.focus();
                return;
            }

            if (password.value !== confirmPassword.value) {
                showMessage("As senhas não coincidem.");
                confirmPassword.focus();
                return;
            }

            showMessage(
                "Cadastro demonstrativo validado! A integração será feita depois.",
                true
            );
            return;
        }

        document.body.classList.add("dashboard-active");
        authView.style.display = "none";
        app.style.display = "";
        window.scrollTo(0, 0);
    });
});

/* Logout demonstrativo */
document.addEventListener("DOMContentLoaded", () => {
    const logoutButton = document.getElementById("logoutButton");

    if (!logoutButton) return;

    logoutButton.addEventListener("click", () => {
        const confirmLogout = window.confirm("Deseja realmente sair da sua conta?");

        if (!confirmLogout) return;

        document.body.classList.remove("dashboard-active");

        const authView = document.getElementById("authView");
        const app = document.querySelector(".app");

        if (authView) authView.style.display = "";
        if (app) app.style.display = "none";

        window.scrollTo(0, 0);
    });
});
