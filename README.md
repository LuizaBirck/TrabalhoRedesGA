# TrabalhoRedesGA
Sistema de sincronização de arquivos P2P usando UDP

# Sistema de Sincronização de Arquivos P2P

Este projeto implementa um sistema de atualização de arquivos distribuídos com múltiplos nodos (peers) utilizando o protocolo UDP em Python.

# Descrição

O sistema permite a sincronização automática de arquivos entre diferentes nodos em uma rede. Cada nodo funciona simultaneamente como cliente e servidor, detectando alterações em sua pasta local e propagando essas alterações para os outros nodos da rede.

# Funcionalidades

- Detecção automática de novos arquivos
- Sincronização de arquivos entre múltiplos nodos
- Detecção e propagação de remoção de arquivos
- Suporte para execução em diferentes ambientes (mesmo computador ou computadores diferentes)

# Como executar

1. Clone este repositório
2. Execute um nodo com o comando: python3 nodo.py <id_do_nodo>
Onde <id_do_nodo> pode ser 1, 2 ou 3 (ou 4 no teste de adição de peer)

# Configuração

A configuração dos nodos é feita através do dicionário `NODES_CONFIG` no início do arquivo `nodo.py`. Para executar em um único computador, use IPs localhost (127.0.0.1). Para executar em computadores diferentes, substitua pelos IPs reais das máquinas.

# Desenvolvido para

Trabalho Prático da disciplina de Redes de Computadores.
