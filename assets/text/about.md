## Motivation
In traditional sports, stats can be used to enhance the viewer's experience. However, could this be the case for E-sports and fighting games? How would this stas be tracked? How can they be visualised? What insights from the game can we gather from them?

## What is this?
Backyard Insight is a *proof-of-concept* dashboard that displays stats from past *Guilty Gear -Strive-* tournaments. Currently it only tracks the top 6/8 matches. The stats are divided into two tabs:

* **Match Predictions** - The graph represents a player's predicted chance to win. This prediction is created by **[Win Prediction](https://colab.research.google.com/drive/1ybJt9Y1jr8Qtdvq8T515--zxLptH8D7v?usp=sharing)** machine learning model. By hovering over the graph, the visualations at the top will change, reflecting the state of the match at that time, e.g. what the current health totals are. Additionally if the character *Asuka* is present in the match, an additional visualation that shows the spell hand and percentile is displayed. The strength of the current spell is determined by the **[Asuka Spell](https://colab.research.google.com/drive/1HPtgk7gfxv6YQVEiv5CYf8RlGwLRczoV?usp=sharing)** machine learning model.

* **Match Stats** - This tab mainly shows 'counting' stats of indivdual matches. Stats such as number of psych burst use, tension bar usage, burst bar usage, etc... You can change the type of graph that represents the data to whatever you believe suits the data.

## Dataset
This dashboard was made in conjunction to **[Backyard Observer](https://github.com/tmltsang/Backyard-Observer)**, a yoloV8 vision model that was the basis for the dataset. At the moment the dataset is not hosted anywhere but you see some data cleaning [here](https://colab.research.google.com/drive/1_gkzzw3t4O7hxUaud6jyS6_gkZBsgGU-?usp=sharing). If you are interested in the dataset feel free to reach out.

## Maintainer
Thomas Tsang (thomas.ml.tsang@gmail.com)
