document.addEventListener('DOMContentLoaded', function () {
    const adicionarBotoes = document.querySelectorAll('.adicionar');
  
    adicionarBotoes.forEach(function (adicionarBotoes) {
      adicionarBotoes.addEventListener('click', function () {
        const produtoDiv = adicionarBotoes.closest('.flex-col');
        const nome = produtoDiv.dataset.nome;
        const valor = parseFloat(produtoDiv.dataset.valor);
        const quantidade = parseInt(produtoDiv.querySelector('.quantidade').textContent);
  
        // Restante do código para armazenar no localStorage...
        const produtoInfo = { nome, valor, quantidade };
        const produtos = JSON.parse(localStorage.getItem('produtos')) || [];
        produtos.push(produtoInfo);
        localStorage.setItem('produtos', JSON.stringify(produtos));
      });
    });
  });