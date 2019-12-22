# -*- coding: utf-8 -*-
# author: Ethosa

from retranslator import Translator


class Java2Cpp(Translator):
    def __init__(self, codeString="", extra=[], useRegex=False):
        """initialize class

        Keyword Arguments:
            codeString {str} -- source code on Java (default: {\"})
            extra {list} -- include your own rules (default: {[]})
            useRegex {bool} -- this parameter tells you to use regex (default: {False})
        """
        self.codeString = codeString
        self.Transform = self.compile = self.translate  # callable objects

        #  create little magic ...
        self.rules = Java2Cpp.FIRST_RULES[:]
        self.rules.extend(extra)
        Translator.__init__(self, codeString, self.rules, useRegex)

    FIRST_RULES = [
        # // ...
        #
        (r"([\r\n]*)[ ]*//[^\r\n]*",
         r"\1", None, 0),

        # System.out.print("Hello world")
        # cout << "Hello world";
        (r"System.out.print[ ]*\([ ]*([^\r\n]+)[ ]*\)",
         r"std::cout << \1", None, 0),

        # System.out.println("Hello world")
        # std::cout << "Hello world" << std::endl;
        (r"System.out.println[ ]*\([ ]*([^\r\n]+)[ ]*\)",
         r"std::cout << \1 << std::endl", None, 0),

        # public void test(){}
        # public:
        # void test(){}
        (r"(?P<indent>[ ]*)public[ ]*(?P<return_type>\S+)[ ]*(?P<method_name>\S+)[ ]*\(",
         r"\g<indent>public:\n\g<indent>\g<return_type> \g<method_name>(", None, 0),

        # public static void test(){}
        # public:
        # static void test(){}
        (r"(?P<indent>[ ]*)public[ ]*(?P<other>\S+)[ ]*(?P<return_type>\S+)[ ]*(?P<method_name>\S+)[ ]*\(",
         r"\g<indent>public:\n\g<indent>\g<other> \g<return_type> \g<method_name>(", None, 0),

        # String
        # std::string
        (r"\bString",
         r"std::string", None, 0),

        # Namespace.test
        # Namespace::test
        (r"([^\r\n]+)\.([^\r\n]+)",
         r"\1::\2", None, 0),

        # public abstract class
        # class
        (r"(public abstract|static) class", r"class", None, 0),

        # long
        # unsigned int
        (r"\blong\b",
         r"unsigned int", None, 0),

        # Random rnd = new Random()
        #
        (r"(Random|var)[ ]*[a-zA-Z0-9_]+[ ]*=[ ]*new[ ]*Random[ ]*\([ ]*\)",
         r"", None, 0),

        # min + rnd.nextInt(max - min + 1)
        # rand_r() % min + (max - min + 1)
        (r"(\S+)[ ]*\+[ ]*[a-zA-Z0-9_]+::nextInt(\([^\)]+\))",
         r"rand_r() % \2 + \1", None, 0),

        # 100_000_000
        # 100000000
        (r"(\d+)[_]+(\d+)",
         r"\1\2", None, 5),

        # 100L
        # 100
        (r"[ ]*(\d+)L\b",
         r" \1", None, 0),

        # class Main{}
        # class Main{};
        (r"(?P<indent>[ ]*)class[ ]*(?P<class_name>\w+)[ ]*{[\r\n]+(?P<body>(?P<bindent>[ ]+)[^\r\n]+[\r\n]+((?P=bindent)[^\r\n]+[\r\n]+)*)}",
         r"\g<indent>class \g<class_name> {\n\g<body>};", None, 0),

        # test{
        # }
        # test
        # {
        # }
        (r"(?P<indent>[ ]*)(?P<info>[^\r\n]*){[\r\n]",
         r"\g<indent>\g<info>\n\g<indent>{\n", None, 0),

        # String[] a
        # String a[]
        (r"(\w+)\[\][ ]*(\w+)",
         r"\1 \2[]", None, 0),

        # }
        # ...
        # -------
        # }
        #
        # ...
        (r"}[\r\n]([ ]*)(\S)",
         r"}\n\n\1\2", None, 0),

        #
        # #include <iostream>
        (r"\A",
         r"#include <iostream>\n#include <vector>\n#include <cstdlib>\n#include <time.h>\n", None, 0),

        # var ...
        # auto ...
        (r"([ ]*)var[ ]*",
         r"\1auto ", None, 0),

        # end ...
        # int main ...
        (r"\Z",
         (r"\n\nint main (int argc, char *argv[])\n{"
          r"\n    srand(time(NULL));\n    std::vector"
          r"<std::string> args(argv, argv + argc);\n "
          r"   Main m;\n    m.main(args.data());\n}"), None, 0),

        # ;
        #
        (r"[\r\n]+[ ]*;[\r\n]+",
         r"\n", None, 0),

        #
        #
        (r"",
         r"", None, 0)
    ]
