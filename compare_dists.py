from unicodedata import name
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#supported distributions and parameters
DIST_PARAMS = {
    'normal' : ['loc', 'scale']
    , 'poisson' : ['lam']
    , 'exponential' : ['scale']
    , 'weibull' : ['a']
}

def make_sidebar():
    _ = st.sidebar.empty()
    selected_dist = st.sidebar.selectbox(
        'Distribution',
        list(DIST_PARAMS)
    )
    func = getattr(np.random, selected_dist)
    all_params = {param: st.sidebar.number_input(label=param) for param in DIST_PARAMS[selected_dist]}
    dists = [(func ,all_params)]
    
    
    two_dist = st.sidebar.select_slider("", ["One dist", "Two dist"])
    
    if two_dist=='Two dist':
        st.sidebar.markdown("""---""")
        second_dist = st.sidebar.selectbox(
            'Distribution',
            list(DIST_PARAMS), key='ola'
        )
        second_func = getattr(np.random, second_dist)
        second_dist_params = {param: st.sidebar.number_input(label=param, key=param_i) for param_i, param in enumerate(DIST_PARAMS[second_dist])}
        dists.append((second_func, second_dist_params))
    return dists

def make_middle(dists):
    col1, col2, col3 = st.columns(3)
    with col1:
        size = st.number_input(label='size', value=1000)
    with col2:
        bins = st.number_input(label='nbins', value=50)
    with col3:
        alpha = st.number_input(label='alpha', value=.8, min_value=0.0, max_value=1.0)

    all_data = pd.DataFrame(
        {series_name:dist(**params, size=size)
        for series_name, (dist, params) in
        zip(['this','other'], dists)
        }
    )
    make_plots(all_data=all_data, bins=bins, alpha=alpha)
    

def make_plots(all_data, bins, alpha):
    sns.set_theme(style="white", rc={"axes.linewidth": ".5", 'lines.linewidth' : '.5'} )
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, gridspec_kw={'height_ratios': [4, 1]})


    ax1 = all_data.plot(kind='hist', bins=bins, ax=axes[0], alpha=alpha, legend=False)
    ax2=sns.boxplot(data=all_data.melt(), x='value', y='variable', ax=axes[1],showfliers=False)
    ax2.get_yaxis().set_visible(False)
    ax2.xaxis.set_label_coords(1,-.5) 

    ax1.set_ylabel('Frequency', rotation=0)
    ax1.yaxis.set_label_coords(-.1,1.05)

    sns.despine()
    _ = st.pyplot(fig=fig)
    
def main()->None:
    dists = make_sidebar()
    make_middle(dists)

if __name__=='__main__':
    main()