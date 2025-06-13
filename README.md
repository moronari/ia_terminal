# Gemini Terminal Assistant

Este é um projeto simples em Python que demonstra como interagir com a API do Google Gemini para criar um assistente de terminal. Ele permite que o usuário converse com o Gemini e, com permissão explícita, execute comandos sugeridos pelo modelo diretamente no terminal.

## ⚠️ Aviso de Segurança Importante ⚠️

A execução de comandos gerados por um modelo de IA diretamente no seu sistema pode ser **extremamente perigosa** e levar a perda de dados ou comprometimento do sistema. Este projeto é para fins **educacionais e de demonstração**. Sempre revise e compreenda qualquer comando antes de permitir sua execução.

## Funcionalidades

-   Conversa interativa com o modelo Gemini.
-   Sugere comandos Linux com base nas perguntas do usuário.
-   Solicita confirmação antes de executar qualquer comando sugerido.
-   Exibe a saída e os erros dos comandos executados.

## Pré-requisitos

-   Python 3.x
-   `pip` (gerenciador de pacotes do Python)
-   Uma conta no [Google Cloud](https://console.cloud.google.com/)
-   Uma chave de API da "Generative Language API" (Gemini API)

## Configuração

1.  **Clone o repositório (ou baixe os arquivos):**
    ```bash
    git clone [https://github.com/moronari/ia_terminal.git](https://github.com/moronari/ia_terminal.git)
    cd ia_terminal
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install google-generativeai
    ```
4.  **Obtenha sua Chave de API do Gemini:**
    -   Vá para o [Google Cloud Console](https://console.cloud.google.com/).
    -   Crie ou selecione um projeto.
    -   Vá em "APIs e Serviços" > "Biblioteca", procure por "Generative Language API" e ative-a.
    -   Vá em "APIs e Serviços" > "Credenciais", clique em "Criar Credenciais" > "Chave de API".
    -   **Copie sua chave de API!**
5.  **Configure a Chave de API como uma variável de ambiente:**
    **IMPORTANTE:** Nunca coloque sua chave de API diretamente no código ou faça upload dela para o GitHub!
    ```bash
    export GOOGLE_API_KEY="SUA_CHAVE_DE_API_AQUI"
    ```
    Para que a variável seja persistente, adicione a linha acima ao seu `~/.bashrc` ou `~/.zshrc` e execute `source ~/.bashrc`.

## Como Usar

Com o ambiente virtual ativado e a chave de API configurada, execute o script:

```bash
python ia_terminal.py
