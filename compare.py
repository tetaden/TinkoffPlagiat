import argparse
import ast
import re
import codecs

class Normalizer:
    def __init__(self, path):
        f = codecs.open(path, "r", "utf_8_sig")
        file = ast.unparse(ast.parse(f.read()))
        text_file = self.normalize(file)
        self.file = text_file

    def normalize(self, text):
        text = re.sub(r'\"[^"]*\"', '',text) # Удаляем комментарии
        tokens = [re.sub(r'\s+', ' ', line) for line in text.split('\n')] # убираем лишние пробелы
        tokens = [token.lower() for token in tokens] # приводим строки к нижнему регистру
        tokens = [token for token in tokens if (token != ' ' or token != '')] # удаляем мусорные строки
        return tokens

    def get_tokens(self):
        return self.file

class Comparator:

    def __init__(self, file1, file2):
        self.file_tokens1 = file1
        self.file_tokens2 = file2

    @staticmethod
    def levinstein(word1, word2):
        n, m = len(word1), len(word2)
        D = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            D[i][0] = i
        for j in range(m + 1):
            D[0][j] = j
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                c = 1 if word1[i - 1] != word2[j - 1] else 0
                D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + c)
        return D[-1][-1]

    def get_result(self):
        n = min(len(self.file_tokens1), len(self.file_tokens2))
        dist = []
        for i in range(n):
            word1 = self.file_tokens1[i]
            word2 = self.file_tokens2[i]
            m = max(len(word1), len(word2))
            if m != 0:
                dist.append(1 - (self.levinstein(word1, word2) / m ))
        return round(sum(dist) / max(len(self.file_tokens1), len(self.file_tokens2)), 2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='directions to python files')
    parser.add_argument('input', type=str, help='input file')
    parser.add_argument('output', type=str, help='output file')
    files = parser.parse_args()

    list_of_files = []
    with open(files.input, 'r') as input:
        for line in input.read().split('\n'):
            file1, file2  = line.split()
            list_of_files.append((file1, file2))
    results = []
    for comb in list_of_files:
        file1 = Normalizer(comb[0]).get_tokens()
        file2 = Normalizer(comb[1]).get_tokens()
        results.append(Comparator(file1, file2).get_result())
    f = open(files.output, 'w')
    for res in results:
        f.write(str(res) + '\n')