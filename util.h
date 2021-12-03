#include <fstream>
#include <string>
#include <vector>
#include <sstream>

using strvec_t = std::vector<std::string>;
using str_t = std::string;

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

std::string join(const strvec_t& strvec, str_t join_string)
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

