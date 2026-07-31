from dash_app_2.app.app import app


app.run(
    host="0.0.0.0", 
    port=8050,
    debug=True,
    dev_tools_hot_reload=True
)