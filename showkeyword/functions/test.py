import networkx as nx

level = 3
numofkeys = 7 #the number of mainkeywords   #2**level -1 #sum of G.P. with common ratio = 2
show = False

from preprocessing import get_data, word_by_sent, wbys_to_word, word_to_idx, idx_by_sent
text = get_data('data/test_middle.txt')
wbys = word_by_sent(text) # [['fooled', 'word', 'energy'], ['energy', 'bars', 'contain', 'saturated', 'fat', 'snickers', 'bar'], ... ]
wordlist = wbys_to_word(wbys) # ['fooled', 'word', 'energy', 'bars', ... ]
wtoi = word_to_idx(wordlist) # {'fooled': 0, 'word': 1, 'energy': 2, 'bars': 3, ... }
ibys = idx_by_sent(wbys, wtoi) # [[0, 1, 2], [2, 3, 4, 5, 6, 7, 8], ... ]

from textrank import count_window, textrank_keyword
counter = count_window(ibys, window=5) # {edge: weight} {(0, 1): 1, (1, 2): 1, (0, 2): 1, (2, 3): 6, (3, 4): 2,  ... }
# textrank 값이 높은 단어 numofkeys 개
mainkeywords = textrank_keyword(ibys, wordlist, numofkeys)
# [('bars', 5.299685817363776), ('bar', 2.9241898262135697), ('saturated', 2.637340972593308), ('fat', 2.6167433602101577), ('energy', 1.9782967575065245), ('protein', 1.8757418129733594), ('nutrition', 1.7938081245543516)]

import visualization as vis
cnt_draw = vis.counter_draw(counter,wordlist) # [('fooled', 'word' 1), ('word', 'energy', 1), ('fooled', 'energy', 1), ('energy', 'bars', 6), ... ]

# 단순연결 그래프. 연결된 노드가 많을 수록 진한 색
IG = vis.initialGraph(cnt_draw)
# vis.drawgraph(IG, cmap = "Blues", nodesize = 350, graphtype = None, savepath=None, show = show)

vis.communityGraph(IG) 
# vis.drawgraph(IG, cmap = "Pastel1", nodesize = 350, graphtype = "community", savepath="community.png", show = show)

# 주어진 단어와 단순연결된 그래프
# energy_SG = vis.subGraph(IG, "energy")
# vis.drawgraph(energy_SG, cmap = "Oranges", nodesize = 350, graphtype = None, savepath="subgraph.png", show = show)

# 주어진 단어와 동일한 커뮤니티의 그래프
SCG = vis.subCommunityGraph(IG, mainkeywords[0][0]) #only after communityGraph() method
vis.drawgraph(SCG, cmap = "Pastel1", nodesize = 350, graphtype = "community", savepath="subcommunity.png", show = show)

"""
The core of this project:
1. Method textrankGraph() must be implemented after communityGraph() method and textrank_keyword() method.
2. It takes one mainkeyword tuple which formed like: ('bars', 1.8823393131581336).
3. The parameter 'subgraph' determines wheter the result is 
   subgraph of community graph or just whole community graph, which includes given mainkeyword.
4. You can use any type for graphtype parameter("community", "textrank", None), but "textrank" shows the best visualization.
"""
# 주어진 단어와 동일한 커뮤니티에 속한 노드들로만 다시 textrank 계산.
# textrank 계산할 때에 주어진 단어를 제외하고 나머지 단어들 간의 textrank 계산.
# 같은 커뮤니티 내에서 textrank 값 재설정
TG = vis.textrankGraph(IG, mainkeywords[0], subgraph = False) #textrank graph with whole community
vis.drawgraph(TG, cmap = "YlGn", graphtype = "textrank", savepath="textrankgraph.png",show = show)
# 주어진 단어와, 위에서 구한 textrank 상위 top 5 개의 단어로만 이루어진 그래프 (단순연결 그래프에서 추출)
STG = vis.textrankGraph(IG, mainkeywords[0], subgraph = True) #sub textrank graph 
# vis.drawgraph(STG, cmap = "YlGn", graphtype = "textrank", savepath="subtextrankgraph.png",show = show)

# 각 mainkeyword 의 STG 를 한번에 보여줌
submindmaplist = []
for keyword in mainkeywords:
    STG = vis.textrankGraph(IG, keyword, subgraph = True) #sub textrank graph
    submindmaplist.append(STG)
   #  vis.drawgraph(STG, cmap = "YlGn", graphtype = "textrank", savepath= keyword[0] + ".png",show = show)

mindmap = nx.compose_all(submindmaplist)
vis.drawgraph(mindmap, cmap = "Set2", graphtype = "textrank", savepath="mindmap.png",show = True)