from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# Configurações do Supabase enviadas por você
SUPABASE_URL = "https://dxzudxyrarhnshhkfcxx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR4enVkeHlyYXJobnNoaGtmY3h4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzcxNTY2OTAsImV4cCI6MjA5MjczMjY5MH0._3K9HX9Na0m6JaWeKpgSGEIz6kqEG_mB3ozFmWNDca8"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resgatar', methods=['POST'])
def resgatar():
    data = request.json
    key_digitada = data.get('key')
    
    # Busca a key no banco
    response = supabase.table("keys_promocionais").select("*").eq("chave", key_digitada).eq("usada", False).execute()
    
    if len(response.data) > 0:
        # Marca como usada
        supabase.table("keys_promocionais").update({"usada": True}).eq("chave", key_digitada).execute()
        return jsonify({"success": True, "livro": response.data[0]['livro_nome']})
    
    return jsonify({"success": False, "message": "Chave inválida, expirada ou já utilizada."})

if __name__ == '__main__':
    app.run(debug=True)