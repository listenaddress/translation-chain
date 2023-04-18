import sys
from common.translation_chain import TranslationChain

# Get all of the chains in the cache that have been finished
finished_chains = TranslationChain.get_finished_chains()
print(finished_chains)

# For each chain, print out the input, output, and how long it took
print("")
print("Finished chains...")

for chain in finished_chains:
    print(chain.input)
    print("⬇️")
    print(chain.output)
    print("")
