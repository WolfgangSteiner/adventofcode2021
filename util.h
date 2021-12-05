#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <cstdlib>

using strvec_t = std::vector<std::string>;
using intvec_t = std::vector<int>;
using intmat_t = std::vector<std::vector<int>>;
using str_t = std::string;

template <typename T>
using mat_t = std::vector<std::vector<T>>;

strvec_t readlines(std::string filename)
{
    strvec_t res;
    std::ifstream in(filename);
    str_t str;

    while (std::getline(in, str))
    {
        res.push_back(str);
    }

    return res;
}    

template<typename T>
std::string join(const std::vector<T>& strvec, str_t join_string)
{
    std::stringstream res;
    bool is_first = true;

    for (auto str : strvec) {
        if (!is_first) res << join_string;
        res << str;
        is_first = false;
    }

    return res.str();
}

strvec_t split(str_t str, char c)
{
    std::stringstream ss(str);
    strvec_t res;
    std::string s;

    while (std::getline(ss, s, c)) {
        res.push_back(s);
    }

    return res;
}

void print_intvec(const intvec_t& vec)
{
    std::cout << join(vec, ", ") << std::endl;
}

void print_intmat(const intmat_t& mat)
{
    for (auto row : mat)
    {
        print_intvec(row);
    }
}


intvec_t to_int(const strvec_t& strvec)
{
    intvec_t res;
    for (auto s : strvec)
    {
        res.push_back(atoi(s.c_str()));
    }
    return res;
}
