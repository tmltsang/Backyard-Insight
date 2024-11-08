## Motivation
In traditional sports, stats can be used to enhance the viewing experience. However, could this be the case for fighting games as well? How would these stats be tracked? How could they be visualised? What insights from the game can we gather from them?

## What is this?
Backyard Insight is a *proof-of-concept* dashboard that displays stats from past *Guilty Gear -Strive-* tournaments. Currently it only tracks the top 6/8 matches. The stats shown are:

### Main Dashboard
The initial landing page. On the left, you can select a tournament, tournament round and game number to see some visualisations across two tabs
* **Game Predictions** - The main feature the graph that represents a player's predicted chance to win. This prediction is created by **[Win Prediction](https://colab.research.google.com/drive/1ybJt9Y1jr8Qtdvq8T515--zxLptH8D7v?usp=sharing)** machine learning model. By hovering over the graph, the visualisations at the top will change, reflecting the state of the game at that time trying to closely mock the in-game UI, e.g. what the current health totals are. Additionally if the character *Asuka* is present in the game, an additional visualisation that shows the spell hand and percentile is displayed. The strength of the current spell is determined by the **[Asuka Spell](https://colab.research.google.com/drive/1HPtgk7gfxv6YQVEiv5CYf8RlGwLRczoV?usp=sharing)** machine learning model.

* **Game Stats** - This tab shows a comparison of resources (such as burst and tension) used between players within a game. The statistic to compare and the graph to represent them can be changed via the dropdowns.

### Player Stats
Found under the 'Player Stats' menu option on the top, select a **player** via the dropdown and see all their stats represented as tables.

The top table under *Game Stats* is the raw resource usage by game or round.

The bottom table under *Total Stats* is an aggregate of resource usage, with a breakdown on each stat by round or game and win or loss. By default it shows the aggregate across all matches but can be further broken down per character, tournament, tournament round or any combination of them. The column names are abbreviations, hover over the header to see exactly what it represents.

Filters can be applied to all columns in either table to find rounds with whatever condition you would like.

## Dataset
This dashboard was made in conjunction to **[Backyard Observer](https://github.com/tmltsang/Backyard-Observer)**, a yoloV8 vision model that was the basis for the dataset. At the moment the dataset is not hosted anywhere but you see some data cleaning [here](https://colab.research.google.com/drive/1_gkzzw3t4O7hxUaud6jyS6_gkZBsgGU-?usp=sharing). If you are interested in the dataset feel free to reach out.

## Maintainer
Thomas Tsang (thomas.ml.tsang@gmail.com)
