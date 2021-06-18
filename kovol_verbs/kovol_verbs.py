# This file contains the KovolVerb and PredictedKovolVerb classes

import kovol_verbs
from tabulate import tabulate


class KovolVerb:
    def __init__(self, future1s, english):
        # Meta data
        self.kovol = future1s
        self.english = english
        self.tpi = ""  # Tok pisin
        self.author = ""  # Who entered the data

        # Remote past tense
        self.remote_past_1s = ""
        self.remote_past_2s = ""
        self.remote_past_3s = ""
        self.remote_past_1p = ""
        self.remote_past_2p = ""
        self.remote_past_3p = ""

        # Recent past tense
        self.recent_past_1s = ""
        self.recent_past_2s = ""
        self.recent_past_3s = ""
        self.recent_past_1p = ""
        self.recent_past_2p = ""
        self.recent_past_3p = ""

        # Future tense
        self.future_1s = future1s
        self.future_2s = ""
        self.future_3s = ""
        self.future_1p = ""
        self.future_2p = ""
        self.future_3p = ""

        # Imperative forms
        self.singular_imperative = ""
        self.plural_imperative = ""

        # Other forms
        self.short = ""

    def __str__(self):
        return 'Kovol verb: {kovol}, "{eng}"'.format(kovol=self.kovol, eng=self.english)

    def __repr__(self):
        return self.__str__()

    # Methods to call several attributes together in groups
    def get_remote_past_tense(self):
        remote_past_tense = (
            self.remote_past_1s,
            self.remote_past_2s,
            self.remote_past_3s,
            self.remote_past_1p,
            self.remote_past_2p,
            self.remote_past_3p,
        )
        return remote_past_tense

    def get_recent_past_tense(self):
        recent_past_tense = (
            self.recent_past_1s,
            self.recent_past_2s,
            self.recent_past_3s,
            self.recent_past_1p,
            self.recent_past_2p,
            self.recent_past_3p,
        )
        return recent_past_tense

    def get_future_tense(self):
        future_tense = (
            self.future_1s,
            self.future_2s,
            self.future_3s,
            self.future_1p,
            self.future_2p,
            self.future_3p,
        )
        return future_tense

    def get_imperatives(self):
        return (self.singular_imperative, self.plural_imperative)

    def get_all_conjugations(self):
        """Return a list of all conjugations for easily comparing verbs."""
        return (
            self.get_remote_past_tense()
            + self.get_recent_past_tense()
            + self.get_remote_past_tense()
            + self.get_imperatives()
        )

    def print_paradigm(self):
        """Use tabulate to print a nice paradigm table to the terminal."""
        table = [
            ["1s", self.remote_past_1s, self.recent_past_1s, self.future_1s, ""],
            [
                "2s",
                self.remote_past_2s,
                self.recent_past_2s,
                self.future_2s,
                self.singular_imperative,
            ],
            ["3s", self.remote_past_3s, self.recent_past_3s, self.future_3s, ""],
            ["1p", self.remote_past_1p, self.recent_past_1p, self.future_1p, ""],
            [
                "2p",
                self.remote_past_2p,
                self.recent_past_2p,
                self.future_2p,
                self.plural_imperative,
            ],
            ["3p", self.remote_past_3p, self.recent_past_3p, self.future_3p, ""],
        ]
        headers = [
            "",
            "Remote past tense",
            "Recent past tense",
            "Future tense",
            "Imperative",
        ]
        print('\n {sing}, "{eng}"'.format(sing=self.future_1s, eng=self.english))
        print(tabulate(table, headers=headers, tablefmt="rst"))
        print("Short form: {short}".format(short=self.short))


