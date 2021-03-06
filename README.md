# SIBYL_dataset

## Format
- Pickle format(List)
  - Pickle https://docs.python.org/3.8/library/pickle.html
- Disassembler Instruction and CFG(control flow glaph)

## Dataset Contents
- gcc  7.5.0
- clang 6.0.0
- openssl 3.0.0a, 1.0.1f, 1.0.1u
- busybox 1.32.0open_mydata_pickle
- gdb 9.2
- sqlite 2.8.17
- httpd 2.4.43

## Sample Code
```
import pickle
def open_mydata_pickle(filepath):
    f = open(filepath, 'rb')
    dataset_pickle = pickle.load(f)
    f.close()
    # Debug print.
    for x in range(0, 3):
        print("----")
        print("--DEBUG: {}" .format(dataset_pickle[x][0]))
        print("--DEBUG: {}" .format(dataset_pickle[x][1]))
        print("--DEBUG: {}" .format(dataset_pickle[x][2]))
        print("--DEBUG: {}" .format(dataset_pickle[x][3]))
        print("--DEBUG: {}" .format(dataset_pickle[x][4]))
        print("--DEBUG: {}" .format(dataset_pickle[x][5]))
        print("--DEBUG length: {}" .format(len(dataset_pickle)))
    return dataset_pickle
```

---

## SIBYL_dataset_Extractor
- Require IDA Pro version 7.3 (Warning: python version is 2.XX)

## LISENCE
* Apache License 2.0

---

# PAPER
## SIBYL: A Method for Detecting Similar Binary Functions Using Machine Learning
- Publication: IEICE TRANSACTIONS on Information and Systems   Vol.E105-D    No.4    pp.755-765
- Publication Date: 2022/04/01
- Publicized: 2021/12/28
- Online ISSN: 1745-1361
- DOI: 10.1587/transinf.2021EDP7135

### Summary
Binary code similarity comparison methods are mainly used to find bugs in software, to detect software plagiarism, and to reduce the workload during malware analysis. In this paper, we propose a method to compare the binary code similarity of each function by using a combination of Control Flow Graphs (CFGs) and disassembled instruction sequences contained in each function, and to detect a function with high similarity to a specified function. One of the challenges in performing similarity comparisons is that different compile-time optimizations and different architectures produce different binary code. The main units for comparing code are instructions, basic blocks and functions. The challenge of functions is that they have a graph structure in which basic blocks are combined, making it relatively difficult to derive similarity. However, analysis tools such as IDA, display the disassembled instruction sequence in function units. Detecting similarity on a function basis has the advantage of facilitating simplified understanding by analysts. To solve the aforementioned challenges, we use machine learning methods in the field of natural language processing. In this field, there is a Transformer model, as of 2017, that updates each record for various language processing tasks, and as of 2021, Transformer is the basis for BERT, which updates each record for language processing tasks. There is also a method called node2vec, which uses machine learning techniques to capture the features of each node from the graph structure. In this paper, we propose SIBYL, a combination of Transformer and node2vec. In SIBYL, a method called Triplet-Loss is used during learning so that similar items are brought closer and dissimilar items are moved away. To evaluate SIBYL, we created a new dataset using open-source software widely used in the real world, and conducted training and evaluation experiments using the dataset. In the evaluation experiments, we evaluated the similarity of binary codes across different architectures using evaluation indices such as Rank1 and MRR. The experimental results showed that SIBYL outperforms existing research. We believe that this is due to the fact that machine learning has been able to capture the features of the graph structure and the order of instructions on a function-by-function basis. The results of these experiments are presented in detail, followed by a discussion and conclusion.

### Reference
https://search.ieice.org/bin/summary.php?id=e105-d_4_755

### key words
 - Similarity, Binary Code, Function, NLP, Machine Learning
