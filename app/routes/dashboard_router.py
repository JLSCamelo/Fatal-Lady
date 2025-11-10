# CODIGO NAO ESTA COMPLETO - NECESSITA MELHORIAS VISUAIS


from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")


@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    
    # vendas
    query_vendas = "SELECT data, valortotal FROM pedidos"
    df_vendas = pd.read_sql(query_vendas, db.bind)
    df_vendas["data"] = pd.to_datetime(df_vendas["data"])
    
    # produtos mais vendidos
    query_produtos = """
        SELECT p.nome, SUM(i.quantidade) AS total_vendido
        FROM itens_pedido i
        JOIN produtos p ON i.produto_id = p.id_produto
        GROUP BY p.nome
        ORDER BY total_vendido DESC
        LIMIT 5
    """
    df_produtos = pd.read_sql(query_produtos, db.bind)
    
    # vendas por categoria
    query_categoria = """
        SELECT c.nome AS categoria, SUM(i.quantidade * i.preco_unitario) AS total_categoria
        FROM itens_pedido i
        JOIN produtos p ON i.produto_id = p.id_produto
        JOIN categoria c ON p.id_categoria = c.id
        GROUP BY c.nome
    """
    df_categoria = pd.read_sql(query_categoria, db.bind)
    
    # vendas por fabricante
    query_fabricante = """
        SELECT f.nome AS fabricante, SUM(i.quantidade * i.preco_unitario) AS total_fabricante
        FROM itens_pedido i
        JOIN produtos p ON i.produto_id = p.id_produto
        JOIN fabricantes f ON p.id_fabricante = f.id
        GROUP BY f.nome
    """
    df_fabricante = pd.read_sql(query_fabricante, db.bind)
    
    # métodos de pagamento
    query_pagamento = """
        SELECT metodopagamento, COUNT(*) AS total
        FROM pagamentos
        GROUP BY metodopagamento
    """
    df_pagamento = pd.read_sql(query_pagamento, db.bind)
    
    # avaliações
    query_avaliacoes = """
        SELECT p.nome, AVG(a.nota) AS media_nota
        FROM avaliacoes a
        JOIN produtos p ON a.id_produto = p.id_produto
        GROUP BY p.nome
        ORDER BY media_nota DESC
    """
    df_avaliacoes = pd.read_sql(query_avaliacoes, db.bind)
    
    # total de produtos
    query_total_produtos = "SELECT COUNT(*) as total FROM produtos"
    df_total_produtos = pd.read_sql(query_total_produtos, db.bind)







    # cálculos
    total_revenue = float(df_vendas["valortotal"].sum()) if not df_vendas.empty else 0
    total_orders = len(df_vendas)
    total_products = int(df_total_produtos["total"].iloc[0]) if not df_total_produtos.empty else 0
    avg_rating = float(df_avaliacoes["media_nota"].mean()) if not df_avaliacoes.empty else 0



    # gráficos e costumização

    colors = {
        'primary': '#6366f1',
        'secondary': '#8b5cf6',
        'success': '#10b981',
        'warning': '#f59e0b',
        'danger': '#ef4444',
        'background': '#1e293b',
        'text': '#e2e8f0'
    }
    
    # layout padrão p/ todos os gráficos
    default_layout = dict(
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        font=dict(color=colors['text'], family='Inter, sans-serif'),
        margin=dict(t=80, b=60, l=60, r=40),
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )






    # FATURAMENTO MENSAL --------------------------------
    vendas_mensais = (
        df_vendas.groupby(df_vendas["data"].dt.to_period("M"))["valortotal"]
        .sum()
        .reset_index()
    )
    vendas_mensais["data"] = vendas_mensais["data"].astype(str)
    
    fig_vendas = go.Figure()
    fig_vendas.add_trace(go.Scatter(
        x=vendas_mensais["data"],
        y=vendas_mensais["valortotal"],
        mode='lines+markers',
        name='Faturamento',
        line=dict(color=colors['primary'], width=3),
        marker=dict(size=10, color=colors['secondary']),
        fill='tonexty',
        fillcolor='rgba(99, 102, 241, 0.1)'
    ))
    fig_vendas.update_layout(
        **default_layout,
        title=dict(text='📅 Faturamento Mensal (R$)', font=dict(size=20)),
        xaxis_title='Período',
        yaxis_title='Valor Total (R$)',
        xaxis=dict(gridcolor='#334155'),
        yaxis=dict(gridcolor='#334155', tickformat=',.2f')
    )
    grafico_vendas = fig_vendas.to_html(full_html=False, include_plotlyjs="cdn", config={'displayModeBar': True})

    # TOP 5 PRODUTOS -----------------------------------------
    fig_produtos = go.Figure()
    fig_produtos.add_trace(go.Bar(
        x=df_produtos["total_vendido"],
        y=df_produtos["nome"],
        orientation='h',
        marker=dict(
            color=df_produtos["total_vendido"],
            colorscale=[[0, colors['primary']], [1, colors['secondary']]],
            line=dict(width=0)
        ),
        text=df_produtos["total_vendido"],
        textposition='auto'
    ))
    fig_produtos.update_layout(
        **default_layout,
        title=dict(text='🛍️ Top 5 Produtos Mais Vendidos', font=dict(size=20)),
        xaxis_title='Quantidade Vendida',
        yaxis_title='Produto',
        xaxis=dict(gridcolor='#334155'),
        yaxis=dict(gridcolor='#334155')
    )
    grafico_produtos = fig_produtos.to_html(full_html=False, include_plotlyjs=False)

    # VENDAS POR CATEGORIA --------------------------------------------
    fig_categoria = go.Figure()
    fig_categoria.add_trace(go.Pie(
        labels=df_categoria["categoria"],
        values=df_categoria["total_categoria"],
        hole=0.4,
        marker=dict(
            colors=[colors['primary'], colors['secondary'], colors['success'], 
                   colors['warning'], colors['danger']],
            line=dict(color=colors['background'], width=2)
        ),
        textinfo='label+percent',
        textfont=dict(size=14)
    ))
    fig_categoria.update_layout(
        **default_layout,
        title=dict(text='🏷️ Distribuição de Vendas por Categoria', font=dict(size=20)),
    )
    grafico_categoria = fig_categoria.to_html(full_html=False, include_plotlyjs=False)

    # VENDAS POR FABRICANTE ----------------------------------------------
    fig_fabricante = go.Figure()
    fig_fabricante.add_trace(go.Bar(
        x=df_fabricante["fabricante"],
        y=df_fabricante["total_fabricante"],
        marker=dict(
            color=df_fabricante["total_fabricante"],
            colorscale=[[0, colors['success']], [1, colors['primary']]],
            line=dict(width=0)
        ),
        text=df_fabricante["total_fabricante"].apply(lambda x: f'R$ {x:,.2f}'),
        textposition='outside'
    ))
    fig_fabricante.update_layout(
        **default_layout,
        title=dict(text='🏭 Vendas por Fabricante', font=dict(size=20)),
        xaxis_title='Fabricante',
        yaxis_title='Total de Vendas (R$)',
        xaxis=dict(gridcolor='#334155'),
        yaxis=dict(gridcolor='#334155', tickformat=',.2f')
    )
    grafico_fabricante = fig_fabricante.to_html(full_html=False, include_plotlyjs=False)

    # PAGAMENTOS -----------------------------------------------
    fig_pagamento = go.Figure()
    fig_pagamento.add_trace(go.Bar(
        x=df_pagamento["total"],
        y=df_pagamento["metodopagamento"],
        orientation='h',
        marker=dict(
            color=[colors['primary'], colors['secondary'], colors['success'], colors['warning']],
            line=dict(width=0)
        ),
        text=df_pagamento["total"],
        textposition='auto'
    ))
    fig_pagamento.update_layout(
        **default_layout,
        title=dict(text='💳 Métodos de Pagamento Mais Utilizados', font=dict(size=20)),
        xaxis_title='Quantidade de Transações',
        yaxis_title='Método de Pagamento',
        xaxis=dict(gridcolor='#334155'),
        yaxis=dict(gridcolor='#334155')
    )
    grafico_pagamento = fig_pagamento.to_html(full_html=False, include_plotlyjs=False)

    # AVALIAÇÕES -----------------------------------------
    fig_avaliacoes = go.Figure()
    fig_avaliacoes.add_trace(go.Bar(
        x=df_avaliacoes["nome"],
        y=df_avaliacoes["media_nota"],
        marker=dict(
            color=df_avaliacoes["media_nota"],
            colorscale=[[0, colors['danger']], [0.5, colors['warning']], [1, colors['success']]],
            line=dict(width=0),
            cmin=0,
            cmax=5
        ),
        text=df_avaliacoes["media_nota"].apply(lambda x: f'{x:.1f}'),
        textposition='outside'
    ))
    fig_avaliacoes.update_layout(
        **default_layout,
        title=dict(text='⭐ Avaliação Média por Produto', font=dict(size=20)),
        xaxis_title='Produto',
        yaxis_title='Nota Média',
        xaxis=dict(gridcolor='#334155'),
        yaxis=dict(gridcolor='#334155', range=[0, 5])
    )
    grafico_avaliacoes = fig_avaliacoes.to_html(full_html=False, include_plotlyjs=False)

    # LISTA DE CATEGORIAS FILTRO ----------------------------------
    categorias_list = df_categoria["categoria"].tolist() if not df_categoria.empty else []


    # RENDERIZAR TEMPLATE ----------------------------------
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "grafico_vendas": grafico_vendas,
            "grafico_produtos": grafico_produtos,
            "grafico_categoria": grafico_categoria,
            "grafico_fabricante": grafico_fabricante,
            "grafico_pagamento": grafico_pagamento,
            "grafico_avaliacoes": grafico_avaliacoes,
            "total_revenue": f"{total_revenue:,.2f}",
            "total_orders": total_orders,
            "total_products": total_products,
            "avg_rating": f"{avg_rating:.1f}",
            "categorias": categorias_list
        },
    )







