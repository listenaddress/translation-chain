import sys
from common.translation_chain import TranslationChain

chain = TranslationChain.load(sys.argv[1])
chain.run()
