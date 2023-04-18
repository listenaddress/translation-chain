import sys
from common.translation_chain import TranslationChain, Step

chain = TranslationChain.load(sys.argv[1])
chain.run()

# Print out the final translation and how long it took to translate
if chain.finished:
    print("Translation: " + chain.output)
    print("Time to translate: " + str(chain.finished - chain.created) + " seconds")
else:
    print("Translation not finished.")
    print("Last step finished: " + Step(**chain.steps[chain.current_step - 1]).type)