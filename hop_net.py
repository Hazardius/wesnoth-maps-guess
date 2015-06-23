#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

import numpy as np

def vector_to_answer(vector):

    def letter(index):
        return "ACDGHIKMQRSUWXN"[index]

    answer_id = 14
    if sum(vector) == -12:
        for i in range(len(vector)):
            if vector[i] == 1:
                if answer_id != 14:
                    answer_id = 14
                    break
                answer_id = i
    return letter(answer_id)


class HopfieldNetwork(object):


    def __init__(self,
                 inputs_number=98,
                 patterns_file="patternsT.pat",
                 tests_file="testsT.tst",
                 out="results.txt",
                 debug=False,
                 save_res=True,
                 seed=None):
        self.debug = debug
        self.inputs_number = inputs_number
        self.patterns_file = patterns_file
        self.tests_file = tests_file
        self.results_file = out
        self.neurons = []
        if self.debug:
            print "1. RNG seeding."
        if seed is not None:
            np.random.seed(seed)
        else:
            np.random.seed(np.random.randint(0, 256))
        if self.debug:
            print "2. Network initialization."
        for _ in range(self.inputs_number):
            self.neurons.append(self.create_neuron())
        if self.debug:
            print "3. Loading of patterns."
        patterns = self.open_patterns_file(self.patterns_file)
        if self.debug:
            print "4. Training."
        self.train_network(patterns)
        if self.debug:
            print "5. Testing."
            print "5.1. Loading test data."
        tests = self.open_tests_file(self.tests_file)
        if self.debug:
            print "5.2. Executing tests."
        results = self.test(tests, save_res)
        if save_res:
            if self.debug:
                print "6. Saving the results."
            self.save_to_file(self.results_file, results)

    def save_to_file(self, dest_file, content):
        opened_file = codecs.open(dest_file, "w", "utf-8")
        opened_file.write(content)

    def open_patterns_file(self, path):
        """ Opening a file specified by a path. """

        def letter_2_vector(char):

            def index(index):
                return {
                    'A': 0,
                    'C': 1,
                    'D': 2,
                    'G': 3,
                    'H': 4,
                    'I': 5,
                    'K': 6,
                    'M': 7,
                    'Q': 8,
                    'R': 9,
                    'S': 10,
                    'U': 11,
                    'W': 12,
                    'X': 13,
                }[index]

            vector = []
            if char != '\n':
                vector = [-1 for i in range(self.inputs_number / 7)]
                vector[index(char)] = 1
                # vector += index(char)
            return vector

        patterns = []
        with open("./patterns/" + path) as text_file:
            for line in text_file:
                if len(line) != 8:
                    continue
                new_pattern = []
                for letter in line:
                    new_pattern = new_pattern + letter_2_vector(letter)
                patterns.append(new_pattern)
        return patterns

    def open_tests_file(self, path):
        """ Opening a file specified by a path. """

        def letter_2_vector(char):

            def index(index):
                return {
                    'A': 0,
                    'C': 1,
                    'D': 2,
                    'G': 3,
                    'H': 4,
                    'I': 5,
                    'K': 6,
                    'M': 7,
                    'Q': 8,
                    'R': 9,
                    'S': 10,
                    'U': 11,
                    'W': 12,
                    'X': 13,
                }[index]

            vector = []
            if char == 'N':
                return [-1 for i in range(self.inputs_number / 7)]
                # return [0 for i in range(self.inputs_number / 7)]
                # return [1 for i in range(self.inputs_number / 7)]
                # return self.initialize_weights(self.inputs_number / 7)
            if char != '\n':
                vector = [-1 for i in range(self.inputs_number / 7)]
                vector[index(char)] = 1
                # vector += index(char)
            return vector

        tests = []
        with open("./tests/" + path) as text_file:
            for line in text_file:
                if len(line) != 10:
                    continue
                new_test = []
                for letter in line:
                    if letter == ' ':
                        break
                    new_test = new_test + letter_2_vector(letter)
                expected = letter_2_vector(line[-2])
                tests.append((new_test, expected))
        return tests

    def random_vector(self, minmax):
        return [elem[0] + ((elem[1] - elem[0]) * np.random.rand()) for elem in minmax]

    def initialize_weights(self, problem_size):
        minmax = [[-0.5, 0.5] for _ in range(problem_size)]
        return self.random_vector(minmax)


    class Neuron(object):


        def __init__(self, init_weights):
            self.weights = init_weights

        def __repr__(self):
            return str(self.weights)

        def __str__(self):
            return "Neuron: " + str(self.weights) + "\n"


    def create_neuron(self):
        neuron = self.Neuron(self.initialize_weights(self.inputs_number))
        return neuron

    def train_network(self, patterns, times=1):
        for _ in range(times):
            for i in range(len(self.neurons)):
                for j in range((i + 1), len(self.neurons)):
                    if i == j:
                        continue
                    wij = 0.0
                    for pattern in patterns:
                        wij += pattern[i] * pattern[j]
                    self.neurons[i].weights[j] = wij
                    self.neurons[j].weights[i] = wij
        return

    def propagate_was_change(self):

        def sigmoid(activation):
            if activation >= 0:
                return 1
            return -1

        i = np.random.randint(0, len(self.neurons))
        activation = 0
        j = 0
        for neuron in self.neurons:
            if i == j:
                continue
            activation += neuron.weights[i]* neuron.output
            j += 1
        output = sigmoid(activation)
        change = (output != self.neurons[i].output)
        self.neurons[i].output = output
        return change

    def get_output(self, pattern, evals=100):
        iterating_nr = 0
        for neuron in self.neurons:
            neuron.output = pattern[iterating_nr]
            iterating_nr += 1
        for _ in range(evals):
            self.propagate_was_change()
        return [self.neurons[i].output for i in range(len(self.neurons))]

    def test(self, tests, to_save=False):
        tested = 0
        predicted = 0
        results = ""
        for test in tests:
            neural_output = self.get_output(test[0])
            expected = vector_to_answer(test[1])
            predicted_letter = vector_to_answer(neural_output[84:len(neural_output)])
            if expected == predicted_letter:
                predicted += 1
            if not to_save:
                print "Test " + str(tested + 1)
                print "-----"
                print "Surroundings:"
                print (vector_to_answer(test[0][:14]) + " " +
                       vector_to_answer(test[0][14:28]) + " " +
                       vector_to_answer(test[0][28:42]))
                print (vector_to_answer(test[0][42:56]) + " " +
                       vector_to_answer(test[0][56:70]) + " " +
                       vector_to_answer(test[0][70:84]))
                nex = ""
                npr = ""
                # if self.debug:
                #     nex = str(test[1])
                #     npr = str(neural_output[84:len(neural_output)])
                print "Expected:  " + expected + " " + nex
                print "Predicted: " + predicted_letter + " " + npr
                if expected == predicted_letter:
                    print "SUCCESS!\n"
                else:
                    print "FAIL!\n"
            else:
                results += "Test number: " + str(tested + 1) + "\n"
                results += "Expected: " + expected + "\n"
                results += "Predicted: " + predicted_letter + "\n"
                if expected == predicted_letter:
                    results += "SUCCESS!" + "\n"
                else:
                    results += "FAIL!" + "\n"
                results += "----------\n"
            tested += 1
        if to_save:
            end_info = "Tested:" + str(tested) + "\n"
            end_info += "Predicted: " + str(predicted) + "\n"
            end_info += "Successful predictions: " + str(predicted*100.0/tested) + "%\n"
            results = end_info + "----------\n" + results
            if self.debug:
                print "Successful predictions: " + str(predicted*100.0/tested) + "%"
        else:
            print "Tested:" + str(tested)
            print "Predicted: " + str(predicted)
            print "Successful predictions: " + str(predicted*100.0/tested) + "%"
        return results
