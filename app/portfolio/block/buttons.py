import streamlit as st
from app.portfolio.dialog.nova_carteira import nova_carteira
from app.portfolio.dialog.delete_wallet import delete_wallet

def render_choose_wallet_buttons(wallets):
    """Renderiza os botões das carteiras."""
    for wallet in wallets:
        wallet_name = wallet.get("name", "Carteira Sem Nome")
        wallet_id = wallet.get("id")

        BUTTON_COLS_RATIO = [3, 1, 1]  # Coluna principal, link e configurações
        col1, col2, col3 = st.columns(BUTTON_COLS_RATIO)
        with col1:
            if st.button(wallet_name, key=f"wallet_{wallet_id}"):
                st.session_state.wallet_id = wallet_id
                st.rerun()  # Evite 'st.rerun()' depreciado
        with col2:
            st.button("🔗", key=f"link_{wallet_id}")  # Placeholder
        with col3:
            if st.button("⚙️", key=f"config_{wallet_id}"):  # Placeholder
                delete_wallet(wallet_id)
            
    if st.button("Criar Nova Carteira", key="new_wallet"):
        nova_carteira()