#include <string>
#include <cassert>
#include <sstream>
#include <filesystem>
#include <iostream>
#include <cstdlib>

int system(std::string s)
{
  return system(s.c_str());
}


int main(int argc, char** argv)
{
  assert(argc == 2);
  std::filesystem::path filepath(argv[1]);
  auto exe_path = "bin" / filepath.stem();

  std::stringstream cmd;
  cmd << "clang++ "
      << "--std=c++20 "
      << "-Wall "
      << "-Werror "
      << "-Wextra "
      << "-Wpedantic "
      << "-Wconversion "
      << filepath 
      << " -o " << exe_path;
  std::cout << cmd.str() << std::endl;
  auto result = system(cmd.str());
  if (result == 0) 
  {
    system(exe_path.string());
  }
}
