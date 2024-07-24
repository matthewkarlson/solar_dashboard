import plotly.express as px

def get_bar_chart(df, x, y):
    fig = px.bar(df, x= 'datetime' , y= 'Revenue (Invoiced)')
    return fig
