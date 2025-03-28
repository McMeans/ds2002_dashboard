from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd
import numpy as np
import json
import plotly
from plotly import graph_objects as go

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    chart_type = request.form.get("chart_type", "box")

    # Read coffee exports data
    df = pd.read_csv('coffee_exports.csv')
    df['Year'] = df['Year'].astype(str)
    df['Export_Tons'] = df['Export_Tons'].astype(float)  # Convert to tons (multiply by 1000)
    df['Export_Value_USD'] = df['Export_Value_USD'].astype(float)

    # Select chart type
    if chart_type == "bar":
        fig = px.bar(df, x="Region", y="Export_Value_USD", color="Year", title="Coffee Exports by Country")
    elif chart_type == "scatter":
        # this chart had to change structure since the orignal design didn't show data
        fig = go.Figure()
        for country in df['Country'].unique():
            country_data = df[df['Country'] == country]
            fig.add_trace(
                go.Scatter(
                    x=country_data['Export_Tons'].values.tolist(),
                    y=country_data['Export_Value_USD'].values.tolist(),
                    mode='markers',
                    marker=dict(size=15),
                    name=country,
                    text=country_data['Year']
                )
            )
        fig.update_xaxes(title='Export_Tons')
        fig.update_yaxes(title='Export_Value_USD')
        fig.update_layout(title="Coffee Exports: Volume vs Value")
    else:
        fig = px.box(df, x="Country", y="Export_Value_USD", color="Region", title="Coffee Export Values by Region")

    # df = pd.DataFrame({
    #     "Category": np.random.choice(["A", "B", "C", "D"], size=100),
    #     "Value": np.random.randint(10, 100, size=100),
    #     "Group": np.random.choice(["X", "Y"], size=100)
    # })

    # # Select chart type
    # if chart_type == "bar":
    #     fig = px.bar(df, x="Category", y="Value", color="Group", title="Bar Chart")
    # elif chart_type == "scatter":
    #     fig = px.scatter(df, x="Category", y="Value", color="Group", title="Scatter Plot")
    # else:
    #     fig = px.box(df, x="Category", y="Value", color="Group", title="Box Plot")

    fig.update_layout(
        plot_bgcolor='#1a1c23',
        paper_bgcolor='#1a1c23',
        font_color='#ffffff',
        autosize=True,
        margin=dict(t=50, l=50, r=50, b=50),
        height=600
    )
    fig.update_xaxes(showgrid=False, color='#cccccc')
    fig.update_yaxes(showgrid=False, color='#cccccc')
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("index.html", graphJSON=graphJSON, chart_type=chart_type)

if __name__ == "__main__":
    app.run(debug=True)