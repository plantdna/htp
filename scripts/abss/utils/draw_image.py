import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# 0: 白 1: 绿 2 黄 3 红 4 灰
color_list = ['white', 'green','orange','red', 'gray']

def draw_group(chr_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for chr_id in range(1, 11):
        chr_df = pd.read_csv('{}/chr{}.csv'.format(chr_path, chr_id))
        fig, ax = plt.subplots(figsize=(math.ceil(chr_df.shape[1]/10), math.ceil(chr_df.shape[0]/10)))
        heatmap_data = chr_df.iloc[0:, 2:].values
        clist=[]
        data_set = np.unique(heatmap_data)
        for i in data_set:
            clist.append(color_list[i])

        newcmp = LinearSegmentedColormap.from_list('chaos',clist)
        ax.imshow(heatmap_data, cmap=newcmp, interpolation=None)
        ax.set_aspect('auto')
        plt.savefig('{}/chr{}.png'.format(output_path, chr_id), format='png', dpi=300)
        plt.close()



def draw_sample(chr_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    chr_dfs = []
    max_cols = 0
    for chr_id in range(1, 11):
        chr_df = pd.read_csv('{}/chr{}.csv'.format(chr_path, chr_id))
        if chr_df.shape[1]-2 > max_cols:
            max_cols = chr_df.shape[1]
        chr_dfs.append(chr_df)
    
    sample_num = len(chr_dfs[0])
    for i in range(sample_num):
        sample_data = []
        sample_code = chr_dfs[0].iloc[i]['call_code']
        for chr_df in chr_dfs:
            sample_chr_data = [int(v) for v in chr_df.iloc[i].tolist()[2:]]
            if len(sample_chr_data) < max_cols:
                sample_chr_data+=([0]*(max_cols-len(sample_chr_data)))
            sample_data.append(sample_chr_data)

        fig, ax = plt.subplots(figsize=(20, 20))
        heatmap_data = np.array(sample_data)

        clist=[]
        data_set = np.unique(heatmap_data)
        for i in data_set:
            clist.append(color_list[i])

        newcmp = LinearSegmentedColormap.from_list('chaos',clist)

        ax.imshow(heatmap_data, cmap=newcmp, interpolation=None)
        ax.set_aspect('auto')

        ax.set_xticks([])
        ax.set_yticks(np.arange(heatmap_data.shape[0]))

        ax.spines[:].set_visible(False)

        ax.set_yticklabels(['Chr{}'.format(i) for i in range(1, 11)], fontsize=36)
        ax.set_yticks(np.arange(heatmap_data.shape[0]+1)-.5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=20)
        ax.tick_params(which="minor", bottom=False, left=False)
        ax.set_title(sample_code, fontsize=36)

        plt.savefig('{}/{}.png'.format(output_path, sample_code), format='png', dpi=300)
        plt.close()