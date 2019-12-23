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
        # (r"([^\r\n]+)\.([^\r\n]+)",
        #  r"\1::\2", None, 0),

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
        (r"(\S+)[ ]*\+[ ]*[a-zA-Z0-9_]+.nextInt(\([^\)]+\))",
         r"rand() % \2 + \1", None, 0),

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
         (r"#include <iostream>\n#include <vector>\n"
          r"#include <cstdlib>\n#include <time.h>\n#"
          r"include <map>\n#include <cassert>\n#incl"
          r"ude <set>\n#include <deque>\n#include <a"
          r"lgorithm>\n"), None, 0),

        # Object
        # void*
        (r"Object",
         r"void*", None, 0),

        # Integer
        # int
        (r"\bInteger",
         r"int", None, 0),

        # import asd.*;
        #
        (r"[\r\n]import[ ]*[^\r\n]+;",
         r"", None, 0),

        # package asd.*;
        #
        (r"[\r\n]package[ ]*[^\r\n]+;",
         r"", None, 0),

        # catch (Exception e)
        # catch (...)
        (r"catch[ ]*\([ ]*Exception[ ]*[a-zA-Z0-9_]+[ ]*\)",
         r"catch (...)", None, 0),

        # (int)5.0
        # *((int*)5.0)
        (r"\([ ]*(int|float|double|unsigned int)[ ]*\)[ ]*(\S+)",
         r"*((\1*)\2)", None, 0),

        # var ...
        # auto ...
        (r"([ ]*)var[ ]*",
         r"\1auto ", None, 0),

        # end ...
        # int main ...
        (r"\Z",
         (r"\n\nint main (int argc, char *argv[])\n{"
          r"\n    std::vector<std::string> args(argv"
          r", argv + argc);\n    Main m;\n    m.main"
          r"(args.data());\n}"), None, 0),

        # ;
        #
        (r"[\r\n]+[ ]*;[\r\n]+",
         r"\n", None, 0),


        # ----------- Hash Map -----------
        # HashMap<String, int> m = new HashMap<>();
        # std::map<std::string, int> m;
        (r"(?P<first>(HashMap|auto)(?P<mapinfo><[^,]+,[ ]*[^>]+>)[ ]*(?P<var_name>[a-zA-Z0-9_]+)[ ]*=[ ]*new[ ]*HashMap<>\(\))",
         r"std::map\g<mapinfo> \g<var_name>", None, 0),

        # m.put("1", 1)
        # m["1"] = 1
        ((r"(?P<first>std::map(?P<mapinfo><[^,]+,[ ]*[^>]+>)[ ]*(?P<var_name>[a-zA-Z0-9_]+)[ ]*)"
          r"(?P<putting>[\s\S]+(?P=var_name)).put\((?P<key>[^,]+),[ ]*(?P<value>[^\)]+)\)"),
         (r"std::map\g<mapinfo> \g<var_name>\g<putting>[\g<key>] = \g<value>"), None, 70),

        # m.get("a")
        # m["a"]
        ((r"(?P<first>std::map(?P<mapinfo><[^,]+,[ ]*[^>]+>)[ ]*(?P<var_name>[a-zA-Z0-9_]+)[ ]*)"
          r"(?P<getting>[\s\S]+(?P=var_name)).get\([ ]*(?P<key>[^\)]+)\)"),
         (r"std::map\g<mapinfo> \g<var_name>\g<getting>[\g<key>]"), None, 70),

        # m.containsKey("a")
        # m["a"]
        ((r"(?P<first>std::map(?P<mapinfo><[^,]+,[ ]*[^>]+>)[ ]*(?P<var_name>[a-zA-Z0-9_]+)[ ]*)"
          r"(?P<getting>[\s\S]+(?P=var_name)).containsKey\([ ]*(?P<key>[^\)]+)\)"),
         (r"std::map\g<mapinfo> \g<var_name>\g<getting>.find(\g<key>) != \g<var_name>.end()"), None, 70),

        # m.size()
        # m.count()
        ((r"(?P<first>std::map(?P<mapinfo><[^,]+,[ ]*[^>]+>)[ ]*(?P<var_name>[a-zA-Z0-9_]+)[ ]*)"
          r"(?P<getting>[\s\S]+(?P=var_name)).size\([ ]*\)"),
         (r"std::map\g<mapinfo> \g<var_name>\g<getting>.count()"), None, 70),
        # ----------- Hash Map -----------


        # ----------- Hash Set -----------
        # HashSet<String> m = new HashSet();
        # std::set<std::string> m;
        ((r"HashSet(?P<setinfo><[^>]+>)[ ]*(?P<var>[a-zA-Z0-9_]+)[ ]*=[ ]*new[ ]*HashSet[ ]*\(\)"),
         (r"std::set\g<setinfo> \g<var>"), None, 0),

        # m.add("hello world")
        # m.insert("hello world")
        ((r"(?P<first>std::set(?P<setinfo><[^>]+>)[ ]*(?P<var>[a-zA-Z0-9_]+)[ ]*)"
          r"(?P<adding>[\s\S]+(?P=var)).add\([ ]*(?P<elem>[^\)]+)\)"),
         (r"std::set\g<setinfo> \g<var>\g<adding>.insert(\g<elem>)"), None, 70),

        # m.contains("hello world")
        # m.find("hello world") != m.end()
        ((r"(?P<first>std::set(?P<setinfo><[^>]+>)[ ]*(?P<var>[a-zA-Z0-9_]+)[ ]*)"
          r"(?P<containing>[\s\S]+(?P=var)).contains\([ ]*(?P<elem>[^\)]+)\)"),
         (r"std::set\g<setinfo> \g<var>\g<containing>.find(\g<elem>) != \g<var>.end()"), None, 70),

        # cout << m
        # for (auto& obj: m) cout << obj
        ((r"(?P<first>std::set(?P<setinfo><[^>]+>)[ ]*(?P<var>[a-zA-Z0-9_]+)[ ]*)"
          r"(?P<before>[\s\S]+)std::cout[ ]*<<[ ]*(?P<cout>(?P=var)[ ]*)(?P<last>[^\.])"),
         (r"std::set\g<setinfo> \g<var>\g<before>for (auto& obj: \g<var>) std::cout << obj \g<last>"), None, 70),
        # ----------- Hash Set -----------


        # ----------- Array List -----------
        # ArrayList<String> l = new ArrayList();
        # std::deque<std::string> l;
        ((r"ArrayList(?P<deque><[^>]+>)[ ]*(?P<var>[a-zA-Z0-9_]+)[ ]*=[ ]*new[ ]*ArrayList[ ]*\(\)"),
         (r"std::deque\g<deque> \g<var>"), None, 0),

        # l.add("hello world")
        # l.push_back("hello world")
        ((r"(?P<first>std::deque(?P<deque><[^>]+>)[ ]*(?P<var>[a-zA-Z0-9_]+)[ ]*)"
          r"(?P<adding>[\s\S]+(?P=var)).add\([ ]*(?P<elem>[^\)]+)\)"),
         (r"std::deque\g<deque> \g<var>\g<adding>.push_back(\g<elem>)"), None, 70),

        # l.get(0)
        # l.at(0)
        ((r"(?P<first>std::deque(?P<deque><[^>]+>)[ ]*(?P<var>[a-zA-Z0-9_]+)[ ]*)"
          r"(?P<getting>[\s\S]+(?P=var)).get\([ ]*(?P<elem>[^\)]+)\)"),
         (r"std::deque\g<deque> \g<var>\g<getting>.at(\g<elem>)"), None, 70),

        # l.isEmpty()
        # l.empty()
        ((r"(?P<first>std::deque(?P<deque><[^>]+>)[ ]*(?P<var>[a-zA-Z0-9_]+)[ ]*)"
          r"(?P<check>[\s\S]+(?P=var)).isEmpty\([ ]*\)"),
         (r"std::deque\g<deque> \g<var>\g<check>.empty()"), None, 70),

        # l.indexOf("a")
        # std::find(l.begin(), l.end(), "a")
        ((r"(?P<first>std::deque(?P<deque><[^>]+>)[ ]*(?P<var>[a-zA-Z0-9_]+)[ ]*)"
          r"(?P<before>[\s\S]+)(?P<cout>(?P=var)).indexOf\([ ]*(?P<elem>[^\)]+)\)"),
         (r"std::deque\g<deque> \g<var>\g<before>std::find(\g<var>.begin(), \g<var>.end(), \g<elem>)"), None, 70),

        # cout << l
        # for (auto& obj: l) cout << obj
        ((r"(?P<first>std::deque(?P<deque><[^>]+>)[ ]*(?P<var>[a-zA-Z0-9_]+)[ ]*)"
          r"(?P<before>[\s\S]+)std::cout[ ]*<<[ ]*(?P<cout>(?P=var)[ ]*)(?P<last>[^\.])"),
         (r"std::deque\g<deque> \g<var>\g<before>for (auto& obj: \g<var>) std::cout << obj \g<last>"), None, 70),
        # ----------- Array List -----------

        # java.util.Set
        # Set
        ((r"java\.[^\.]+\.(\w+)"),
         (r"\1"), None, 0),

        #
        #
        ((r""),
         (r""), None, 0)
    ]
