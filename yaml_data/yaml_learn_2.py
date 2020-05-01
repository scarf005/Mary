from yaml_loader import open_yaml

a = open_yaml('pre_gen_monsters.yaml',True)
print(a)

intestine = a.get('p_crawling_intestine')
print(intestine.get('Trait_comp'))