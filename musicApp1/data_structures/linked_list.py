class Node:
    def __init__(self, song):
        self.song = song
        self.next = None
        self.prev = None


class PlayList:
    def __init__(self):
        self.head = None
        self.current = None
        self.tail = None
        self.size = 0
        self.is_playing = False

    def add_song(self, song):
        new_node = Node(song)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def remove_song(self, node):
        try:
            if not node:
                return

            # Eğer silinecek node head ise
            if node == self.head:
                self.head = node.next
                if self.head:
                    self.head.prev = None
                if node == self.current:
                    self.current = self.head

            # Eğer silinecek node tail ise
            elif node == self.tail:
                self.tail = node.prev
                if self.tail:
                    self.tail.next = None
                if node == self.current:
                    self.current = self.tail

            # Ortadaki bir node ise
            else:
                node.prev.next = node.next
                node.next.prev = node.prev
                if node == self.current:
                    self.current = node.next

            self.size -= 1

        except Exception as e:
            print(f"Şarkı silme hatası: {e}")

    def get_current_song(self):
        return self.current.song if self.current else None

    def get_all_songs(self):
        songs = []
        current = self.head
        while current:
            songs.append(current.song)
            current = current.next
        return songs

    def play_next(self):
        try:
            if self.current and self.current.next:
                self.current = self.current.next
                self.current.song.play()
                self.is_playing = True
                return True
            return False
        except Exception as e:
            print(f"Sonraki şarkıya geçme hatası: {e}")
            return False

    def play_previous(self):
        try:
            if self.current and self.current.prev:
                self.current = self.current.prev
                self.current.song.play()
                self.is_playing = True
                return True
            return False
        except Exception as e:
            print(f"Önceki şarkıya geçme hatası: {e}")
            return False

    def play_current(self):
        try:
            if self.current:
                self.current.song.play()
                self.is_playing = True
                return True
            return False
        except Exception as e:
            print(f"Mevcut şarkıyı çalma hatası: {e}")
            return False

    def get_node_at_index(self, index):
        if index < 0 or not self.head:
            return None
        
        current = self.head
        for _ in range(index):
            if not current:
                return None
            current = current.next
        return current