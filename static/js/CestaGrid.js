
function atualizarValorTotal() {
    const valorProdutos = document.querySelectorAll(".valor_produto");
    const quantidades = document.querySelectorAll(".quantidade");
    let total = 0;

    for (let i = 0; i < valorProdutos.length; i++) {
        const valorProduto = parseFloat(valorProdutos[i].textContent.replace(",", ".")); // Converte o valor para número
        const quantidade = parseInt(quantidades[i].textContent);
        total += valorProduto * quantidade;
    }

    document.getElementById("valor_total").textContent = total.toFixed(2).replace(".", ","); // Exibe o valor total no formato desejado
}

// Seleciona todos os botões "menos" na tabela
const menosButtons = document.querySelectorAll(".menos");

menosButtons.forEach((menosButton) => {
    menosButton.addEventListener("click", () => {
        const quantidadeElement = menosButton.parentElement.querySelector(".quantidade");
        let valorAtual = parseInt(quantidadeElement.textContent);

        if (valorAtual > 0) {
            valorAtual--; // Diminui 1 do valor atual
            quantidadeElement.textContent = valorAtual; // Atualiza o conteúdo

            if (valorAtual === 0) {
                // Se a quantidade chegar a zero, remova a linha da tabela
                const tabelaRow = menosButton.closest(".produto-row");
                if (tabelaRow) {
                    tabelaRow.remove();
                }
            }
        }
        atualizarValorTotal();
    });
});

// Seleciona todos os botões "mais" na tabela
const maisButtons = document.querySelectorAll(".mais");

maisButtons.forEach((maisButton) => {
    maisButton.addEventListener("click", () => {
        const quantidadeElement = maisButton.parentElement.querySelector(".quantidade");
        let valorAtual = parseInt(quantidadeElement.textContent);

        if (valorAtual > 0) {
            valorAtual++; // Aumenta 1 do valor atual
            quantidadeElement.textContent = valorAtual; // Atualiza o conteúdo
        }
        atualizarValorTotal();
    });
});

// Adicione esse trecho de código no final do JavaScript existente

// Chama a função para calcular o valor total inicial
atualizarValorTotal();

const esvaziar = document.getElementById("esvaziar");

esvaziar.addEventListener("click", () => {
    const tabela = document.querySelector("tbody"); // Seleciona o corpo da tabela
    tabela.innerHTML = ''; // Remove todo o conteúdo do corpo da tabela
    atualizarValorTotal();
});