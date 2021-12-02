#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>

struct vec2i
{
  int x{};
  int z{};
};

vec2i vec2i_add(vec2i a, vec2i b)
{
  return {a.x + b.x, a.z + b.z};
}

bool operator==(vec2i a, vec2i b)
{
  return a.x == b.x && a.z == b.z;
}


std::vector<vec2i> parse_file(std::string filename)
{
  std::fstream s(filename, s.in);
  std::vector<vec2i> result;

  while (true) {
    std::string direction;
    int amount;
    s >> direction >> amount;

    vec2i delta; 

    if (direction == "forward") {
      delta = { amount, 0 };
    } 
    else if (direction == "down") {
      delta = { 0, amount };
    }
    else if (direction == "up") {
      delta = { 0, -amount };
    }

    result.push_back(delta);

    if (s.eof()) break;
  }

  return result;
}

vec2i part_one(std::string filename)
{
  auto cmds = parse_file(filename);

  vec2i position;

  for (auto delta : cmds)
  {
    position = vec2i_add(position, delta);
  }

  return position;
}

vec2i part_two(std::string filename)
{
  auto cmds = parse_file(filename);

  vec2i pos;
  int aim{};

  for (auto cmd : cmds)
  {
    aim += cmd.z;
    pos.x += cmd.x;
    pos.z += cmd.x * aim;
  }

  return pos;
}

int main(void)
{
  auto pos = part_one("data/day02_test.txt");
  assert((pos == vec2i{15,10}));

  pos = part_one("data/day02.txt");
  std::cout << "Part One: X = " << pos.x << " Z = " << pos.z << " --> " << pos.x * pos.z << std::endl;

  pos = part_two("data/day02_test.txt");
  assert((pos == vec2i{15,60}));
  pos = part_two("data/day02.txt");
  std::cout << "Part Two: X = " << pos.x << " Z = " << pos.z << " --> " << pos.x * pos.z << std::endl;
}

