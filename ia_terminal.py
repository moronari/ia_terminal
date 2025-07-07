import os
import google.generativeai as genai
import subprocess
import platform

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
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Detecta o sistema operacional para fornecer comandos mais precisos.
        os_name = platform.system()

        # Prompt de sistema aprimorado para focar o modelo no seu papel de especialista.
        system_instruction = f"""
        Você é um especialista em linha de comando para o sistema operacional '{os_name}'.
        Sua única tarefa é responder com o comando exato para a solicitação do usuário ou explicar um comando.

        REGRAS:
        1.  **SEMPRE** inicie sua resposta com 'Comando:' seguido do comando exato.
        2.  **NÃO** adicione explicações, saudações ou qualquer texto extra, a menos que o usuário peça explicitamente uma explicação.
        3.  Se a solicitação for para explicar um comando, explique-o de forma concisa, mas ainda comece com 'Comando:'.
        4.  Toa pergunta deve ser interpretada no contexto do sistema operacional '{os_name}'.
        5.  Entenda que o seu objetivo é enviar os melhores comandos baseado na solicitação do prompt.
        6.  O comando deve ser o mais direto e idiomático possível para '{os_name}'.

        Exemplos de Solicitação de Comando:
        Usuário: Listar arquivos ocultos.
        Comando: ls -a

        Usuário: Criar um diretório chamado "teste".
        Comando: mkdir teste

        Usuário: Remover um arquivo chamado 'temp.txt'.
        Comando: rm temp.txt

        Usuário: Listar todos os arquivos, incluindo os ocultos, em formato longo.
        Comando: ls -la

        Usuário: criar um novo diretorio chamado 'documentos'
        Comando: mkdir documentos

        Exemplo de Explicação de Comando:
        Usuário: o que o comando 'grep -r "TODO" .' faz?
        Comando: O comando `grep -r "TODO" .` procura recursivamente (-r) pela string "TODO" em todos os arquivos do diretório atual (.).
        """
        full_prompt = f"{system_instruction}\nUsuário: {prompt}\n"
        response = model.generate_content(full_prompt)
        gemini_text = response.text.strip()

        # Tenta identificar se o Gemini sugeriu um comando pela linha "Comando:"
        if gemini_text.startswith("Comando:"):
            command_to_execute = gemini_text.replace("Comando:", "").strip()
            print(f"{Colors.GREEN}Gemini sugeriu o comando: {Colors.YELLOW}{Colors.BOLD}`{command_to_execute}`{Colors.RESET}")
            
            while True:
                confirm_prompt = f"{Colors.MAGENTA}Deseja executar o comando? (s/n/? para ajuda): {Colors.RESET}"
                confirm = input(confirm_prompt).lower()

                if confirm == 's':
                    print(f"{Colors.CYAN}Executando: {Colors.YELLOW}{command_to_execute}{Colors.RESET}")
                    try:
                        # Removido 'capture_output=True' e 'text=True'.
                        # Agora, a saída do comando será exibida diretamente no terminal em tempo real.
                        print(f"\n{Colors.CYAN}--- Início da Saída do Comando ---{Colors.RESET}")
                        subprocess.run(command_to_execute, shell=True, check=True)
                        print(f"{Colors.CYAN}--- Fim da Saída do Comando ---{Colors.RESET}")
                    except subprocess.CalledProcessError as e:
                        # A mensagem de erro do próprio comando já foi exibida no terminal.
                        # Apenas informamos que o comando falhou.
                        print(f"\n{Colors.RED}Erro: O comando terminou com o código de saída {e.returncode}.{Colors.RESET}")
                    except FileNotFoundError:
                        print(f"{Colors.RED}Erro: O comando '{command_to_execute.split()[0]}' não foi encontrado.{Colors.RESET}")
                    break # Sai do loop de confirmação
                elif confirm == 'n':
                    print(f"{Colors.YELLOW}Comando não executado.{Colors.RESET}")
                    break # Sai do loop de confirmação
                elif confirm == '?':
                    print(f"{Colors.CYAN}Solicitando explicação para o Gemini...{Colors.RESET}")
                    explanation_prompt = f"""Você é um instrutor especialista em linha de comando para o sistema operacional '{os_name}'.
Sua tarefa é fornecer uma explicação detalhada, clara e didática para o seguinte comando.
Explique o que cada parte do comando (programa, flags, argumentos) faz. Não execute o comando. Apenas explique.
Comando para explicar: `{command_to_execute}`"""
                    explanation_response = model.generate_content(explanation_prompt)
                    print(f"\n{Colors.CYAN}{Colors.BOLD}--- Explicação do Comando ---{Colors.RESET}")
                    print(explanation_response.text.strip())
                    print(f"{Colors.CYAN}{Colors.BOLD}-----------------------------{Colors.RESET}\n")
                else:
                    print(f"{Colors.RED}Opção inválida. Comando não executado.{Colors.RESET}")
                    break # Sai do loop de confirmação
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