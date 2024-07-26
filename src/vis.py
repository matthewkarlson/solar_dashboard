import plotly.express as px
import plotly.graph_objects as go
def get_bar_chart(df, x, y):
    fig = px.bar(df, x= x , y=y)
    return fig

def get_comparison_chart(df, x, y1, y2, title):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df[x],
        y=df[y1],
        name=y1,
        marker_color = 'darkgreen'
    ))

    fig.add_trace(go.Bar(
        x=df[x],
        y=df[y2],
        name=y2,
        marker_color = 'lightgreen'
    ))

    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title='Revenue',
        barmode='group',
        xaxis_tickangle=-45
    )
    return fig