"""Pengolahan data dasbor: standardisasi, PCA, k-means, graf kNN, centrality, komunitas.

Menjalankan:  python analisis.py
Masukan  : data/Sumber_Data_UAS_Visdat.xlsx
Keluaran : data/data_terolah.csv, data/edges_knn.csv, data/data.json
"""
import json
import networkx as nx
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

K_KLASTER, K_KNN, SEED = 4, 5, 7
KOLOM = {0: 'no', 1: 'provinsi', 2: 'kawasan', 3: 'pajak', 4: 'desen', 5: 'mandiri',
         6: 'efpad', 7: 'efpajak', 8: 'ipm', 11: 'pend', 20: 'pdrb', 21: 'pdrbk'}
V8 = ['pajak', 'desen', 'mandiri', 'efpad', 'efpajak', 'ipm', 'pdrb', 'pdrbk']
V5 = V8[:5]

df = pd.read_excel('data/Sumber_Data_UAS_Visdat.xlsx', header=None).iloc[3:41]
d = df[list(KOLOM)].rename(columns=KOLOM).reset_index(drop=True)
for c in d.columns[3:]:
    d[c] = d[c].astype(float)

# 1. Standardisasi (z-score, simpangan baku populasi)
Z = (d[V8] - d[V8].mean()) / d[V8].std(ddof=0)

# 2. PCA 2 komponen
pca = PCA(2).fit(Z)
pc = pca.transform(Z)

# 3. k-means; label diurutkan menurut rata-rata rasio pajak (1 = tertinggi)
km = KMeans(K_KLASTER, n_init=50, random_state=1).fit(Z)
urut = d.assign(l=km.labels_).groupby('l').pajak.mean().sort_values(ascending=False).index.tolist()
klaster = np.array([urut.index(l) for l in km.labels_])
sil = silhouette_score(Z, klaster)

# 4. Graf kNN pada 5 variabel inti (z-score), bobot = cosine similarity
Z5 = ((d[V5] - d[V5].mean()) / d[V5].std(ddof=0)).values
Xn = Z5 / np.linalg.norm(Z5, axis=1, keepdims=True)
S = Xn @ Xn.T
G = nx.Graph()
G.add_nodes_from(range(len(d)))
for i in range(len(d)):
    s = S[i].copy()
    s[i] = -9
    for j in np.argsort(-s)[:K_KNN]:
        G.add_edge(i, int(j), w=round(float(S[i, j]), 4))   # tepi dua arah digabung

# 5. Komunitas Louvain, degree dan betweenness centrality
komunitas_set = nx.community.louvain_communities(G, weight='w', seed=SEED, resolution=1)
kom = [0] * len(d)
for ci, c in enumerate(sorted(komunitas_set, key=lambda c: -len(c))):
    for n in c:
        kom[n] = ci
dc, bc = nx.degree_centrality(G), nx.betweenness_centrality(G)
mod = nx.community.modularity(G, komunitas_set, weight='w')

# Keluaran
out = d.rename(columns={'pend': 'realisasi_pendapatan_miliar_rp'})
for v in V8:
    out['z_' + v] = Z[v].round(4)
out['pc1'], out['pc2'] = pc[:, 0].round(4), pc[:, 1].round(4)
out['klaster'] = klaster + 1
out['degree_centrality'] = [round(dc[i], 4) for i in range(len(d))]
out['betweenness_centrality'] = [round(bc[i], 4) for i in range(len(d))]
out['komunitas'] = np.array(kom) + 1
out.to_csv('data/data_terolah.csv', index=False, encoding='utf-8')

edges = pd.DataFrame([{'sumber': d.provinsi[u], 'target': d.provinsi[v], 'cosine_similarity': a['w']}
                      for u, v, a in G.edges(data=True)]).sort_values('cosine_similarity', ascending=False)
edges.to_csv('data/edges_knn.csv', index=False, encoding='utf-8')

nodes = [dict(i=i, prov=d.provinsi[i], reg=d.kawasan[i], pc1=round(float(pc[i, 0]), 3), pc2=round(float(pc[i, 1]), 3),
              cl=int(klaster[i]), raw={v: float(d[v][i]) for v in V8}, z={v: round(float(Z[v][i]), 3) for v in V8},
              pend=float(d.pend[i]), deg=round(dc[i], 4), btw=round(bc[i], 4), com=kom[i]) for i in range(len(d))]
json.dump(dict(nodes=nodes, edges=[dict(s=u, t=v, w=a['w']) for u, v, a in G.edges(data=True)], V8=V8,
               evr=[round(x, 4) for x in pca.explained_variance_ratio_], load=np.round(pca.components_, 3).tolist(),
               K=K_KLASTER, kk=K_KNN, sil=round(sil, 3), mod=round(mod, 3)),
          open('data/data.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(f'PCA {pca.explained_variance_ratio_.round(3)} | silhouette {sil:.3f} | tepi {G.number_of_edges()} '
      f'| komunitas {len(komunitas_set)} | modularitas {mod:.3f}')
