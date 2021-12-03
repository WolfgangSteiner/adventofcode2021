#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>
#include <cstdint>
#include <functional>
#include "util.h"


std::vector<int> parse_sequence(const std::vector<std::string>& seq)
{
    int word_length = seq[0].size();
    std::vector<int> acc(word_length, 0);

    for (auto str : seq)
    {
        for (int i = 0; i < word_length; ++i)
        {
            if (str[i] == '1') acc[i]++; 
            else acc[i]--;
        }
    }

    return acc;
}

int binary_to_int(std::string s)
{
    uint32_t res = 0x0;
    size_t word_length = s.size();
    uint32_t shift = word_length - 1;

    for (char c : s)
    {
        uint32_t bit = c == '1' ? 1 : 0;
        res |= (bit << (shift--));
    }
    
    return res;
}

std::pair<int, int> compute_gamma_epsilon(const std::vector<std::string>& seq)
{
    auto acc = parse_sequence(seq);
    std::string gamma_str;
    int word_length = seq[0].size();
    
    for (auto val : acc)
    {
        const char token = (val > 0) ? '1' : '0';
        gamma_str.push_back(token);
    }

    int gamma = binary_to_int(gamma_str);
    int epsilon = (1 << word_length) - 1 - gamma;
        
    return std::make_pair(gamma, epsilon);
}


std::vector<std::string> filter_sequence(const std::vector<std::string>& seq, int pos, char value)
{
    std::vector<std::string> res;

    for (auto s : seq)
    {
        if (s[pos] == value) res.push_back(s);
    }

    return res;
}


int compute_scrubber_value(const std::vector<std::string>& seq, std::function<char(int)> det)
{
    auto seq2 = seq;
    int pos = 0;
    int word_length = seq[0].size();

    while (seq2.size() > 1 && pos < word_length)
    {
        auto acc = parse_sequence(seq2);
        char value_of_significant_bit = det(acc[pos]);
        seq2 = filter_sequence(seq2, pos, value_of_significant_bit);
        pos++;   
    }

    assert(seq2.size() == 1);

    return binary_to_int(seq2[0]);
}

int compute_oxy(const std::vector<std::string>& seq)
{
    return compute_scrubber_value(seq, [](int a) { return a >= 0 ? '1' : '0'; });
}

int compute_co2(const std::vector<std::string>& seq)
{
    return compute_scrubber_value(seq, [](int a) { return a >= 0 ? '0' : '1'; });
}

int part_one(std::string filename)
{
    auto seq = readlines(filename);
    auto acc = parse_sequence(seq);
    auto [gamma, epsilon] = compute_gamma_epsilon(seq);
    return gamma * epsilon;
}

void test_part_one()
{
    auto seq = readlines("data/day03_test.txt");
    assert(seq.size() == 12);
    auto acc = parse_sequence(seq);
    assert((acc == (std::vector<int>){2, -2, 4, 2, -2}));
    auto [gamma, epsilon] = compute_gamma_epsilon(seq);
    assert(gamma == 22 && epsilon == 9);
    assert(part_one("data/day03_test.txt") == 22 * 9);
}


int part_two(std::string filename)
{
    auto seq = readlines(filename);
    auto oxy = compute_oxy(seq);
    int co2 = compute_co2(seq);
    return oxy * co2;
}

void test_part_two()
{
    auto seq = readlines("data/day03_test.txt");
    auto oxy = compute_oxy(seq);
    auto co2 = compute_co2(seq);
    assert(oxy == 23);
    assert(co2 == 10);
}

int main(int, char**)
{
    test_part_one();
    int res1 = part_one("data/day03.txt");
    std::cout << "Part One: " << res1 << std::endl;

    test_part_two();
    int res2 = part_two("data/day03.txt");
    std::cout << "Part Two: " << res2 << std::endl;
}
