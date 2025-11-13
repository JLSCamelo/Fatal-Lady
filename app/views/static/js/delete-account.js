document.getElementById("btn-danger").addEventListener("click", async () => {
    if (!confirm("Tem certeza que deseja excluir sua conta? Essa ação não pode ser desfeita.")) {
        return;
    }

    const resposta = await fetch("/excluir/conta", {
        method: "post",
        credentials: "include" // envia o cookie do token
    });

    if (resposta.ok) {
        alert("Enviamos um email, para confirmação!");
        window.location.href = "/"; // redireciona para home
    } else {
        const erro = await resposta.json();
        alert("Erro ao excluir conta: " + erro.detail);
    }
});

