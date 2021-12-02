#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>

std::vector<int> read_file(std::string filename)
{
  std::fstream s(filename, s.in);
  std::vector<int> result;

  while (true) {
    int x;
    s >> x;
    if (s.eof()) break;
    result.push_back(x);
  }

  return result;
}

int count_increases(const std::vector<int>& seq)
{
  int result = 0;
  int prev_value = seq.front();
  
  for (int x : seq)
  {
    if (x > prev_value) result++;
    prev_value = x;
  }
  return result;
}

std::vector<int> sliding_window(const std::vector<int>& seq)
{
  std::vector<int> result;
  for (size_t i = 2; i < seq.size(); ++i)
  {
    result.push_back(seq[i-2] + seq[i-1] + seq[i]);
  }

  return result;
}


int part_one(std::string filename)
{
  return count_increases(read_file(filename));
}

int part_two(std::string filename)
{
  auto data = read_file(filename);
  return count_increases(sliding_window(data));
}

int main(int, char**)
{
  assert(part_one("data/day01_test.txt") == 7);
  std::cout << "Part 1: " << part_one("data/day01.txt") << std::endl;

  assert(part_two("data/day01_test.txt") == 5);
  std::cout << "Part 2: " << part_two("data/day01.txt") << std::endl;
}
