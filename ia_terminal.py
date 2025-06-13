import os
import google.generativeai as genai
import subprocess

# --- Constantes de Cores ANSI ---
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

# --- Configuração da API ---
# Configura a chave da API do Gemini
# A chave é lida da variável de ambiente GOOGLE_API_KEY
api_key_env = os.environ.get("GOOGLE_API_KEY")

if api_key_env:
    genai.configure(api_key=api_key_env)
else:
    # A mensagem de erro será impressa no bloco __main__ ou na função se tentarem usar.
    pass # genai.configure não será chamado se a chave não existir

def chat_and_execute_command(prompt):
    """
    Envia um prompt para o modelo Gemini e, se o Gemini sugerir um comando,
    pergunta ao usuário se deve executá-lo.
    """
    if not api_key_env: # Verifica se a chave foi carregada na inicialização do script
        print(f"{Colors.RED}Erro: A variável de ambiente GOOGLE_API_KEY não está configurada.{Colors.RESET}")
        print(f"{Colors.YELLOW}Por favor, execute: export GOOGLE_API_KEY='SUA_CHAVE_DE_API_AQUI'{Colors.RESET}")
        return # Impede a continuação se a chave não estiver configurada

    try:
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        
        # Este é um "prompt de sistema" para guiar o comportamento do Gemini
        # Ele tenta direcionar o Gemini para sugerir comandos quando apropriado
        full_prompt = f"""
Você é um assistente de terminal útil. Quando um usuário pede para realizar uma ação no terminal,
você deve sugerir o comando exato do Linux para realizar essa ação.
**Não execute o comando, apenas o sugira. A sugestão deve começar com 'Comando:'**
Se eu te der um comando, você pode explicá-lo.
Se a pergunta não for sobre comandos do terminal, responda normalmente.

Exemplos:
Usuário: Listar arquivos ocultos.
Comando: ls -a

Usuário: Criar um diretório chamado "teste".
Comando: mkdir teste

Usuário: Remover um arquivo chamado 'temp.txt'.
Comando: rm temp.txt

Usuário: {prompt}
"""
        response = model.generate_content(full_prompt)
        gemini_text = response.text.strip()

        # Tenta identificar se o Gemini sugeriu um comando pela linha "Comando:"
        if gemini_text.startswith("Comando:"):
            command_to_execute = gemini_text.replace("Comando:", "").strip()
            print(f"{Colors.GREEN}Gemini sugeriu o comando: {Colors.YELLOW}{Colors.BOLD}`{command_to_execute}`{Colors.RESET}")
            
            confirm_prompt = f"{Colors.MAGENTA}Deseja executar este comando? (s/n): {Colors.RESET}"
            confirm = input(confirm_prompt).lower()

            if confirm == 's':
                print(f"{Colors.CYAN}Executando: {Colors.YELLOW}{command_to_execute}{Colors.RESET}")
                try:
                    # Usar subprocess.run é mais seguro que os.system
                    # shell=True permite a execução de comandos complexos com pipes e redirecionamentos
                    # mas aumenta o risco se a entrada não for confiável. Use com cautela.
                    result = subprocess.run(command_to_execute, shell=True, capture_output=True, text=True, check=True)
                    print(f"\n{Colors.BOLD}Saída do comando:{Colors.RESET}")
                    print(result.stdout)
                    if result.stderr:
                        print(f"{Colors.RED}{Colors.BOLD}Erros (stderr):{Colors.RESET}")
                        print(result.stderr)
                except subprocess.CalledProcessError as e:
                    print(f"{Colors.RED}Erro ao executar o comando (código de saída {e.returncode}):{Colors.RESET}")
                    if e.stdout:
                        print(f"{Colors.BOLD}Saída (stdout):{Colors.RESET}\n{e.stdout}")
                    if e.stderr:
                        print(f"{Colors.RED}{Colors.BOLD}Erros (stderr):{Colors.RESET}\n{e.stderr}")
                except FileNotFoundError:
                    print(f"{Colors.RED}Erro: O comando '{command_to_execute.split()[0]}' não foi encontrado.{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}Comando não executado.{Colors.RESET}")
        else:
            # Se o Gemini não sugeriu um comando, imprime a resposta normal
            print(f"{Colors.GREEN}Gemini: {gemini_text}{Colors.RESET}")
        
    except Exception as e:
        print(f"{Colors.RED}Ocorreu um erro inesperado: {e}{Colors.RESET}")

if __name__ == "__main__":
    if not api_key_env:
        # Esta mensagem será mostrada se o script for executado diretamente sem a chave API.
        print(f"{Colors.RED}Erro crítico: A variável de ambiente GOOGLE_API_KEY não está configurada.{Colors.RESET}")
        print(f"{Colors.YELLOW}Por favor, defina-a antes de executar o script.{Colors.RESET}")
        exit(1) # Encerra o script se a chave não estiver disponível.

    print(f"{Colors.CYAN}{Colors.BOLD}Bem-vindo ao Gemini Terminal Assistant!{Colors.RESET}")
    print(f"{Colors.CYAN}Digite '{Colors.RED}sair{Colors.CYAN}' para encerrar a conversa.{Colors.RESET}")
    print(f"{Colors.CYAN}Experimente perguntar: '{Colors.GREEN}Como eu listo os arquivos na pasta atual?{Colors.CYAN}'{Colors.RESET}")
    print("-" * 50)

    while True:
        user_input = input(f"{Colors.BLUE}{Colors.BOLD}Você: {Colors.RESET}")
        if user_input.lower() == 'sair':
            print(f"{Colors.CYAN}Encerrando o assistente. Até mais!{Colors.RESET}")
            break
        
        chat_and_execute_command(user_input)