class PredictedKovolVerb(KovolVerb):
    def __init__(self, remote_past_1s, recent_past_1s, english=""):
        super().__init__(future1s="", english=english)
        self.remote_past_1s = remote_past_1s
        self.recent_past_1s = recent_past_1s
        self.vowels = [
            "i",
            "e",
            "ɛ",
            "a",
            "ə",
            "u",
            "o",
            "ɔ",
        ]  # Vowels in Kovol language

        self.root = self.predict_root()
        self.predict_verb()
        self.errors = []

    def __str__(self):
        return "Predicted verb for {rp}, {p}".format(
            rp=self.remote_past_1s, p=self.recent_past_1s
        )

    def __repr__(self):
        return self.__str__()

    def predict_root(self):
        remote_past_tense = self.remote_past_1s[0:-2]  # strip -om
        past_tns = self.recent_past_1s[0:-3]  # strip -gom

        if len(past_tns) > len(remote_past_tense):
            return past_tns
        elif len(past_tns) == len(remote_past_tense):
            return remote_past_tense
        else:
            return remote_past_tense

    def root_ending(self):
        """Returns whether the root ends in a Vowel or Consonant"""
        if self.root[-1] in self.vowels:
            return "V"
        else:
            return "C"

    def verb_vowels(self):
        """Returns a string containing just the vowels"""
        v = [c for c in self.root if c in self.vowels]
        v = "".join(v)
        return v

    def predict_verb(self):
        try:
            self.predict_future_tense()
            self.predict_recent_past_tense()
            self.predict_remote_past()
            self.predict_imperative()
        except IndexError:
            print(f"Index error, {self}")
            # raise IndexError(f"failure on {self}. {self.future_1s}")

    def predict_future_tense(self):
        # Figure out suffixes to use
        if self.root[-1] == "a":
            suffixes = ["anim", "aniŋ", "aŋ", "ug", "wa", "is"]
        else:
            suffixes = ["inim", "iniŋ", "iŋ", "ug", "wa", "is"]
        # Add suffixes to root
        if self.root[-1] == "l":
            suffixes = ["ɛnim", "ɛniŋ", "aŋ", "olug", "wa", "ɛlis"]
            future_tense = [self.root[:-2] + sfx for sfx in suffixes]
            future_tense[4] = self.root + suffixes[4]  # don't replace for -wa

        elif self.root_ending() == "V":
            future_tense = [self.root[:-1] + sfx for sfx in suffixes]
            future_tense[4] = self.root + suffixes[4]  # don't replace for -wa
        else:
            future_tense = [self.root + sfx for sfx in suffixes]
            future_tense[4] = self.root + suffixes[4]  # don't replace for -wa

        self.future_1s = future_tense[0]
        self.future_2s = future_tense[1]
        self.future_3s = future_tense[2]
        self.future_1p = future_tense[3]
        self.future_2p = future_tense[4]
        self.future_3p = future_tense[5]

    def predict_recent_past_tense(self):
        last_vowel = self.verb_vowels()[-1]
        root = self.root

        # Figure out which suffixes to use
        if root[-1] == "u":
            suffixes = ["gum", "gɔŋ", "ge", "uŋg", "guma", "gund"]
        elif last_vowel == "i":
            suffixes = ["gɔm", "gɔŋ", "ge", "ɔŋg", "gima", "gɔnd"]
        elif root[-1] == "a":
            suffixes = ["gam", "gɔŋ", "ga", "aŋg", "gama", "gand"]
        elif root[-1] == "l":
            suffixes = ["gam", "gɔŋ", "ga", "aŋg", "gama", "gand"]
            # Special case when there's only 1 vowel in root
            if len(self.verb_vowels()) == 1:
                root = self.root.replace("ɔ", "a")
        else:
            suffixes = ["gɔm", "gɔŋ", "ge", "ɔŋg", "gɔma", "gɔnd"]

        # Combine the suffixes with the root

        # Root ending in C loses it's C
        if self.root_ending() == "C":
            # m assimilates to ŋ
            if root[-1] == "m":
                past_tense = [root[:-1] + "ŋ" + sfx for sfx in suffixes]
                past_tense[3] = root + suffixes[3]
            else:
                past_tense = [root[:-1] + sfx for sfx in suffixes]
                # Special rule for l, root is shortened
                if root[-1] == "l":
                    past_tense[3] = root[:-2] + suffixes[3]
                else:
                    past_tense[3] = root + suffixes[3]
        # Root ending in V
        elif self.root_ending() == "V":
            past_tense = [root + sfx for sfx in suffixes]
            past_tense[3] = root[:-1] + suffixes[3]

        # No need to predict 1s, user gave it to class
        self.recent_past_2s = past_tense[1]
        self.recent_past_3s = past_tense[2]
        self.recent_past_1p = past_tense[3]
        self.recent_past_2p = past_tense[4]
        self.recent_past_3p = past_tense[5]

    def predict_remote_past(self):
        if self.root[-1] == "u":
            suffixes = ["um", "uŋ", "ut", "umuŋg", "umwa", "umind"]
        elif self.root[-1] == "a":
            suffixes = ["am", "aŋ", "at", "amuŋg", "amwa", "amind"]
        else:
            suffixes = ["ɔm", "ɔŋ", "ɔt", "omuŋg", "omwa", "ɛmind"]

        if self.root_ending() == "V":
            remote_past = [self.root[:-1] + sfx for sfx in suffixes]
        else:
            remote_past = [self.root + sfx for sfx in suffixes]

        # No need to predict 1s, user gave it to class
        self.remote_past_2s = remote_past[1]
        self.remote_past_3s = remote_past[2]
        self.remote_past_1p = remote_past[3]
        self.remote_past_2p = remote_past[4]
        self.remote_past_3p = remote_past[5]

    def predict_imperative(self):
        if self.root[-1] == "g":
            suffixes = ["u", "as"]
        else:
            suffixes = ["e", "as"]
        if self.root_ending() == "V":
            imperatives = [self.root[0:-1] + sfx for sfx in suffixes]
        else:
            imperatives = [self.root + sfx for sfx in suffixes]

        self.singular_imperative = imperatives[0]
        self.plural_imperative = imperatives[1]

    def print_with_kovol_verb(self, kovol_verb):
        print("Actual verb:")
        kovol_verb.print_paradigm()
        print("\nPredicted verb:")
        self.print_paradigm()

    def get_prediction_errors(self, kovol_verb):
        """Compare predicted Kovol verb to the actual one, returning a dict of differences. The key for the dict
        is the tense and actor (as a string) and the value is the tuple (actual data, predicted data)"""
        diff = {}
        order = [
            "remote_past_1s",
            "remote_past_2s",
            "remote_past_3s",
            "remote_past_1p",
            "remote_past_2p",
            "remote_past_3p",
            "recent_past_1s",
            "recent_past_2s",
            "recent_past_3s",
            "recent_past_1p",
            "recent_past_2p",
            "recent_past_3p",
            "future_1s",
            "future_2s",
            "future_3s",
            "future_1p",
            "future_2p",
            "future_3p",
            "singular_imperative",
            "plural_imperative",
        ]
        predicted = self.get_all_conjugations()
        actual = kovol_verb.get_all_conjugations()
        for o, p, a in zip(order, predicted, actual):
            if a != p:
                diff[o] = (a, p)
        self.errors = diff
        return self.errors
