#include <iostream>
#include <vector>
#include <cstdlib>
#include <time.h>


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
    srand(time(NULL));
    std::vector<std::string> args(argv, argv + argc);
    Main m;
    m.main(args.data());
}