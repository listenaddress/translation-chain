import sys
from common.constants import *
from common.translation_chain import TranslationChain

"""
(All steps are calls to GPT-4 unless otherwise specified)
1. Pull out main 3 neuroscience concepts in the paper and describe 3 possible ways to translate each concept to developmental biology
2. Construct and execute a query to find most relevant papers to make a translation
3. Summarize results of 2 using GPT 3.5 (cheaper/faster)
    1. Look at each one and decide if it tells us anything about the translation we’re trying to make
    2. Summarize everything these papers have to tell us
4. Given 1 and 3.2, summarize the best options we have going forward to translate the paper/concepts at hand
5. Make a translation using output from 4
6. Construct and execute a query to find most relevant papers to output of 5
7. Summarize results of 6 using GPT 3.5
    1. Use GPT 3.5 to go through each one and decide if it tells us anything about the translation we’re making
    2. Summarize everything these papers have to tell us about the subjects in our final translation
8. Adjust abstract given what's learned from these papers
9. Critique in general—what doesn’t make sense as dev bio? Fix any grammatical mistakes. 
10. Add citations if/where it makes sense
11. Save translation to our hypothesis repository 
12. Run job to review translations and return the top 10% most novel, compelling, and scientifically feasible abstracts 

And here's how the process will start:
1. Process will be loading (i.e. either created or loaded from cache)
2. We'll run the process and it'll start on whatever step is the current step
"""

# Set up translation process
message = sys.argv[1]
process = TranslationChain.load(message)
print(process)

# Step 1 (pull_neuroscience_concepts_and_describe_possible_translations)
# Pull out main 3 neuroscience concepts in the paper and describe 3 possible ways to translate each concept to developmental biology
prompt = "You are a translator—you translate neuroscience to developmental biology. Deep symmetries exist between these fields. Use them to infer novel, grounded and plausible hypotheses in developmental biology. " + \
    "Follow these instructions carefully. Each translation from neuroscience to developmental biology should:" + \
    "- Read as developmental biology. Neuroscience concepts like 'hippocampus' translated to most relevant/related developmental biology term." + \
    "- Use real terms from developmental biology literature." + \
    "- Don't include any neuroscience words, like a part of the brain. Do the best you can to find the most relevant translation." + \
    "- Be compelling. No fanciful language just be scientifically novel and plausible, given what is known in science." + \
    "- Unless necessary to prove a point, the translation should be structurally similar to the input. " + \
    "For example, here are some terms and plausible translations ('N:' is neuroscience and 'D:' is Developmental Biology):" + \
    "N:Neuron D:Cell" + \
    "N:Behavior D:Morphogenesis" + \
    "N:Millisecond D:Minute" + \
    "N:Memory D:Pattern Memory" + \
    "N:Brain D:Body" + \
    "N:Retina D:Epithelium" + \
    "N:Synapse D:Gap junction" + \
    "N:Navigating D:Navigating in morphospace" + \
    "N:Lateralization D:Left-right asymmetry" + \
    "N:Mental illness D:Birth defects" + \
    "N:Psychiatry D:Developmental teratology" + \
    "N:Senses D:Receptors" + \
    "N:Action potential D:Change of vmem" + \
    "N:Consciousness D:Somatic consciousness" + \
    "N:Neuroimaging D:Body tissue imaging" + \
    "N:Synaptic D:Electrical-synaptic" + \
    "N:Cognitive D:Proto-cognitive" + \
    "N:Psychiatry D:Developmental teratology" + \
    "N:Space D:Anatomical morphospace" + \
    "N:Animal D:Tissue" + \
    "N:Goals D:Target morphologies" + \
    "N:Muscle contractions D:Cell behavior" + \
    "N:Behavioral space D:Morphospace" + \
    "N:Pattern completion D:Regeneration" + \
    "N:Behavior D:Morphogenesis" + \
    "N:Think D:Regenerate" + \
    "N:Event-related potentials D:Bioelectrical signals" + \
    "N:Transcranial D:Optogenetic" + \
    "N:Down the axon D:Across the cell surface" + \
    "N:Action potential movement within an axon D:Differential patterns of Vmem across single cells’ surface" + \
    "N:Neurogenesis D:Cell proliferation" + \
    "N:Neuromodulation D:Developmental signaling" + \
    "N:Critical plasticity periods D:Competency windows for developmental induction events" + \
    "N:What are the goals of hedgehogs D:What are the target morphologies of hedgehogs" + \
    "N:On brains. Retina, behavioral plasticity, muscle, synaptic activity and lateralization D:On bodies. Epithelium, regenerative capacity, cell, cell-signaling activity  and left-right asymmetry" + \
    "[Examples done][For now, don't make a full translation, let's first: 1. Pull out main 3 neuroscience concepts in the following abstract and 2. Describe, in detail, 3 ways to translate each concept to developmental biology. What do these translated concepts mirror or relate to the neuroscience concept? Make sure sure these are scientifically compelling and feasible translations. Be creative but straight forward and grounded in what's known in science literature.]Here's the abstract: " + \
    process.message

print(prompt)

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": prompt},
    ]
)

print(response)
if response.choices and response.choices[0].message.content:
    process.steps.append({
        "step": 1,
        "step_type": "pull_neuroscience_concepts_and_describe_possible_translations",
        "output": response.choices[0].message.content,
        # Model should be response.model if it exists
        "model": response.model if hasattr(response, "model") else "GPT",
    })

    print(process)

    process.save()
else:
    print("No response from GPT-4 for the pull_neuroscience_concepts_and_describe_possible_translations step")
    sys.exit(1)
