import json
class GenerateLanguageModel:
    """
        This class generates a language model from a list of lines.
        Each line is a dictioanry.
    """
    def __init__(self, lines=None, path=None) -> None:
        """
        Initialize the Generate_Language_Model with a list of lines.
        JSON path can also be given.

        Inputs:
            lines (list[dict[str:any]]): The list of dictionaries to process.
            Json Path
        """


        def read_json_file(file_path):
            """
            This function reads a JSON file and returns a list of dictionaries.

            Inputs:
                file_path (str): The path to the JSON file.

            Returns:
                list[dict[str, any]]: A list of dictionaries read from the JSON file.
            """
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data


        if lines is None and path is None:
            raise ValueError("You must provide either 'lines' for dictionary \
                or 'path' for JSON files")
        if lines is not None and path is not None:
            raise ValueError("You can only provide either 'lines' or 'path', not both")
        if path is not None:
            self.lines = read_json_file(path)


    def filter_by_category(self, category, value):
        """
        This function filters a list of dictionaries based on a category and a value

        Inputs:
            lines (list[dic[str:any]]): The list of dictionaries to filter.
            category (str): The category to filter by.
            value (str): The value to filter by.

        Returns:
            list[dict]: A list of dictionaries that match the filter.
        """
        lst = []
        for dic in self.lines:
            if dic[category] == value:
                lst.append(dic)
        return lst


    def remove_punc_and_lower_and_split(self, sentence):
        """
        This function takes a sentence as input, removes punctuation, converts it
        to lowercase, and splits it into words.

        Inputs:
            sentence (str): The sentence to process.

        Returns:
            list[str]: A list of words in the sentence.
        """
        punctuation =  '!-;:?/.,\'"'
        translator = str.maketrans("", "", punctuation)
        edited = sentence.lower().translate(translator)
        return edited.split()


    def generate_n_grams(self, sentence, n):
        """
        This function takes a sentence and an integer n as inputs, and
        generates n-grams from the sentence.

        Inputs:
            sentence (str): The sentence to process.
            n (int): The number of words in each n-gram.

        Returns:
            list[str]: A list of n-grams.
        """
        splitted_sen = self.remove_punc_and_lower_and_split(sentence)
        return [tuple(splitted_sen[i:i+n]) for i in range(len(splitted_sen)-n+1)]


    def count_n_grams(self, n, lines=None):
        """
        This function takes a list of lines and an integer n as inputs, and counts
        the occurrence of each n-gram in the lines.

        Inputs:
            lines (list): The lines to process.
            n (int): The number of words in each n-gram.

        Returns:
            dict[str:int]: A dictionary where the keys are n-grams and the values
            are their counts.
    
        """
        if lines is None:
            lines = self.lines
        dic = {}
        for line in lines:
            txt = line["text_entry"]
            grams = self.generate_n_grams(txt, n)
            for gram in grams:
                dic[gram] = dic.get(gram, 0) + 1
        return dic


    def generate_language_model(self, category=None, value=None):
        """
        This function generates a language model from the lines.

            Inputs:
                category (str, optional): The category to filter by. If None, no
                filtering is performed.
                value (str, optional): The value to filter by. If None, no filtering
                is performed.

            Returns:
                dict: A dictionary where the keys are n-grams and the values are
                lists of tuples where the first element is the next token
                and the second element is its probability.
        """
        model = {}
        lines = self.lines
        if category is not None and value is not None:
            lines = self.filter_by_category(category, value)
        for i in range(1,5):
            k_grams = self.count_n_grams(i, lines)
            suffixes = self.count_n_grams(i+1, lines)
            for suffix, count in suffixes.items():
                k_gram = suffix[:-1]
                probability = count / k_grams[k_gram]
                counter = suffix[-1]
                model[k_gram] = model.get(k_gram, []) + [(counter, probability)]
        return model


model = GenerateLanguageModel(path="lines_sample.json")
print(model.generate_language_model())
print(model.generate_language_model(category="speaker", value="EMILIA"))
