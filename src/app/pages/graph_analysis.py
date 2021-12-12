import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl

import streamlit as st
import plotly.express as px
import plotly.io as pio
import os
import base64

from ..constants import *
from ...graph_utils import get_k_common_followers, get_top_followers, from_pandas_to_pyviz_net

pio.templates.default = "plotly_dark"


def pv_static(fig, name='graph'):
    # https://github.com/napoles-uach/stvis
    h1 = fig.height
    h1 = int(h1.replace('px', ''))
    w1 = fig.width
    w1 = int(w1.replace('px', ''))
    fig.show(name+'.html')
    return components.html(
        fig.html, height=h1+30, width=w1+30
    )


def set_graph_analysis(df):

    st.title('Graph Analysis of the Networks of Hispanic Twitch Streamers')
    st.subheader("How do streamers follow each other?")

    menu_items = ["PyViz", "Gephi"]
    menu_variables = st.radio(
        "",
        menu_items,
    )
    if menu_items.index(menu_variables) == 0:
        show_streamers_pyviz_graphs(df)
    else:
        # st.text("Sorry, this feature is not implemented yet")
        show_gephi_graphs()


def show_streamers_pyviz_graphs(df):
    # Define list of streamer to visualize in a graph
    streamer_list = df.sort_values(
        "num_followers", ascending=False).name.tolist()

    # Multiselect dropdown menu (returns a list)
    selected_streamer = st.selectbox(
        'Select streamer to visualize', streamer_list)
    image_col, _, _, _ = st.columns(4)
    image_col.image(df[df['name'] == selected_streamer]
                    ['profile_image_url'].values[0], width=100)

    row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
        (.1, 1.5, .5, 1.5, .1))

    with row3_1:
        st.subheader('Graph 1')
        st.markdown(explanations_of_graph_1)

        # if len(selected_streamer) == 0:
        #     st.text('Choose at least 1 streamer to visualize')

        # elif len(selected_streamer) > 1:
        #     st.text('Choose at most 1 streamer to visualize')
        # # Create network graph when user selects >= 1 item
        # else:
        df = get_top_followers(
            df.copy(), common_followers_with=selected_streamer)

        net1 = from_pandas_to_pyviz_net(df, emphasize_node=selected_streamer)

        pv_static(net1, name="reports/graph")

    with row3_2:
        st.subheader('Graph 2')
        st.markdown(explanations_of_graph_2)

        # if len(selected_streamer) == 0:
        #     st.text('Choose at least 1 streamer to visualize')

        # elif len(selected_streamer) > 1:
        #     st.text('Choose at most 1 streamer to visualize')
        # # Create network graph when user selects >= 1 item
        # else:
        df2 = get_k_common_followers(
            "data/streamers.feather", common_followers_with=selected_streamer)

        net2 = from_pandas_to_pyviz_net(df2, emphasize_node=selected_streamer)

        pv_static(net2, name="reports/graph2")


def show_gephi_graphs():
    image_mapping = {"11. Carola Network Downsampled.png": "https://drive.google.com/file/d/15UYwfW-a4Jl66j8PKWqWbVxAMeQV32v_/view?usp=sharing",
                     "12. Nissaxter Network downsampeld.png": "https://drive.google.com/file/d/1hnw6cczJnbR6ZS8-uVWPFv1z7_4NHTX5/view?usp=sharing",
                     "5. Twitch 30000 followers downsampled.png": "https://drive.google.com/file/d/1itq2yLykr8n0l2nWAnYpz8L-XkU4RHRS/view?usp=sharing",
                     "3. Twitch 100000 followers by views downsample.png": "https://drive.google.com/file/d/1ivRn3VOoNoD8f-_LaViI4odpUZRGx_jK/view?usp=sharing",
                     "4. Twitch 100000 followers downsamled.png": "https://drive.google.com/file/d/1f-aCAXW4RhGf4WJqtA-V6b2vJUSKv_dL/view?usp=sharing",
                     "9. Twitch ASMR dowsampled.png": "https://drive.google.com/file/d/1PQvnT9uolchlgx5KFExtwQGGg_ZMUdFJ/view?usp=sharing",
                     "6. Twitch Just Chatting downsampled.png": "https://drive.google.com/file/d/1PyvyQMP704icQDy3S_lEF4vBD19Ml0JD/view?usp=sharing",
                     "7. Twitch League of Legends downsampled.png": "https://drive.google.com/file/d/1oR3PtAKy8Fwu85VAmU0Ks1NQk8mLJDeh/view?usp=sharing",
                     "8. Twitch Minecraft downsampled.png": "https://drive.google.com/file/d/1m5SNyNe4dsOL3ZBaX-A8qVeAZ5gQema3/view?usp=sharing",
                     "10. Twitch Music downsampled.png": "https://drive.google.com/file/d/160bllFOG2UhrZqCZ8ioPhWlSUa-JQG1f/view?usp=sharing",
                     "2. Twitch partners downsampled.png": "https://drive.google.com/file/d/1tNS8QpjHO_XKFMNnMRoNBUsoNL_U9Dcs/view?usp=sharing",
                     "1. Twitch top 100 streamers downsampled.png": "https://drive.google.com/file/d/1qOLXeuFEFQUGOhbyEVlZpmHSBFZEy-6v/view?usp=sharing"}
    st.subheader('Graphs Made with Gephi')
    # 2 columns showing the images of the graphs generated by Gephi

    images = [img for img in os.listdir('app/main/images') if img.endswith('.png')]
    st.markdown(
        "Click on the images to see them on full resolution or click [here](https://drive.google.com/drive/folders/1sLFmG8H_ccWvvZcTS-vsuiaTParDkmf5)"\
            " to see more.", unsafe_allow_html=True)
    for i in range(len(images)//2):
        col1, col2 = st.columns(2)
        # get the two images from the dictionary
        image_path1, image_path2 = images[i*2:i*2+2]
        name1, name2 = [" ".join(path.split(".")[0].split(' ')[:-1])
                        for path in [image_path1, image_path2]]
        imagefile1, imagefile2 = open(f"app/main/images/{image_path1}", "rb"), open(f"app/main/images/{image_path2}", "rb")
        contents1,contents2 = imagefile1.read(), imagefile2.read()
        data_url1, data_url2 = base64.b64encode(contents1).decode("utf-8"),base64.b64encode(contents2).decode("utf-8")
        imagefile1.close(), imagefile2.close()

        with col1:
            st.markdown(f'''
                <a href="{image_mapping[images[i*2]]}" target="_blank" style="text-align: center; display: block; text-decoration:none" >
                    <img src="data:image/gif;base64,{data_url1}" width="600" alt="{name1}">
                    <p style="color:darkgrey" >{name1}</p>
                </a>
                ''',unsafe_allow_html=True
            )
        with col2:
            st.markdown(f'''
                <a href="{image_mapping[images[i*2+1]]}" target="_blank" style="text-align: center; display: block; text-decoration:none" >
                    <img src="data:image/gif;base64,{data_url2}" width="600" alt="{name2}">
                    <p style="color:darkgrey" >{name2}</p>
                </a>
                ''',unsafe_allow_html=True 
            )
