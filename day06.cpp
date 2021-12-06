#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>
#include <cstdint>
#include <functional>
#include <numeric>
#include "util.h"

using namespace std;
constexpr int today = 6;

vector<uint64_t> parse_file(string filename)
{
    vector<uint64_t> res(9, 0);
    strvec_t input = readlines(filename);
    intvec_t seq = to_int(split(input[0], ','));
    for (int val : seq)
    {
        const size_t index = static_cast<size_t>(val);
        res[index]++;
    }

    return res;
} 


uint64_t simulate_growth(vector<uint64_t> input, int cycles)
{
    vector<uint64_t> current_state = input;

    for (int c = 0; c < cycles; ++c)
    {
        uint64_t num_zeros = current_state[0];
        for (size_t i = 1; i < 9; ++i)
        {
            current_state[i-1] = current_state[i];
        }
        current_state[6] += num_zeros;
        current_state[8] = num_zeros;
    }

    return std::accumulate(current_state.begin(), current_state.end(), (uint64_t)0);
}


uint64_t part_one()
{
    auto input = parse_file(input_filename(today));
    return simulate_growth(input, 80);
}

void test_part_one()
{
    auto input = parse_file(test_filename(today));
    assert(input[0] == 0);
    assert(input[1] == 1);
    assert(input[2] == 1);
    assert(input[3] == 2);
    assert(input[4] == 1);
    assert(input[5] == 0);
    assert(input[6] == 0);
    assert(input[7] == 0);
    assert(input[8] == 0);

    uint64_t res1 = simulate_growth(input, 18);
    assert(res1 == 26);

    uint64_t res2 = simulate_growth(input, 80);
    assert(res2 == 5934);
}


uint64_t part_two()
{
    auto input = parse_file(input_filename(today));
    return simulate_growth(input, 256);
}


void test_part_two()
{
    auto input = parse_file(test_filename(today));
    uint64_t res = simulate_growth(input, 256);
    assert(res == 26984457539);
}

int main(int, char**)
{
    test_part_one();
    uint64_t res1 = part_one();
    std::cout << "Part One: " << res1 << std::endl;

    test_part_two();
    uint64_t res2 = part_two();
    std::cout << "Part Two: " << res2 << std::endl;
}
