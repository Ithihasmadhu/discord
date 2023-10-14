# Read the names from legends.txt
with open('legends.txt', 'r') as legends_file:
    legendary_names = legends_file.read().splitlines()

# Prefix each name with "Shadow"
shadow_names = ["Shadow " + name for name in legendary_names]

# Save the modified names to shadow.txt
with open('shadow.txt', 'w') as shadow_file:
    for name in shadow_names:
        shadow_file.write(name + '\n')

print('Names with "Shadow" prefix saved to shadow.txt')
