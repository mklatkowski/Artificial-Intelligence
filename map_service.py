import os
import plotly.graph_objects as go
from dotenv import load_dotenv


def show_map(lons, lats, text, mode):
    load_dotenv()
    token = 'pk.eyJ1IjoibWtsYXRrb3dza2kiLCJhIjoiY2x1c2VoMW9mMG1ldTJrcGE4dmFla25nbiJ9.zofzNvIXGr1VG-TiyoSOwQ'
    fig = go.Figure(go.Scattermapbox(
        mode=mode,
        lon=lons, lat=lats,
        text=text, textposition="bottom right"))

    print("cos")
    fig.update_layout(
        mapbox={
            'accesstoken': token,
            'style': "outdoors",
            'zoom': 12,
            'center': {'lon': sum(lons) / len(lons), 'lat': sum(lats) / len(lats)}
        },
        showlegend=False)

    fig.show()


def show_track(coordinates):
    mode = 'text+lines'

    lats, lons, texts = coordinates
    show_map(lats, lons, texts, mode)


