---
layout: post
title:  "Cryptopals Set 1"
date:   2017-04-21 09:00:00 +0100
time_to_read: 8
has_code: true
has_math: true
redirect_from: 2017/04/21/cryptopals-challenge-set-1.html
---

This is the start of a mini-series where I walk through the [Cryptopals Challenges](http://cryptopals.com/). There are 8 sets of exercises and I'll be tackling 1 per blog post. If you've already completed the challenges, this series might be useful for comparison (let me know if you have any suggestions).

#### Cryptopals Sets: ####
- [Set 1: Basics]({% post_url 2017-04-20-cryptopals-challenge-set-1 %}) &nbsp;&nbsp;&nbsp;←
- [Set 2: Block crypto]({% post_url 2017-05-13-cryptopals-challenge-set-2%})
- [Set 3: Block and stream crypto]({% post_url 2017-07-14-cryptopals-challenge-set-3%})
- <span class="dead-link">Set 4: Stream crypto and randomness</span>
- <span class="dead-link">Set 5: Diffie-Hellman and friends</span>
- <span class="dead-link">Set 6: RSA and DSA</span>
- <span class="dead-link">Set 7: Hashes </span>
- <span class="dead-link">Set 8: Abstract Algebra</span>

I've chosen to do them in Python 2, but many of the solutions should also work for Python 3. I'm doing this to better grasp practical cryptography attacks.

<b>Warning:</b> There are spoilers (solutions) below!

<iframe class="youtube-video center-media" src="https://www.youtube.com/embed/rog8ou-ZepE" frameborder="0" allowfullscreen></iframe>
<p class="image-label">A very relevant music video</p>

<h3 id="1-convert-hex-to-base64">
  1. Convert hex to base64
</h3>

The very first exercise is to convert a hexadecimal string to base64. This is a trivial task using Python.

{% highlight python %}
hex_str = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
decoded = hex_str.decode("hex")
# I'm killing your brain like a poisonous mushroom
base64_str = decoded.encode("base64")
# SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t\n
{% endhighlight %}

<h3 id="2-fixed-xor">
  2. Fixed XOR
</h3>

The second exercise is to "write a function that takes two equal-length buffers and produces their XOR combination".

The exercise provides hexadecimal strings as input so we must convert them to the raw byte representation in order to XOR them. I converted them to bytearrays but there may be a better Python type. Then, we just XOR each byte using Python's in build XOR operator `^`.

{% highlight python %}

def xor(b1, b2):
    b = bytearray(len(b1))
    for i in range(len(b1)):
        b[i] = b1[i] ^ b2[i]
    return b

b1 = bytearray.fromhex("1c0111001f010100061a024b53535009181c")
b2 = bytearray.fromhex("686974207468652062756c6c277320657965")

b = bytes(xor(b1, b2))
# the kid don’t play

b.encode("hex")
# 746865206b696420646f6e277420706c6179
{% endhighlight %}

<h3 id="3-single-byte-xor-cipher">
  3. Single-byte XOR cipher
</h3>

This is when the Cryptopals Challenge starts to get interesting! In this exercise, the plaintext has been encrypted with one character (known as a [Caesar cipher](https://en.wikipedia.org/wiki/Caesar_cipher")). The goal is to find this character (the key), given a ciphertext provided in hexadecimal.

There are not many ASCII characters (only 256 to be exact) so I just tried all combinations. For each key, I decrypted the ciphertext to get a plaintext and I scored that plaintext based on the likelihood it was in English. I did this by looking at the character frequency of the plaintext and comparing it to the character frequency of the [English language](http://www.cryptograms.org/letter-frequencies.php#Letters"). This obviously only works against English plaintexts.

The code below is a simplified version of the [original version](https://gist.github.com/mikeecb/0d75f46521fe526a0138ae5265392505).

{% highlight python %}
def score(s):
    # Hacky (and incorrect) way to determine whether a piece of text is in english.
    freq = {}
    freq[' '] = 700000000
    freq['e'] = 390395169
    freq['t'] = 282039486
    freq['a'] = 248362256
    freq['o'] = 235661502
    # ...
    freq['z'] = 2456495
    score = 0
    for c in s.lower():
        if c in freq:
            score += freq[c]
    return score

def break_single_key_xor(b1):
    max_score = None
    english_plaintext = None
    key = None

    for i in range(256):
        b2 = [i] * len(b1)
        plaintext = bytes(xor(b1, b2))
        pscore = score(plaintext)

        if pscore > max_score or not max_score:
            max_score = pscore
            english_plaintext = plaintext
            key = chr(i)
    return key, english_plaintext

b1 = bytearray.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
print break_single_key_xor(b1)
# ('X', "Cooking MC's like a pound of bacon")
{% endhighlight %}

<h3 id="4-detect-single-character-xor">
  4. Detect single-character XOR
</h3>

This question is a rehash of the previous question. Instead of finding the most likely plaintext possible given one ciphertext, we are given 60 ciphertexts.

The code below is a simplified version of the [original version](https://gist.github.com/mikeecb/e26a56ba2200563b803e428a0ca4ea1b).

{% highlight python %}
max_score = None
english_plaintext = None
key = None

# The ciphertexts are provided in a file named 4.txt
for line in open("4.txt", "r"):
    line = line.rstrip()
    b1 = bytearray.fromhex(line)

    for i in range(256):
        b2 = [i] * len(b1)
        plaintext = bytes(xor(b1, b2))
        pscore = score(plaintext)

        if pscore > max_score or not max_score:
            max_score = pscore
            english_plaintext = plaintext
            key = chr(i)

print key, english_plaintext
# 5 Now that the party is jumping
{% endhighlight %}

<h3 id="5-implement-repeating-key-xor">
  5. Implement repeating-key XOR
</h3>

In this exercise, we are asked to encrypt a piece of text with a repeating-key (a [Vigenère cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher")). This was fairly simple to achieve using code from previous questions.

The code below is a simplified version of the [original version](https://gist.github.com/mikeecb/ba92f9db295225da2b0c62de828b5fa8).

{% highlight python %}
lines = [
    "Burning 'em, if you ain't quick and nimble\n",
    "I go crazy when I hear a cymbal",
]

text = "".join(lines)
key = bytearray("ICE" * len(text))
plaintext = bytes(xor(bytearray(text), key))
plaintext.encode("hex")
# 0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f
{% endhighlight %}

<h3 id="6-breaking-repeating-key-xor">
  6. Break repeating-key XOR
</h3>

When I said "this is when the Cryptopals Challenge starts to get interesting!" in [exercise 3](#3-single-byte-xor-cipher), I was wrong. It actually becomes interesting now! Let's break a Vigenère cipher!

#### Hamming distance ####

The first subtask is to write a function to determine the Hamming distance (distance is just the number of differing bits) between two encoded strings. A nice property (or is it the definition?) of XOR, is that the result of XOR'ing two bits is 1 if and only if they are different. We can therefore determine the Hamming distance between two strings by XOR'ing them (using the function we previously created) and counting up the number of 1 bits.

{% highlight python %}
def hamming_distance(enc_str1, enc_str2):
    differing_bits = 0
    for byte in xor(b1, b2):
        differing_bits += bin(byte).count("1")
    return differing_bits

b1 = bytearray("this is a test")
b2 = bytearray("wokka wokka!!!")

hamming_distance(b1, b2)
# 37
{% endhighlight %}

#### Determining likely key sizes ####

To break a Vigenère cipher, we need to determine the key and to do that we must first determine the key size. We can use the normalized Hamming distance between ciphertext blocks (groups of bytes of key size length) to guess the key size. The key size with the smallest normalized Hamming distance is probably the actual key size used. Using this heuristic, we discover the most likely key size is 2 bytes (followed by 3 bytes and then 29 bytes) for the ciphertext provided.

This works because the bits of the plaintext are generally not uniformly random (e.g. if the plaintext is some English text) and the Hamming distance between two English characters is typically smaller than that between two random bytes (e.g. ~2-3 vs ~4).

Let's take two ciphertext blocks `c1`, `c2`. If we have chosen the correct key size, then `c1 = p1 ⊕ k` and `c2 = p1 ⊕ k` where `p1`, `p2` are they plaintext blocks' respective plaintext blocks and `k` is the key. The normalized Hamming distance between the two blocks tends to the normalized Hamming distance between `p1` and `p2` (~2-3). If the key size is incorrect, then `c1 = p1 ⊕ k1` and `c2 = p1 ⊕ k2` where `p1`, `p2` are they plaintext blocks' as before and `k1` and `k2` are separate different keys. The normalized Hamming distance between the two blocks tends to the normalized Hamming distance between two random bytes (~4).

Still confused? Check out this [stackoverflow answer](https://crypto.stackexchange.com/questions/8115/repeating-key-xor-and-hamming-distance).

{% highlight python %}
# The ciphertext is provided in a file named 6.txt
b = bytearray("".join(list(open("6.txt", "r"))).decode("base64"))

normalized_distances = []
for KEYSIZE in range(2, 40):
    b1 = b[: KEYSIZE]
    b2 = b[KEYSIZE: KEYSIZE * 2]
    b3 = b[KEYSIZE * 2: KEYSIZE * 3]
    b4 = b[KEYSIZE * 3: KEYSIZE * 4]

    normalized_distance = float(
        hamming_distance(b1, b2) +
        hamming_distance(b2, b3) +
        hamming_distance(b3, b4)
    ) / (KEYSIZE * 3)

    normalized_distances.append(
        (KEYSIZE, normalized_distance)
    )

normalized_distances = sorted(normalized_distances, key=lambda (\_, y): y)
# [(2, 2.0), (3, 2.6666666666666665), (29, 2.793103448275862), ...]
{% endhighlight %}

<b>Note</b>: Don't forget to decode the ciphertext from base64! I spent way too long trying to fix that bug.

#### Putting it all together ####

Now that we have a list of potential key sizes ordered by likelihood, we can go through each and see if it is the correct one.

We can turn this Vigenère cipher problem into `N` Caesar cipher problems where `N = KEYSIZE`. To find each byte of the key, we find the bytes of the ciphertext that were encrypted by that key byte and compute the key byte using the function we used to break the Caesar cipher in [exercise 3](#3-single-byte-xor-cipher).

Once we have the entire key (it's "Terminator X: Bring the noise" by the way), we can decrypt the ciphertext using the same method we used to performed encryption in [exercise 5](#5-implement-repeating-key-xor) (XOR is it's own inverse).

The code below is a simplified version of the [original version](https://gist.github.com/mikeecb/e4a0ac51c74a1f3252220c4c36817510).

{% highlight python %}

for KEYSIZE, _ in normalized_distances[:5]:
    block_bytes = [[] for _ in range(KEYSIZE)]
    for i, byte in enumerate(b):
        block_bytes[i % KEYSIZE].append(byte)

    keys = ""
    for bbytes in block_bytes:
        keys += break_single_key_xor(bbytes)[0]

    key = bytearray(keys * len(b))
    plaintext = bytes(xor(b, key))

    print keys
    print KEYSIZE
    print plaintext

# Some nonsense ...

# Terminator X: Bring the noise
# 29
# I'm back and I'm ringin' the bell
# A rockin' on the mike while the fly girls yell
# In ecstasy in the back of me
# Well that's my DJ Deshay cuttin' all them Z's
# Hittin' hard and the girlies goin' crazy
# Vanilla's on the mike, man I'm not lazy.
#
# I'm lettin' my drug kick in
# It controls my mouth and I begin
# To just let it flow, let my concepts go
# My posse's to the side yellin', Go Vanilla Go!
# ...

# More nonsense ...
{% endhighlight %}

<h3 id="7-aes-in-ecb-mode">
  7. AES in ECB mode
</h3>

The last two exercises in this set involve working with a real encryption standard, [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) (although [ECB mode](https://crypto.stackexchange.com/questions/20941/why-shouldnt-i-use-ecb-encryption) is hopefully not used as it's insecure)! I'll discuss ECB mode further in the next exercise, where we have to break AES in ECB mode, but for this one, let's just decrypt a given ciphertext.

By the way, we are told the ciphertext is encrypted using AES-128 which means the blocks are 128 bits long.

{% highlight python %}
from Crypto.Cipher import AES

obj = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
# The ciphertext is provided in a file named 7.txt
ciphertext = "".join(list(open("7.txt", "r"))).decode("base64")
plaintext = obj.decrypt(ciphertext)
# I'm back and I'm ringin' the bell
# A rockin' on the mike while the fly girls yell
# In ecstasy in the back of me
# Well that's my DJ Deshay cuttin' all them Z's
# Hittin' hard and the girlies goin' crazy
# Vanilla's on the mike, man I'm not lazy.
#
# I'm lettin' my drug kick in
# It controls my mouth and I begin
# To just let it flow, let my concepts go
# My posse's to the side yellin', Go Vanilla Go!
# ...
{% endhighlight %}

<b>Note:</b> I used the [pycrypto](https://pypi.python.org/pypi/pycrypto) module but had a few `import` issues on my MacBook when installed using pip. If you have similar issues, have a look at this [stackoverflow answer](https://stackoverflow.com/questions/19623267/importerror-no-module-named-crypto-cipher#20968427).

<h3 id="8-detect-aes-in-ecb-mode">
  8. Detect AES in ECB mode
</h3>

We've made it to the last exercise (in the first set)! The rest of the exercises built up to this one. Let's get started.

#### Electronic Codebook (ECB) mode ####

[ECB mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_Codebook_.28ECB.29) is one of simplest block cipher mode of operation. The plaintext is divided into blocks of a fixed size and each block is encrypted separately. Decryption is performed in a similar fashion.

The disadvantage of this mode is that identical plaintext blocks are encrypted to identical ciphertext blocks. This gives attackers information about patterns in the plaintext.

Ciphertexts that have many repeating identical blocks are therefore very likely to have been encrypted using ECB mode. We can use this information to solve this exercise. The task is to find which hexadecimal string in a file is most likely to be a ciphertext encrypted using AES in ECB mode.

{% highlight python %}
from collections import defaultdict

def repeated_blocks(buffer, block_length=16):
    reps = defaultdict(lambda: -1)
    for i in range(0, len(buffer), block_length):
        block = bytes(buffer[i:i + block_length])
        reps[block] += 1
    return sum(reps.values())

max_reps = 0
ecb_ciphertext = None

# The ciphertext is provided in a file named 8.txt
for ciphertext in list(open("8.txt", "r")):
    ciphertext = ciphertext.rstrip()
    reps = repeated_blocks(bytearray(ciphertext))
    if reps > max_reps:
        max_reps = reps
        ecb_ciphertext = ciphertext

ecb_ciphertext
# d880619740a8a19b7840a8a31c810a3d08649af70dc06f4fd5d2d69c744cd283e2dd052f6b641dbf9d11b0348542bb5708649af70dc06f4fd5d2d69c744cd2839475c9dfdbc1d46597949d9c7e82bf5a08649af70dc06f4fd5d2d69c744cd28397a93eab8d6aecd566489154789a6b0308649af70dc06f4fd5d2d69c744cd283d403180c98c8f6db1f2a3f9c4040deb0ab51b29933f2c123c58386b06fba186a
{% endhighlight %}

<b>Note:</b> Although we didn't break the ciphertext (by discovering the key or plaintext), we at least know the mode it was encrypted in.

### Fin ###

That's it! I hope you enjoyed walking through the first set of Cryptopals Challenges. Want to keep going? Read through the [second set]({% post_url 2017-05-13-cryptopals-challenge-set-2%}) of exercises.
