---
layout: post
title:  "Cryptopals Set 2"
date:   2017-05-13 12:00:00 +0100
time_to_read: 15
has_code: true
redirect_from: 2017/05/13/cryptopals-challenge-set-2.html
---

This is the second installment of a mini-series where I walk through the [Cryptopals Challenges](http://cryptopals.com/). This challenge focuses on [block cipher cryptography](https://en.wikipedia.org/wiki/Block_cipher). I suggest reading previous walk-through posts before reading this one.

#### Cryptopals Sets: ####
- [Set 1: Basics]({% post_url 2017-04-20-cryptopals-challenge-set-1 %})
- [Set 2: Block crypto]({% post_url 2017-05-13-cryptopals-challenge-set-2%}) &nbsp;&nbsp;&nbsp;←
- [Set 3: Block and stream crypto]({% post_url 2017-07-14-cryptopals-challenge-set-3%})
- <span class="dead-link">Set 4: Stream crypto and randomness</span>
- <span class="dead-link">Set 5: Diffie-Hellman and friends</span>
- <span class="dead-link">Set 6: RSA and DSA</span>
- <span class="dead-link">Set 7: Hashes </span>
- <span class="dead-link">Set 8: Abstract Algebra</span>

<b>Warning:</b> There are spoilers (solutions) below!

<iframe class="youtube-video center-media" src="https://www.youtube.com/embed/zNJ8_Dh3Onk" frameborder="0" allowfullscreen></iframe>
<p class="image-label">Another extremely relevant music video</p>

<h3 id="9-implement-pkcs7-padding">
  9. Implement PKCS#7 padding
</h3>

Block ciphers work by encrypting single blocks of plaintext or decrypting single blocks of ciphertext. However, most messages we want to encrypt are irregularly sized and need to be padded to be a multiple the block size (usually 8 or 16 bytes).

This exercise asks us to implement [PKCS#7](https://tools.ietf.org/html/rfc2315) padding. In PKCS#7, we append a byte representing the number `N`, `N` times to the end of buffer such that the buffer length is a multiple of the block size. Notice that this PKCS#7 does not work with blocks of size greater than 255.

{% highlight python %}
def pad_pkcs7(buffer, block_size):
    if len(buffer) % block_size:
        padding = (len(buffer) / block_size + 1) * block_size - len(buffer)
    else:
        padding = 0
    # Padding size must be less than a byte
    assert 0 <= padding <= 255
    new_buffer = bytearray()
    new_buffer[:] = buffer
    new_buffer += bytearray([chr(padding)] * padding)
    return new_buffer

buffer = bytearray("YELLOW SUBMARINE")
pad_pkcs7(buffer, 20)
# bytearray(b'YELLOW SUBMARINE\x04\x04\x04\x04')
{% endhighlight %}

#### Unpad PKCS#7 ####

We're going to need an inverse function to "unpad" a potentially padded buffer later on, so let's just write one up now.

Remember, if there are not `N` bytes, each representing the number `N`, at the end of the buffer, then the buffer has not been padded (at least not with PKCS#7)!

{% highlight python %}
def unpad_pkcs7(buffer):
    padding = buffer[-1]
    for i in range(len(buffer) - 1, len(buffer) - padding - 1, -1):
        if buffer[i] != buffer[-1]:
            return buffer
    new_buffer = bytearray()
    new_buffer[:] = buffer[:-padding]
    return new_buffer
{% endhighlight %}

<h3 id="10-implement-cbc-mode">
  10. Implement CBC mode
</h3>

This exercise involves writing AES-128 functions to encrypt and decrypt in CBC mode by using the AES-128 in ECB mode as done in [exercise 7]({% post_url 2017-04-20-cryptopals-challenge-set-1 %}#7-aes-in-ecb-mode).

#### Cipherblock Chaining (CBC) mode ####

In [CBC mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_Block_Chaining_.28CBC.29), each plaintext block is XOR'd with the previous ciphertext block before being encrypted, essentially chaining the cipherblocks together. The first block is XOR'd with an initialization vector (IV) before being encrypted and the IV is usually considered public knowledge.

This solves the ECB issue where identical plaintext blocks are encrypted to identical ciphertext blocks. However, a disadvantage (compared to EBC and other modes), is that each block cannot be encrypted in parallel and that the message must be padded to be a multiple of the block size.

We can test the correctness of the encrypt and decrypt methods by ensuring the encryption and then decryption of a plaintext returns said plaintext (i.e. `d_k(e_k(p)) == p` where `e_k` is an encryption function using a key `k` and `d_k` is an decryption function using a key `k`).

The code below is a simplified version of the [original version](https://gist.github.com/mikeecb/96ced9e90c6083f434d0026fb3d353e3).

{% highlight python %}
def aes_128_ecb_enc(buffer, key):
    obj = AES.new(key, AES.MODE_ECB)
    return bytearray(obj.encrypt(bytes(buffer)))

def aes_128_ecb_dec(buffer, key):
    obj = AES.new(key, AES.MODE_ECB)
    return bytearray(obj.decrypt(bytes(buffer)))

def aes_128_cbc_enc(buffer, key, iv):
    plaintext = pad_pkcs7(buffer, AES.block_size)
    ciphertext = bytearray(len(plaintext))
    prev_block = iv
    for i in range(0, len(plaintext), AES.block_size):
        ciphertext[i: i + AES.block_size] = aes_128_ecb_enc(
            xor(plaintext[i: i + AES.block_size], prev_block),
            key,
        )
        prev_block = ciphertext[i: i + AES.block_size]
    return ciphertext

def aes_128_cbc_dec(ciphertext, key, iv):
    plaintext = bytearray(len(ciphertext))
    prev_block = iv
    for i in range(0, len(ciphertext), AES.block_size):
        plaintext[i: i + AES.block_size] = xor(
            aes_128_ecb_dec(bytes(ciphertext[i: i + AES.block_size]), key),
            prev_block
        )
        prev_block = ciphertext[i: i + AES.block_size]
    return unpad_pkcs7(plaintext)

plaintext = bytearray("Hello my name is Michael")
iv = bytearray([chr(0)] * AES.block_size)
key = "YELLOW SUBMARINE"

assert aes_128_cbc_dec(aes_128_cbc_enc(plaintext, key, iv), key, iv) == plaintext
# Assertion passes - encryption and decryption are correct
{% endhighlight %}

#### Decrypting the ciphertext ####

Ok, let's use the `aes_123_cbc_dec` defined above to decrypt the ciphertext given in this exercise.

{% highlight python %}
# The ciphertext are provided in a file named 10.txt
ciphertext = bytearray("".join(list(open("10.txt", "r"))).decode("base64"))
aes_128_cbc_dec(ciphertext, key, iv)
# I'm back and I'm ringin' the bell
# A rockin' on the mike while the fly girls yell
# In ecstasy in the back of me
# Well that's my DJ Deshay cuttin' all them Z's
# Hittin' hard and the girlies goin' crazy
# Vanilla's on the mike, man I'm not lazy.

# I'm lettin' my drug kick in
# ...
{% endhighlight %}

<h3 id="11-an-ecb-cbc-detection-oracle">
  11. An ECB/CBC detection oracle
</h3>

In this exercise, we are asked to write an function to randomly encrypt a buffer with AES-128 in either ECB or CBC mode and with a random 128 bit key, and then to write an oracle that determines if a ciphertext was encrypted using ECB or CBC mode.

Let's go step by step.

#### Generating a random key ####

I just used Python's `random` module to create `N` random bytes where `N` is the length of the key in bytes. However, this is almost certainly not a secure way to generate keys randomly...

{% highlight python %}
from random import randint

def random_key(length):
    key = bytearray(length)
    for i in range(length):
        key[i] = chr(randint(0, 255))
    return key

print repr(random_key(16))
# bytearray(b'\xe0L\xa7\xb3Z\xd6\xc0e\x87vc\xc4*\x96,\x14')
{% endhighlight %}

#### Encrypting data under an unknown key ####

The next step is to write a function that encrypts a string. The exercise gives an exact specification of what the function should do, so let's write it down:

* Prepend and append 5-10 bytes (the exact number chosen randomly) to the plaintext. I assume the number of bytes prepended is the same as the number of bytes appended, but that they are different and chosen randomly.
* Encrypt with AES-128 in ECB mode half the time and in CBC mode the rest of the time.
* If encrypting with AES-128 in CBC mode, use a random IV.
* The key to encrypt the input should be chosen randomly.

{% highlight python %}
def encryption_oracle(buffer):
    bytes_to_add = randint(5, 10)
    plaintext = pad_pkcs7(
        random_key(bytes_to_add) +
        buffer +
        random_key(bytes_to_add),
        AES.block_size
    )
    key = bytes(random_key(16))
    if randint(0, 1):
        # Return a tuple of the ciphertext and 1 to
        # indicate it has been encrypted in ECB mode
        return aes_128_ecb_enc(plaintext, key), 1
    else:
        iv = random_key(16)
        # Return a tuple of the ciphertext and 0 to
        # indicate it has been encrypted in CBC mode
        return aes_128_cbc_enc(plaintext, key, iv), 0

encryption_oracle(bytearray("My name is Michael"))
# bytearray(b'x\xb5:\xe14\xaf\x10EK\x04[\xd6#\xe5\xf3OClz\x9c\x90\xce^\xfb\xbb\x86\x16\x97\xdcQ\x10\x15'), 1
{% endhighlight %}

<b>Note:</b> Although not in the original specification, I decided to return a tuple containing the ciphertext and a bit representing the mode in which the plaintext was encrypted. This will help testing in the next step.

#### Detect the block cipher mode ####

To determine if a ciphertext was encrypted in ECB or CBC mode, I used the `repeated_blocks` function we wrote in [exercise 8]({% post_url 2017-04-20-cryptopals-challenge-set-1 %}#8-detect-aes-in-ecb-mode). If a ciphertext has repeated blocks, I assumed it was encrypted in ECB mode. In order to test this heuristic, I ran the encryption oracle a thousand times and ensured I detected the correct mode every time.

It seems to work.

{% highlight python %}
def is_ecb_mode(buffer, block_size):
    return repeated_blocks(buffer, block_size) > 0

# The ciphertext are provided in a file named 11.txt
plaintext = bytearray("".join(list(open("11.txt", "r"))))
for i in range(1000):
    # ecb_mode is True when the plaintext is encrypted using ECB mode
    ciphertext, ecb_mode = encryption_oracle(plaintext)
    if ecb_mode != is_ecb_mode(ciphertext, AES.block_size):
        print "Detection does not work"
        exit()

print "Detection works"
{% endhighlight %}

<b>Note:</b> I provided the lyrics to [Rappers Delight](http://www.metrolyrics.com/rappers-delight-lyrics-sugarhill-gang.html) as the plaintext to be encrypted in the file `11.txt`.

<h3 id="12-byte-at-a-time-ecb-decryption">
  12. Byte-at-a-time ECB decryption (Simple)
</h3>

Obviously these challenges aren't meant to be easy, but I think the walkthrough for this question is slightly underspecified. Then again, this is the first attack that will break real crypto...

In this exercise, we break AES-128 encryption in ECB mode! We can do this with a specially crafted attack that works if we can control the first `N` bytes of the plaintext.

#### Encryption oracle 2.0 ####

Unlike the first from the [previous exercise](#11-an-ecb-cbc-detection-oracle), the new `encryption_oracle` function that should not add 5-10 random bytes to the start and end of the plaintext. I was momentarily confused by this.

The code below is a simplified version of the [original version](https://gist.github.com/mikeecb/e703ad2ee2afa8c70cdaf29d69d82227).

{% highlight python %}
key = bytes(random_key(16))

def encryption_oracle(data):
    unknown_string = bytearray((
        "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\n" +
        "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\n" +
        "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\n" +
        "YnkK"
    ).decode("base64"))
    plaintext = pad_pkcs7(
        data + unknown_string,
        AES.block_size,
    )
    return aes_128_ecb_enc(plaintext, key)
{% endhighlight %}

#### Detect the block size ####

This part of the exercise stumped for few moments. At first, I thought about reusing the same code to determine the block size from [exercise 6]({% post_url 2017-04-20-cryptopals-challenge-set-1 %}#6-breaking-repeating-key-xor). However, this felt like cheating since we could only do this previously by assuming that the ciphertext was encrypted in ECB mode and in this exercise, we can't assume that (yet).

My solution was actually much easier than the previous technique. We can just increase the size of the plaintext byte-by-byte until the ciphertext increases. The jump (difference) between the ciphertext sizes should be of block size. This works because we are padding each plaintext to be a multiple of the block size.

{% highlight python %}
def get_block_size(oracle):
    ciphertext_length = len(oracle(bytearray()))
    i = 1
    while True:
        data = bytearray("A" * i)
        new_ciphertext_length = len(oracle(data))
        block_size = new_ciphertext_length - ciphertext_length
        if block_size:
            return block_size
        i += 1
{% endhighlight %}

#### Check if ECB mode  ####

This attack (and exercise) is to decrypt a ciphertext encrypted in ECB mode. Needless to say, in order to carry out this attack, we must first know that the ciphertext was encrypted in ECB mode.

We can use the `is_ecb_mode` function from the [previous exercise](#11-an-ecb-cbc-detection-oracle) but must make sure that the plaintext prefix (the part of the plaintext that we control) contains two identical blocks as the rest of the plaintext might not. I decided to use `"YELLOW SUBMARINEYELLOW SUBMARINE"` as the plaintext prefix as it's 32 bytes long (2 blocks) and both blocks are identical.

#### Byte-by-byte decryption  ####

Now we can start looking at cracking the unknown string. As explained in the challenge description, we can do this by crafting special data to feed into the oracle and discovering the unknown string byte-by-byte.

If we feed data that is of length `block_size - 1`, the last byte in the block of the plaintext before it is encrypted in the oracle will be the first byte of the unknown string.

Here's a beautiful ASCII art diagram depicting the plaintext before it is encrypted (for demonstration, the block size is 8 bytes, the unknown string is `"THE UKNOWN STRING..."` and the specially crafted input data is `"AAAAAAA"`).

`+-------------------------------`<br/>
`|AAAAAAAT|HE UNKNO|WN STRIN|G...`<br/>
`+-------------------------------`<br/>

We can compare the first block of the ciphertext (of the above plaintext encrypted with our oracle) with the ciphertext returned by the oracle when passed `"AAAAAAAA"` as the input data to determine if the first byte of the unknown string is `"A"`. If it is not `"A"`, we could try again with `"AAAAAAAB"` as the input data and so on (trying all possible bytes).

Voila! We now know the first byte of the unknown string. We can discover the second by passing `"AAAAAA"` (or `block_size - 2`) as the specially crafted input data. We would then compare this to the ciphertext produced by the oracle when passing in `"AAAAAATA"`, `"AAAAAATB"`, `"AAAAAATc"` and so on (assuming `"T"` is the first byte of the unknown string).

I know what you're thinking. What happens when we "run out" of bytes to pass in as the input to the oracle? Surely this will only discover the first block of the unknown string. You're right! To solve this, we shouldn't pass in 1 block as the input to the oracle, but instead `N` bytes where `N` is the length of the unknown string rounded up to the nearest block size multiple!

<b>Note:</b> The remaining bytes in the input don't have to be `"A"`. They just need to be the identical in both ciphertexts in order to compare the ciphertexts correctly.

#### Detect the unknown string size ####

We can detect the length of the unknown string in almost the exact same way as we detected the block size.

{% highlight python %}
def get_unknown_string_size(oracle):
    ciphertext_length = len(oracle(bytearray()))
    i = 1
    while True:
        data = bytearray("A" * i)
        new_ciphertext_length = len(oracle(data))
        if ciphertext_length != new_ciphertext_length:
            return new_ciphertext_length - i
        i += 1
{% endhighlight %}

#### Cracking the unknown string ####

The code below is a simplified version of the [original version](https://gist.github.com/mikeecb/f4847ffdec5a03445cd58344056c179d).

{% highlight python %}
def get_unknown_string(oracle):
    block_size = get_block_size(oracle)
    is_ecb = is_ecb_mode(
        oracle(bytearray("YELLOW SUBMARINE" * 2)),
        block_size,
    )
    assert is_ecb
    unknown_string_size = get_unknown_string_size(oracle)

    unknown_string = bytearray()
    unknown_string_size_rounded = (
        ((unknown_string_size / block_size) + 1) *
        block_size
    )
    for i in range(unknown_string_size_rounded - 1, 0, -1):
        d1 = bytearray("A" * i)
        c1 = oracle(d1)[:unknown_string_size_rounded]
        for c in range(256):
            d2 = d1[:] + unknown_string + chr(c)
            c2 = oracle(d2)[:unknown_string_size_rounded]
            if c1 == c2:
                unknown_string += chr(c)
                break
    return unknown_string

print get_unknown_string(encryption_oracle)
# Rollin' in my 5.0
# With my rag-top down so my hair can blow
# The girlies on standby waving just to say hi
# Did you stop? No, I just drove by
{% endhighlight %}

<h3 id="13-ecb-cut-and-paste">
  13. ECB cut-and-paste
</h3>

The goal of this exercise is to change the content of a ciphertext (produced using AES-128 in ECB mode) such that when it is decrypted, you have replaced some of the plaintext (that you were not in control of) with your own content.

In particular, given a function `profile_for` that takes an email (say `foo@bar.com`), creates a profile which it then encodes in the form `email=foo@bar.com&uid=10&role=user` and then returns it encrypted, change the encrypted encoded profile to be an admin (i.e. replace `role=user` with `role=admin`).

The first part of the exercise isn't very interesting. Here's the setup functions I wrote.

{% highlight python %}
def str_to_dict(string):
    obj = {}
    for kv in string.split("&"):
        kv = kv.split("=")
        obj[kv[0]] = kv[1]
    return obj

def profile_for(email_buffer):
    email = bytes(email_buffer)
    email = email.replace("&", "").replace("=", "")
    profile = "email=" + email + "&uid=10&role=user"
    padded_buffer = bytes(pad_pkcs7(bytearray(profile), AES.block_size))
    return aes_128_ecb_enc(padded_buffer, key)

def dec_profile(profile):
    return bytes(unpad_pkcs7(aes_128_ecb_dec(profile, key)))
{% endhighlight %}

#### Cutting-and-pasting ####

The actual interesting part of this exercise is replacing `role=user` with `role=admin`. I did this in two steps.

Firstly, I created an arbitrary email, say `MY_EMAIL`, such that `email=MY_EMAIL&uid=10&role=` was block aligned (i.e. the length of that string was a multiple of the block size). I then passed it to the oracle (the `profile_for` function) to get a valid ciphertext and clipped it so that only the encrypted blocks of `email=MY_EMAIL&uid=10&role=` were kept. I called this clipped ciphertext the `profile_prefix`.

Secondly, I created another arbitrary email, say `MY_SECOND_EMAIL`, where `MY_SECOND_EMAIL = EMAIL_PREFIX || "admin" || EMAIL_POSTFIX` (`||` denotes string concatenation). The constraints were as follows:

- The `email=EMAIL_PREFIX` string must be block aligned.
- The `"admin" || EMAIL_POSTFIX` string must also be block aligned and `EMAIL_POSTFIX` must be a valid [PKCS#7](#9-implement-pkcs7-padding) padding.

With these constraints, I construct the `profile_postfix` by taking only the ciphertext blocks corresponding to `"admin" || EMAIL_POSTFIX`. The new admin profile is then `profile_prefix || profile_postfix` and we can decrypt it to check!

The code below is a simplified version of the [original version](https://gist.github.com/mikeecb/7d20e1ae992bc46ac880af3a804c9bd9).

{% highlight python %}
key = bytes(random_key(AES.block_size))

def create_admin_profile():
    block_size = get_block_size(profile_for)

    # Let's make the length of "email=...&uid=10&role=" a multiple of block_size
    # so that "user" is block aligned
    mandatory_bytes = "email=&uid=10&role="
    remaining_bytes = (len(mandatory_bytes) / block_size + 1) * block_size
    email_len = remaining_bytes - len(mandatory_bytes)
    email = "A" * email_len
    profile_prefix = profile_for(bytearray(email))[:remaining_bytes]

    # Let's make the length of "email=..." a multiple of block_size so that
    # the rest of the user inputted email is block aligned
    mandatory_bytes = "email="
    remaining_bytes = (len(mandatory_bytes) / block_size + 1) * block_size
    email_len = remaining_bytes - len(mandatory_bytes)
    email = "A" * email_len
    email += pad_pkcs7("admin", block_size)
    profile_postfix = profile_for(email)[
        remaining_bytes:remaining_bytes + block_size
    ]

    profile = profile_prefix + profile_postfix
    return bytes(dec_profile(profile))

create_admin_profile()
# 'email=AAAAAAAAAAAAA&uid=10&role=admin'
{% endhighlight %}

<b>Note:</b> I computed everything in terms of a computed `block_size`, so this function should work if we were to, say, increase the block size to `32`. Also, although I set the email to `AAAAAAAAAAAAA`, the content is arbitrary as long as it is that length (13 bytes).

<h3 id="14-byte-at-a-time-ecb-decryption-harder">
  14. Byte-at-a-time ECB decryption (Harder)
</h3>

This exercise is a rehash of [exercise 12](#12-byte-at-a-time-ecb-decryption) but instead of the encryption oracle encrypting `user_input || unknown_string`, the oracle encrypts `random_prefix || user_input || unknown_string`. The aim of this exercise is still to decrypt the `unknown_string` however the presence of the `random_prefix` makes it harder. I assume the `random_prefix` is constant (as the `unknown_string` is constant).

This isn't too much harder than the first. Once you determine the size of the unknown `random_prefix`, you can pad it to be a multiple of the block size, and then just offset the part of the ciphertext you care about by the length of the padded prefix.

Discovering the size of the unknown `random_prefix` using only the encryption oracle is a bit more difficult. I came up with a trick that works in the following way:

1. Create a buffer of block size length
2. Concatenate your buffer with itself `N` times (where `N` is a large positive integer) and use this as your input to the encryption oracle. For example, if `N = 2` and your buffer is `"YELLOW SUBMARINE"`, your input would be `"YELLOW SUBMARINEYELLOW SUBMARINE"`.
3. Pass your input to the encryption oracle to obtain a ciphertext. Search the ciphertext for `N` consecutive identical blocks. The index of the first byte of the `N` blocks is the beginning of your input and also the length of the `random_prefix`!
4. If you can't find `N` consecutive identical blocks in the ciphertext, it's probably because the `random_prefix` is not block aligned. Prepend 1 byte to your input and go back to step 3. <br/><b>Note:</b> To get the true size of the `random_prefix`, you must subtract the number of prepended padding bytes.
5. If you have prepended `block_size - 1` bytes to the input and you still cannot find `N` consecutive identical blocks, the ciphertext wasn't encrypted in ECB mode and we're out of luck.

The code below is a simplified version of the [original version](https://gist.github.com/mikeecb/96ced9e90c6083f434d0026fb3d353e3).

{% highlight python %}
key = bytes(random_key(16))
random_prefix = random_key(randint(0, 256))

def encryption_oracle(data):
    unknown_string = bytearray((
        "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\n" +
        "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\n" +
        "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\n" +
        "YnkK"
    ).decode("base64"))
    plaintext = pad_pkcs7(
        random_prefix + data + unknown_string,
        AES.block_size,
    )
    return aes_128_ecb_enc(plaintext, key)

def get_prefix_size(oracle, block_size):
    for prefix_padding_size in range(block_size):
        reps = 10
        prefix_padding = bytearray("A" * prefix_padding_size)
        buffer = oracle(prefix_padding + bytearray("YELLOW SUBMARINE" * reps))
        prev_block = count = index = None
        for i in range(0, len(buffer), block_size):
            block = buffer[i: i + block_size]
            if block == prev_block:
                count += 1
            else:
                index = i
                prev_block = block
                count = 1

            if count == reps:
                return index, prefix_padding_size

def get_unknown_string(oracle):
    block_size = get_block_size(oracle)
    prefix_size_rounded, prefix_padding_size = get_prefix_size(oracle, block_size)
    unknown_string_size = (
        get_unknown_string_size(oracle) -
        prefix_size_rounded -
        prefix_padding_size
    )

    unknown_string = bytearray()
    unknown_string_size_rounded = (
        ((unknown_string_size / block_size) + 1) *
        block_size
    )
    for i in range(unknown_string_size_rounded - 1, 0, -1):
        d1 = bytearray("A" * (i + prefix_padding_size))
        c1 = oracle(d1)[
            prefix_size_rounded:
            unknown_string_size_rounded + prefix_size_rounded
        ]
        for c in range(256):
            d2 = d1[:] + unknown_string + chr(c)
            c2 = oracle(d2)[
                prefix_size_rounded:
                unknown_string_size_rounded + prefix_size_rounded
            ]
            if c1 == c2:
                unknown_string += chr(c)
                break
    return unknown_string

get_unknown_string(encryption_oracle)
# Rollin' in my 5.0
# With my rag-top down so my hair can blow
# The girlies on standby waving just to say hi
# Did you stop? No, I just drove by
{% endhighlight %}

<h3 id="15-pkcs7-padding-validation">
  15. PKCS#7 padding validation
</h3>

In this exercise, we are instructed to determine if a plaintext has a valid PKCS#7 padding. If it does, we should strip it off and if not, throw an exception. We can do this with minimal changes to the `unpad_pkcs7` function we wrote in [exercise 9](#9-implement-pkcs7-padding).

{% highlight python %}
def unpad_valid_pkcs7(buffer):
    padding = buffer[-1]
    if padding >= AES.block_size:                  
        return buffer  
    for i in range(len(buffer)-1, len(buffer)-padding, -1):
        if buffer[i] != buffer[-1]:
            raise Exception("Bad PKCS#7 padding.")
    new_buffer = bytearray()
    new_buffer[:] = buffer[:-padding]
    return new_buffer

unpad_valid_pkcs7(bytearray("ICE ICE BABY\x04\x04\x04\x03"))
# Traceback (most recent call last):
#  File "15.py", line 10, in <module>
#    print unpad_valid_pkcs7(bytearray("ICE ICE BABY\x04\x04\x04\x03"))
#  File "15.py", line 5, in unpad_valid_pkcs7
#    raise Exception("Bad PKCS#7 padding.")
# Exception: Bad PKCS#7 padding.
{% endhighlight %}

<h3 id="16-cbc-bitflipping-attacks">
  16. CBC bitflipping attacks
</h3>

This exercise involves cracking encryption in CBC mode! Essentially, we want to change some ciphertext, produced by an encryption oracle, such that a decryption oracle sees the string `";admin=true;"` is present in it's plaintext.

#### Oracles ####

The oracles are fairly simple to write so there's not much to say. The key thing is that the bytes `";"` and `"="` are escaped so we can't just pass `";admin=true;"` as the user input to the encryption oracle.

{% highlight python %}
key = bytes(random_key(AES.block_size))
iv = bytearray(random_key(AES.block_size))

def encryption_oracle(input_data):
    input_data = input_data.replace(';','%3b').replace('=','%3d')
    plaintext = bytearray(
        "comment1=cooking%20MCs;userdata=" +
        input_data +
        ";comment2=%20like%20a%20pound%20of%20bacon"
    )
    return aes_128_cbc_enc(plaintext, key, iv)

def is_admin(enc_data):
    plaintext = aes_128_cbc_dec(enc_data, key, iv)
    return ";admin=true;" in plaintext
{% endhighlight %}

#### Flipping off the bits ####

Since we XOR each decrypted block with the previous ciphertext block in CBC mode, we can change a byte in the plaintext by changing the byte at the same index in the previous block (though this completely corrupts the previous plaintext block!). We can use this to produce the unescaped characters `";"` and `"="` in the plaintext!

My solution involved passing a buffer with a throwaway block (I don't mind if it gets corrupted) concatenated with `"AadminAtrueA"` as the user input. I managed to change the `"A"` bytes in `"AadminAtrueA"` to either `";"` or `"="` by changing the bytes at the same offset in the throwaway block using simple XOR magic.

The code below is a simplified version of the [original version](https://gist.github.com/mikeecb/b56277816343dc71ff811c5f2783621b).

{% highlight python %}
def crack():
    first_block = bytearray('A' * AES.block_size)
    second_block = bytearray("AadminAtrueA")
    plaintext = first_block + second_block
    ciphertext = encryption_oracle(plaintext)
    # We 'know' the prefix is two blocks long
    offset = 32
    # Change the first byte in first_block 'A' so we change the first byte in
    # second_block to be ';'
    ciphertext[offset] = bytes(
        xor(
            bytearray(chr(ciphertext[offset])),
            xor(bytearray("A"), bytearray(";"))
        )
    )
    # Change the 7th byte in first_block 'A' so we change the first byte in
    # second_block to be '='
    ciphertext[offset + 6] = bytes(
        xor(
            bytearray(chr(ciphertext[offset + 6])),
            xor(bytearray("A"), bytearray("="))
        )
    )
    # Change the 12th byte in first_block 'A' so we change the first byte in
    # second_block to be ';'
    ciphertext[offset + 11] = bytes(
        xor(
            bytearray(chr(ciphertext[offset + 11])),
            xor(bytearray("A"), bytearray(";"))
        )
    )
    return is_admin(ciphertext)
{% endhighlight %}


<b>Note:</b> I assumed that I know the exact length of the prefix (32 bytes or 2 blocks) as encryption algorithms are usually public knowledge. However, if I didn't know the length, I could calculate it using the `get_prefix_size` function that I wrote in [exercise 14](#14-byte-at-a-time-ecb-decryption-harder).

### Fin ###

Okay, wow. This set of exercises took me considerably longer than the [first set]({% post_url 2017-04-20-cryptopals-challenge-set-1%}) and the post ended up way too long. I’m going to think about splitting up the sets in half. Anyway, hope you enjoyed and found this post helpful! Still have time? Read through the [third set]({% post_url 2017-07-14-cryptopals-challenge-set-3%})!
