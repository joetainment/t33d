"""
title_case_lowercase.py

Comprehensive reference dict of words that are typically lowercased in title case,
organized by style guide consensus and t33d custom rules.

Usage:
    from title_case_lowercase import LOWERCASE_WORDS

    def flatten(d):
        words = set()
        for v in d.values():
            if isinstance(v, list):
                words.update(v)
            elif isinstance(v, dict):
                words.update(flatten(v))
        return words

    ALL_LOWERCASE = flatten(LOWERCASE_WORDS)
"""

LOWERCASE_WORDS = {

    "standard": {

        "articles": {
            "definite":   ["the"],
            "indefinite": ["a", "an"],
        },

        "conjunctions": {
            "coordinating": ["and", "but", "or", "nor", "for", "yet", "so"],
            "subordinating": [
                "as", "if", "once", "than", "that", "though",
                "till", "when", "where", "while",
            ],
            "correlative_fragments": [
                # Only the lowercase half of pairs like "either/or", "not only/but also"
                "both", "either", "neither", "not", "whether",
            ],
        },

        "prepositions": {
            "one_letter":   ["a"],          # rare but exists ("a" as prep in "a priori")
            "two_letter":   ["at", "by", "in", "of", "on", "to", "up"],
            "three_letter": ["for", "off", "out", "per", "via", "vs."],
            "four_letter":  ["from", "into", "like", "near", "onto", "over",
                             "past", "than", "thru", "upon", "with"],
            "five_letter":  ["about", "above", "after", "along", "among",
                             "apart", "below", "circa", "cross", "down",
                             "given", "minus", "since", "under", "until",
                             "unto",  "until", "using", "worth"],
            "six_plus_letter": [
                "across", "against", "around", "before", "behind",
                "beside", "between", "beyond", "during", "except",
                "inside", "outside", "through", "toward", "towards",
                "within", "without",
            ],
        },

        "to_be_verbs": {
            # Short forms sometimes lowercased in informal or minimal styles
            # (not universal — most guides capitalize verbs; listed for awareness)
            "informal_only": ["is", "are", "was", "were", "be", "am"],
        },

    },

    "style_guide_variations": {
        # Where the major guides explicitly differ

        "chicago": {
            # Chicago lowercases all prepositions regardless of length
            "lowercase_all_prepositions": True,
            "always_lowercase": ["to", "of", "in", "on", "at", "by", "for",
                                  "with", "from", "into", "over", "than", "that",
                                  "as", "but", "or", "nor", "and", "yet", "so"],
        },

        "ap": {
            # AP capitalizes prepositions 4+ letters
            "capitalize_prepositions_of_length": 4,
            "always_lowercase": ["to", "of", "in", "on", "at", "by", "for",
                                  "and", "but", "or", "nor", "a", "an", "the"],
        },

        "apa": {
            # APA capitalizes all words 4+ letters
            "capitalize_words_of_length": 4,
            "always_lowercase": ["and", "as", "at", "but", "by", "for",
                                  "if",  "in", "nor", "of", "off", "on",
                                  "or",  "so", "the", "to", "up", "via", "yet"],
        },

        "mla": {
            # MLA (9th ed): lowercase articles, prepositions, coordinating conjunctions
            "always_lowercase": ["a", "an", "the",
                                  "and", "but", "or", "nor", "for", "so", "yet",
                                  "as", "at", "by", "for", "in", "of", "on",
                                  "to", "up", "via"],
        },

    },

    "t33d_custom": {
        # Deliberate additions for t33d project style
        # Rule: lowercase unless the word opens the filename/title segment

        "connectors": ["vs", "vs.", "via", "per"],

        "technical_shorthand": [
            # Common in tech writing, treated as prepositions/conjunctions
            "aka",   # also known as
            "aka.",
            "et",    # et al., etc.
            "etc",
            "etc.",
            "ie",    # id est
            "i.e.",
            "eg",    # exempli gratia
            "e.g.",
            "nb",    # nota bene (rare in titles but possible)
        ],

        "filepath_conjunctions": [
            # Words that appear as joiners in hyphenated folder/file names
            # e.g.  Scripting-and-Tools,  Setup-for-Maya
            "and", "or", "for", "to", "the", "a", "an",
            "in",  "of", "on",  "at", "by",  "with",
        ],

    },

    "never_lowercase_exceptions": {
        # Reminders: these are ALWAYS capitalized regardless of position
        "proper_nouns":     ["Maya", "Python", "GitHub", "Obsidian", "Zettlr"],
        "acronyms":         ["API", "UI", "UX", "VFX", "DCC", "LOD", "UV"],
        "first_word_rule":  "Always capitalize the first word of any title or filename segment",
        "last_word_rule":   "Capitalize the last word (Chicago convention — optional for t33d)",
    },

}


if __name__ == "__main__":
    # Quick sanity print — flatten and show all lowercase word candidates
    def flatten(d: dict) -> set:
        words = set()
        for v in d.values():
            if isinstance(v, list):
                words.update(v)
            elif isinstance(v, dict):
                words.update(flatten(v))
            # skip bools and strings
        return words

    standard   = flatten(LOWERCASE_WORDS["standard"])
    t33d_extra = flatten(LOWERCASE_WORDS["t33d_custom"])
    combined   = standard | t33d_extra

    print("=== Standard lowercase candidates ===")
    print(sorted(standard))

    print("\n=== t33d additions ===")
    print(sorted(t33d_extra))

    print(f"\n=== Combined unique words: {len(combined)} ===")
    print(sorted(combined))


