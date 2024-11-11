"""
Name: Maya Louise Asuero
ID: 248480
CSCI 201 UV2 - Lempel Ziv
Description: Sample implementation of lempel ziv compression algorithm. Includes both LZ77 and LZ78.
********************************************************************************
I hereby attest to the truth of the following facts:

1. I have not discussed the python code in my program with anyone other than my instructor of the teaching assistants assigned to this course.

2. I have not used python code obtained from another student, or any other unauthorized source, whether modified or unmodified.

3. If any python code of documentation used in my program was obtained from another source, it has been clearly noted with citations in the comments of my program.
********************************************************************************
"""
import argparse
import struct

# uses sliding window
def lz77_compress(input):
    """
    search length is 1024 bytes.
    algorithm allocates 4 bytes for representing offset
    length 
    """
    len_search = 1024 
    len_lookahead = 10
    out = []
    i = 0
    
    while i < len(input):        
        search_buffer = (max(0, i-len_search), max(0,i))

        # if > 1 bytes representation (i.e. image)
        if i == 0 or search_buffer == (0,0):
            res = struct.pack(">Hc",0,bytes(chr(input[i]),'iso-8859-1'))
            i += 1
        else:
            offset, length, nextChar = findLongestMatch(input, search_buffer, len_lookahead, i)
            offset = offset << 5
            pref = offset + length
            res = struct.pack(">Hc",pref, bytes(chr(nextChar),'iso-8859-1'))
            i = i+length+1
        out.append(res)
    return out

def lz77_decompress(input):
    i = 0
    output = []
    while i < len(input):
        pref, char = struct.unpack(">Hc",input[i:i+3])
        offset = pref >> 5
        length = pref - (offset << 5)

        if offset == 0  and length == 0:
            output.append(char)

        else:
            start = len(output) - offset
            for idx in range(length):
                output.append(output[start+idx])
            output.append(char)
        i += 3

    return output

def findLongestMatch(input, searchSpace,lookahead, current):
    sb_start, sb_end = searchSpace
    lh_start, lh_end = current, current+1+lookahead
    search_buffer_window = input[sb_start:sb_end]
    lookahead_window = input[lh_start:lh_end]

    # offset, length = match2(search_buffer_window,lookahead_window)    
    offset, length = match(input, search_buffer_window,lookahead_window)
    if current + length + 1 <= len(input):
        return offset, length, input[current+length]
    elif offset == 0 and length == 0:
        return offset, length,input[current]
    else:
        return offset, length, ord('\r')

def match(input, sb, lh):
    m = len(sb)
    n = len(lh)

    offset = 0
    res = 0
    # traverses search buffer
    for i in range(m):
        # print('i:',i)
        for j in range(n):
            curr = 0
            if n == 1 and sb[0] == lh[0]:
                offset = 1
                res = 1
                break
            if lh[0] not in sb:
                offset = 0
                res = 0
                break
            else:
                while (i + curr) < m and (j + curr) < n and sb[i + curr] == lh[j + curr]:
                    curr += 1
                    if curr > res:
                        res = curr
                        offset = m - i
                break
    return offset, res

# uses dictionary
def lz78_compress(input):
    """
    for each ch in input, ch is checked if found in dictionary
    if found, append to a holder string that contains characters already in dictionary
    """
    dictionary = {}
    out = None
    
    return out

def lz78_decompress(input):
    dictionary = {}
    out = 0
    return out

def main():
    text = []

    parser = argparse.ArgumentParser(description="Compress or decompress a file.")
    parser.add_argument('-c', '--compress',action='store_true',help="File to compress")
    parser.add_argument('-d', '--decompress',action='store_true', help="File to decompress")
    parser.add_argument('-a', '--algorithm', type=str, help="Compression algorithm")
    parser.add_argument('-f', '--file', type=str, help="File to process")
    
    args = parser.parse_args()

    if args.compress and not args.decompress and args.algorithm == 'lz77':
        with open(args.file,'rb') as f_in:
            text = f_in.read()
        output = lz77_compress(text)
        print('size:',len(text), len(output))

        output_filename = "compressed-"+args.file
        with open(output_filename, 'wb') as f_out:
            for i in output:
                f_out.write(i)
        f_out.close()

    elif args.compress and not args.decompress and args.algorithm == 'lz78':
        output = lz78_compress(text)

    elif args.decompress and not args.compress and args.algorithm == 'lz77':
        with open(args.file,'rb') as f_in:
            text = f_in.read()
        filename = args.file.replace('compressed-','original-')

        output = lz77_decompress(text)
        print('size:',len(text), len(output))

        with open(filename, 'wb') as f_out:
            for i in output:
                f_out.write(i)
        f_out.close()

    elif args.decompress and not args.compress and args.algorithm == 'lz78':
        output = lz78_decompress(text)
    else:
        print("Error.")



if __name__ == "__main__":
    main()