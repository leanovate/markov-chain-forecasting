# Forecasting on kanban boards with the markov-chain model

In this notebook we will train and test a markov-chain model on data extracted from a team's kanban board.

This is inspired by the talk 'Forecasting in Complex Systems' from Olga Heismann on the LKCE 2018. See the following links for reference:
* [Vimeo](https://vimeo.com/302850933)
* [Slideshare](https://de.slideshare.net/lkce/olga-heismann-forcasting-in-complex-systems)


## Preview the notebook
You can see a preview of the notebook rendered by github by clicking [here](markov-notebook.ipynb)

## Run the notebook:
If you want to play around with the notebook you have to run it. An easy way is to use docker:
```
git clone git@github.com:leanovate/markov-chain-forecasting.git

docker run -p 8888:8888 -v $(pwd)/markov-chain-forecasting:/home/jovyan/markov-chain-forecasting jupyter/minimal-notebook
```