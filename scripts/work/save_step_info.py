import sys
from common.translation_chain import TranslationChain

content = sys.argv[1]
hash = sys.argv[2]
step = int(sys.argv[3])

translation_chain = TranslationChain.load(hash=hash)

print(translation_chain)

# translation_chain.steps.append({
#     "step": step,
#     "step_type": "pull_neuroscience_concepts_and_describe_possible_translations",
#     "output": content,
#     "model": "gpt-4-0314"
# })

# translation_chain.save()
