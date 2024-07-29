import plotly.express as px
import plotly.graph_objects as go

def display_custom_block(title, col):
    html_content = f"""
    <div style = "text-align: center; border: 3px solid lightgreen; border-radius: 10px;">
        <h3>{title}</h3>
    </div>
    """
    col.markdown(html_content, unsafe_allow_html=True)



def get_bar_chart(df, x, y, title):
    fig = px.bar(df, x= x , y=y)
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title='Revenue',
        xaxis_tickangle=-45
    )
    fig.update_traces(marker_color='lightgreen')
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
def get_line_chart(df, x, y, title):
    fig = px.line(df, x= x , y=y)
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title='Revenue',
        xaxis_tickangle=-45
    )
    return fig
