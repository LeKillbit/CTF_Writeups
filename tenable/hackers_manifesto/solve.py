#!/usr/bin/env python3

data = open("hacker_manifesto.txt", "rb").read()

def reset_chunk(c):
    ret = b""
    ret += b"\x00"
    ret += b"\x00"
    ret += bytes([c[2]])
    return ret

def insert(chunks, idx, offset, length):
    ret = []
    if length & 1 != 0:
        offset += 256
    if (length >> 1) & 1 != 0:
        offset += 512
    to_add = chunks[idx-offset:idx-offset+length//4]
    if to_add != b"":
        chunks = chunks[:idx] + to_add + [reset_chunk(chunks[idx])] + chunks[idx+1:]
    return chunks


def chunking(data):
    chunks = []
    for i in range(0, len(data), 3):
        chunks.append(bytes([data[i], data[i+1], data[i+2]]))
    return chunks

def decoding_complete(chunks):
    for chunk in chunks:
        offset = chunk[0]
        length = chunk[1]
        char = chunk[2]
        if offset != 0 or length != 0:
            return False
    return True
        

def decode(data):
    ret = b""

    chunks = chunking(data)

    while not decoding_complete(chunks):
        
        for i in range(len(chunks)):
            offset = chunks[i][0]
            length = chunks[i][1]
            char = chunks[i][2]
            if offset != 0 or length != 0:
                chunks = insert(chunks, i, offset, length)
                ret = b"".join(chunks).replace(b"\x00\x00",b"")
                break
    return ret

ret = decode(data)
print(ret.decode())
