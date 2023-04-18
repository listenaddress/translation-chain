import sys
from common.translation_chain import TranslationChain, Step

chain = TranslationChain.load(sys.argv[1])
chain.run()

# Print out the final translation and how long it took to translate
if chain.finished_at:
    print("Translation: " + chain.final_translation)
    print("Time to translate: " + str(chain.finished_at - chain.created_at) + " seconds")
else:
    print("Translation not finished.")
    print("Last step finished: " + Step(**chain.steps[chain.current_step - 1]).type)