document.getElementsByClassName("btn-danger").addEventListener("click", async () => {
    if (!confirm("Tem certeza que deseja excluir sua conta? Essa ação não pode ser desfeita.")) {
        return;
    }

    const resposta = await fetch("/usuarios/conta", {
        method: "DELETE",
        credentials: "include" // envia o cookie do token
    });

    if (resposta.ok) {
        alert("Conta excluída com sucesso!");
        window.location.href = "/"; // redireciona para home
    } else {
        const erro = await resposta.json();
        alert("Erro ao excluir conta: " + erro.detail);
    }
});

