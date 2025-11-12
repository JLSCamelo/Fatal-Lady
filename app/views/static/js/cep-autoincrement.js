 document.getElementById("cep").addEventListener("blur", async function () {
        const cep = this.value.replace(/\D/g, "");
        if (cep.length !== 8) {
          alert("CEP inválido. Digite um CEP com 8 números.");
          return;
        }
    
        try {
          const response = await fetch(`/frete/completar_cadastro/${cep}`);
          if (!response.ok) throw new Error("Erro ao buscar CEP");
    
          const data = await response.json();
    
          document.getElementById("rua").value = data.rua || "";
          document.getElementById("bairro").value = data.bairro || "";
          document.getElementById("cidade").value = data.cidade || "";
          document.getElementById("estado").value = data.estado || "";
    
        } catch (error) {
          console.error(error);
          alert("Não foi possível buscar o endereço. Verifique o CEP e tente novamente.");
        }
      });