"""Rooms — self-training collections with sentiment."""
import re


def _normalize(text):
    return set(re.sub(r'[^a-z0-9 ]', '', text.lower()).split())


class Room:
    def __init__(self, name, description="", store=None):
        self.name = name
        self.description = description
        self.store = store
        self.tiles = []
        self.sentiment = 0.5
    
    def feed(self, question, answer, confidence=0.5, source="agent", tags=None):
        from .tile import Tile
        tile = Tile(question=question, answer=answer, domain=self.name,
                   confidence=confidence, source=source, tags=tags)
        if self.store:
            self.store.add(tile)
        self._load()
        alpha = 0.1
        self.sentiment = self.sentiment * (1 - alpha) + confidence * alpha
        return tile
    
    def _load(self):
        if self.store:
            self.tiles = [t for t in self.store.all_tiles() if t.domain == self.name]
    
    def query(self, question):
        if not self.tiles:
            return None
        q_words = _normalize(question)
        best, best_score = None, 0
        for tile in self.tiles:
            t_words = _normalize(tile.question) | _normalize(tile.answer)
            overlap = len(q_words & t_words) / max(len(q_words), 1)
            score = overlap * tile.priority
            if score > best_score:
                best_score = score
                best = tile
        if best:
            best.record_use(best_score > 0.1)
            if self.store:
                self.store.add(best)
        return best
    
    def context(self, limit=10):
        if not self.tiles:
            return f"[Room: {self.name}] Empty."
        top = sorted(self.tiles, key=lambda t: t.priority, reverse=True)[:limit]
        lines = [f"[Room: {self.name} | {len(self.tiles)} tiles | sentiment: {self.sentiment:.2f}]"]
        for t in top:
            lines.append(f"  Q: {t.question}")
            lines.append(f"  A: {t.answer[:100]}")
        return "\n".join(lines)
