import os
import google.generativeai as genai

# Certifique-se de que sua chave de API esteja configurada como variável de ambiente
# export GOOGLE_API_KEY="SUA_CHAVE_DE_API_AQUI"
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("Erro: A variável de ambiente GOOGLE_API_KEY não está configurada.")
    print("Por favor, defina-a antes de executar este script.")
    exit()

genai.configure(api_key=api_key)

print("Listando modelos disponíveis que suportam 'generateContent':\n")
try:
    for m in genai.list_models():
        # A maioria dos modelos de conversação e geração de texto suportam 'generateContent'
        if 'generateContent' in m.supported_generation_methods:
            print(f"Nome do Modelo: {m.name}")
            print(f"  Display Name: {m.display_name}")
            print(f"  Descrição: {m.description}")
            print(f"  Limites de entrada de tokens: {m.input_token_limit}")
            print(f"  Limites de saída de tokens: {m.output_token_limit}")
            print("-" * 30)
except Exception as e:
    print(f"Ocorreu um erro ao listar os modelos: {e}")
    print("Verifique se sua chave de API está correta e se a API está ativada no Google Cloud Console.")
    print("Também pode ser um problema de região ou permissões.")

print("\nListando todos os modelos disponíveis (incluindo outros métodos):")
try:
    for m in genai.list_models():
        print(f"Nome do Modelo: {m.name}")
        print(f"  Supported Methods: {m.supported_generation_methods}")
        print("-" * 30)
except Exception as e:
    print(f"Ocorreu um erro ao listar todos os modelos: {e}")