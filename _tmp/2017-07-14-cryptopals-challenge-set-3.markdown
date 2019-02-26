---
layout: post
title:  "Cryptopals Set 3"
date:   2017-07-14 12:00:00 +0100
has_code: true
time_to_read: 12
---

Welcome to the third installment of my [Cryptopals Challenges](http://cryptopals.com/) mini-series / walkthrough! Some challenges focus on [block cipher cryptography](https://en.wikipedia.org/wiki/Block_cipher) (as before) and others focus on [stream ciphers](https://en.wikipedia.org/wiki/Stream_cipher). As always, I highly recommend reading previous challenge sets before this one. I often refer back to previous solutions!

#### Cryptopals Sets: ####
- [Set 1: Basics]({% post_url 2017-04-20-cryptopals-challenge-set-1 %})
- [Set 2: Block crypto]({% post_url 2017-05-13-cryptopals-challenge-set-2%})
- [Set 3: Block and stream crypto]({% post_url 2017-07-14-cryptopals-challenge-set-3%}) &nbsp;&nbsp;&nbsp;←
- <span class="dead-link">Set 4: Stream crypto and randomness</span>
- <span class="dead-link">Set 5: Diffie-Hellman and friends</span>
- <span class="dead-link">Set 6: RSA and DSA</span>
- <span class="dead-link">Set 7: Hashes </span>
- <span class="dead-link">Set 8: Abstract Algebra</span>

<b>Warning:</b> There are spoilers (solutions) below!

<iframe class="youtube-video center-media" src="https://www.youtube.com/embed/rog8ou-ZepE" frameborder="0" allowfullscreen></iframe>
<p class="image-label">This one again?!</p>

<h3 id="17-cbc-padding-oracle">
  17. The CBC padding oracle
</h3>

The first part of this exercise asks us to write a function to pad and encrypt a random string in a set of given plaintexts and to write a function that checks the padding of the plaintext given the ciphertext, iv and key.

{% highlight python %}
input_strings = [
    "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
    "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
    "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
    "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93",
]

rand_key = None

# Slight modification of the previously defined aes_128_cbc_dec function.
# We don't unpad the decrypted ciphertext in this method.
def aes_128_cbc_dec(ciphertext, key, iv):
    plaintext = bytearray(len(ciphertext))
    prev_block = iv
    for i in range(0, len(ciphertext), AES.block_size):
        plaintext[i: i + AES.block_size] = xor(
            aes_128_ecb_dec(bytes(ciphertext[i: i + AES.block_size]), key),
            prev_block
        )
        prev_block = ciphertext[i: i + AES.block_size]
    return plaintext

def cbc_enc_random_string(input_strings):
    global rand_key
    rand_key = random_key(AES.block_size)
    input_string = input_strings[randint(0, len(input_strings) - 1)]
    iv = random_key(AES.block_size)
    return aes_128_cbc_enc(input_string, bytes(rand_key), iv), iv

def padding_oracle(ciphertext, iv):
    input_string = aes_128_cbc_dec(ciphertext, bytes(rand_key), iv)
    try:
        unpad_valid_pkcs7(input_string)
        return True
    except:
        return False
{% endhighlight %}

The existence of a padding oracle lets us decrypt the ciphertext! We can corrupt specific bytes within a ciphertext block to discover the associated byte within the plaintext block! A good description (which I used) of the [padding oracle attack](https://en.wikipedia.org/wiki/Padding_oracle_attack) can be found on Wikipedia.

For example, lets say we have `N` ciphertext blocks. We can decrypt the second block by corrupting the first block like so:

1. Let the last byte in the ciphertext block `C_1` be `c_1_15`. Corrupt `C_1` so that `c_1_15 = c_1_15 ⊕ gp_2_15 ⊕ 0x01` where `gp_2_15` is our guess for the last byte in the second plaintext block called `p_2_15` (`⊕` is the XOR sign).
2. If our guess for `p_2_15` is correct, when we decrypt the `C_1|C_2`, the byte `p_2_15` will likely `0x01` and will have valid padding. There is a possibility that `p_2_15` is `0x02` and `p_2_14` is also `0x02`, which would produce a valid padding, but it's less likely.
3. If our guess in incorrect, try the other 254 possibilities for `p_2_15` until the padding succeeds!
4. Now corrupt `c_1_14 = c_1_14 ⊕ gp_2_14 ⊕ 0x02` and `c_1_15 = c_1_15 ⊕ gp_2_15 ⊕ 0x02`. In the unlikely even that we incorrectly guessed `p_2_15`, we should notice the mistake in this step and we can go back to step 2.
5. Keep on going until we have correctly guessed the whole block!
6. Now do the same for the third block by corrupting the second block and decrypting `C_1|C_2|C_3`! We actually only need to decrypt `C_2|C_3`!

**Note:** We can decrypt the first ciphertext block by corrupting the `IV` block.

This problem was quite tricky and I discovered one or two bugs in previous
padding code! Here's my solution:

{% highlight python %}
def crack_block(block, iv):
    plaintext_block = bytearray()
    start_guess = 0
    while len(plaintext_block) < AES.block_size:
        for guess in range(start_guess, 256):
            padding = len(plaintext_block) + 1
            # Copy the IV so we don't corrupt it for future guesses
            corrupted_iv = bytearray(iv)
            for byte in range(1, padding + 1):
                # Use the "correct" guesses of plaintext block bytes
                if byte < padding:
                    corrupted_iv[-byte] =  bytes(xor(
                        xor(
                            bytearray([iv[-byte]]),
                            bytearray(chr(plaintext_block[-byte]))
                        ),
                        bytearray(chr(padding))
                    ))
                # Guess the correct byte
                else:
                    corrupted_iv[-byte] =  bytes(xor(
                        xor(bytearray([iv[-byte]]), bytearray(chr(guess))),
                        bytearray(chr(padding))
                    ))
            if padding_oracle(block, corrupted_iv):
                # If the padding oracle doesn't complain... we've guessed the
                # correct byte!
                plaintext_block = bytearray(chr(guess)) + plaintext_block
                start_guess = 0
                break
        else:
            # If we cannot find a correct padding, the guess for the previous
            # byte was incorrect... so try another one!
            try:
                start_guess = int(plaintext_block[0]) + 1
                plaintext_block = plaintext_block[1:]
            except:
                # This occurs if the last ciphertext block is just a padding
                # block... I don't know why my encryption is sometimes adding
                # an extra block
                return bytearray()
    return plaintext_block

def crack(ciphertext, iv):
    ciphertext = iv + ciphertext
    plaintext = ''
    for i in range(len(ciphertext) / AES.block_size):
        # We only really need to pass two blocks to the padding oracle...
        # The block to the decrypt, and the one before it which we corrupt
        plaintext += crack_block(
            ciphertext[(i + 1) * AES.block_size: (i + 2) * AES.block_size],
            ciphertext[i * AES.block_size: (i + 1) * AES.block_size]
        )
    return unpad_valid_pkcs7(plaintext)

ciphertext, iv = cbc_enc_random_string(input_strings)
plaintext = crack(ciphertext, iv)
print plaintext
{% endhighlight %}

<b>Update</b> (28 Nov 2017): The crack method above should instead iterate over every block in the original ciphertext (i.e. `range(len(ciphertext) / AES.block_size - 1)`). The code above incorrectly iterates over the `iv` as well. Credit to Doug Friedman for pointing this bug out and providing the solution.

<h3 id="18-implement-ctr">
  18. Implement CTR, the stream cipher mode
</h3>

This challenge involves implementing the [CTR encryption mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Counter_.28CTR.29) (otherwise known as **COUNTER** mode for good reason). I'm not going to explain how it works as the challenge does a good job of doing that. However, remember to decode the ciphertext provided!

My implementation uses AES in ECB mode to create the keystream. This wasn't clear in the challenge description but it produced the correct answer.

{% highlight python %}
def aes_128_ctr_keystream_block(key, nonce, block_count):
    return aes_128_ecb_enc(
        # '<Q' format is a little endian unsigned long long (64 bits)
        bytearray(pack('<Q', nonce)) + bytearray(pack('<Q', block_count)),
        key
    )

def aes_128_ctr_keystream_generator(key, nonce):
    block_count = 0
    while True:
        x = aes_128_ctr_keystream_block(bytes(key), nonce, block_count) 
        for byte in x:
            yield byte
        block_count += 1

def aes_128_ctr(buffer, key, nonce):
    def xor(b1, b2):
        b = bytearray()
        for byte in b1:
            # Note, we need to use b2.next() as it's a generator
            b.append(ord(byte) ^ b2.next())
        return b
    return xor(buffer, aes_128_ctr_keystream_generator(key, nonce))

# Don't forget to decode this string!
ciphertext = bytearray("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==").decode("base64")
print aes_128_ctr(
    ciphertext,
    pad_pkcs7(bytearray("YELLOW SUBMARINE"), AES.block_size),
    0
)
# Yo, VIP Let's kick it Ice, Ice, baby Ice, Ice, baby
{% endhighlight %}

<h3 id="19-break-fixed-nonce-ctr-mode-using-substitutions">
  19. Break fixed-nonce CTR mode using substitutions
</h3>

This problem teaches us how to break encryption in CTR mode if the nonce and key used is the same for multiple ciphertexts.

My "solution" involved guessing keystream bytes and decrypting (XOR'ing) respective ciphertext bytes. I compared byte `N` across each ciphertext and determined the most likely guess based on English letter frequencies. Unfortunately, as each ciphertext had different lengths, the last few characters of my keystream guess were incorrect!

{% highlight python %}
def crack_keystream(ciphertexts):
    keystream = bytearray()
    max_ciphertext_length = max(map(len, ciphertexts))
    for i in range(max_ciphertext_length):
        bytes_at_index = map(
            ord, # Convert bytes to ints for XOR'ing
            filter(
                lambda x: x, # Filter out empty bytes
                map(
                    lambda x: x[i:i + 1], # Try to get the byte at i index
                    ciphertexts
                )
            )
        )
        max_score = None
        key = None
        for guess in range(256):
            b2 = [guess] * len(bytes_at_index)
            decrypted_bytes = bytes(xor(bytes_at_index, b2))
            pscore = score(decrypted_bytes)
            if pscore > max_score or not max_score:
                max_score = pscore
                key = chr(guess)
        keystream.append(key)
    return keystream

key = random_key(AES.block_size)
FIXED_NONCE = 0
ciphertexts = []
for encoded_plaintext in list(open("19.txt", "r")):
    plaintext = bytearray(encoded_plaintext).decode("base64")
    ciphertexts.append(aes_128_ctr(plaintext, key, FIXED_NONCE))

keystream = crack_keystream(ciphertexts)
for ciphertext in ciphertexts:
    print xor(ciphertext, keystream)
# i have met them at close of dau                            
# coming with vivid faces                                    
# from counter or desk among greu                            
# eighteenth-century houses.                                 
# i have passed with a nod of thidhi 6                       
# or polite meaningless words,                               
# or have lingered awhile and sae                            
# polite meaningless words,                                  
# and thought before I had done                              
# of a mocking tale or a gibe                                
# to please a companion                                      
# around the fire at the club,                               
# being certain that they and I                              
# but lived where motley is worn6                            
# all changed, changed utterly:                              
# a terrible beauty is born.                                 
# that woman's days were spent                               
# in ignorant good will,                                     
# her nights in argument                                     
# until her voice grew shrill.                               
# what voice more sweet than her                             
# when young and beautiful,                                  
# she rode to harriers?                                      
# this man had kept a school                                 
# and rode our winged horse.                                 
# this other his helper and frieb                            
# was coming into his force;                                 
# he might have won fame in the i*d                          
# so sensitive his nature seemed                             
# so daring and sweet his thoughxj                           
# this other man I had dreamed                               
# a drunken, vain-glorious lout.                             
# he had done most bitter wrong                              
# to some who are near my heart,                             
# yet I number him in the song;                              
# he, too, has resigned his part                             
# in the casual comedy;                                      
# he, too, has been changed in he7 x4                        
# transformed utterly:                                       
# a terrible beauty is born.
{% endhighlight %} 

**Note:** On a more serious note (sorry Vanilla), the text provided is the [Easter, 1916](https://en.wikipedia.org/wiki/Easter,_1916) poem by [W. B. Yeats](https://en.wikipedia.org/wiki/W._B._Yeats).

I'm pretty sure this could be avoided using common English 2/3-grams. Unfortunately, I'm lazy so let's move on...

<h3 id="20-break-fixed-nonce-ctr-statistically">
  20. Break fixed-nonce CTR statistically
</h3>

Ok, so mistakes were made! I actually solved this (in a sense), in [exercise 19](#19-break-fixed-nonce-ctr-mode-using-substitutions). I should have done it manually in exercise 19 and statistically now. Let's do it slightly differently using our solution from [exercise 6]({% post_url 2017-04-20-cryptopals-challenge-set-1%}#6-breaking-repeating-key-xor)!

Unfortunately, I still get the same error where my key is slightly wrong but I think this is due to my crappy 'score' algorithm which scores a piece of text based on how close it is to English.

{% highlight python %}
key = random_key(AES.block_size)
FIXED_NONCE = 0
ciphertexts = []
for encoded_plaintext in list(open("20.txt", "r")):
    plaintext = bytearray(encoded_plaintext).decode("base64")
    ciphertexts.append(aes_128_ctr(plaintext, key, FIXED_NONCE))

# Trim the ciphertexts to the length of the least long one
min_ciphertext_length = min(map(len, ciphertexts))
ciphertexts = [bytes(ciphertext[:min_ciphertext_length]) for ciphertext in ciphertexts]
b = bytearray("".join(ciphertexts))
print repr(b)

block_bytes = [[] for _ in range(min_ciphertext_length)]
for i, byte in enumerate(b):
    block_bytes[i % min_ciphertext_length].append(byte)

keys = ""
for bbytes in block_bytes:
    keys += break_single_key_xor(bbytes)[0]
key = bytearray(keys * len(b))
plaintext = bytes(xor(b, key))

print plaintext
# N'm rated "R"...this is a warning, ya better void / PDuz I came back to attack others in spite- ...
{% endhighlight %}

**Note:** My plaintext is printed as one long string if I use code from [exercise 6]({% post_url 2017-04-20-cryptopals-challenge-set-1%}#6-breaking-repeating-key-xor) so I truncated it slightly. Fixing this is left as a exercise for the reader.

<h3 id="21-implement-mt19937-mersenne-twister-rng">
  21. Implement the MT19937 Mersenne Twister RNG
</h3>

This exercise asks the victim (me) to implement the [Mersenne Twister RNG](https://en.wikipedia.org/wiki/Mersenne_Twister), the most widely used general-purpose [pseudorandom number generator](https://en.wikipedia.org/wiki/Pseudorandom_number_generator). We're instructed to use the pseudo-code from the [Wikipedia article](https://en.wikipedia.org/wiki/Mersenne_Twister) but since it already provides a Python implementation, I'm using that. Next! 

(I feel like I've been cheating quite a bit in this set of challenges eee).

<h3 id="22-crack-an-mt19937-seed">
  22. Crack an MT19937 seed
</h3>

In this challenge, we crack a MT19937 seed! However, our cracking program assumes that the random numbers generated are seeded with a UNIX timestamp. Realistically, I believe a lot of people out there will seed their PRNGs with the current system time so this seems like a realistic attack. I decided to brute force this!

{% highlight python %}
seed = None

def get_rand_int():
    # Use Python's PRNG to sleep for a random time period
    sleep(randint(40, 1000))
    # For testing purposes
    global seed
    seed = int(time())
    rand_int = MT19937(seed).extract_number()
    sleep(randint(40, 1000))
    return rand_int

def crack_seed():
    rand_int = get_rand_int()
    current_time = int(time())
    for seed in range(current_time, current_time - 2500, -1):
        if MT19937(seed).extract_number() == rand_int:
            return seed
    raise Exception('Could not crack MT19937 seed.')

print crack_seed()
# 1499970065
{% endhighlight %}

<h3 id="23-clone-mt19937-rng-from-output">
  23. Clone an MT19937 RNG from its output
</h3>

In this exercise, we copy a MT19937 PRNG! Essentially, we can copy the state of an existing MT19937 by observing 624 consecutive generated random numbers and "untemper-ing" them! Attackers can learn what your PRNG will produce in the future using this method!

I admit, struggled quite a bit with the untempering aspect of this question as it involves inverting functions in the form: `f(x) = x >> 18` (not so hard) and the function `g(x) = x >> 15 & 4022730752`. I adapted an existing algorithm [shared by James Roper](https://jazzy.id.au/2010/09/22/cracking_random_number_generators_part_3.html) for the second form of functions.

{% highlight python %}
def unshift_right_xor(value, shift):
    result = 0
    for i in range(32 / shift + 1):
        result ^= value >> (shift * i)
    return result

# Borrowed from https://jazzy.id.au/2010/09/22/cracking_random_number_generators_part_3.html
def unshift_left_mask_xor(value, shift, mask):
    result = 0
    for i in range(0, 32 / shift + 1):
        part_mask = (0xffffffff >> (32 - shift)) << (shift * i)
        part = value & part_mask
        value ^= (part << shift) & mask
        result |= part
    return result

def untemper(y):
    value = y
    value = unshift_right_xor(value, 18)
    value = unshift_left_mask_xor(value, 15, 4022730752)
    value = unshift_left_mask_xor(value, 7, 2636928640)
    value = unshift_right_xor(value, 11)
    assert temper(value) == y
    return value

def copy_MT19937_prng(prng):
    untempered_values = []
    for i in range(624):
        untempered_values.append(untemper(prng.extract_number()))
    copied_prng = MT19937.create_from_state(untempered_values)
    return copied_prng

def assert_prngs_equal(prng1, prng2):
    for _ in range(1000):
        assert prng1.extract_number() == prng2.extract_number()

prng = MT19937(19) # Arbitrary seed
copied_prng = copy_MT19937_prng(prng)
assert_prngs_equal(prng, copied_prng)
{% endhighlight %}

**Note:** The method `MT19937.create_from_state` initializes a new `MT19937` object with the provided internal state!

<h3 id="24-create-mt19937-stream-cipher-and-break-it">
  24. Create the MT19937 stream cipher and break it
</h3>

Ok, we're at the last exercise in this set of challenges! In this exercise we're tasked with writing a (broken) stream cipher that's based on the MT19937 PRNG and then breaking it. First things first, let's create the stream cipher!

{% highlight python %}
def trivial_keystream_generator(seed):
    prng = MT19937(seed)
    while True:
        # Generate bytes
        yield prng.extract_number() % pow(2, 8)

def trivial_stream_cipher(buffer, seed):
    def xor(b1, b2):
        b = bytearray()
        for byte in b1:
            b.append(byte ^ b2.next())
        return b
    return xor(buffer, trivial_keystream_generator(seed))

plaintext = bytearray("MY NAME IS MICHAEL")
# Create a 16-bit seed
seed = randint(0, pow(2, 16))
ciphertext = trivial_stream_cipher(plaintext, seed)
assert plaintext == trivial_stream_cipher(ciphertext, seed)
{% endhighlight %}

Now that that's done, we're tasked with encrypting a known plaintext prefixed with a random number of random characters and from it's ciphertext, we need to recover the 16-bit seed (the "key").

Since the seed is only 16-bits long, I decided to brute force it. If I missed the point of this sub-exercise, I apologise.

{% highlight python %}
def crack(ciphertext):
    for seed in range(pow(2, 16)):
        possible_plaintext = trivial_stream_cipher(ciphertext, seed)
        if possible_plaintext[-14:] == bytearray(["A"] * 14):
            return seed

plaintext = random_key(randint(0, 256)) + bytearray(["A"] * 14)
seed = randint(0, pow(2, 16))
ciphertext = trivial_stream_cipher(plaintext, seed)
assert seed == crack(ciphertext)
{% endhighlight %}

The last part is quite similar but I'm not sure if I quite understood the task at hand (it seems too simple and doesn't seem to reveal any glaring attacks). Please let me know if you think I've missed the point with my solution.

{% highlight python %}
def password_token_product_of_MT19937(password_token):
    current_time = int(time())
    MIN_IN_SEC = 60
    # Assume the password token was generated within the last 10 minutes
    for seed in range(current_time - 10 * MIN_IN_SEC, current_time):
        # Try extracting 1000 random numbers from the PRNG
        prng = MT19937(seed)
        for _ in range(1000):
            if password_token == prng.extract_number():
                return True
    return False

prng = MT19937(int(time()))
for _ in range(randint(0, 1000)):
    password_token = prng.extract_number()
assert password_token_product_of_MT19937(password_token)
{% endhighlight %}

### Fin

Another set of challenges done! I'm not too sure if I understood the point behind many of the exercises in this set so I would really appreciate any feedback! I think the [CBC padding oracle exercise](#17-cbc-padding-oracle) was my favourite and probably the most difficult. I also think this write-up was more casual and like a stream of thoughts than the previous two. I didn't think there was that much to explain this time...

Anyway, I hope you enjoyed and stay tuned for the next set!
