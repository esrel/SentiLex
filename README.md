# SentiLex
Simple Lexicon-based Sentiment Analysis  
  
usage:  
python scripts/SentiLex.py   
   -t '+'                      # token separator in the lexicons  
   -p data/en-lexicon.tsv      # polarity lexicon  
   -s data/en-shifters.tsv     # polarity shifter lexicon  
   -i data/en-intensifiers.tsv # intensifier lexicon  
   -x input_file               # data to label as document-per-line  
