def build_keyword_trait_map(trait_keywords):
    keyword_trait_map = {}
    for trait in trait_keywords:
        for keyword in trait["keywords"]:
            keyword_trait_map[keyword] = trait["trait_identifier"]
    return keyword_trait_map
