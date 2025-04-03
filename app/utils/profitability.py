import pandas as pd
import calendar
import plotly.express as px

def calculate_historical_profitability(df_history:pd.DataFrame, asset:list=None):
    if not isinstance(df_history, pd.DataFrame):
        raise ValueError("O parâmetro 'df' deve ser um pandas DataFrame.")

    # Verificar colunas obrigatórias
    required_columns = {"date", "close", "asset_name"}
    if not required_columns.issubset(df_history.columns):
        raise ValueError(f"O DataFrame deve conter as colunas: {required_columns}")

    # Filtrar por ativo, se especificado
    if asset:
        df_history = df_history[df_history['asset_name'] == asset].copy()
        if df_history.empty:
            raise ValueError(f"Nenhum dado encontrado para o ativo '{asset}'.")

    # Converter 'date' para datetime e ordenar
    df_history["date"] = pd.to_datetime(df_history["date"])
    df_history.sort_values(by="date", inplace=True)

    # Adicionar colunas de ano e mês
    df_history["year"] = df_history["date"].dt.year
    df_history["month"] = df_history["date"].dt.month

    # Agrupar para calcular os valores inicial e final do mês
    grouped = df_history.groupby(["year", "month", "asset_name"])
    profitability = grouped["close"].agg(
        value_beginning="first",
        value_end="last"
    ).reset_index()

    # Calcular o fechamento do mês anterior
    profitability["previous_end"] = profitability.groupby("asset_name")["value_end"].shift(1)

    # Calcular rentabilidade percentual e diferença em valores
    profitability["monthly_return"] = (
        (profitability["value_end"] - profitability["previous_end"]) / profitability["previous_end"] * 100
    )
    profitability["value_diff"] = profitability["value_end"] - profitability["previous_end"]

    # Remover linhas sem dados do mês anterior
    profitability.dropna(subset=["previous_end"], inplace=True)

    return profitability


def calcular_rentabilidade_mensal(df_history:pd.DataFrame, asset:list=None):
    """
    Calcula a rentabilidade mensal de um ativo ou de todos os ativos no DataFrame.

    Args:
        df (pd.DataFrame): DataFrame com colunas 'date', 'close', e 'asset_name'.
        asset (str, opcional): Nome do ativo a ser filtrado. Se None, considera todos os ativos.

    Returns:
        pd.DataFrame: DataFrame pivotado com a rentabilidade mensal média por ano.
    """
    
    profitability = calculate_historical_profitability(df_history=df_history, asset=asset)

    # Agrupar por ano e mês para calcular as médias
    resumo = profitability.groupby(["year", "month"]).agg(
        avg_monthly_return=("monthly_return", "mean"),
        avg_value_diff=("value_diff", "mean")
    ).reset_index()

    # Arredondar valores
    resumo["avg_monthly_return"] = resumo["avg_monthly_return"].round(2)
    resumo["avg_value_diff"] = resumo["avg_value_diff"].round(2)

    # Criar DataFrame pivotado
    df_pivot = resumo.pivot(index="year", columns="month", values="avg_monthly_return")
    df_pivot.columns = [calendar.month_abbr[month] for month in df_pivot.columns]
    df_pivot = df_pivot.fillna("-") 
    df_pivot.reset_index(inplace=True)

    return df_pivot

#calcular_rentabilidade_mensal(df_historico_dividendos)