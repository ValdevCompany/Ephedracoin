import hashlib
import time
import random
import json


# Класс для транзакции
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()

    def __str__(self):
        return json.dumps({
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp
        })


# Класс для блока
class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{[str(tx) for tx in self.transactions]}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()


# Класс для блокчейна
class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []
        self.current_transactions = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        # Создаем первый блок (генезис-блок)
        genesis_block = Block(0, "0", [])
        self.chain.append(genesis_block)

    def add_transaction(self, sender, receiver, amount):
        # Добавляем транзакцию
        transaction = Transaction(sender, receiver, amount)
        self.current_transactions.append(transaction)

    def add_block(self):
        # Добавляем новый блок в цепочку
        last_block = self.chain[-1]
        block = Block(len(self.chain), last_block.hash, self.current_transactions)
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.current_transactions = []

    def print_chain(self):
        # Печатаем информацию о блоках
        for block in self.chain:
            print(f"Block {block.index} Hash: {block.hash}")
            for tx in block.transactions:
                print(f"  {tx}")
            print("")


# Пример работы блокчейна
def main():
    blockchain = Blockchain(difficulty=4)

    # Добавляем несколько транзакций
    blockchain.add_transaction(sender="Alice", receiver="Bob", amount=10)
    blockchain.add_transaction(sender="Bob", receiver="Charlie", amount=5)

    # Майним блок и добавляем его в цепочку
    blockchain.add_block()

    # Добавляем еще транзакции и блок
    blockchain.add_transaction(sender="Alice", receiver="Charlie", amount=3)
    blockchain.add_transaction(sender="Charlie", receiver="Alice", amount=2)
    blockchain.add_block()

    # Печатаем все блоки и транзакции
    blockchain.print_chain()


if __name__ == "__main__":
    main()
