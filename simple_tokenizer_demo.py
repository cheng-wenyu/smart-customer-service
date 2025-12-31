#!/usr/bin/env python3
"""
简单的Tokenizer演示
"""

def manual_bpe_demo():
    """手动演示BPE原理"""
    
    print("🎯 BPE算法手动演示")
    print("=" * 50)
    
    # 假设的训练文本
    corpus = [
        "low lower newest widest",
        "low low low low",
        "new new new new", 
        "wide wide wide wide",
        "lowest newer widening"
    ]
    
    print("训练文本:")
    for text in corpus:
        print(f"  {text}")
    
    print("\n1. 初始词汇表（所有字符）:")
    initial_vocab = set()
    for text in corpus:
        for char in text.replace(" ", ""):
            initial_vocab.add(char)
    print(f"   {sorted(initial_vocab)}")
    
    print("\n2. 统计字符对频率:")
    pairs = {}
    for text in corpus:
        words = text.split()
        for word in words:
            for i in range(len(word)-1):
                pair = (word[i], word[i+1])
                pairs[pair] = pairs.get(pair, 0) + 1
    
    # 显示最频繁的字符对
    sorted_pairs = sorted(pairs.items(), key=lambda x: x[1], reverse=True)[:3]
    for (c1, c2), count in sorted_pairs:
        print(f"   '{c1}{c2}': {count}次")
    
    print("\n3. 合并最频繁的字符对 'lo':")
    print("   发现 'l' + 'o' 经常出现，合并成 'lo'")
    
    print("\n4. 新的词汇表:")
    new_vocab = initial_vocab | {'lo'}  # 添加新token
    print(f"   {sorted(new_vocab)}")
    
    print("\n5. 用新词汇表重新分词:")
    test_words = ["low", "lower", "newest", "widest"]
    for word in test_words:
        if word.startswith("lo"):
            segmentation = ["lo", word[2:]] if len(word) > 2 else ["lo"]
        else:
            segmentation = list(word)
        print(f"   '{word}' → {segmentation}")

if __name__ == "__main__":
    manual_bpe_demo()
