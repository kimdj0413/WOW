import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from finch import FINCH
from GlobalFunction import get_config_data

def load_and_merge_df():
    config = get_config_data()
    stock_diff_path = config['StockData']['save_path']
    diff_path_list = []
    stock_code_list = []

    for filename in os.listdir(stock_diff_path):
        if filename.endswith('.csv'):
            diff_path_list.append(os.path.join(stock_diff_path, filename))
            stock_code_list.append(filename.split('_')[0])

    diff_list = [pd.read_csv(file, index_col=0) for file in diff_path_list]
    merged_stock_df = pd.concat(diff_list, ignore_index=True)
    print(f'{", ".join(stock_code_list)} DataFrame is merged successfully.')

    return merged_stock_df

def df_clustering(merged_stock_df):
    c, num_clust, _ = FINCH(merged_stock_df, distance='euclidean')
    cluster = pd.DataFrame(c)
    print("*****   Information of Cluster   *****")
    print(num_clust)
    choose_partition = input("Choose partition number : ")
    cluster = cluster.iloc[:, int(choose_partition)]
    cluster.name = 'cluster'
    print('Clustering success!')
    return cluster

def show_clustering_3D(merged_stock_df, cluster):
    cluster_df = pd.concat([merged_stock_df, cluster], axis=1)

    fig = plt.figure(figsize=(24, 16))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(cluster_df['Open'], cluster_df['High'], cluster_df['Close'], c=cluster_df['cluster'], cmap='Set1')

    ax.set_title('3D Cluster')
    ax.set_xlabel('Open')
    ax.set_ylabel('High')
    ax.set_zlabel('Close')

    legend1 = ax.legend(*scatter.legend_elements(), title="Cluster")
    ax.add_artist(legend1)

    def update_angle(num):
        ax.view_init(elev=10, azim=num)
        return fig,

    ani = FuncAnimation(fig, update_angle, frames=np.arange(0, 360, 1), interval=50)

    plt.show()

def show_clustering_2D(merged_stock_df, cluster):
    cluster_df = pd.concat([merged_stock_df, cluster], axis=1)
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(cluster_df['Open'], cluster_df['High'], cluster_df['Close'], c=cluster_df['cluster'], cmap='Set1')

    ax.set_title('3D')
    ax.set_xlabel('Open')
    ax.set_ylabel('High')
    ax.set_zlabel('Close')

    legend1 = ax.legend(*scatter.legend_elements(), title="Cluster")
    ax.add_artist(legend1)

    plt.show()

if __name__ == "__main__":
    merged_stock_df = load_and_merge_df()
    cluster = df_clustering(merged_stock_df)
    show_clustering_3D(merged_stock_df, cluster)
    # show_clustering_2D(merged_stock_df, cluster)