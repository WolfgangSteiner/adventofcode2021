#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>
#include <cstdint>
#include <functional>
#include "util.h"
#include <unordered_map>

using namespace std;

using map_t = unordered_map<size_t, int>;


size_t compute_key(int x, int y) { return (size_t)x << 32 | (size_t) y; }


void mark_cell(map_t& map, int x, int y)
{
    size_t key = compute_key(x,y);
    auto find_iter = map.find(key);
    if (find_iter != map.end())
    {
        find_iter->second++;
    }
    else
    {
        map.insert(make_pair(key, 1));
    }
}


map_t parse_file(string filename, bool only_orthogonal)
{
    auto input = readlines(filename);
    map_t res;
     
    for (auto line : input)
    {
        int x1, y1, x2, y2;
        sscanf(line.c_str(), "%d,%d -> %d,%d", &x1, &y1, &x2, &y2);
        if (x1 == x2 || y1 == y2 || only_orthogonal == false)
        {
            int x = x1;
            int y = y1;
            int delta_x = (x2 - x1);
            int delta_y = (y2 - y1);
            int step_x = delta_x > 0 ? 1 : delta_x < 0 ? -1 : 0;
            int step_y = delta_y > 0 ? 1 : delta_y < 0 ? -1 : 0;

            while (x != x2 || y != y2)
            {
                mark_cell(res, x, y);
                x += step_x;
                y += step_y;
            }

            mark_cell(res, x2, y2);
        }
    }

    return res;
}


void print_grid(const map_t& map)
{
    for (int y = 0; y < 10; ++y)
    {
        for (int x = 0; x < 10; ++x)
        {
            auto key = compute_key(x, y);
            auto find_iter = map.find(key);
            if (find_iter == map.end())
            {
                cout << ".";
            }
            else
            {
                cout << find_iter->second;
            }
        }
        cout << endl;
    }
    cout << endl;
}


int count_dangerous_cells(std::string filename, bool only_orthogonal)
{
    auto map = parse_file(filename, only_orthogonal);
    int count = 0;

    for (const auto& cell : map)
    {
        if (cell.second > 1) count++;
    }

    return count;
}


int part_one(std::string filename)
{
    return count_dangerous_cells(filename, true);
}


void test_part_one()
{
    auto map = parse_file("data/day05_test.txt", true);
    print_grid(map);
    int result = part_one("data/day05_test.txt");
    assert(result == 5);
}


int part_two(std::string filename)
{
  return count_dangerous_cells(filename, false);
}

void test_part_two()
{
    auto map = parse_file("data/day05_test.txt", false);
    print_grid(map);
    int result = part_two("data/day05_test.txt");
    assert(result == 12);
}

int main(int, char**)
{
    test_part_one();
    int res1 = part_one("data/day05.txt");
    std::cout << "Part One: " << res1 << std::endl;

    test_part_two();
    int res2 = part_two("data/day05.txt");
    std::cout << "Part Two: " << res2 << std::endl;
}
