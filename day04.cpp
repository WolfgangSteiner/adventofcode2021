#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>
#include <cstdint>
#include <functional>
#include "util.h"

using namespace std;

struct cell_t {
  cell_t(int value) : value(value) {};
  cell_t() {}
  int value{};
  bool hit{};
};


struct board_t {
  bool completed{};
  mat_t<cell_t> mat;
};

void print_board(const board_t& board)
{
    for (const auto& row : board.mat)
    {
        for (const auto& cell : row)
        {
            if (cell.value < 10) std::cout << " ";
            std::cout << "  " << cell.value << (cell.hit ? "+" : ".");
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

 
bool board_contains_completed_row(const board_t& b)
{
    for (const auto& row : b.mat)
    {
        bool completed = std::all_of(row.begin(), row.end(), [](const auto& cell){return cell.hit == true;});
        if (completed) return true;
    }

    return false;
}


bool board_col_is_completed(const board_t& b, size_t index)
{
    for (const auto& row : b.mat)
    {
        if (row[index].hit == false) return false;
    }
    return true;
}
     

bool board_contains_completed_col(const board_t& b)
{
    for (size_t i = 0; i < b.mat[0].size(); ++i)
    {
        bool completed = board_col_is_completed(b, i);
        if (completed) return true;
    }

    return false;
}
            

void check_number(board_t& b, int number)
{
    for (auto& row : b.mat)
    {
        for (auto& cell : row)
        {
            if (cell.value == number) cell.hit = true;
        }
    }

    b.completed = board_contains_completed_row(b) || board_contains_completed_col(b);
}


std::vector<board_t*> check_number(std::vector<board_t>& boards, int number)
{
  std::vector<board_t*> res;
    for (auto& b : boards)
    {
        check_number(b, number);
        if (b.completed) res.push_back(&b);
    }

    return res;
}


int compute_score(const board_t& board, int number)
{
    int sum{};
    for (const auto& row : board.mat)
    {
        for (const auto& cell : row)
        {
            if (cell.hit == false) sum += cell.value;
        }
    }

    return sum * number;
}

std::pair<intvec_t, std::vector<board_t>> parse_file(str_t filename)
{
    auto input = readlines(filename);
    auto numbers = to_int(split(input[0], ','));
    std::vector<board_t> boards;

    board_t board;  

    for (size_t i = 2; i < input.size(); ++i)
    {
        const str_t& line = input[i];
        if (line.empty())
        {
            boards.push_back(board);
            board.mat.clear();
            continue;
        }

        std::vector<cell_t> row;
        std::istringstream ss(line);
        for (int i = 0; i < 5; ++i)
        {
            int value;
            ss >> value; 
            row.emplace_back(value);
        }
        board.mat.push_back(row);
    }

    boards.push_back(board);
    return std::make_pair(numbers, boards);
}


int play_bingo(std::string filename, size_t winning_rounds)
{
  auto[numbers, boards] = parse_file(filename);
  size_t num_completed_boards = 0;
  if (winning_rounds == -1)
  {
      winning_rounds = boards.size();
  }

  for (int number : numbers)
  {
      //cout << number << endl;
      auto winning_boards = check_number(boards, number);
      if (winning_boards.size() != 0)
      {
          num_completed_boards += winning_boards.size();
          cout << "Completed boards: " << num_completed_boards << "/" << winning_rounds << endl;
          if (num_completed_boards == winning_rounds)
          {
              cout << "Winning Board:" << endl;
              print_board(*winning_boards.back());
              return compute_score(*winning_boards.back(), number);
          }
          else
          {
            for (auto winning_board : winning_boards)
              std::erase_if(
                  boards,
                  [](const auto& board) { return board.completed; });
          }
      }
  }

  return 0;
}

 
int part_one(std::string filename)
{
    return play_bingo(filename, 1);
}

void test_part_one()
{
    cell_t cell(33);
    assert(cell.value == 33);
    auto[numbers, boards] = parse_file("data/day04_test.txt");
    // for (const auto& board : boards) print_board(board);
    assert(boards.size() == 3);
    assert(boards[0].mat.size() == 5);
    assert(boards[0].mat[0].size() == 5);
    assert(part_one("data/day04_test.txt") == 4512);
}


int part_two(std::string filename)
{
    return play_bingo(filename, -1);
}

void test_part_two()
{
    int score = part_two("data/day04_test.txt");
    assert(score == 1924);
}

int main(int, char**)
{
    test_part_one();
    int res1 = part_one("data/day04.txt");
    std::cout << "Part One: " << res1 << std::endl;

    test_part_two();
    int res2 = part_two("data/day04.txt");
    std::cout << "Part Two: " << res2 << std::endl;
}
