from datetime import datetime
from hashlib import sha256
import json

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount
        }

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, diff, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.diff = diff
        self.hash = self.calc_hash()

    def calc_hash(self):
        transactions_str = json.dumps([tx.to_dict() for tx in self.transactions], sort_keys=True)
        hash_string = (str(self.index) + str(self.previous_hash) +
                       str(self.timestamp) + transactions_str + str(self.nonce) + str(self.diff))
        return sha256(hash_string.encode()).hexdigest()

    def is_valid(self):
        return self.hash[:self.diff] == '0' * self.diff

    def mine_block(self):
        target = '0' * self.diff
        while self.hash[:self.diff] != target:
            self.nonce += 1
            self.hash = self.calc_hash()
        print(f"Block mined: {self.hash}")

class Blockchain:
    def __init__(self):
        self.diff = 4
        self.chain = [self.create_genesis_block()]
        self.ireward = 50
        self.block_per_halving = 210000

    def create_genesis_block(self):
        return Block(0, "0", str(datetime.now()), [], self.diff, nonce=0)

    def latest(self):
        return self.chain[-1]

    def add_transaction(self, sender, receiver, amount):
        transaction = Transaction(sender, receiver, amount)
        latest_block = self.latest()
        # Add transaction to the latest block or create a new block if necessary
        latest_block.transactions.append(transaction)

    def add_block(self):
        latest = self.latest()
        new_block = Block(index=latest.index + 1,
                          previous_hash=latest.hash,
                          timestamp=str(datetime.now()),
                          transactions=latest.transactions,
                          diff=self.diff,
                          nonce=0)
        new_block.mine_block()
        reward = self.get_block_reward(new_block.index)
        reward_transaction = Transaction(sender="Network", receiver="Miner", amount=reward)
        new_block.transactions.append(reward_transaction)
        self.chain.append(new_block)

    def get_block_reward(self, block_index):
        halvings = block_index // self.block_per_halving
        reward = self.ireward / (2 ** halvings)
        return reward

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calc_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

            if not current_block.is_valid():
                return False

        return True

# Пример использования:
blockchain = Blockchain()
blockchain.add_transaction("Alice", "Bob", 100)
blockchain.add_block()  # Добавляем блок с одной транзакцией

blockchain.add_transaction("Bob", "Charlie", 50)
blockchain.add_block()  # Добавляем еще один блок с другой транзакцией

print("Is blockchain valid?", blockchain.is_valid())

for block in blockchain.chain:
    print(f"Index: {block.index}, Timestamp: {block.timestamp}, Hash: {block.hash}, Previous Hash: {block.previous_hash}")
    for tx in block.transactions:
        print(f"  Transaction: {tx.to_dict()}")
