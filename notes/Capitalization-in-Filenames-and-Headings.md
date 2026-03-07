
These are always to be lowercase, and there are some exceptions that should always be uppercase.

For a complete understanding, see the Python dictionary below.

=== Standard lowercase candidates ===
['a', 'about', 'above', 'across', 'after', 'against', 'along', 'am', 'among', 'an', 'and', 'apart', 'are', 'around', 'as', 'at', 'be', 'before', 'behind', 'below', 'beside', 'between', 'beyond', 'both', 'but', 'by', 'circa', 'cross', 'down', 'during', 'either', 'except', 'for', 'from', 'given', 'if', 'in', 'inside', 'into', 'is', 'like', 'minus', 'near', 'neither', 'nor', 'not', 'of', 'off', 'on', 'once', 'onto', 'or', 'out', 'outside', 'over', 'past', 'per', 'since', 'so', 'than', 'that', 'the', 'though', 'through', 'thru', 'till', 'to', 'toward', 'towards', 'under', 'until', 'unto', 'up', 'upon', 'using', 'via', 'vs.', 'was', 'were', 'when', 'where', 'whether', 'while', 'with', 'within', 'without', 'worth', 'yet']

=== t33d additions ===
['a', 'aka', 'aka.', 'an', 'and', 'at', 'by', 'e.g.', 'eg', 'et', 'etc', 'etc.', 'for', 'i.e.', 'ie', 'in', 'nb', 'of', 'on', 'or', 'per', 'the', 'to', 'via', 'vs', 'vs.', 'with']

=== Combined unique words: 99 ===
['a', 'about', 'above', 'across', 'after', 'against', 'aka', 'aka.', 'along', 'am', 'among', 'an', 'and', 'apart', 'are', 'around', 'as', 'at', 'be', 'before', 'behind', 'below', 'beside', 'between', 'beyond', 'both', 'but', 'by', 'circa', 'cross', 'down', 'during', 'e.g.', 'eg', 'either', 'et', 'etc', 'etc.', 'except', 'for', 'from', 'given', 'i.e.', 'ie', 'if', 'in', 'inside', 'into', 'is', 'like', 'minus', 'nb', 'near', 'neither', 'nor', 'not', 'of', 'off', 'on', 'once', 'onto', 'or', 'out', 'outside', 'over', 'past', 'per', 'since', 'so', 'than', 'that', 'the', 'though', 'through', 'thru', 'till', 'to', 'toward', 'towards', 'under', 'until', 'unto', 'up', 'upon', 'using', 'via', 'vs', 'vs.', 'was', 'were', 'when', 'where', 'whether', 'while', 'with', 'within', 'without', 'worth', 'yet']


We do not generally use Chicago style of heading capitalization, because it can be difficult to remember and confusing to authors. It also often makes for awkward filenames.

Only when specially noted do we use the Chicago style of heading capitalization.

The Chicogo style refers to a style in which the wast word is almost always capitalized regardless of whether or not it's in our lists of words not to capitalize.

Special Proper Nouns
====================

Some proper nouns come from brand names that are explicitly lowercase first.

We attempt to preserve these where possible.  E.g.  iPhone

Where do our Capitalization Rules Come from
============================================

The T33D style guide's capitalization rules are a variation of standard English publication, combined with additions by T33D that are relevant to our industry/domain.

**`standard`** -- the agreed-upon core, split into articles, conjunctions (coordinating / subordinating / correlative fragments), and prepositions bucketed by letter count. Prepositions by length is useful because it maps directly to the AP/Chicago/APA rules.

**`style_guide_variations`** -- documents where Chicago, AP, APA, and MLA actually differ, in case you ever want to reference why a decision was made or switch rules later.

**`t33d_custom`** -- your own additions: `vs/via/per` as connectors, technical shorthand like `e.g./aka/etc`, and an explicit `filepath_conjunctions` list that's the practical working list for your hyphenated folder names.

**`never_lowercase_exceptions`** -- a reminder layer for proper nouns, acronyms, and the first-word rule. Worth having in the same file so the logic stays in one place.


```

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
            # (not universal -- most guides capitalize verbs; listed for awareness)
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
        "last_word_rule":   "Capitalize the last word (Chicago convention -- optional for t33d)",
    },

}


if __name__ == "__main__":
    # Quick sanity print -- flatten and show all lowercase word candidates
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
```