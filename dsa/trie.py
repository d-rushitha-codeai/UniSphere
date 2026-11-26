
class TrieNode:
    """A node in the Trie."""
    def __init__(self):
        self.children = {}
        self.student_ids = set()
        self.is_end_of_word = False


class Trie:
    """Trie for prefix-based student searching."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, student_id):
        word = word.strip().lower()

        if not word:
            return

        current = self.root

        for character in word:
            if character not in current.children:
                current.children[character] = TrieNode()

            current = current.children[character]
            current.student_ids.add(student_id)

        current.is_end_of_word = True

    def search_prefix(self, prefix):
        prefix = prefix.strip().lower()

        if not prefix:
            return set()

        current = self.root

        for character in prefix:
            if character not in current.children:
                return set()

            current = current.children[character]

        return current.student_ids.copy()
