import os
import google.generativeai as genai
import subprocess

# Configura a chave da API do Gemini
# A chave é lida da variável de ambiente GOOGLE_API_KEY
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def chat_and_execute_command(prompt):
    """
    Envia um prompt para o modelo Gemini e, se o Gemini sugerir um comando,
    pergunta ao usuário se deve executá-lo.
    """
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Erro: A variável de ambiente GOOGLE_API_KEY não está configurada.")
        print("Por favor, execute: export GOOGLE_API_KEY='SUA_CHAVE_DE_API_AQUI'")
        return

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
            print(f"Gemini sugeriu o comando: `{command_to_execute}`")
            
            confirm = input("Deseja executar este comando? (s/n): ").lower()
            if confirm == 's':
                print(f"Executando: {command_to_execute}")
                try:
                    # Usar subprocess.run é mais seguro que os.system
                    # shell=True permite a execução de comandos complexos com pipes e redirecionamentos
                    # mas aumenta o risco se a entrada não for confiável. Use com cautela.
                    result = subprocess.run(command_to_execute, shell=True, capture_output=True, text=True, check=True)
                    print("\nSaída do comando:")
                    print(result.stdout)
                    if result.stderr:
                        print("Erros (stderr):")
                        print(result.stderr)
                except subprocess.CalledProcessError as e:
                    print(f"Erro ao executar o comando (código de saída {e.returncode}):")
                    print(f"Saída (stdout): {e.stdout}")
                    print(f"Erros (stderr): {e.stderr}")
                except FileNotFoundError:
                    print(f"Erro: O comando '{command_to_execute.split()[0]}' não foi encontrado.")
            else:
                print("Comando não executado.")
        else:
            # Se o Gemini não sugeriu um comando, imprime a resposta normal
            print(f"Gemini: {gemini_text}")
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    print("Bem-vindo ao Gemini Terminal Assistant!")
    print("Digite 'sair' para encerrar a conversa.")
    print("Experimente perguntar: 'Como eu listo os arquivos na pasta atual?'")

    while True:
        user_input = input("Você: ")
        if user_input.lower() == 'sair':
            print("Encerrando o assistente. Até mais!")
            break
        
        chat_and_execute_command(user_input)