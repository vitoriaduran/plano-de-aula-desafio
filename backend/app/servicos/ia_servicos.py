from groq import Groq
import os
import json
import re
from dotenv import load_dotenv

class IAServico:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv('GROQ_API_KEY')

        if not api_key:
            print("ERRO: A chave GROQ_API_KEY não foi encontrada no .env")

        self.client = Groq(
            api_key=os.getenv('GROQ_API_KEY')
        )

    def gerar_sugestao_aula(self, titulo, disciplina, ementa=""):
        contexto_extra = f"Use como base esta ementa: {ementa}" if ementa else ""

        prompt = f"""
        Atue como um Assistente Pedagógico.
        Gere sugestões para um plano de aula sobre "{titulo}" na disciplina de "{disciplina}".
        {contexto_extra}
        Responda APENAS com JSON puro no formato:
        {{
            "objetivo": "texto",
            "ementa": "texto",
            "conteudos": "texto",
            "recursos": "texto",
            "tags": ["tag1", "tag2", "tag3"]
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            texto = response.choices[0].message.content
            texto_limpo = re.sub(r"```(?:json)?", "", texto)

            texto_limpo = texto_limpo.replace("```", "").strip()

            try:
                dados = json.loads(texto_limpo)
            except json.JSONDecodeError:
                return {
                    "erro": "A IA retornou um formato inesperado. Tente novamente",
                    "resposta_bruta": texto_limpo[:200]
                }

            chaves_esperadas = ["objetivo", "ementa", "conteudos", "recursos", "tags"]
            for chave in chaves_esperadas:
                if chave not in dados:
                    dados[chave] = ""
            return dados

        except Exception as e:
            return {"erro": f"Erro ao consultar a IA: {str(e)}"}