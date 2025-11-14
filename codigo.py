import random
import pandas as pd

# =========================================
# 1. GERANDO DADOS DE COMPRAS (FICTÍCIOS)
# =========================================
clientes = ["Ana", "Bruno", "Carla", "Daniel", "Eva"]
produtos = ["xpto", "notebook", "teclado", "monitor", "cadeira"]

compras = []
for i in range(10):
    compras.append({
        "cliente": random.choice(clientes),
        "produto": random.choice(produtos)
    })

df = pd.DataFrame(compras)
print("\n=== Compras Originais (Identificáveis) ===")
print(df)

# =========================================
# 2. Associação original
# =========================================
def clientes_por_produto_original(df):
    mapping = {}
    for prod in df["produto"].unique():
        mapping[prod] = df[df["produto"] == prod]["cliente"].unique().tolist()
    return mapping

print("\n=== Associação direta produto -> clientes (risco de identificação) ===")
print(clientes_por_produto_original(df))


# =========================================
# 3. PRIVATIZAÇÃO COM K-ANONYMITY E RUÍDO
# =========================================
def privatizar_dados(df, k=3):
    df_priv = df.copy()

    df_priv["anon_id"] = [f"user_{i}" for i in range(len(df_priv))]
    random.shuffle(df_priv["anon_id"].values)

    df_priv = df_priv.drop(columns=["cliente"])

    counts = df_priv["produto"].value_counts()

    for produto, count in counts.items():
        if count < k:
            faltam = k - count
            for _ in range(faltam):
                df_priv.loc[len(df_priv)] = {
                    "produto": produto,
                    "anon_id": f"user_fake_{random.randint(1000,9999)}"
                }

    return df_priv

df_priv = privatizar_dados(df, k=3)

print("\n=== Dados após PRIVATIZAÇÃO ===")
print(df_priv)


# =========================================
# 4. Associação anônima
# =========================================
def clientes_por_produto_anon(df):
    mapping = {}
    for prod in df["produto"].unique():
        mapping[prod] = df[df["produto"] == prod]["anon_id"].unique().tolist()
    return mapping

print("\n=== Novo mapeamento produto -> IDs anônimos ===")
print(clientes_por_produto_anon(df_priv))


# =========================================
# 5. MÉTODO: BUSCA POR PERFIL
# =========================================
def buscar_coincidencias(df, perfil):
    """
    df: dataframe (original ou anonimizado)
    perfil: dict com características, ex: {"produto": "xpto"}
    """

    filtro = df.copy()

    for chave, valor in perfil.items():
        if chave not in df.columns:
            print(f"Campo '{chave}' não existe no conjunto de dados.")
            return 0
        
        filtro = filtro[filtro[chave] == valor]

    return len(filtro)


# =========================================
# 6. TESTAR A BUSCA POR PERFIL
# =========================================

perfil_teste = {"produto": "teclado"}
print("\n=== Testando busca de perfil (dados anônimos) ===")
print(f"Perfis encontrados: {buscar_coincidencias(df_priv, perfil_teste)}")
