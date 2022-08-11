# telegram_analytics
Analysis telegram chats and generate word cloud. Also Generate bar plot from statistical data.

## How to run
First, add `src` to `PYTHONPATH` by run the following code in main repo directory:
```
export PYTHONPATH=${PWD}
```

Second, run following code to generate a word cloud from a json file in `data` directory:
```
python src/chat_analysis/analysis.py
```
