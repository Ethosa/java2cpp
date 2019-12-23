#include <iostream>
#include <vector>
#include <cstdlib>
#include <time.h>
#include <map>
#include <cassert>
#include <set>
#include <deque>
#include <algorithm>




class Main 
{
    public:
    static void main(std::string args[])
    {
        std::cout << "Hello world" << std::endl;
        std::cout << "ban";
        auto a = 1;

        for (int i = 0; i < 100; ++i)
        {
            std::cout << test() << std::endl;
        }

        std::map<std::string, int> m;
        m["hello world"] = 5;
        m["a"] = 1777;
        std::cout << m["hello world"] << std::endl;
        std::cout << m["a"] << std::endl;

        if (m.find("b") != m.end())
            std::cout << "contains!" << std::endl;
        else
            std::cout << "not contains :(" << std::endl;

        std::set<std::string> b;
        b.insert("lol");
        for (auto& obj: b) std::cout << obj << std::endl;
        if (b.find("lol") != b.end()) std::cout << "lol contains :|" << std::endl;

        std::deque<std::string> c;
        c.push_back("Hello world");
        for (auto& obj: c) std::cout << obj << std::endl;
        auto index = std::find(c.begin(), c.end(), "Hello world");
        std::cout << c.at(0) << std::endl;
    }

    public:
    static int test()
    {
        int b = rand() % (64 - 5 + 1) + 5;
        return b;
    }

    public:
    std::string test(std::string a)
    {
        unsigned int i = 100;
        unsigned int j = 100000;
        std::string timed = "timed";
        return timed + a;
    }

};

int main (int argc, char *argv[])
{
    std::vector<std::string> args(argv, argv + argc);
    Main m;
    m.main(args.data());
}