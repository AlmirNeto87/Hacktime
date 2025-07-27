import streamlit as st
from fpdf import FPDF
import datetime
from io import BytesIO
import time

# Configurar a página
st.set_page_config(page_title="PDV Geek", page_icon="🕹️", layout="wide")



# Exibe tela de carregamento apenas na primeira vez
if "loaded" not in st.session_state:
    st.session_state.loaded = False

if not st.session_state.loaded:
    st.markdown("""
        <style>
        .loader-container {
            position: fixed;
            top: 0; left: 0;
            width: 100vw;
            height: 100vh;
            background-color: #000;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            animation: fadeOut 2s ease-out 2.5s forwards;
        }

        .loader-text {
            color: #00ffcc;
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            animation: blink 1s infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }

        @keyframes fadeOut {
            to { opacity: 0; visibility: hidden; }
        }
        </style>

        <div class="loader-container">
            <div class="loader-text">👾 Press Start...</div>
        </div>
    """, unsafe_allow_html=True)

    time.sleep(3)  # Espera antes de carregar o conteúdo
    st.session_state.loaded = True
    st.rerun()




# CSS: Fonte Orbitron, fundo e responsividade
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

        html, body {{
            height: 100%;
            margin: 0;
            padding: 0;
            font-family: 'Orbitron', sans-serif;
            animation: fadeIn 1s ease-in;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}


        /* Botões de adicionar produto */
        button[kind="secondary"] {{
            transition: all 0.3s ease;
            border-radius: 8px !important;
        }}

        button[kind="secondary"]:hover {{
            background-color: #7209b7 !important;
            color: white !important;
            transform: scale(1.05);
            box-shadow: 0px 0px 8px rgba(114, 9, 183, 0.6);
        }}

        /* Para botão padrão também */
        .stButton > button {{
            transition: all 0.3s ease;
        }}

        .stButton > button:hover {{
            background-color: #560bad !important;
            color: white !important;
            transform: scale(1.05);
            box-shadow: 0 0 8px rgba(86, 11, 173, 0.4);
        }}
    </style>
""", unsafe_allow_html=True)


# Sessão
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []
if "total" not in st.session_state:
    st.session_state.total = 0.0
if "zoom_imagem" not in st.session_state:
    st.session_state.zoom_imagem = None

# Lista de produtos (simples e fixa por agora)
produtos = [
    {
        "nome": "Camisa Strage Thigs",
        "preco": 59.90,
        "imagem": "images/camisa.png"
    },
    {
        "nome": "Camisa Star-wars",
        "preco": 79.90,
        "imagem": "images/camisa1.png"
    },
    {
        "nome": "Camisa Video-Game",
        "preco": 49.90,
        "imagem": "images/camisa2.png"
    },
        {
        "nome": "Camisa Dragon Ball",
        "preco": 69.90,
        "imagem": "images/camisa4.png"
    },
        {
        "nome": "Camisa He-man",
        "preco": 49.90,
        "imagem": "images/camisa5.png"
    },
        {
        "nome": "Camisa Star-Wars",
        "preco": 49.90,
        "imagem": "images/camisa6.png"
    },
        {
        "nome": "Camisa AnimeStar-wars",
        "preco": 49.90,
        "imagem": "images/camisa7.png"
    },
        {
        "nome": "Camisa Cultura Anime- Geek",
        "preco": 49.90,
        "imagem": "images/camisa8.png"
    },
    {
        "nome": "Camisa Draon Ball - He-man ",
        "preco": 49.90,
        "imagem": "images/camisa9.png"
    },
]

# Menu topo
aba = st.radio("Navegação", ["🏪 Catálogo", "🛒 Carrinho"], horizontal=True, label_visibility="collapsed")

# Zoom
def exibir_zoom(imagem_path, nome):
    st.markdown("---")
    st.markdown(f"### 🔍 Zoom - {nome}")
    st.image(imagem_path, use_column_width=True)
    st.button("Fechar Zoom", on_click=lambda: st.session_state.update({"zoom_imagem": None}))
def gerar_recibo():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Recibo de Compra - Geek Store", ln=True, align='C')

    pdf.set_font('Arial', '', 12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=True)
    pdf.ln(10)

    for item in st.session_state.carrinho:
        pdf.cell(200, 10, txt=f"{item['nome']} - R$ {item['preco']:.2f}", ln=True)

    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, txt=f"Total: R$ {st.session_state.total:.2f}", ln=True)

    # Gera PDF como string binária e converte em BytesIO
    pdf_bin = pdf.output(dest='S').encode('latin-1')
    buffer = BytesIO(pdf_bin)
    return buffer


# Catálogo
if aba == "🏪 Catálogo":
    st.markdown("<h1 style='text-align: center; color: #f72585;'>🕹️ Geek Store - Catálogo</h1>", unsafe_allow_html=True)
    cols = st.columns(3)

    for idx, produto in enumerate(produtos):
        with cols[idx % 3]:
            st.image(produto["imagem"], width=200)
            st.markdown(f"**{produto['nome']}**")
            st.markdown(f"💵 R$ {produto['preco']:.2f}")
            col_add, col_zoom = st.columns([1, 1])
            with col_add:
                if st.button(f"🛒 Adicionar", key=f"add_{idx}"):
                    st.session_state.carrinho.append(produto)
                    st.session_state.total += produto["preco"]
                    st.success(f"{produto['nome']} adicionado!")
            with col_zoom:
                if st.button(f"🔍 Zoom", key=f"zoom_{idx}"):
                    st.session_state.zoom_imagem = produto

    if st.session_state.zoom_imagem:
        exibir_zoom(
            st.session_state.zoom_imagem["imagem"],
            st.session_state.zoom_imagem["nome"]
        )

# Carrinho
elif aba == "🛒 Carrinho":
    st.markdown("<h1 style='color: #f72585;'>🛒 Carrinho de Compras</h1>", unsafe_allow_html=True)

    if st.session_state.carrinho:
        for idx, item in enumerate(st.session_state.carrinho):
            col1, col2, col3 = st.columns([5, 2, 1])
            with col1:
                st.write(f"**{item['nome']}** - R$ {item['preco']:.2f}")
            with col2:
                st.image(item["imagem"], width=80)
            with col3:
                if st.button("❌", key=f"remove_{idx}"):
                    st.session_state.total -= item["preco"]
                    st.session_state.carrinho.pop(idx)
                    st.rerun()

        st.markdown(f"### 💰 Total: R$ {st.session_state.total:.2f}")

        if st.button("✅ Finalizar Venda"):
            recibo = gerar_recibo()
            st.success("Venda finalizada com sucesso!")
            st.download_button(
                label="📄 Baixar Recibo em PDF",
                data=recibo,
                file_name="recibo_geek_store.pdf",
                mime="application/pdf"
            )
            st.session_state.carrinho = []
            st.session_state.total = 0.0
    else:
        st.info("Carrinho está vazio.")

# Rodapé
st.markdown("""
    <div style="text-align: center; padding: 20px; background-color: #1f1f1f; color: white; margin-top: 2rem;">
        <p>Todos os direitos reservados Geek Store 2025</p>
    </div>
""", unsafe_allow_html=True)
