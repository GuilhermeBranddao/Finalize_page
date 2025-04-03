# Função para classificar ativos
def classify_asset(asset: str) -> str:
    if asset.endswith('11.SA'):
        return 'FII'
    elif asset.endswith('3.SA'):
        return 'Ação'
    elif asset.endswith('4.SA'):
        return 'Ação Preferencial'
    return 'Outro'